"""
This module computes evaluation metrics for MSMARCO dataset on the ranking task. Intenral hard coded eval files version. DO NOT PUBLISH!
Command line:
python ms_marco_eval.py <path_to_reference_file> <path_to_candidate_file>

Creation Date : 06/12/2018
Last Modified : 08/06/2020
Authors : Daniel Campos <dacamp@microsoft.com>, Rutger van Haasteren <ruvanh@microsoft.com>
"""
import os
import sys
from collections import Counter

MaxMRRRank = 1000


def load_reference(path_to_reference):
    """Load Reference reference relevant document
    Args:path_to_reference (str): path to a file to load.
    Returns:qids_docids_gold (dict): dictionary mapping from query_id (int) to relevant documents (list of ints).
    """
    qids_docids_gold = {}
    with open(path_to_reference,'r') as file:
        for line in file:
            try:
                line = line.strip().split('\t')
                qid = int(line[0])
                if qid in qids_docids_gold:
                    pass
                else:
                    qids_docids_gold[qid] = []
                qids_docids_gold[qid] = line[1]
            except:
                raise IOError('\"%s\" is not valid format' % line)
    return qids_docids_gold


def validate_candidate_has_enough_ranking(qids_to_candidate_docids_ranking):
    for qid in qids_to_candidate_docids_ranking:
        doc_cnt = len(qids_to_candidate_docids_ranking[qid])
        if doc_cnt > MaxMRRRank:
            print('Too many documents ranked ({}). Please Provide top {} documents for qid:{}'.format(doc_cnt, MaxMRRRank, qid))


def load_candidate(path_to_candidate):
    """Load candidate data from a file.
    Args:path_to_candidate (str): path to file to load.
    Returns:qids_to_candidate_docids_ranking (dict): dictionary mapping from query_id (int) to a list of 1000 document ids(int) ranked by relevance and importance
    """

    qids_to_candidate_docids_ranking = {}
    with open(path_to_candidate,'r') as file:
        for line in file:
            try:
                line = line.strip().split('\t')
                qid, did, rank = int(line[0]), line[1], int(line[2])
                if qid in qids_to_candidate_docids_ranking:
                    pass
                else:
                    # By default, all PIDs in the list of 1000 are 0. Only override those that are given
                    qids_to_candidate_docids_ranking[qid] = []
                qids_to_candidate_docids_ranking[qid].append((did, rank))
            except:
                raise IOError('\"%s\" is not valid format' % line)
        validate_candidate_has_enough_ranking(qids_to_candidate_docids_ranking)
        print('Quantity of Documents ranked for each query is as expected. Evaluating')
    return {qid: sorted(qids_to_candidate_docids_ranking[qid], key=lambda x: (x[1], x[0]), reverse=False)
            for qid in qids_to_candidate_docids_ranking}


def compute_metrics(qids_docids_gold, qids_to_candidate_docids_ranking, exclude_qids):
    """Compute MRR metric
    Args:    
    p_qids_docids_gold (dict): dictionary of query-document mapping
        Dict as read in with load_reference or load_reference_from_stream
    p_qids_to_candidate_docids_ranking (dict): dictionary of query-document candidates
    Returns:
        dict: dictionary of metrics {'MRR': <MRR Score>}
    """
    all_scores = {}
    MRR_1, MRR_3, MRR_10, MRR_100, MRR = 0, 0, 0, 0, 0
    ranking = []
    for qid in qids_to_candidate_docids_ranking:
        if qid in qids_docids_gold and qid not in exclude_qids:
            ranking.append(0)
            docid_gold = qids_docids_gold[qid]
            candidate_docids_ranking_list = qids_to_candidate_docids_ranking[qid]
            for i in range(MaxMRRRank):
                if candidate_docids_ranking_list[i][0] == docid_gold:   # Match
                    if i < 1:
                        MRR_1 += 1 / (i + 1)
                    if i < 3:
                        MRR_3 += 1 / (i + 1)
                    if i < 10:
                        MRR_10 += 1 / (i + 1)
                    if i < 100:
                        MRR_100 += 1 / (i + 1)
                    MRR += 1 / (i + 1)
                    ranking.pop()
                    ranking.append(i+1)
                    break
    if len(ranking) == 0:
        raise IOError("No matching QIDs found. Are you sure you are scoring the evaluation set?")

    MRR_1 /= len(qids_docids_gold)
    MRR_3 /= len(qids_docids_gold)
    MRR_10 /= len(qids_docids_gold)
    MRR_100 /= len(qids_docids_gold)
    MRR /= len(qids_docids_gold)

    all_scores['MRR@1 (P)'] = MRR_1
    all_scores['MRR@3'] = MRR_3
    all_scores['MRR@10'] = MRR_10
    all_scores['MRR@100'] = MRR_100
    all_scores['MRR'] = MRR
    all_scores['QueriesRanked'] = len(set(qids_to_candidate_docids_ranking) - exclude_qids)
    all_scores['Docs/Query'] = len(next(iter(qids_to_candidate_docids_ranking.values())))
    return all_scores


