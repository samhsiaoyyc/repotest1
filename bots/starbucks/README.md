TO RUN LOCALLY: 
---------------
- Train model:
    - starbucks/ $ rasa train
- Start the actions server in a separate window:
    - $ rasa run actions
- Run Rasa core server (three options):
    - $ rasa shell (cmdline interface)
    - $ rasa interactive (cmdline for debugging/creating train data)
    - $ rasa run --credentials credentials.yml --endpoints endpoints.yml (deploy to endpoint)
- Run in browser with Rasa X for annotation/review:
    - $ rasa export (retrieves conv. logs from database)
    - $ rasa x
    - $ `Do you want to continue with the default SQLite event broker?` -> yes
    - rasa x should open in your web browser; go to conversations to review and annotate
- Run conversation tests:
    - $ ./tests/run_tests.sh -entity_thresh {} -intent_thresh {} -response_thresh {} -reg_thresh {}
    - run_tests.sh will run rasa conversation tests, then run summarize_test.py which gives the test results a pass/fail grade based on the f1-score thresholds set and check for regressions that exceed the regression threshold. Threshold defaults to 0 for regression, and 0.80 for others, or can be set with a command line argument. The process outputs 3 pass/fail grades to the terminal, and creates a file results/RESULT_SUMMARY.txt, which prints out any failing entities/intents/responses with their f1-score and a regression table.

DEPLOYMENT TO K8:
-----------------
- Building docker container:
    - Build: `sudo docker build . -t kittai/ngchat-rasax:starbucksbot-0.0.1 -f bots/starbucks/starbucks.dockerfile`
    - Push: `sudo docker push kittai/ngchat-rasax:starbucksbot-0.0.1`
- Upload model file to Azure:
    - For now just upload to file share through the portal
- K8:
    - If deploy file has been changed: `kubectl apply -f k8s/bots/starbucks.yml`
    - `kubectl get pods -n seasalt` (see all the pods in the deployment listed, including current starbucks bot name)
    - `kubectl delete pod {starbucks_pod_name} -n seasalt` (deleting a pod will make it rerun with the new files)
    - To get the IP address, run `kubectl get services` and look for the external IP of the starbucks-bot-core service.
    - You can now point the Facebook to `{IP}/webhooks/facebook/webhook`. Note that it may take a minute for the bot to start up before it is accessible.

TO RUN ON FACEBOOK MESSENGER:
-----------------------------
- Start rasa and rasa actions server
    - rasa run --credentials credentials.yml --endpoints endpoints.yml
    - rasa run actions
