# Example bot for TaiShin Bank zh version

TODO:

- [ ] Streaming Twilio SMS service.
- [ ] Streaming Twilio Voice service.

## Get Started

### Installation

rasa x's latest version was `0.27.3`, For consistency, we use rasa x `0.26.3`:

  pip install rasa-x==0.26.3 --extra-index-url https://pypi.rasa.com/simple

However the current installer of rasa x `0.26.3` include rasa `1.8.3`, rasa sdk `1.9.0` and TensorFlow `2.1.0`. Please downgrade those versions:

  pip install rasa==1.8.3
  pip instrall rasa-sdk==1.8.0

If you have issue with tensorflow imported problem while using rasa, [this page](https://www.tensorflow.org/install/source) may do some help.

### Run

  cd ngChat/
  export PYTHONPATH=/absolute_path_to_ngChat/:$PYTHONPATH	
  rasa train --data bots/tsbank-zh/data/ -c bots/tsbank-zh/config.yml -d bots/tsbank-zh/domain.yml --out bots/tsbank-zh/models/ 
  rasa shell -m bots/tsbank-zh/models/ -v

To add more stories, use:

  rasa interactive --data bots/tsbank-zh/data/ -c bots/tsbank-zh/config.yml -d bots/tsbank-zh/domain.yml --out bots/tsbank-zh/models/ 

for e2e testing:

  rasa test -u bots/tsbank-zh/data/ -c bots/tsbank-zh/config.yml -d bots/tsbank-zh/domain.yml --out bots/tsbank-zh/results --e2e --stories bots/tsbank-zh/test_stories.md
