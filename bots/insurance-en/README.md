# Example bot for E Call Bao

TODO:

- [X] fix error for setting slots (by running interactive)
- [X] provide button payload as answers
- [X] finish test stories

## Get Started

### Test the bot

	rasa run actions &
	rasa train
	rasa shell -v

Then you can type:

> Your input ->  hi 
>> Hey! How are you?
>
> Your input ->  i'd like to quote insurance
>> What is your name? 
>
> Your input ->  xuchen yao
>> is the applicant currently under guardianship?
>
> Your input ->  why do you ask
>> If the applicant is under guardianship, we cannot legally provide insurance to them without a legal guardian present.
>> 
>> is the applicant currently under guardianship?
>
> Your input ->  no
>> could you please provide your birthday?
>
> Your input ->  01/01/1970
>> how many days do you want to insure for?
> 
> Your input ->  10 days
>> which country are you traveling to?
> 
> Your input ->  japan
>> what's the total insurance amount?
>
> Your input ->  $10000
>> amount can only be between $60,000 to $1500,000
>> what's the total insurance amount?
>
>  Your input ->  $100000
>> do you need air ambulance support?
>
>  Your input ->  yes

### Installation

rasa x's latest version was 0.27, however it didn't work for me. 0.26.3 works:

	pip install  rasa-x==0.26.3 --extra-index-url https://pypi.rasa.com/simple
	
This also installs `rasa 1.8.3`, `rasa sdk 1.8.0` and TensorFlow `2.1.0`.

### Run

	rasa run actions &
	rasa train
	rasa shell -v

To add more stories, use:

	rasa interactive
	

To see story visualization on Mac, you'll need:

	brew install graphviz
	dot -Tpng story_graph.dot -o story_graph.png

for e2e testing:

	rasa test --e2e --stories test_stories.md

### Note

1. I hesitate to use `rasa x` because it modifies my source files in the background. I had some `regex` incorrectly defined in `nlu.md` and it was deleted by `rasa x`.


## Design Guidelines

[How many stories do you need?](https://blog.rasa.com/designing-rasa-training-stories/)

[rasa-demo](https://github.com/RasaHQ/rasa-demo) and its [actions.py](https://github.com/RasaHQ/rasa-demo/blob/master/demo/actions.py), [nlu.md](https://raw.githubusercontent.com/RasaHQ/rasa-demo/master/data/nlu/nlu.md), [stories.md](https://raw.githubusercontent.com/RasaHQ/rasa-demo/master/data/core/stories.md)
