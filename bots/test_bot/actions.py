"""Test bot for deployment and api testing."""
# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGreet(Action):
    """Greet."""

    def name(self) -> Text:
        """Set name."""
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Utter a greeting."""
        if tracker.get_slot('name'):
            dispatcher.utter_message(f"Coming to you straight from a custom action: Hello, "
                                     f"{tracker.get_slot('name')}! How are you?")
        else:
            dispatcher.utter_message("Coming at you straight from a custom action: Hello there! How are you?")

        return []
