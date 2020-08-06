"""
Definition of customer service connctor action.

History:
2020/05/21 Created by Noel
"""

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Form, SlotSet
from typing import Any, Text, Dict, List

REPEAT_LIMITATION = 3


class ActionCheckState(Action):
    """The action to transfer to agent of customer service."""

    def name(self) -> Text:
        """Every action needs a name to identify it."""
        return "action_tranfer_to_servicer"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """To connect to agent of customer service."""
        dispatcher.utter_message(template="utter_to_service")
        # TODO: transer to twilio
        return [
            Form(None)
        ]


class ActionRepeate(Action):
    """The action to don't get understand and please repeat."""

    def name(self) -> Text:
        """Every action needs a name to identify it."""
        return "action_repeate"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Every action needs a name to identify it."""
        if tracker.get_slot("repeat_count") > REPEAT_LIMITATION:
            dispatcher.utter_message(template="utter_to_service")
            # TODO: transer to twilio
            return [
                Form(None)
            ]
        else:
            dispatcher.utter_message(template="utter_again")
            return [
                SlotSet("repeat_count", tracker.get_slot("repeat_count") + 1)
            ]
