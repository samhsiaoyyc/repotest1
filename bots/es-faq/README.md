# Running Locally

1. Download ``elasticsearch-7.8.0``, and extract the archive. ([Instructions](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-install.html#run-elasticsearch-local))
2. In ``elasticsearch-7.8.0/bin``, start multiple (e.g. 3) instances of Elasticsearch to form a multi-node cluster. ([Instructions](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started-install.html#run-elasticsearch-local)) For example, on Linux and macOS, run:
```
./elasticsearch
./elasticsearch -Epath.data=data2 -Epath.logs=log2
./elasticsearch -Epath.data=data3 -Epath.logs=log3
``` 
3. Install dependencies by running ``pip install -r requirements.txt``.
4. Download the pre-trained BERT model and extract the archive. For example, English BERT-Base, Uncased:
```
wget https://storage.googleapis.com/bert_models/2020_02_20/uncased_L-12_H-768_A-12.zip
unzip uncased_L-12_H-768_A-12.zip
```
5. Start BERT service, notice you need to start separate services for different languages with corresponding BERT model. Notice without the ``-cpu`` option, the service will be run on GPU. However, there is no significant performance differences between using CPU and GPU for this bot.
```
bert-serving-start -model_dir uncased_L-12_H-768_A-12 -num_worker=4 -cpu
```

# Evaluation

Using data ``data/bank_FAQ_2020.csv``.
The data has 2180 FAQ intents and 26327 questions, including 1243 intents with 2 or more training examples. Among the 1243 intents, each has on average 21.18 questions as training examples, totaling 25389 examples. The data is shuffled randomly with python `random` and seed = 1, then split using a train/test split of 80/20.

Each mini-batch is of size 2048, where BERT server would split the job into mini-batches of size 256.

| Method   | index time (batch avg) | response time (query avg) | MAP/MRR@1 | MRR@3  |
| -------- | ---------------------- | ------------------------- | ----------| -------|
| TEXT     | 1.17s                  | 0.0032s                   | 0.6605    | 0.7290 |
| BERT CPU | 50.25s                 | 0.1145s                   | 0.5470    | 0.6212 |
| BERT GPU | 50.51s                 | 0.1119s                   | 0.5470    | 0.6212 |

1. No significant performance difference is found between BERT on CPU or GPU. It is possible to use BERT with CPU for both training and prediction.

2. Accuracy is low for this data for the following reasons:
   - training examples for each intent is not enough:
    among 1243 intents with 2 or more training examples, each intent has 21.18 examples on average.

   - many training examples in different intents are very similar, thus led to confusion:
        - Intent 6: 我想要用龍騰**貴賓室** / Intent 207: 機場**貴賓室**
        - Intent 24: **常搭捷運**要用哪張卡 / Intent 164: 可以告訴我平**常搭捷運**的金融卡紅利算法嗎？

Comparing this dataset against ``data/train_zh_cn.json``. This data set has 85 FAQ intents, with 14850 questions as training examples. On average, each intent has 174.71 training examples. The data is shuffled randomly with python `random` and seed = 1, then split using a train/test split of 80/20.

| Method | MAP/MRR@1 | MRR@3  |
| ------ | ----------| -------|
| TEXT   | 0.8896    | 0.9142 |
| BERT   | 0.9319    | 0.9506 |

The result suggests data augmentation/assisted authoring is still very important for improving the accuracies of the performance.

# Relevant References
[ElasticSelector](https://github.com/seasalt-ai/ngChat#elastic-selector)

[``bert-as-service`` Deployment](https://github.com/seasalt-ai/ngChat/blob/master/k8s/bert-as-service/README.md)