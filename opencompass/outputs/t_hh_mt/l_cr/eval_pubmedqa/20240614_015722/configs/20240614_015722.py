ARC_c_datasets=[
    dict(abbr='ARC-c',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.openicl.icl_evaluator.AccEvaluator'),
            pred_postprocessor=dict(
                options='ABCD',
                type='opencompass.utils.text_postprocessors.first_option_postprocess'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='arc',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
datasets=[
    dict(abbr='pubmedQA',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.pubmedQAEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='pubmedqa',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
fever_datasets=[
    dict(abbr='fever',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.feverEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='fever',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
hotpotqa_datasets=[
    dict(abbr='HotpotQA',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.HotpotQAEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='hotpotqa',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
mmlu_datasets=[
    dict(abbr='MMLU',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.openicl.icl_evaluator.AccEvaluator'),
            pred_postprocessor=dict(
                options='ABCD',
                type='opencompass.utils.text_postprocessors.first_option_postprocess')),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='mmlu',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
models=[
    dict(abbr='llama-3-8b-ragga-disturb',
        batch_padding=True,
        batch_size=1,
        generation_kwargs=dict(
            do_sample=False,
            eos_token_id=[
                128001,
                128009,
                ]),
        max_out_len=50,
        meta_template=dict(
            begin='<|start_header_id|>system<|end_header_id|>\n\n<|eot_id|>',
            round=[
                dict(begin='<|start_header_id|>user<|end_header_id|>\n\n',
                    end='<|eot_id|>',
                    role='HUMAN'),
                dict(begin='<|start_header_id|>assistant<|end_header_id|>\n\n',
                    generate=True,
                    role='BOT'),
                ]),
        model_kwargs=dict(
            device_map='auto',
            torch_dtype='torch.bfloat16'),
        path='/data/wxh/RAG/code/llama3-8b-instruct-ragga-disturb',
        run_cfg=dict(
            num_gpus=2),
        tokenizer_kwargs=dict(
            padding_side='left',
            truncation_side='left',
            trust_remote_code=True),
        tokenizer_path='/data/wxh/RAG/code/llama3-8b-instruct-ragga-disturb',
        type='opencompass.models.myModel'),
    ]
musique_datasets=[
    dict(abbr='MuSiQue',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.musiqueEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='musique',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
nq_datasets=[
    dict(abbr='nq',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.nqEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='nq',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
obqa_datasets=[
    dict(abbr='openbookqa',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.openicl.icl_evaluator.AccEvaluator'),
            pred_postprocessor=dict(
                options='ABCD',
                type='opencompass.utils.text_postprocessors.first_option_postprocess'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='obqa',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
pubhealth_datasets=[
    dict(abbr='PubHealth',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.pubhealthEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='pubhealth',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
pubmedQA_datasets=[
    dict(abbr='pubmedQA',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.pubmedQAEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='pubmedqa',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
triviaqa_datasets=[
    dict(abbr='TriviaQA',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.TQAEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='tqa',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
webq_datasets=[
    dict(abbr='WebQ',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.webQEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='webq',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
wikimultihop_datasets=[
    dict(abbr='WikiMultihopQA',
        eval_cfg=dict(
            evaluator=dict(
                type='opencompass.datasets.WikiMultihopQAEvaluator'),
            pred_role='BOT'),
        infer_cfg=dict(
            inferencer=dict(
                type='opencompass.openicl.icl_inferencer.GenInferencer'),
            prompt_template=dict(
                template=dict(
                    round=[
                        dict(prompt='{classification_query}',
                            role='HUMAN'),
                        ]),
                type='opencompass.openicl.icl_prompt_template.PromptTemplate'),
            retriever=dict(
                type='opencompass.openicl.icl_retriever.ZeroRetriever')),
        name='wiki',
        path='/data/zfr/finalTest/opencompass/generate_docs/true_hh_mt_results/',
        reader_cfg=dict(
            input_columns=[
                'classification_query',
                'query',
                ],
            output_column='answer'),
        type='opencompass.datasets.omniDataset'),
    ]
work_dir='outputs/t_hh_mt/l_cr/eval_pubmedqa/20240614_015722'