- If running on local machine:
    - Install ngrok (https://ngrok.com/download)
    - Start the ngrok process: $./ngrok http 5005
- Setup the webhook on Facebook
    - For the free version of ngrok, the url changes every time it's run so you have to reset the webhook in facebook each time
    - Facebook for developers -> My Apps -> Webhooks -> Edit subscription
        - {https://_______.ngrok.io}/webhooks/facebook/webhook/
        - Verify token = VolliTheVolligator
    - Also change this in Messenger -> Webhooks -> Edit callback URL
- Use messenger to send a message to CoffeeBot - in development mode only users with special permission are allowed to use the bot

FUTURE IMPROVEMENTS:
--------------------
- generalize actions.py to base required slots on menu (ie/ it should not ask size for a baked good)
- composite entities in order to support multiple item selection in one utterance
    - https://pypi.org/project/rasa-composite-entities/ 
- explore different dialogue management - rasa forms are awful 
- Switch to using RasaX for deployment to take advantage of conversation annotation tools
    - https://rasa.com/docs/rasa-x/installation-and-setup/customize/ 
- Whenever requesting a slot (size, add-ons, etc) provide some options
    - how to keep track of popular/previously ordered options?

REMINDER:
----------
- Run before pushing:
    - flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
    - pytype --keep-going bots/starbucks

SPHINX DOCUMENTATION:
---------------------
- Building Sphinx documentation:
    - Update the api documentation:
        - $ sphinx-apidoc -f -o sphinx/source bots/starbucks
    - Run the build:
        - /sphinx$ make {build_type}
    - Built files can be found in bots/starbucks/docs

   
CURRENT CAPABILITIES:
---------------------
- Greeting/goodbye
- Volligator FAQ
- Load menu from a json file
    - Ask about the menu
    - Ask about a category on the menu
- Manage a cart:
    - Add an item
    - Remove an item
    - List all items in the cart
    - Empty the entire cart
- "Checkout" (shell is there, just no actually purchasing capability)

CART.PY OVERVIEW:
------------------
- class Cart:
    - attributes: cart_items, active_item, menu
    - methods:
        - add_item_instance(to_add: ItemInstance) -> None
        - add_item_name(item_name: Text)
        - add_option(item_name: Text, option: Text) -> int
        - modify_quantity(item_name: Text, new_quant: int) -> int
        - modify_option(item_name, option_name, option_value) -> None
        - get_matching_menu(store_name, menu_dir_path) -> Any
        - get_matching_cart_item(item_name) -> Any
        - fetch_item(item_name) -> Any
        - remove_item(item_name) -> None
        - list_contents() -> Text
        - sum_{cost|calories}() -> float
        - clear() -> None
        - checkout() -> None
        - get_requested(requested_item) -> tuple
        - get_item_names() -> List
- class Menu:
    - attributes: name, menu_items, categories
    - methods:
        - load_menu(name, menu_dir_path)
        - from_json(menu_path) -> Any
        - get_matching_menu_item(item_name) -> Any
        - get_matching_menu_category(cat_name) -> Any
        - describe_menu() -> Text
        - describe_category(category) -> Text
        - match_requested(requested, search_type={item|category}) -> List
- class ItemType:
    - attributes: name, image, description, base_cost, base_calories, option_fields, option_types, requirements
    - methods:
        - from_data(name, data) -> ItemType
        - get_matching_item_option(option) -> Any
        - describe_item() -> Text
        - describe_options(option) -> Text
- class ItemInstance:
    - attributes: item_type, options, quantity
    - methods:
        - from_item_name(name, menu) -> Any
        - to_text() -> Text
        - {cost|calories}() -> float
        - unmet_requirements() -> List
- class OptionField:
    - attributes: name, opt_type, category, selected, quantity, calories, price
    - methods:
        - from_data(name, data) -> OptionField
        - to_text() -> Text
    

JSON MENU FORMAT SCHEMA: 
------------------------
menu file naming: '/{store_name}_menu.json'

json file menu item format:

    "{item_name}": {
        "description": "{Description_text}",
        "image": "{image_url}"
        "category": "{category_name}",
        "price": "{price in dollars - ex/ 4.50}", 
        "calories": "{calories as an integer}",
        "required_slots": [
            "{required slot 1}", 
            "{required slot 2}"
        ],
        "options": {
            "{opt_name}": {
                "type": "{option_type}",
                "category": bool, (can users select only one?)
                "selected": bool,
                "quantity": null, (null unless quantity required)
                "calories": "{# cal}",
                "price": "{price in dollars}"
            }
        }
    }
NOTES: 
    - base price should be based on the cheapest version of the item, like the smallest size
    - price for options should represent how much is added to the base price. For example, if an 8oz espresso is 1.50 and a 12oz espresso is 1.75, the base cost for the item would be 1.50 and the price for the option '12oz' would be .25.

RASA USER STORIES:
-------------------
- I want to train my models:
    - rasa train
- I want to train my models and run Rasa in the terminal:
    - rasa train
    - rasa run actions
    - rasa shell
- I want to train my models and run Rasa in Rasa X:
    - rasa train
    - rasa run actions
    - rasa x
- I want to train my models and run Rasa in interactive mode:
    - rasa train
    - rasa run actions
    - rasa interactive
- When I edit and save nlu.md, I want to retrain my nlu model:
    - if (save nlu.md): rasa train nlu
- When I edit and save domain.md, I want to retrain my core model:
    - if (save domain.md): rasa train core
- When I edit and save actions.py, I want to restart my actions server: 
    - if (save actions.py): rasa run actions
- I want to change the name of an intent, utterance, or action
    - vim: :%s/{old name}/{new name}/g
    - find and replace names in: actions.py, domain.yml, stories.md, nlu.md, conversation_tests.md

RASA ISSUES & SOLUTIONS:
-------------------------
- NameError or EventType error:
   - May be forgetting import
   - from typing import Text, List, Dict, Any, Union
   - from rasa_sdk import Action, Tracker
   - from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
   - from rasa_sdk.executor import CollectingDispatcher
   - from rasa_sdk.forms import FormAction
- When attempting to run "Asyncio error: Event loop is already running"
    - Check questionary version, if questionary > 1.5.1, revert to questionary==1.5.1
    - UPDATE: After using questionary==1.5.1 for about a month, it randomly gave me the same error again. I downgraded to questionary==1.4.0 as suggested in the Rasa forum and it is working again. https://forum.rasa.com/t/error-this-event-loop-is-already-running/24017/3 
    - UPDATE: on 5/15/20 I switched to a Linux environment and again, questionary==1.5.1 did not work. Looks like 1.4 is the most consistant 
- When attempting to train "cudart64-101.dll cannot be found"
    - downgrade to cudatoolkit==10.1
- SlotSet doesn't actually change the values when you run your action
    - SlotSet is an event and should be passed back in the return list, it cannot be called inside the run method
- ConveRT dependencies unavailable on windows OS
    - ConveRT{Tokenizer|Featurizer} require tensorflow-text which is currently not available on windows OS
    - Switch to WhitespaceTokenizer or train on a different OS: https://github.com/tensorflow/text/issues/44 
- FollowUpActions: 
    - It may be the case that returning more than one FollowUpAction from a run method will only activate the last one. When I returned [FollowupAction("actions_clear_slots"), "FollowupAction("actions_cart_to_string")], clear_slots was never triggered. From what I read online it seems that maybe only one FollowUpAction can be triggered by returning from a run function. However, I got it to work by swapping the order and returning ["cart_to_string", "clear_slots"] - I'm not sure why this worked. 
- Annoying warnings from Tensorflow:
    - If you do not have a nvidia graphics card, you may get a large amount of warnings from tensorflow when running rasa train or shell. Tensorflow will automatically use your CPU if no nvidia graphics card is detected, but as far as I can tell there is no way to remove these warnings
- Breaking out of forms:
    - Forms become problematic when you are inside of one but the user wants to ask a question or break out of the form. Other intents can be forced by modifying the domain file and slot_mappings in actions.py.
    - domain: add {trigger: action_(name)} next to the intents that you want to force
    - slot_mappings: add (not_intent="{intent_name}") as a parameter to any call that doesn't already specify an intent (combining this with something that specifies (intent="{intent_name"}) will throw an error)
- Doesn't tell me where error is coming from when training: For example, I get the error "Feature 'intent_{}' could not be found in feature map". This means that I called my intent the wrong thing in another file - but which file?? I have a typo but I have no idea where it is
    - I want a way to check my files *before* I train to make sure that there are no typos and that intents/entities/slots are present in domain, nlu, and stories
- Changing intent/entity/action names
    - apparently rasa maintains some sort of history of previously trained models. If you rename an intent, entity, or action, rasa will continue to classify them as the old name (even if those names no longer exist in any of your files and you retrain!!). The old names no long have any actions tied to them so the bot does nothing.
    - UPDATE: I tried renaming the problem intents (describe_menu -> TEST_MENU) in domain, stories, and nlu, and then retrained the models. During training I could see that the old-old intent names (ask_describe_menu) that were causing problems were gone, and I saw both describe_menu and TEST_MENU. After testing I immediately reverted my changes and retrained the models again. This time only the correct intent names were maintained. This doesn't seem like a good solution, but it is the only thing that worked for me.