def quality_checks_qids(qids_docids_gold, qids_to_candidate_docids_ranking):
    """Perform quality checks on the dictionaries

    Args:
    p_qids_to_relevant_documentids (dict): dictionary of query-document mapping
        Dict as read in with load_reference or load_reference_from_stream
    p_qids_to_candidate_docids_ranking (dict): dictionary of query-document candidates
    Returns:
        bool,str: Boolean whether allowed, message to be shown in case of a problem
    """
    message = ''
    allowed = True

    # Create sets of the QIDs for the submitted and reference queries
    candidate_set = set(qids_to_candidate_docids_ranking.keys())
    ref_set = set(qids_docids_gold.keys())

    # Check that we do not have multiple documents per query
    for qid in qids_to_candidate_docids_ranking:
        # Remove all zeros from the candidates
        duplicate_pids = set([item for item, count in Counter(qids_to_candidate_docids_ranking[qid]).items() if count > 1])

        if len(duplicate_pids-set([0])) > 0:
            message = "Cannot rank a document multiple times for a single query. QID={qid}, PID={pid}".format(
                    qid=qid, pid=list(duplicate_pids)[0])
            allowed = False

    return allowed, message


def compute_metrics_from_files(path_to_reference, path_to_candidate, exclude_qids, perform_checks=True):
    """Compute MRR metric
    Args:    
    p_path_to_reference_file (str): path to reference file.
        Reference file should contain lines in the following format:
            QUERYID\tdocumentID
            Where documentID is a relevant document for a query. Note QUERYID can repeat on different lines with different documentIDs
    p_path_to_candidate_file (str): path to candidate file.
        Candidate file sould contain lines in the following format:
            QUERYID\tdocumentID1\tRank
            If a user wishes to use the TREC format please run the script with a -t flag at the end. If this flag is used the expected format is 
            QUERYID\tITER\tDOCNO\tRANK\tSIM\tRUNID 
            Where the values are separated by tabs and ranked in order of relevance 
    Returns:
        dict: dictionary of metrics {'MRR': <MRR Score>}
    """
    qids_docids_gold = load_reference(path_to_reference)
    qids_to_candidate_docids_ranking = load_candidate(path_to_candidate)
    if perform_checks:
        allowed, message = quality_checks_qids(qids_docids_gold, qids_to_candidate_docids_ranking)
        if message != '': print(message)

    return compute_metrics(qids_docids_gold, qids_to_candidate_docids_ranking, exclude_qids)


def load_exclude(path_to_exclude_folder):
    """Load QIDS for queries to exclude
    Args: 
    path_to_exclude_folder (str): path to folder where exclude files are located

    Returns: 
        set: a set with all qid's to exclude
    """
    qids = set()
    # List all files in a directory using os.listdir
    for a_file in os.listdir(path_to_exclude_folder):
        if os.path.isfile(os.path.join(path_to_exclude_folder, a_file)):
            with open(os.path.join(path_to_exclude_folder, a_file), 'r') as f:
                f.readline() #header
                for l in f:
                    qids.add(int(l.split('\t')[0]))
    print("{} excluded qids loaded".format(len(qids)))
    return qids


def main(path_to_reference=None, path_to_candidate=None):
    """ Command line:
    python msmarco_doc_eval.py <path_to_reference_file> <path_to_candidate_file> <queries_to_exclude>
    """
    # Args
    if len(sys.argv) == 1 and (path_to_reference is None or path_to_candidate is None):
        print("Usage: msmarco_doc_eval.py <path_to_reference_file> <path_to_candidate_file> <queries_to_exclude>")
        return
    if path_to_reference is None:
        if len(sys.argv) >= 2:
            path_to_reference = sys.argv[1]
    if path_to_candidate is None:
        if len(sys.argv) >= 3:
            path_to_candidate = sys.argv[2]
    exclude_qids = set()
    if len(sys.argv) >= 4:
        exclude_qids = load_exclude(sys.argv[3])  # Public implementation

    # Evaluation
    metrics = compute_metrics_from_files(path_to_reference, path_to_candidate, exclude_qids)

    # Output
    print('#####################')
    for metric in metrics:
        val = metrics[metric]
        if isinstance(val, float):
            val = '{:.5f}'.format(val)
        print('{}:\t{}'.format(metric, val))
    print('#####################')


if __name__ == '__main__':
    print("================  Random Ordering  ================")
    main("dlm/runs/gold.msmarco_doc_ans_small.fh.dev.tsv", "../data/msmarco_doc_ans_small/fh/run.dev.small_shuffled.tsv")
    print("================  Before Reranking ================")
    main("dlm/runs/gold.msmarco_doc_ans_small.fh.dev.tsv", "../data/msmarco_doc_ans_small/fh/run.dev.small.tsv")
    print("================  After Reranking  ================")
    main("dlm/runs/gold.msmarco_doc_ans_small.fh.dev.tsv", "runs/run.monot5.doc_fh.dev.tsv")
