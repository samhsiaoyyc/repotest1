# flake8: noqa
import os
import time
import random
from collections import defaultdict
from typing import Tuple

from ngchat_plugins.nlu.selectors.elastic_selector import ElasticSelector
from ngchat_plugins.importers.faq_importer import FAQImporter

from rasa.nlu.training_data import TrainingData

from rasa.nlu.training_data import load_data

class Evaluator:
    def __init__(self, config):
        self.train_exs = []
        self.test_exs = []
        self.selector = ElasticSelector(config)

    def import_data(self, faq_path) -> None:
        config_path = os.path.join("bots/es-faq", "config.yml")

        importer = FAQImporter(config_path)
        importer.faq_paths = [faq_path]
        importer.synonym_paths = []
        importer.augment_with_synonyms = False
        importer.timezone = "Asia/Taipei"
        training_examples, nlg_stories, entity_synonyms = importer._load_files()
        training_data = TrainingData(
            training_examples=training_examples,
            entity_synonyms=entity_synonyms,
            regex_features=[],
            lookup_tables=[],
            nlg_stories=nlg_stories
        )
        training_data.fill_response_phrases()

        # training_data = load_data("data/train_zh_cn.json")
        # td_responses = load_data("data/responses_zh_cn.md")
        # training_data = training_data.merge(td_responses)
        # training_data.fill_response_phrases()

        # train/test split
        training_examples = [ex for ex in training_data.training_examples if ex.get('intent') == 'faq']
        examples_per_response_key = defaultdict(lambda: [])
        for ex in training_examples:
            examples_per_response_key[ex.get('response_key')].append(ex)

        for intent in examples_per_response_key:
            examples = examples_per_response_key[intent]
            random.Random(1).shuffle(examples)
            split_offset = max(1, int(0.8 * len(examples)))
            self.train_exs.extend(examples[:split_offset])
            self.test_exs.extend(examples[split_offset:])

    def test_train_time(self) -> Tuple[float, float]:
        start_time = time.time()
        self.selector._inject_index(self.train_exs, {})
        time_taken = (time.time() - start_time)
        batch_nums = max(1, int(len(self.train_exs) / 2048))
        return time_taken, time_taken/batch_nums

    def _mean_ap(self, test_exs, gold_labels, N, method, embs_in_batch=True) -> float:
        if method == self.selector.SimMethod.EMBEDDING:
            text_embs = self.selector._text_to_emb(test_exs) if embs_in_batch else None
        mean_ap = 0
        for idx, ex in enumerate(test_exs):
            ap = 0
            true_pos_seen = 0
            if method == self.selector.SimMethod.EMBEDDING:
                text_embs_idx = text_embs[idx] if embs_in_batch else self.selector._text_to_emb([ex])[0]
            else:
                text_embs_idx = None
            search_results = self.selector._search(ex, text_embs_idx, N, method, date_enabled=False)
            retrieved_docs = search_results["hits"]["hits"]
            total_retrieved = len(retrieved_docs)
            if retrieved_docs:
                for i in range(N):
                    if total_retrieved > i:
                        predicted_label = retrieved_docs[i]["_source"]["response_key"]
                    else:
                        predicted_label = "dummy_label"
                    if gold_labels[idx] == predicted_label:
                        true_pos_seen += 1
                        ap += true_pos_seen / (i + 1)
                    else:
                        ap += 0
                if true_pos_seen != 0:
                    ap = ap / true_pos_seen
                mean_ap += ap
            else:
                mean_ap += 0

        mean_ap = mean_ap / len(test_exs)
        return mean_ap

    def _mrr(self, test_exs, gold_labels, N, method, embs_in_batch=True) -> float:
        if method == self.selector.SimMethod.EMBEDDING:
            text_embs = self.selector._text_to_emb(test_exs) if embs_in_batch else None
        mrr = 0
        for idx, ex in enumerate(test_exs):
            rank = 0
            if method == self.selector.SimMethod.EMBEDDING:
                text_embs_idx = text_embs[idx] if embs_in_batch else self.selector._text_to_emb(ex)[0]
            else:
                text_embs_idx = None
            search_results = self.selector._search(ex, text_embs_idx, N, method, date_enabled=False)
            retrieved_docs = search_results["hits"]["hits"]
            if retrieved_docs:
                total_retrieved = len(retrieved_docs)
                for i in range(N):
                    if total_retrieved > i:
                        predicted_label = retrieved_docs[i]["_source"]["response_key"]
                    else:
                        predicted_label = "dummy_label"
                    if gold_labels[idx] == predicted_label:
                        rank += 1
                        mrr += 1 / rank
                        break
                    else:
                        rank += 1
            else:
                mrr += 0

        mrr = mrr / len(test_exs)
        return mrr

    def test_response_time(self, test_exs, N, method, embs_in_batch=True) -> Tuple[float, float]:
        gold_labels = [ex.get('response_key') for ex in test_exs]
        start_time = time.time()
        mean_ap = self._mean_ap(test_exs, gold_labels, N, method, embs_in_batch)
        total_time = time.time() - start_time
        avg_resp_time = total_time/ len(test_exs)
        return mean_ap, avg_resp_time

