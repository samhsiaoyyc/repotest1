"""
Evaluate MAP@1 and MAP@3 of a given model.

History:
2020/06/05 Authored by Xuchen Yao
"""
import requests
import time
import json
from collections import defaultdict
from typing import (
    Dict,
    Text,
    List,
    Tuple,
)


class QQDataset(object):
    """A dataset for Q&Q pairs."""

    def __init__(
        self,
        train_nlu_json: Text,
        test_nlu_json: Text,
        train_response_md: Text,
    ):
        """Construct a dataset

        Args:
            train_nlu_json (Text): 'data/nlu.json'
            test_nlu_json (Text): 'test_nlu.json'
            train_response_md (Text): 'data/responses.md'
        """
        self.faq_intent2questions_train = self.load_nlu_data_json(train_nlu_json)
        self.faq_intent2questions_test = self.load_nlu_data_json(test_nlu_json)
        self.faq_intent2response = self.load_response_md(train_response_md)

    @staticmethod
    def load_nlu_data_json(file_path) -> Dict[Text, List]:
        """Load a nlu.json file.

        Args:
            file_path ([type]): file path

        Returns:
            Dict[Text, List]: a mapping between faq intent and a list of similar questions
        """
        faq_intent2questions = defaultdict(list)
        with open(file_path) as f:
            data = json.load(f)["rasa_nlu_data"]["common_examples"]
        for line in data:
            intent = line["intent"]
            question = line["text"]
            if intent.startswith("faq/"):
                faq_intent2questions[intent].append(question)
        return faq_intent2questions

    @staticmethod
    def load_response_md(file_path: Text) -> Dict[Text, Text]:
        """Load a responses.md file

        Args:
            file_path (Text): file path

        Returns:
            Dict[Text, Text]: a mapping between faq intent and response
        """
        faq_intent2response = {}
        with open(file_path) as f:
            data = f.readlines()

            intent = ""
            for line in data:
                line = line.strip()
                if line.startswith("##"):
                    continue
                elif line.startswith("*"):
                    intent = line[1:].strip()
                elif line.startswith("- "):
                    response = line.strip().replace("- ", "")
                    if intent.startswith("faq/"):
                        faq_intent2response[intent] = response
        return faq_intent2response


class Evaluator:
    """Evaluate model response by posting queries to /model/parse endpoint.
    """

    def __init__(self, dataset: QQDataset, server="http://localhost:5005/model/parse"):
        """Init Evaluator.

        Args:
            dataset ([QQDataset]): a QQDataset
            server (str, optional): server address. Defaults to "http://localhost:5005/model/parse".
        """
        self.dataset = dataset
        self.server = server
        self.test_questions: List[Text] = []
        self.gold_questions: List[List[Text]] = []
        self.gold_responses: List[Text] = []

        for intent, ques_ls in self.dataset.faq_intent2questions_test.items():
            for ques in ques_ls:
                self.test_questions.append(ques)
                self.gold_questions.append(self.dataset.faq_intent2questions_train[intent])
                self.gold_responses.append(self.dataset.faq_intent2response[intent])

    def get_model_responses(self) -> Tuple[List[List[Text]], List[List[Text]], float]:
        """Post query to model and get responses

        Returns:
            Tuple[List[Text], List[Text], float]: a list of model responses, questions, and average time
        """
        model_responses = []
        model_questions = []
        time_ls = []
        for question in self.test_questions:
            start_time = time.time()
            retrival = requests.post(self.server, json={"text": question}).json()
            time_ls.append(time.time() - start_time)

            ranking = retrival["question_selector"]["faq"]["ranking"]
            responses = [x["name"] for x in ranking]
            model_responses.append(responses)
            model_questions.append([x["most_similar_question"] for x in ranking])
            # print(question, responses)

        avg_resp_time = sum(time_ls) / len(time_ls)
        return model_responses, model_questions, avg_resp_time

    def get_hit_list(self, gold_questions, model_questions, test_questions) -> List[int]:
        """Get Hit list.

        Args:
            gold_questions ([type]): gold questions
            model_questions ([type]): most similar questions returned by model
            test_questions ([type]): questions to send to model

        Returns:
            List[int]: a list of hit@?, ? is -1 when not hit
        """
        assert len(gold_questions) == len(
            model_questions
        ), "response length don't match"

        hit_at = []
        for i, gold_response in enumerate(gold_questions):
            hit_idx = -1
            print()
            print(f"======== question:       {test_questions[i]}")
            print(f"======== model response: {model_questions[i]}")
            print(f"======== gold response:  {gold_response}")
            for idx, model_question in enumerate(model_questions[i]):
                # print(model_question, gold_response)
                if model_question in gold_response:
                    hit_idx = idx
                    break
            hit_at.append(hit_idx)
        print(hit_at)
        return hit_at

    @staticmethod
    def MAP(at_n: int, hit_at: List[int]) -> Tuple[float, int, int]:
        """Calculate Mean Average Precision

        Args:
            at_n (int): ? for MAP@?
            hit_at (List[int]): a list of hits positions

        Returns:
            Tuple[float, int, int]: MAP number, number of hits, and total number of answers
        """
        if not hit_at:
            print("Metric MAP: hit_at is empty!")
            return 0, 0, 0
        num_answers = len(hit_at)
        num_hits = 0
        for h in hit_at:
            # Note h starts from 0 (1st candidate hits)
            if h >= 0 and h <= at_n - 1:
                num_hits += 1
        mapn = num_hits * 1.0 / num_answers
        return mapn, num_hits, num_answers

    def evaluate(self):
        """Evaluate model performance by calculating MAP@1 and MAP@3
        """
        model_responses, model_questions, avg_resp_time = self.get_model_responses()

        print("======= Testing Responses ======")
        hit_at = self.get_hit_list(self.gold_responses, model_responses, self.test_questions)
        map_1_q = self.MAP(1, hit_at)
        map_3_q = self.MAP(3, hit_at)
        print(len(self.gold_questions), len(model_questions), len(self.test_questions))
        print()

        print("======= Testing Similar Questions ======")
        hit_at = self.get_hit_list(self.gold_questions, model_questions, self.test_questions)
        map_1_response = self.MAP(1, hit_at)
        map_3_response = self.MAP(3, hit_at)
        print(len(self.gold_questions), len(model_questions), len(self.test_questions))
        print("Test data size: %s" % map_1_q[2])

        print("Average_response_time: %s" % avg_resp_time)
        print("MAP@1 for Comparing Q with Q: %s" % map_1_q[0])
        print("MAP@3 for Comparing Q with Q: %s" % map_3_q[0])
        print("MAP@1 for Comparing A and A: %s" % map_1_response[0])
        print("MAP@3 for Comparing A and A: %s" % map_3_response[0])


if __name__ == "__main__":

    train_nlu_file = "data/nlu.json"
    test_nlu_file = "test_nlu.json"
    response_file = "data/responses.md"

    test_dataset = QQDataset(train_nlu_file, test_nlu_file, response_file)

    evaluator = Evaluator(test_dataset)
    evaluator.evaluate()
