import os
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import List, Set, DefaultDict
import logging
from itertools import permutations

from pydantic import BaseModel
import scipy.special as sp
import numpy as np
from tqdm import tqdm

from .relevance import RelevanceExample, MsMarcoPassageLoader
from ..rerank.base import Query, Text
from ..data.unicode import convert_to_unicode


__all__ = ['MsMarcoExample', 'MsMarcoDataset']


# MsMarcoExample represents a query along with its ranked and re-ranked candidates.
class MsMarcoExample(BaseModel):
    qid: str
    text: str
    candidates: List[str]
    relevant_candidates: Set[str]


class MsMarcoDataset(BaseModel):
    examples: List[MsMarcoExample]

    # Load qrels from the provided path and return a dictionary mapping
    # qid -> set({doc_id, doc_id...}) for all doc_ids with relevance over 1.
    @classmethod
    def load_qrels(cls, path: str) -> DefaultDict[str, Set[str]]:
        qrels = defaultdict(set)
        with open(path) as f:
            for line in f:
                qid, _, doc_id, relevance = line.rstrip().split('\t')
                if int(relevance) >= 1:
                    qrels[qid].add(doc_id)
        return qrels

    # Load a run from the provided path.  The run file contains mappings from
    # a query id and a doc title to a rank.  load_run returns a dictionary
    # mapping query ids to lists of doc titles sorted by ascending rank.
    @classmethod
    def load_run(cls, path: str):
        '''Returns OrderedDict[str, List[str]]'''
        run = OrderedDict()
        with open(path) as f:
            for i, line in enumerate(f):
                # if i == 100 * 1000:
                #     break
                qid, doc_title, rank = line.split('\t')
                if qid not in run:
                    run[qid] = []
                run[qid].append((doc_title, int(rank)))
        sorted_run = OrderedDict()
        for qid, doc_titles_ranks in run.items():
            doc_titles_ranks.sort(key=lambda x: x[1])
            doc_titles = [doc_titles for doc_titles, _ in doc_titles_ranks]
            sorted_run[qid] = doc_titles
        return sorted_run

    @classmethod
    def load_queries(cls,
                     path: str,
                     qrels: DefaultDict[str, Set[str]],
                     run) -> List[MsMarcoExample]:
        queries = []
        with open(path) as f:
            for i, line in enumerate(f):
                # if i == 100:
                #     break
                qid, query = line.rstrip().split('\t')
                queries.append(MsMarcoExample(qid=qid,
                                              text=query,
                                              candidates=run[qid],
                                              relevant_candidates=qrels[qid]))
        return queries

    @classmethod
    def from_folder(cls,
                    folder: str,
                    split: str = 'dev',
                    is_duo: bool = False,
                    run_path: Path = '.') -> 'MsMarcoDataset':
        run_mono = "mono." if is_duo else ""
        query_path = os.path.join(folder, f"queries.{split}.small.tsv")
        qrels_path = os.path.join(folder, f"qrels.{split}.small.tsv")
        if not os.path.isfile(run_path):
            run_path = os.path.join(folder, f"run.{run_mono}{split}.small.tsv")
        return cls(examples=cls.load_queries(query_path,
                                             cls.load_qrels(qrels_path),
                                             cls.load_run(run_path)))

    def query_passage_tuples(self, is_duo: bool = False):
        return [((ex.qid, ex.text, ex.relevant_candidates), perm_pas)
                for ex in self.examples
                for perm_pas in permutations(ex.candidates, r=1+int(is_duo))]

    def to_relevance_examples(self,
                              index_path: str,
                              is_duo: bool = False) -> List[RelevanceExample]:
        loader = MsMarcoPassageLoader(index_path)
        example_map = {}
        for (qid, text, rel_cands), cands in tqdm(self.query_passage_tuples()):
            if qid not in example_map:
                example_map[qid] = [convert_to_unicode(text), [], [], []]
            example_map[qid][1].append([cand for cand in cands][0])
            try:
                passages = [loader.load_passage(cand) for cand in cands]
                example_map[qid][2].append(
                    [convert_to_unicode(passage.all_text)
                     for passage in passages][0])
            except ValueError:
                logging.warning(f'Skipping {passages}')
                continue
            example_map[qid][3].append(cands[0] in rel_cands)
        mean_stats = defaultdict(list)

        for ex in self.examples:
            int_rels = np.array(list(map(int, example_map[ex.qid][3])))
            p = int_rels.sum()/(len(ex.candidates) - 1) if is_duo else int_rels.sum()   # Num of relevant docs retrieved
            mean_stats['Expected P@1 for Random Ordering'].append(np.mean(int_rels))
            n = len(ex.candidates) - p      # Num of irrelevant docs
            N = len(ex.candidates)          # Num of candidate docs
            if len(ex.candidates) <= 1000:  # If a relevant doc exists, R=1, else 0
                mean_stats['Expected R@1000 for Random Ordering'].append(1 if 1 in int_rels else 0)

            numer = np.array([sp.comb(n, i) / (N - i) for i in range(0, n + 1) if i != N]) * p
            if n == N:
                numer = np.append(numer, 0)
            denom = np.array([sp.comb(N, i) for i in range(0, n + 1)])
            rr = 1 / np.arange(1, n + 2)
            mean_stats['Expected MRR@1 for Random Ordering'].append(np.sum(numer[:1] * rr[:1] / denom[:1]))
            mean_stats['Expected MRR@3 for Random Ordering'].append(np.sum(numer[:3] * rr[:3] / denom[:3]))
            mean_stats['Expected MRR@10 for Random Ordering'].append(np.sum(numer[:10] * rr[:10] / denom[:10]))
            mean_stats['Expected MRR@100 for Random Ordering'].append(np.sum(numer[:100] * rr[:100] / denom[:100]))
            mean_stats['Expected MRR for Random Ordering'].append(np.sum(numer * rr / denom))
            ex_index = len(ex.candidates)
            for rel_cand in ex.relevant_candidates:
                if rel_cand in ex.candidates:
                    ex_index = min(ex.candidates.index(rel_cand), ex_index)
            mean_stats['Existing R@10'].append(1 if ex_index < 10 else 0)
            mean_stats['Existing MRR@1'].append(1 / (ex_index + 1) if ex_index < 1 else 0)
            mean_stats['Existing MRR@3'].append(1 / (ex_index + 1) if ex_index < 3 else 0)
            mean_stats['Existing MRR@10'].append(1 / (ex_index + 1) if ex_index < 10 else 0)
            mean_stats['Existing MRR@100'].append(1 / (ex_index + 1) if ex_index < 100 else 0)
            mean_stats['Existing MRR'].append(1 / (ex_index + 1) if ex_index < len(ex.candidates) else 0)

        # Calc mean of all samples
        for k, v in mean_stats.items():
            logging.info(f'{k}: {np.mean(v)}')
        return [RelevanceExample(Query(text=query_text, id=qid),
                                 list(map(lambda s: Text(s[1], dict(docid=s[0])), zip(cands, cands_text))),
                                 rel_cands)
                for qid, (query_text, cands, cands_text, rel_cands) in example_map.items()]
