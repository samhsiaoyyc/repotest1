# -*- coding: utf-8 -*-

"""

As Rasa actions to implement the flow/story of cathay super bot.

Description:
Rasa actions are the things that your bot run in response to user input.
About the actions type, Rasa provide different kind of action you can use.
https://rasa.com/docs/rasa/core/actions/
"""

from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet
from rasa_sdk.forms import FormAction
from datetime import datetime, timezone
import requests
import re
from ngchat_plugins.common.mock_server import (API_HOST, API_RASA_UNBILL, API_RASA_LOGIN, API_RASA_BILL,
                                               API_RASA_MEMBER, API_RASA_BILL_CARD, API_RASA_BILL_SET, API_RASA_TIME_BUSS)


host = API_HOST
unbill_details = []


class ActionUnbillDetail(Action):
    """Confirm is un-bill detail exist. (查詢確認是否有尚未出帳的消費明細)"""

    def name(self) -> Text:
        """Define action name."""
        return "action_unbill_detail_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """

        Execute this action when action triggered by utterance defined in story.

        Run this action to call query un-bill detail api, to get un-bill detail
        data for make sure un-bill is exist.
        """
        # call unbill detail api, it will respond as following
        # {
        #     result: {
        #         items: [{
        #             date: 20200422,
        #             item: 'apple iphone',
        #             amount: 100,
        #             currency_type: 'twd'
        #         }]
        #     }
        # }
        token_header = {"Authorization": tracker.get_slot("user_token")}
        unbill_respond = requests.get(
            host + API_RASA_UNBILL, headers=token_header)
        unbill_details = unbill_respond.json()["result"]["items"]

        if unbill_details:
            unbill_details_twd = [
                unbill for unbill in unbill_details if unbill["currency_type"] == "twd"]
            unbill_details_frd = [
                unbill for unbill in unbill_details if unbill["currency_type"] == "frd"]

            if unbill_details_twd and unbill_details_frd:
                currency_type = "twd/frd"
            elif unbill_details_twd:
                currency_type = "twd"
            else:
                currency_type = "frd"

            return [
                FollowupAction("action_bill_detail_api"),
                SlotSet("currency_type", currency_type),
                SlotSet("unbill_details", unbill_details)
            ]

        else:
            # 轉專人
            dispatcher.utter_message(
                template="utter_exception", message="目前查無尚未出帳的消費明細")
            return []


class ActionBillDetail(Action):
    """Query bill detail. (查詢帳單明細)"""

    def name(self) -> Text:
        """Define action name."""
        return "action_bill_detail_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """

        Execute this action when action triggered by utterance defined in story.

        Run this action to get bill detail data according to currency type.

        """
        # call bill detail api to get
        # if currency_type is frd or twd, [items] as attribute name will respond as following
        # {
        #     result: {
        #         bill_id: "BID001",
        #         date: 20200413,
        #         checkout_date: 20200415,
        #         currency_type: "frd",
        #         items: [
        #             {
        #                 item: "amazon",
        #                 amount: 200
        #             }
        #         ]
        #     }
        # }
        #
        # if currency_type is twd/frd, [items] as attribute name will respond as following
        # {
        #     result: {
        #         bill_id: "BID001",
        #         date: 20200413,
        #         checkout_date: 20200415,
        #         currency_type: "frd",
        #         items: {
        #             frd: [{
        #                     item: "amazon",
        #                     amount: 200
        #             }],
        #             twd: [{
        #                 item: "apple music",
        #                 amount: 150
        #             }]
        #         }
        #     }
        # }
        curr_type = tracker.get_slot("currency_type")

        if tracker.get_slot("unbill_details"):
            unbill_details = tracker.get_slot("unbill_details")
            respond_data = unbill_details
            if curr_type == "twd/frd":
                respond_data_twd = [
                    unbill for unbill in unbill_details if unbill["currency_type"] == "twd"]
                respond_data_frd = [
                    unbill for unbill in unbill_details if unbill["currency_type"] == "frd"]

        if tracker.get_slot("recent_bill_id"):
            bill_id = tracker.get_slot("recent_bill_id")
            bill_params = {"currency_type": curr_type, "bill_id": bill_id}
            bill_respond = requests.get(
                host + API_RASA_BILL, params=bill_params)
            respond_data = bill_respond.json()["result"]
            if curr_type == "twd/frd":
                respond_data_twd = respond_data["items"]["twd"]
                respond_data_frd = respond_data["items"]["frd"]

        if curr_type == "twd/frd":
            dispatcher.utter_message(
                text="台幣明細", json_message=respond_data_twd)
            dispatcher.utter_message(
                text="外幣明細", json_message=respond_data_frd)
            return [FollowupAction("utter_detail")]
        if curr_type == "twd":
            action = "utter_recent_bill_detail"
        else:
            action = "utter_unbill_detail"

        dispatcher.utter_message(json_message=respond_data)
        return [FollowupAction(action)]


class ActionTWDDetailAction(Action):
    """ Query TWD bill detaill. (台幣消費明細)"""

    def name(self) -> Text:
        """Define action name."""
        return "action_twd_detail_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """

        Execute this action when action triggered by utterance defined in story.

        Run this action to get bill detail of twd as Taiwan Dollar.

        """
        if tracker.get_slot("unbill_details"):
            unbill_details_twd = [
                unbill for unbill in tracker.get_slot("unbill_details") if unbill["currency_type"] == "twd"]
            dispatcher.utter_message(
                json_message=unbill_details_twd)
        if tracker.get_slot("recent_bill_id"):
            # call bill detail api to get bill detail that currency type is frd
            # respond data format can follow ActionBillDetail Class above
            bill_respond = requests.get(
                host + API_RASA_BILL,
                params={
                    "currency_type": "twd",
                    "bill_id": tracker.get_slot("recent_bill_id")
                }
            )
            dispatcher.utter_message(
                json_message=bill_respond.json()["result"])

        return [FollowupAction("utter_recent_bill_detail")]


class ActionFRDDetailAction(Action):
    """Query FRD bill detaill. (外幣消費明細)"""

    def name(self) -> Text:
        """Define action name."""
        return "action_frd_detail_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """

        Execute this action when action triggered by utterance defined in story.

        Run this action to get bill detail of twd as Foreign Dollar.

        """
        if tracker.get_slot("unbill_details"):
            unbill_details_frd = [
                unbill for unbill in tracker.get_slot("unbill_details") if unbill["currency_type"] == "frd"]
            dispatcher.utter_message(
                json_message=unbill_details_frd)
        if tracker.get_slot("recent_bill_id"):
            # call bill detail api to get bill detail that currency type is frd
            # respond data format can follow ActionBillDetail Class above
            bill_respond = requests.get(
                host + API_RASA_BILL,
                params={
                    "currency_type": "frd",
                    "bill_id": tracker.get_slot("recent_bill_id")
                }
            )
            dispatcher.utter_message(
                json_message=bill_respond.json()["result"])

        return [FollowupAction("utter_unbill_detail")]


class ActionRecentDetail(Action):
    """Query curenctly credit-card bill detail. (查詢最近一期的信用卡帳單)"""

    def name(self) -> Text:
        """Define action name."""
        return "action_recent_detail_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """

        Execute this action when action triggered by utterance defined in story.

        Run this action to get currently credit-card bill detail.

        """
        # call recent credit card api to get bill, it will respond as following
        # {
        #     result: {
        #         bill_id: "BID001",
        #         card_type: 'gogo卡',
        #         date: 20200413,
        #         checkout_date: 20200415,
        #         deadline_date: 20200420,
        #         bill_type: "electronic",
        #         currency_type: "frd",
        #         items: [{
        #             item: "gold",
        #             amount: 100
        #         }]
        #     }
        # }
        token_header = {"Authorization": tracker.get_slot("user_token")}
        card_bill_respond = requests.get(
            host + API_RASA_BILL_CARD,
            params={
                "from": "lastest"
            },
            headers=token_header
        )
        if card_bill_respond.ok:
            card_bill = card_bill_respond.json()["result"]

            if card_bill["items"]:
                currency_type = card_bill["currency_type"]
                bill_id = card_bill["bill_id"]
                return [
                    FollowupAction("action_bill_detail_api"),
                    SlotSet("currency_type", currency_type),
                    SlotSet("recent_bill_id", bill_id),
                    SlotSet("unbill_details", None)
                ]
            else:
                return [FollowupAction("utter_unfound_detail")]
        else:
            return [FollowupAction("utter_unfound_detail")]


class ActionReSendBill(Action):
    """Resend e-bill detial. (補寄電子帳單)"""

    def name(self) -> Text:
        """Define action name."""
        return "action_resend_ebill_api"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """

        Execute this action when action triggered by utterance defined in story.

        Run this action to resend e-bill detial to user.

        """
        # call member api to get member info, it will respond as following
        # {
        #     result: {
        #         user_name: 'test',
        #         user_mail: '123@mail.com'
        #         user_address: 'Taiwan, Taipei'
        #     }
        # }
        member_respond = requests.get(
            host + API_RASA_MEMBER,
            headers={
                "Authorization": tracker.get_slot("user_token")
            }
        )
        member = member_respond.json()["result"]
        member_mail = member["user_mail"]
        member_address = member["user_address"]

        # call recent credit card api to get bill
        # respond data format can follow ActionBillDetail Class above
        token_header = {"Authorization": tracker.get_slot("user_token")}
        card_bill_respond = requests.get(
            host + API_RASA_BILL_CARD, params={"from": "lastest"}, headers=token_header)
        card_bill = card_bill_respond.json()["result"]

        # call business time api to get time info, it will respond as following
        # {
        #     result: {
        #         bussiness_date: 158051520
        #     }
        # }
        buss_time_respond = requests.get(
            host + API_RASA_TIME_BUSS, headers=token_header)
        buss_time = buss_time_respond.json()["result"]

        bill_flag = False
        time_flag = False
        # check credit card date
        if card_bill["date"]:
            bill_flag = True

        # business time pass 3 days
        if datetime.now(timezone.utc).timestamp() >= buss_time["bussiness_date"]:
            time_flag = True

        if bill_flag:
            raw_date = card_bill["date"]
            date = "%s 年 %s 月" % (str(raw_date)[0:4], str(raw_date)[4:6])
            day = raw_date % 100

            if time_flag:
                if card_bill["bill_type"] == "paper":
                    dispatcher.utter_message(
                        template="utter_paper_bill_checkout",
                        date=date,
                        day=day,
                        address=member_address
                    )
                else:
                    dispatcher.utter_message(
                        template="utter_ebill_checkout",
                        date=date,
                        day=day,
                        email=member_mail
                    )

                return [
                    SlotSet("email", member_mail),
                    SlotSet("date", date),
                    SlotSet("day", day)
                ]
            else:
                if card_bill["bill_type"] == "paper":
                    dispatcher.utter_message(
                        template="utter_paper_bill_uncheckout",
                        date=date,
                        day=day,
                        address=member_address
                    )
                else:
                    dispatcher.utter_message(
                        template="utter_ebill_uncheckout",
                        date=date,
                        day=day,
                        email=member_mail
                    )

                return [
                    SlotSet("email", member_mail),
                    FollowupAction("utter_help_for_unbill_uncheckout")
                ]
        else:
            dispatcher.utter_message(template="utter_fallback")

            return [
                SlotSet("email", member_mail),
                FollowupAction("utter_help")
            ]


class LoginFormAction(FormAction):
    """Implement Login machanism through by form action."""

    def name(self) -> Text:
        """Define identifier of the form"""
        return "login_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """List of required slots that the form has to fill"""
        return ["user_id", "user_password"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """
        Define how to extract slot values from user responses.

        A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked

        """
        return {
            "user_id": self.from_text(),
            "user_password": self.from_text()
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do after all required slots are filled"""
        # call login api, it will respond as following
        # {
        #     token: "test_user"
        # }
        login_respond = requests.post(
            host + API_RASA_LOGIN, json={"user_id": tracker.get_slot("user_id")})
        token = login_respond.json()["token"]

        dispatcher.utter_message(template="utter_submit")
        return [SlotSet("user_token", token)]

    def validate_user_id(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate the value of the slot."""
        if value:
            return {"user_id": value}
        else:
            return {"user_id": None}

    def validate_user_password(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate the value of the slot."""
        if value:
            return {"user_password": value}
        else:
            return {"user_password": None}


class EmailFormAction(FormAction):
    """Implement Reset Email through by form action."""

    def name(self) -> Text:
        """Define identifier of the form"""
        return "reset_email_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """List of required slots that the form has to fill"""
        return ["new_email", "new_email_confirm"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """
        Define how to extract slot values from user responses.

        A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked

        """
        return {
            "new_email": self.from_text(),
            "new_email_confirm": [
                self.from_intent(intent=["affirm"], value=True),
                self.from_intent(intent=["chage_mail"], value=False)
            ]
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do after all required slots are filled"""
        dispatcher.utter_message(template="utter_submit")

        return [
            FollowupAction("resend_email_form"),
            SlotSet("resend_confirm", None)
        ]

    def validate_new_email(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate the value of the slot."""
        format = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

        if re.match(format, value):
            return {"new_email": value}
        else:
            dispatcher.utter_message(template="utter_reset_email")
            return {"new_email": None}

    def validate_new_email_confirm(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate the value of the slot."""
        if value is True:
            return {"new_email_confirm": value}
        else:
            return {"new_email_confirm": None, "new_email": None}


class ResendFormAction(FormAction):
    """Implement Resend Confirmation through by form action."""

    def name(self) -> Text:
        """Define identifier of the form"""
        return "resend_email_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """List of required slots that the form has to fill"""
        return ["resend_confirm"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """
        Define how to extract slot values from user responses.

        A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked

        """
        return {
            "resend_confirm": [
                self.from_intent(intent=["affirm"], value=True),
                self.from_intent(intent=["chage_mail"], value=False)
            ]
        }

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Define what the form has to do after all required slots are filled."""
        dispatcher.utter_message(template="utter_submit")

        if tracker.get_slot("new_email"):
            email = tracker.get_slot("new_email")
        else:
            email = tracker.get_slot("email")

        if tracker.get_slot("resend_confirm"):

            #  call bill set api, it will respond as following
            # { message: 'success' }
            status_code = requests.post(
                host + API_RASA_BILL_SET, json={"email": email}).status_code

            if re.match("2.", str(status_code)):
                dispatcher.utter_message(
                    template="utter_resend_email_done", email=email, date=str(tracker.get_slot("date")))
            else:
                dispatcher.utter_message(template="utter_attention")

            dispatcher.utter_message(template="utter_help_resend")
            return []
        else:
            return [
                SlotSet("new_email", None),
                SlotSet("new_email_confirm", None),
                FollowupAction("reset_email_form")
            ]

    def validate_resend_confirm(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate the value of the slot."""
        if value is True:
            return {"resend_confirm": value}
        else:
            return {"resend_confirm": False}


class SwitchEBillAction(Action):
    """Implement Switch E-Bill through by form action."""

    def name(self) -> Text:
        """Define action name."""
        return "action_switch_ebill"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """Execute this action when action triggered by utterance defined in story."""
        if tracker.get_slot("email"):
            return [FollowupAction("resend_email_form")]
        else:
            return [FollowupAction("reset_email_form")]
