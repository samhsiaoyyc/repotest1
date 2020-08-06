# Taco Bell Bot

This is a chatbot designed to support orders from the Taco Bell menu.

## Docker setup for local development

The following assumes you're running everything on Docker, but should serve
as sufficient reference for setting up in another environment.

First, build an image from the Dockerfile in the top level of this repo. The
current version of the Dockerfile must be modified by adding the following line
before the rasa installation steps:

    RUN ["pip", "install", "questionary==1.5.1"]

To support `chatette`, also add the following:

    RUN ["pip", "install", "chatette==1.6.2"]

The custom actions require the `fuzzywuzzy` library for fuzzy matching, which
optionally uses the `python-Levenshtein` library to execute faster.

    RUN ["pip", "install", "python-Levenshtein=0.12.0"]
    RUN ["pip", "install", "fuzzywuzzy=0.18.0"]

To use the ConveRTTokenizer, we need tensorflow-text. (The most recent verison
is incompatible with the tensorflow version Rasa needs. I don't currently know
what version is needed to ensure compatibility!)

    RUN ["pip", "install", "tensorflow-text"]

Build the image, for example:

    sudo docker build . -t ngchat

Run the image interactively. Forwarding the ports and mounting the working
directory facilitate development.

    sudo docker run -p 5005:5005 -p 5002:5002 -v `pwd`:/app -w /app -it ngchat bash

## Menu Scraper

Training data generation and custom actions both rely on a JSON file with menu
data. Currently, this data is provided by a scraper script.

This script requires the python `selenium` package to be installed along wtih
correct drivers. (The script currently assumes Chrome drivers, but I assume the
script could be modified to use another browser.) Follow the installation
instructions provided (here)[https://pypi.org/project/selenium/]. Once the
driver is installed, export an environment variable specifying the driver path,
e.g.:

    export CHROME_DRIVER_PATH='/home/<username>/bin/chromedriver'

To run the scraper, just call the script:

    python3 taco_scraper.py

The result is saved to `scraped_menu.json`.

Note that the scraper currently is NOT set up to run headless, meaning that it
currently must be run on your local system with a GUI, not on a server. While
we could easily change this in the future to allow it to be incorporated into
an automated build process, the fact that the scraper interacts with the actual
Taco Bell website justifies the reasonable caution provided by a manual
step--we don't actually want this running every time we test our code!

Note that the scraper is currently limited to collecting price, calorie, sauce
option, and addon option information. It does not know about substitution
options. It identifies that drinks have size options, but does not currently
correctly collect the full list of size options.

Many menu items are registered trademarks and annotated as such on the menu.
Rasa does not like these special characters. I currently manually remove these
from the generated 

## Training data generation

The `template_from_menu.py` script generates a chatette template file with items
in the menu:

    python template_from_menu.py scraped_menu.json templates/generated_items.chatette

Run `chatette` to generate training examples
from the templates.

    python3 -m chatette templates/main.chatette -o chatette_out

## Training

Next, train the model, including both the `data` directory and the
generated data in `chatette_out/train`:

    rasa train --data ./data ./chatette_out/train 

The training takes on the order of 5 or 10 minutes on my laptop (without any GPU).

## Running

Once the model has been trained start the rasa actions server:

    rasa run actions &

For an interactive terminal session, run:

    rasa shell

After making any changes to the `actions.py`, be sure to restart the actions
server.

## Testing

To run end-to-end tests:

    rasa test core -s tests/conversation_tests.md --e2e
