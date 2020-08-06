# Cathay Bank Chinese training

There are 3 directory to use

1. `./configs` as directory contain pipelines for training chinese data
	-  `config-default-supervised.yml` & `config.yml` are supervised pipeline with white space tokenizer
	-  `config-jieba-supervised.yml` are supervised pipeline but use jieba tokenizer to replace white space tokenizer 
	-  `config-jieba-mitie.yml` used jieba tokenizer and mitie nlp component
	-  `config-zhchar-supervised.yml` used ZhCharTokenizer, EmbeddingIntentClassifier and CRFEntityExtractor
	-  `config-zhchar-DIET.yml` used ZhCharTokenizer and DIETClassifier
2. `./data` as the directory contain training data
   - `train_data.json` for `jieba-supervised.yml` config to test non-white-space case
   - `train_data_space.json` for `config-default-supervised.yml` config to test white-space case
3. `./components` as the directory contain `jiaba` dictionary and `mitie` model for training 
 [( you can download here )](https://drive.google.com/open?id=1yn5Jz3jwQxCf32AP-M4GnSgLn1_r2TG3) [original source](https://github.com/Aguila-team/Chinese_NLU_by_using_RASA_NLU)

## Get Started

### Installation

rasa x's latest version was 0.27, however it didn't work for me. 0.26.3 works:

	pip install  rasa-x==0.26.3 --extra-index-url https://pypi.rasa.com/simple
	
This also installs `rasa 1.8.3`, `rasa sdk 1.8.0` and TensorFlow `2.1.0`.

Install pipeline dependencies of `Jieba` & `MITIE` :

	pip install jieba 
	pip install cmake
	pip install git+https://github.com/mit-nlp/MITIE.git

For `Jieba` & `MITIE`, also need download pipeline component from google driver [link here](https://drive.google.com/open?id=1yn5Jz3jwQxCf32AP-M4GnSgLn1_r2TG3)

### Set up PYTHONPATH
	Run this one

		export PYTHONPATH=/absolute_path_to_ngChat/:$PYTHONPATH	

	Or prefix PYTHONPATH on every run:

		PYTHONPATH=/absolute_path_to_ngChat/:$PYTHONPATH rasa run  ...

### Run

	rasa train nlu -c configs/config-jieba-mitie.yml -u data/training_data.json --out models/jieba-mitie

### Test NLU pipeline

[docs for testing nlu](https://rasa.com/docs/rasa/user-guide/testing-your-assistant/#evaluating-an-nlu-model)

[components](https://rasa.com/docs/rasa/nlu/components)

#### Summary

| classifier                                      | tokenizer       | time per fold | intent F1 | entity F1 | speed   | space | F1    |
|-------------------------------------------------|-----------------|---------------|-----------|-----------|---------|-------|-------|
| EmbeddingIntentClassifier<br>CRFEntityExtractor | white space     | 5 min        | 80.2%     | 57.7%     | faster  | small | ok    |
| DIETClassifier                                  | white space     | 50 min        | 82.2%     | 61.1%     | slow    | small | better  |
| EmbeddingIntentClassifier<br>CRFEntityExtractor | LM Transformers | 16 min        | 81.6%     | 59.5%     | fast    | large | good  |
| DIETClassifier                                  | LM Transformers | 1h 12min      | 82.7%     | 56.5%     | slower  | large | mixed |
| MITIE                                           | jieba           | 13h           | 76.8%     | 35.4%     | slowest | large | bad   |
| EmbeddingIntentClassifier<br>CRFEntityExtractor | zhChar          | 5 min        | 80.3%     | 58.8%     | fastest  | small | ok    |
| DIETClassifier                                  | zhChar          | 61 min        | 82.3%     | 61.7%     | slow    | small | best  |

Note:

1. "time per fold" includes both training testing time: some classifiers are very fast in training (such as EmbeddingIntentClassifier) but spend most time in testing.
2. every fold of MITIE includes about 15 hyper-parameter tuning, so without tuning time was about 52 min (however F1 isn't good anyways)
3. in terms of space:
	* Mitie: 321MB
	* bert-base-chinese ([details](https://github.com/google-research/bert/issues/155)): 457MB

Verdict:

1. I'd use EmbeddingIntentClassifier + CRFEntityExtractor + Transformers for a balance of speed and performance
2. I'd need to spend more time to find out why DIETClassifier + Transformers gives bad results on entity F1

#### Details

Below is a comparison with running 5 fold cross validation:

- test white-space supervised [EmbeddingIntentClassifier](https://rasa.com/docs/rasa/nlu/components/#embeddingintentclassifier) and [CRFEntityExtractor](https://rasa.com/docs/rasa/nlu/components/#crfentityextractor)

		rasa test nlu  -c configs/config-default-supervised.yml -u data/training_data_space.json --cross-validation

	training time is about 5 minutes per fold.
	
	Results:

	```
	CV evaluation (n=5)
	Intent evaluation results
	train Accuracy: 0.983 (0.002)
	train F1-score: 0.983 (0.002)
	train Precision: 0.983 (0.002)
	test Accuracy: 0.802 (0.009)
	test F1-score: 0.802 (0.007)
	test Precision: 0.812 (0.004)
	Entity evaluation results
	Entity extractor: CRFEntityExtractor
	train Accuracy: 0.998 (0.000)
	train F1-score: 0.783 (0.026)
	train Precision: 0.839 (0.044)
	Entity extractor: CRFEntityExtractor
	test Accuracy: 0.995 (0.002)
	test F1-score: 0.577 (0.082)
	test Precision: 0.684 (0.090)
	```

- test white-space supervised [DIETClassifier](https://rasa.com/docs/rasa/nlu/components/#id20)

		rasa test nlu  -c configs/config-default-DIET.yml -u data/training_data_space.json --cross-validation

	Warning: this joint model takes significant more time to train (50 minutes with 1 fold)
	
	Results:
	
	```
    Intent evaluation results
    train Accuracy: 0.983 (0.001)
    train F1-score: 0.983 (0.001)
    train Precision: 0.984 (0.001)
    test Accuracy: 0.824 (0.013)
    test F1-score: 0.822 (0.014)
    test Precision: 0.829 (0.015)
    Entity evaluation results
    Entity extractor: DIETClassifier
    train Accuracy: 0.998 (0.000)
    train F1-score: 0.855 (0.017)
    train Precision: 0.814 (0.015)
    Entity extractor: DIETClassifier
    test Accuracy: 0.995 (0.001)
    test F1-score: 0.611 (0.037)
    test Precision: 0.642 (0.092)
	```

- test Transformers with EmbeddingIntentClassifier and CRFEntityExtractor

		pip install rasa[transformers]==1.8.3
		rasa test nlu -c configs/config-transformers.yml -u data/training_data.json --cross-validation
	
	This will use all of your GPUs to train; if you prefer to use CPU, you can prefix with `rasa test` with: `CUDA_VISIBLE_DEVICES=-1`.
	
	Results:
	
	```
	CV evaluation (n=5)
	Intent evaluation results
	train Accuracy: 0.982 (0.003)
	train F1-score: 0.982 (0.003)
	train Precision: 0.982 (0.003)
	test Accuracy: 0.818 (0.011)
	test F1-score: 0.816 (0.010)
	test Precision: 0.826 (0.006)
	Entity evaluation results
	Entity extractor: CRFEntityExtractor
	train Accuracy: 0.998 (0.000)
	train F1-score: 0.770 (0.028)
	train Precision: 0.835 (0.027)
	Entity extractor: CRFEntityExtractor
	test Accuracy: 0.996 (0.001)
	test F1-score: 0.595 (0.067)
	test Precision: 0.711 (0.138)
	```

- test Transformers with DIETClassifier

		pip install rasa[transformers]==1.8.3
		rasa test nlu -c configs/config-transformers-DIET.yml -u data/training_data.json --cross-validation
	
	This will use all of your GPUs to train; if you prefer to use CPU, you can prefix with `rasa test` with: `CUDA_VISIBLE_DEVICES=-1`.
	
	Results:
	
	```
	Intent evaluation results
	train Accuracy: 0.981 (0.003)
	train F1-score: 0.981 (0.003)
	train Precision: 0.982 (0.002)
	test Accuracy: 0.830 (0.019)
	test F1-score: 0.827 (0.017)
	test Precision: 0.836 (0.011)
	Entity evaluation results
	Entity extractor: DIETClassifier
	train Accuracy: 0.998 (0.000)
	train F1-score: 0.862 (0.017)
	train Precision: 0.805 (0.021)
	Entity extractor: DIETClassifier
	test Accuracy: 0.994 (0.001)
	test F1-score: 0.565 (0.109)
	test Precision: 0.593 (0.140)
	```


- test jieba supervised

		rasa test nlu --config configs/config-jieba-supervised.yml -u data/training_data.json --cross-validation

	training time is about 10 minutes per fold
	
	Results: 

		CV evaluation (n=5)
		Intent evaluation results
		train Accuracy: 0.978 (0.002)
		train F1-score: 0.978 (0.002)
		train Precision: 0.979 (0.002)
		test Accuracy: 0.779 (0.016)
		test F1-score: 0.778 (0.015)
		test Precision: 0.791 (0.013)
		Entity evaluation results
		Entity extractor: CRFEntityExtractor
		train Accuracy: 0.998 (0.000)
		train F1-score: 0.722 (0.042)
		train Precision: 0.862 (0.034)
		Entity extractor: CRFEntityExtractor
		test Accuracy: 0.995 (0.001)
		test F1-score: 0.443 (0.046)
		test Precision: 0.681 (0.142)

- test jieba-mitie

		rasa test nlu --config configs/config-jieba-mitie.yml -u data/training_data.json --cross-validation

	training time was 2 days 16 hours. Mitie internally does hyper-parameter turning on `C` (15 times each fold), which contributes to the slow time significantly. Without tuning, it takes about 5 hours to run 5 fold CV.

	Results:

	```
	CV evaluation (n=5)
	Intent evaluation results
	train Accuracy: 0.957 (0.022)
	train F1-score: 0.957 (0.023)
	train Precision: 0.958 (0.021)
	test Accuracy: 0.775 (0.012)
	test F1-score: 0.768 (0.016)
	test Precision: 0.773 (0.018)
	Entity evaluation results
	Entity extractor: MitieEntityExtractor
	train Accuracy: 0.997 (0.000)
	train F1-score: 0.626 (0.066)
	train Precision: 0.845 (0.027)
	Entity extractor: MitieEntityExtractor
	test Accuracy: 0.995 (0.001)
	test F1-score: 0.354 (0.074)
	test Precision: 0.498 (0.089)
	```

- test zhchar-supervsied

        cd ngChat
		PYTHONPATH=./:$PYTHONPATH rasa test nlu --config bots/cathay-bank-zh/configs/config-zhchar-supervised.yml -u bots/cathay-bank-zh/data/training_data.json --cross-validation

	training time is about 5 minutes per fold

	Results:

		CV evaluation (n=5)
		Intent evaluation results
		train Accuracy: 0.973 (0.002)
		train F1-score: 0.973 (0.002)
		train Precision: 0.974 (0.002)
		test Accuracy: 0.803 (0.012)
		test F1-score: 0.803 (0.012)
		test Precision: 0.812 (0.014)
		Entity evaluation results
		Entity extractor: CRFEntityExtractor
		train Accuracy: 0.998 (0.000)
		train F1-score: 0.788 (0.024)
		train Precision: 0.830 (0.024)
		Entity extractor: CRFEntityExtractor
		test Accuracy: 0.996 (0.001)
		test F1-score: 0.588 (0.040)
		test Precision: 0.672 (0.030)

- test zhchar-DIET
	
		PYTHONPATH=../../:$PYTHONPATH rasa test nlu --config configs/config-zhchar-DIET.yml -u data/training_data.json --cross-validation
		
	training time is about 60 minutes per fold. Results:
	
		CV evaluation (n=5)
		Intent evaluation results
		train Accuracy: 0.983 (0.001)
		train F1-score: 0.983 (0.001)
		train Precision: 0.984 (0.001)
		test Accuracy: 0.826 (0.005)
		test F1-score: 0.823 (0.006)
		test Precision: 0.830 (0.008)
		Entity evaluation results
		Entity extractor: DIETClassifier
		train Accuracy: 0.998 (0.000)
		train F1-score: 0.874 (0.013)
		train Precision: 0.822 (0.021)
		Entity extractor: DIETClassifier
		test Accuracy: 0.995 (0.001)
		test F1-score: 0.617 (0.083)
		test Precision: 0.629 (0.091)
