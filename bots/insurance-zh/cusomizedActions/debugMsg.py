"""
Definition of debug message action.

History:
2020/05/21 Created by Noel
"""

from datetime import datetime, timezone
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List


STRING_DEBUG_HEAD = "[DEBUG] "
STRING_SUBSTITUTION = ""


class ActionCheckState(Action):
    """The action to check conversation state."""

    def name(self) -> Text:
        """Every action needs a name to identify it."""
        return "action_check_state"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """To print out the information of this state."""
        print(
            "---------- Action Check State %f ----------" % datetime.now(
                tz=timezone.utc
            ).timestamp()
        )
        if tracker.get_slot("is_debug_mode") is True:
            print(STRING_DEBUG_HEAD, "sender_id ", tracker.sender_id)

            print(STRING_SUBSTITUTION)
            print(STRING_DEBUG_HEAD, "slot list:")
            for key in list(tracker.current_slot_values()):
                print(" - " + key + ": " + str(tracker.get_slot(key)))

            print(STRING_SUBSTITUTION)
            print(STRING_DEBUG_HEAD, "active_form ", tracker.active_form)

            print(STRING_SUBSTITUTION)
            print(
                STRING_DEBUG_HEAD,
                "followup_action ",
                tracker.followup_action
            )

            # print(STRING_SUBSTITUTION)
            # print(
            #    STRING_DEBUG_HEAD,
            #    "get_latest_entity_values ",
            #    tracker.get_latest_entity_values()
            # )
            # print(STRING_SUBSTITUTION)
            # print(
            #   STRING_DEBUG_HEAD,
            #   "get_latest_input_channel ",
            #   tracker.get_latest_input_channel()
            # )
            # print(STRING_SUBSTITUTION)
            # print(
            #   STRING_DEBUG_HEAD,
            #   "idx_after_latest_restart ",
            #   tracker.idx_after_latest_restart()
            # )
            # print(STRING_SUBSTITUTION)
            # print(STRING_DEBUG_HEAD, "is_paused ", tracker.is_paused())

            print(STRING_SUBSTITUTION)
            print(STRING_DEBUG_HEAD, "latest_message ")
            print(tracker.latest_message)

            print(STRING_SUBSTITUTION)
            print(
                STRING_DEBUG_HEAD,
                "latest_action_name ",
                tracker.latest_action_name
            )

            # print(STRING_SUBSTITUTION)
            # print(STRING_DEBUG_HEAD, "current_state ")
            # print(tracker.current_state())

            print(STRING_SUBSTITUTION)
            print(STRING_DEBUG_HEAD, "events ")
            print(tracker.events)

            # print(STRING_SUBSTITUTION)
            # print(STRING_DEBUG_HEAD, "events_after_latest_restart ")
            # print(tracker.events_after_latest_restart())

            # copy self
            # print(STRING_SUBSTITUTION)
            # print(STRING_DEBUG_HEAD, "copy")
            # print(tracker.copy())

            # dump Tracker from specific state
            # print(STRING_SUBSTITUTION)
            # print(STRING_DEBUG_HEAD, "from_dict ")
            # print(Tracker.from_dict(tracker.current_state()))
        return []
