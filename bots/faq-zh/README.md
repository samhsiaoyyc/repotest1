# Test Ground for QuestionSelector

1. Train the model:

		PYTHONPATH=~/seasalt.ai/ngChat rasa train
		
2. Serve:

		PYTHONPATH=~/seasalt.ai/ngChat rasa run --enable-api
		
3. Evaluate:

		python3 evaluate.py
		
You should expect to see results:

```
Test data size: 98
Average_response_time: 0.1261317340695128
MAP@1 for Comparing Q with Q: 0.7244897959183674
MAP@3 for Comparing Q with Q: 0.7857142857142857
MAP@1 for Comparing A and A: 0.7244897959183674
MAP@3 for Comparing A and A: 0.7857142857142857
```