if __name__ == "__main__":
    csv_path = "data/bank_FAQ_2020.csv"

    config = {
        "retrieval_intent": "faq",
        "batch_size": 2048,
        "es_indexing": {
            "host": "localhost",
            "port": 9200,
            "index_name": "test_faq",
            "analyzer": "standard"
        },
        "bert_client": {
            "enabled": True,
            "host": "localhost",
            "port": 5555,
            "port_out": 5556
            },
        "eval": {"metric": "map", "N": 1}
        }

    evaluator = Evaluator(config)
    evaluator.import_data(csv_path)

    # test indexing time
    total_time, batch_average = evaluator.test_train_time()
    print(f"Total Indexing Time: {total_time}", f"Batch Average Time: {batch_average}", sep='\n')

    # test response accuracy
    # MAP/MRR@1
    mean_ap_1, avergage_response_time = evaluator.test_response_time(evaluator.test_exs, 1, evaluator.selector.SimMethod.TEXT)
    print(f"MAP@1 TEXT: {mean_ap_1}", f"Avg Resp Time: {avergage_response_time}", sep='\n')
    mean_ap_1, _ = evaluator.test_response_time(evaluator.test_exs, 1, evaluator.selector.SimMethod.EMBEDDING, embs_in_batch=True)
    print("MAP@1 BERT:", mean_ap_1)

    # # MAP@3
    mean_ap_3, _ = evaluator.test_response_time(evaluator.test_exs, 3, evaluator.selector.SimMethod.TEXT)
    print("MAP@3 TEXT:", mean_ap_3)
    mean_ap_3, _ = evaluator.test_response_time(evaluator.test_exs, 3, evaluator.selector.SimMethod.EMBEDDING, embs_in_batch=True)
    print("MAP@3 BERT:", mean_ap_3)

    # MRR@3
    print("MRR@3 TEXT:",
        evaluator._mrr(
            evaluator.test_exs,
            [ex.get('response_key') for ex in evaluator.test_exs], 
            3,
            evaluator.selector.SimMethod.TEXT
        )
    )

    print("MRR@3 BERT:",
        evaluator._mrr(
            evaluator.test_exs,
            [ex.get('response_key') for ex in evaluator.test_exs], 
            3,
            evaluator.selector.SimMethod.EMBEDDING,
            embs_in_batch=True
        )
    )

    _, average_response_time = evaluator.test_response_time(
        evaluator.test_exs[:100],
        1,
        evaluator.selector.SimMethod.EMBEDDING,
        embs_in_batch=False)
    print("Average response time BERT:", average_response_time)