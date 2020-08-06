# flake8: noqa
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from rasa_sdk import Tracker
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from typing import Any, Text, List, Dict, Union
import email


class InsuranceForm(FormAction):

    def name(self) -> str:
        return 'insurance_form'

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return [
            "name",
            "is_under_guardianship",
            "birthday",
            "insurance_day",
            "travel_country",
            "total_amount",
            "need_airlift",
            "email",
        ]

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        dispatcher.utter_message("Thank you for submission")
        return []

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:

        """A dictionary to map required slots to
        - an extracted entity
        - intent: value pairs
        - a whole message
        or a list of them, where a first match will be picked"""

        # TODO: correct this
        return {
            "is_under_guardianship": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ],
            "need_airlift": [
                self.from_intent(intent="affirm", value=True),
                self.from_intent(intent="deny", value=False),
            ]
        }

    def validate_email(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # parseaddr('Full Name <full@example.com>')
        # ('Full Name', 'full@example.com')
        # parseaddr('[invalid!email]')
        # ('', '')
        result = email.utils.parseaddr(value)
        if '@' in result[1]:
            return {"email": result[1]}
        else:
            dispatcher.utter_message(template="utter_correct_email")
            return {"email": None}

    @staticmethod
    def get_travel_countries():
        countries = [
            'Japan', 'Taiwan', 'Burma', 'Cambodia',
            'China/HK/Macao', 'South Korea', 'Laos', 'Malaysia',
            'Singapore', 'Thailand', 'The Philippines', 'Vietnam',
            'Other Countries'
        ]

        return set([c.lower() for c in countries])

    def validate_travel_country(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if value.strip().lower() in self.get_travel_countries():
            return {'travel_country': value.strip()}
        else:
            dispatcher.utter_message(template="utter_correct_country")
            return {'travel_country': None}

    @staticmethod
    def get_amount_range():
        return 60000, 1500000

    def validate_total_amount(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # value: $1000
        try:
            if type(value) is not int:
                value = int(value.replace('$', '').replace(',', '').strip())
            ranges = self.get_amount_range()
            if ranges[0] < value < ranges[1]:
                return {'total_amount': value}
            else:
                raise ValueError
        except ValueError:
            dispatcher.utter_message(template="utter_correct_amount")
            return {'total_amount': None}


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
