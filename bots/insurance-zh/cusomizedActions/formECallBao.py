"""
Definition of ECallBao form action.

History:
2020/05/21 Created by Noel
"""

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet, EventType
# from rasa_sdk.events import BotUttered, ActionExecuted
from typing import Any, Text, Dict, Union, List, Optional

import logging
logger = logging.getLogger(__name__)

REPEAT_LIMITATION = 3


class FromQuoteInsurance(FormAction):
    """The action to ECallBao form."""

    def name(self) -> Text:
        """Every action needs a name to identify it."""
        return "action_fill_eCallBao_form"

    # slots required to fill
    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """Definition of a list for required slots that the form has to be filled."""
        return [
            # ID
            "client_id",
            # ID - confirm
            "client_id_confirm",
            # Birthday
            "client_birth",
            # Birthday - confirm
            "client_birth_confirm",
            # departure time
            "client_departure_time",
            # departure time - confirm
            "client_departure_time_confirm",
            # days for insurance
            "client_durance_days",
            # days for insurance - confirm
            "client_durance_days_confirm",
            # travel internal or external
            "client_travel_board",
            # travel internal or external - confirm
            "client_travel_board_confirm",
            # if external, travel to which country
            "client_travel_country",
            # if external, travel to which country
            "client_travel_country_confirm",
            # expected quote for insurance
            "client_insurance_quote",
            # expected quote for insurance
            "client_insurance_quote_confirm",
            # medical insurance. And it is limited to 20% of quote.
            "client_insurance_medical",
            # medical insurance. And it is limited to 20% of quote.
            "client_insurance_medical_confirm",
            # insurance for sudden illness type C.
            #   And it is limited to 20% of quote.
            "client_insurance_sudden_illness_c",
            # insurance for sudden illness type C.
            #   And it is limited to 20% of quote.
            "client_insurance_sudden_illness_c_confirm",
            # (should rename to air ambulance transport)
            #    the AAT dependend on travel board & travel country
            "client_medical_plane",
            # trial calculation of insurance
            "client_trial_calculation_confirm",
            # check the client before check the mecdical insurance.
            "client_insurance_inconvenience",
            # check the client before check the mecdical insurance.
            "client_insurance_inconvenience_confirm",
            # way to notify client: SMTP or SMS
            "client_notification",
            # confirm entire insurance content
            "client_insurance_confirm"]

    # defined slots's source
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """Definition of slot and intent mapping."""
        return {
            "client_id": self.from_entity(
                entity="client_id", intent=["res_id"]
            ),
            "client_id_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_birth": self.from_entity(
                entity="client_birth", intent=["res_date"]
            ),
            "client_birth_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_departure_time": self.from_entity(
                entity="client_departure_time", intent=["res_time"]
            ),
            "client_departure_time_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_durance_days": self.from_entity(
                entity="client_durance_days", intent=["res_days"]
            ),
            "client_durance_days_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_travel_board": [
                self.from_entity(
                    entity="client_travel_board", intent=["res_board"]
                ),
                self.from_intent(intent=["res_country"], value="external")
            ],
            "client_travel_board_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_travel_country": self.from_entity(
                entity="client_travel_country", intent=["res_country"]
            ),
            "client_travel_country_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_insurance_quote": [
                self.from_entity(
                    entity="client_amount", intent=["res_number"]
                ),
                self.from_intent(intent=["what"], value="QA"),
            ],
            "client_insurance_quote_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_insurance_medical": [
                self.from_entity(
                    entity="client_amount", intent=["res_number"]
                ),
                self.from_intent(intent=["what"], value="QA"),
            ],
            "client_insurance_medical_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_insurance_sudden_illness_c": [
                self.from_entity(
                    entity="client_amount", intent=["res_number"]
                ),
                self.from_intent(intent=["what"], value="QA"),
            ],
            "client_insurance_sudden_illness_c_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            # should rename to air ambulance transport
            "client_medical_plane": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
                self.from_intent(intent=["what"], value="QA")
            ],
            "client_trial_calculation_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_insurance_inconvenience": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_insurance_inconvenience_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ],
            "client_notification": self.from_entity(
                entity="client_notification", intent=["res_medium"]
            ),
            "client_insurance_confirm": [
                self.from_intent(intent=["yes"], value=True),
                self.from_intent(intent=["no"], value=False),
            ]
        }

    # overwrite the logic of request_next_slot
    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:
        """
        Request the next slot and utter template if needed, else return None.

        Add the treshold for transfering to customer service after repeating over 3 times.
        """
        if tracker.get_slot("repeat_count") >= REPEAT_LIMITATION:
            dispatcher.utter_message(template="utter_to_service")
            # TODO: transer to twilio
            return self.deactivate()

        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                logger.debug(f"Request next slot '{slot}'")
                dispatcher.utter_message(
                    template=f"utter_ask_{slot}",
                    **tracker.slots
                )
                return [SlotSet("requested_slot", slot)]

        # no more required slots to fill
        return None

    # submit when form is done
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Definition of sumit."""
        # "Define what the form has to do after all required slots are filled"
        dispatcher.utter_message(template="utter_payment_processing ")

        # utter submit template
        dispatcher.utter_template("utter_submit", tracker)

        # remind the limitation of air ambulance transport
        if tracker.get_slot("client_medical_plane") is True:
            dispatcher.utter_message(
                text="再次提醒貴賓："
            )
            dispatcher.utter_message(
                template="utter_explain_medical_plane"
            )
            dispatcher.utter_message(
                template="utter_limitation_medical_plane"
            )
            dispatcher.utter_message(
                template="utter_explain_asia_12_countries"
            )

        dispatcher.utter_message(
            template="utter_payment_processed_successful "
        )
        # return event
        return []

    # validator for slot defined with naming format: validate_[slot name]
    def validate_client_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate client ID."""
        dispatcher.utter_message(template="utter_thanks")
        # TODO: validate ID format
        return {
            "client_id": value,
            "repeat_count": tracker.get_slot("repeat_count") + 1
        }

    def validate_client_id_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm client ID."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            return {"client_id_confirm": value, "repeat_count": 0}
        else:
            return {"client_id_confirm": None}

    def validate_client_birth(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate birth of client."""
        dispatcher.utter_message(template="utter_thanks")
        # TODO: validate date format
        return {
            "client_birth": value,
            "repeat_count": tracker.get_slot("repeat_count") + 1
        }

    def validate_client_birth_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm birth of client."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            dispatcher.utter_message(template="utter_check_insurance_content")
            return {"client_birth_confirm": value, "repeat_count": 0}
        else:
            return {"client_birth_confirm": None}

    def validate_client_departure_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate departure time of client."""
        dispatcher.utter_message(template="utter_thanks")
        # TODO: validate time format
        return {
            "client_departure_time": value,
            "repeat_count": tracker.get_slot("repeat_count") + 1
        }

    def validate_client_departure_time_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm departure time of client."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            return {"client_departure_time_confirm": value, "repeat_count": 0}
        else:
            return {"client_departure_time_confirm": None}

    def validate_client_durance_days(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate durance days of travel."""
        dispatcher.utter_message(template="utter_thanks")
        # TODO: check days
        #     (it could be longer as years, months)
        return {
            "client_durance_days": value,
            "repeat_count": tracker.get_slot("repeat_count") + 1
        }

    def validate_client_durance_days_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm durance days of travel."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            return {"client_durance_days_confirm": value, "repeat_count": 0}
        else:
            return {"client_durance_days_confirm": None}

    # should rename to air ambulance transport
    def validate_client_travel_board(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate board of travel."""
        dispatcher.utter_message(template="utter_thanks")
        # TODO: validate the real location
        # (user could tell the location directly
        #   which means
        #   the answer could include information of board and country
        #     consider that check if the location is not inclued in
        #     [china(HK, MO)中國(香港、澳門), JP日本, KR韓國, VN越南,
        #     SG新加坡, PH菲律賓, ID印尼, MY馬來西亞,
        #     MM緬甸, TH泰國, LA寮國, KH柬埔寨]
        #     the slot.client_medical_plane should be False in this step
        # )
        slot_obj = {
            "client_travel_board": value,
            "repeat_count": tracker.get_slot("repeat_count") + 1
        }
        if value.lower() == "internal" or value == "國內":
            slot_obj["client_travel_country"] = "Taiwan"
            slot_obj["client_travel_country_confirm"] = True
            slot_obj["client_medical_plane"] = False
        else:
            slot_obj["client_travel_country"] = None
            slot_obj["client_travel_country_confirm"] = None
        return slot_obj

    # should rename to air ambulance transport
    def validate_client_travel_board_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm board of travel."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            return {"client_travel_board_confirm": value, "repeat_count": 0}
        else:
            return {"client_travel_board_confirm": None}

    def validate_client_travel_country(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate country of travel."""
        dispatcher.utter_message(template="utter_thanks")
        # TODO: check if country is not inclued in
        #     [china(HK, MO)中國(香港、澳門), JP日本, KR韓國, VN越南,
        #     SG新加坡, PH菲律賓, ID印尼, MY馬來西亞,
        #     MM緬甸, TH泰國, LA寮國, KH柬埔寨]
        #     the slot.client_medical_plane should be False in this step
        return {
            "client_travel_country": value,
            "repeat_count": tracker.get_slot("repeat_count") + 1
        }

    def validate_client_travel_country_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm country of travel."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            return {"client_travel_country_confirm": value, "repeat_count": 0}
        else:
            return {"client_travel_country_confirm": None}

    def validate_client_insurance_quote(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate Insurance quote."""
        if value == "QA":
            dispatcher.utter_message(
                template="utter_explain_insurance_quote"
            )
            dispatcher.utter_message(
                template="utter_limitation_insurance_quote"
            )
            return {
                "client_insurance_quote": None,
                "repeat_count": tracker.get_slot("repeat_count") + 1
            }
        else:
            dispatcher.utter_message(template="utter_thanks")
            # TODO: validate the insurance range dependent on age ???
            return {
                "client_insurance_quote": value,
                "repeat_count": tracker.get_slot("repeat_count") + 1
            }

    def validate_client_insurance_quote_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm Insurance quote."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            return {"client_insurance_quote_confirm": value, "repeat_count": 0}
        else:
            return {"client_insurance_quote_confirm": None}

    def validate_client_insurance_medical(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Check whether Insurance medical required."""
        if value == "QA":
            dispatcher.utter_message(
                template="utter_explain_insurance_medical"
            )
            dispatcher.utter_message(
                template="utter_limitation_insurance_medical"
            )
            return {
                "client_insurance_medical": None,
                "repeat_count": tracker.get_slot("repeat_count") + 1
            }
        else:
            dispatcher.utter_message(template="utter_thanks")
            # TODO:
            # transformed to number and
            # validate the limitation of 20% insurance quote
            return {
                "client_insurance_medical": value,
                "repeat_count": tracker.get_slot("repeat_count") + 1
            }

    def validate_client_insurance_medical_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm whether Insurance medical required."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            return {
                "client_insurance_medical_confirm": value,
                "repeat_count": 0
            }
        else:
            return {"client_insurance_medical_confirm": None}

    def validate_client_insurance_sudden_illness_c(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Check sudden illness type-c."""
        if value == "QA":
            dispatcher.utter_message(
                template="utter_explain_insurance_sudden_illness_c"
            )
            dispatcher.utter_message(
                template="utter_limitation_insurance_sudden_illness_c"
            )
            return {
                "client_insurance_sudden_illness_c": None,
                "repeat_count": tracker.get_slot("repeat_count") + 1
            }
        else:
            dispatcher.utter_message(template="utter_thanks")
            # TODO:
            # transformed to number and
            # validate the limitation of 20% insurance quote
            return {
                "client_insurance_sudden_illness_c": value,
                "repeat_count": tracker.get_slot("repeat_count") + 1
            }

    def validate_client_insurance_sudden_illness_c_confirm(
        self,
        value: bool,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm sudden illness type-c."""
        dispatcher.utter_message(template="utter_thanks")

        if value:
            if type(tracker.get_slot("client_medical_plane")) == bool:
                # while travel board is internal
                #   or external except asia 12 countries,
                # according conversation flow
                #   we will skip the medical plane ask step.
                # So we need to add trail calculation ask here

                # TODO: Should extract to a process function
                #   for customized_ask_trial_calculation(Case 1 - 4)
                # Case 1
                # if (
                #    client is member of Cathay and quote>=1100(per month?)
                # ):
                #     auto-add insurance_inconvenience for free
                # trailCalculation = 123456789
                # dispatcher.utter_message(text="保費試算金額為新臺幣"+str(trailCalculation)+"元")
                # dispatcher.utter_message(text="您為國泰世華卡友，並且保費超過新臺幣1,100元，保單附贈不便險")
                # dispatcher.utter_message(template="utter_explain_insurance_inconvenience")
                # return {
                #     "client_insurance_sudden_illness_c_confirm": value,
                #     "repeat_count": 0,
                #     "client_trial_calculation": trailCalculation,
                #     "client_insurance_inconvenience": True,
                #     "client_insurance_inconvenience_free": True,
                #     "repeat_count": 0
                # }

                # Case 2
                #     elif qualification to buy insurance_inconvenience
                # trailCalculation = 123456789
                # dispatcher.utter_message(text="保費試算金額為新臺幣"+str(trailCalculation)+"元")
                # return {
                #     "client_insurance_sudden_illness_c_confirm": value,
                #     "repeat_count": 0,
                #     "client_trial_calculation": trailCalculation,
                #     "client_insurance_inconvenience": None,
                #     "client_insurance_inconvenience_free": False,
                #     "repeat_count": 0
                # }

                # Case 3
                #     total quote excess => to servicer
                # trailCalculation = 123456789 > ???
                # dispatcher.utter_message(text="保費試算金額為新臺幣"+str(trailCalculation)+"元")
                # dispatcher.utter_message(text="由於貴賓您的保費試算金額超過電話投保額度")
                # return {
                #     "client_insurance_sudden_illness_c_confirm": value,
                #     "repeat_count": 0,
                #     "client_trial_calculation": trailCalculation,
                #     "repeat_count": REPEAT_LIMITATION # Forcely deactive
                # }

                # Case 4
                # no qualification to buy insurance_inconvenience & confirm
                trailCalculation = 123456789
                dispatcher.utter_message(
                    text="保費試算金額為新臺幣" + str(trailCalculation) + "元"
                )
                return {
                    "client_insurance_sudden_illness_c_confirm": value,
                    "client_trial_calculation": trailCalculation,
                    "client_insurance_inconvenience": False,
                    "client_insurance_inconvenience_confirm": True,
                    "client_insurance_inconvenience_free": False,
                    "repeat_count": 0
                }
            else:
                return {
                    "client_insurance_sudden_illness_c_confirm": value,
                    "repeat_count": 0
                }
        else:
            return {"client_insurance_sudden_illness_c_confirm": None}

    def validate_client_medical_plane(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Check whether medical plane required."""
        # TODO: validate
        if value == "QA":
            dispatcher.utter_message(template="utter_explain_medical_plane")
            dispatcher.utter_message(template="utter_limitation_medical_plane")
            dispatcher.utter_message(
                template="utter_explain_asia_12_countries"
            )
            return {
                "client_medical_plane": None,
                "repeat_count": tracker.get_slot("repeat_count") + 1
            }
        else:
            dispatcher.utter_message(template="utter_thanks")
            # TODO: validate
            # TODO: trail caculate insurance for next step

            # TODO: Should extract to a process function for
            #   customized_ask_trial_calculation(Case 1 - 4)
            # Case 1
            #     if client is member of Cathay and quote >=1100(per month?),
            #     auto-add insurance_inconvenience for free
            # tc_insurance = 123456789
            # dispatcher.utter_message(text="保費試算金額為新臺幣"+str(tc_insurance)+"元")
            # dispatcher.utter_message(text="您為國泰世華卡友，並且保費超過新臺幣1,100元，保單附贈不便險")
            # dispatcher.utter_message(template="utter_explain_insurance_inconvenience")
            # return {
            #     "client_medical_plane": value,
            #     "client_trial_calculation": tc_insurance,
            #     "client_insurance_inconvenience": True,
            #     "client_insurance_inconvenience_free": True,
            #     "repeat_count": 0
            # }

            # Case 2
            #     elif qualification to buy insurance_inconvenience
            # tc_insurance = 123456789
            # dispatcher.utter_message(text="保費試算金額為新臺幣"+str(tc_insurance)+"元")
            # return {
            #     "client_medical_plane": value,
            #     "client_trial_calculation": tc_insurance,
            #     "client_insurance_inconvenience": None,
            #     "client_insurance_inconvenience_free": False,
            #     "repeat_count": 0
            # }

            # Case 3
            #     total quote excess => to servicer
            # tc_insurance = 123456789 > ???
            # dispatcher.utter_message(text="保費試算金額為新臺幣"+str(tc_insurance)+"元")
            # dispatcher.utter_message(text="由於貴賓您的保費試算金額超過電話投保額度")
            # return {
            #     "client_medical_plane": value,
            #     "client_trial_calculation": tc_insurance,
            #     "repeat_count": REPEAT_LIMITATION # Forcely deactive
            # }

            # Case 4
            #     no qualification to buy insurance_inconvenience & confirm
            tc_insurance = 123456789
            dispatcher.utter_message(text="保費試算金額為新臺幣" + str(tc_insurance) + "元")
            return {
                "client_medical_plane": value,
                "client_trial_calculation": tc_insurance,
                "client_insurance_inconvenience": False,
                "client_insurance_inconvenience_confirm": True,
                "client_insurance_inconvenience_free": False,
                "repeat_count": 0
            }

    def validate_client_trial_calculation_confirm(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm whether medical plane required."""
        dispatcher.utter_message(template="utter_thanks")
        if value:
            return {
                "client_trial_calculation_confirm": value,
                "repeat_count": 0
            }
        else:
            return {
                "client_trial_calculation_confirm": None,
                "repeat_count": REPEAT_LIMITATION  # Forcely deactive
            }

    def validate_client_insurance_inconvenience(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Check whether insurance inconvenience required."""
        dispatcher.utter_message(template="utter_thanks")
        if value:
            # TODO: new trail calculation insurance include inconvenience
            # tc_insurance = 123456789
            # tc_inconvenience = 987654321
            # dispatcher.utter_message(text="保費試算金額為新臺幣"+str(tc_insurance)+"元，不便險保費則為新臺幣"+str(tc_inconvenience)+"元")
            return {"client_insurance_inconvenience": value, "repeat_count": 0}
        else:
            return {
                "client_insurance_inconvenience": value,
                "client_insurance_inconvenience_confirm": True,
                "repeat_count": 0
            }

    def validate_client_insurance_inconvenience_confirm(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm whether insurance inconvenience required."""
        dispatcher.utter_message(template="utter_thanks")
        if value:
            return {
                "client_insurance_inconvenience_confirm": value,
                "repeat_count": 0
            }
        else:
            return {
                "client_insurance_inconvenience_confirm": None,
                "repeat_count": REPEAT_LIMITATION  # Forcely deactive
            }

    def validate_client_notification(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Sum up content of insurance."""
        dispatcher.utter_message(template="utter_thanks")

        # TODO: append or not, decided via if-else
        msg_list = ["與您確認此次投保時間為x月x日x時至x月x日x時"]
        msg_list.append("被保人是xxx")
        msg_list.append("旅遊地點是xxx")
        msg_list.append("保額為xxx")
        msg_list.append("實支實付為xxx")
        msg_list.append("突發型疾病為xxx")
        if tracker.get_slot("client_medical_plane") is True:
            msg_list.append("附加醫療專機")
        if tracker.get_slot("client_insurance_inconvenience") is True:
            msg_list.append("附加不便險")
        msg_list.append("保單寄發地址是xxx")
        dispatcher.utter_message(text='，'.join(msg_list) + '。')
        return {
            "client_notification": value,
            "repeat_count": 0
        }

    def validate_client_insurance_confirm(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Confirm content of insurance."""
        dispatcher.utter_message(template="utter_thanks")
        if value:
            return {"client_insurance_confirm": value, "repeat_count": 0}
        else:
            return {
                "client_insurance_confirm": None,
                "repeat_count": REPEAT_LIMITATION  # Forcely deactive
            }
