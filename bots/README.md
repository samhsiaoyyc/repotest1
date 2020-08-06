# Reserved folder for bots

The file structure:

- `bots/<bot_name>/`
	- `data/`
	- `__init__.py`
	- `config.yml`
	- `credentials.yml`
	- `domain.yml`
	- `endpoints.yml`
	
The source code of common customized action should be put in `/common/rasa_plugins/actions/`, that actions can be imported by every bot in order to keep consistency.