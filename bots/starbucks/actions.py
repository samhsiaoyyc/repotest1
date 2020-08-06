"""
Rasa actions file for Volligator Starbucks bot.

Contains custom forms and actions for Starbucks bot
and connects custom actions to external cart implementation.

"""

from typing import Text, List, Dict, Any
from word2number import w2n

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
# from rasa_sdk.events import SessionStarted, ActionExecuted, EventType
from rasa_sdk.executor import CollectingDispatcher
from logging import getLogger

from ngchat_cart import cart

MENU_PATH = "./data/menus/"
logger = getLogger(__name__)


""" CART FUNCTIONALITY """


class ConfirmAdd(Action):
    """Confirm the user wants to add an item to the cart."""

    def name(self) -> Text:
        """Set action name to action_confirm_add.

        Return:
            Text: name of the action

        """
        return "action_confirm_add"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Utter confirm add and display image + buttons.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: list of slotsets and followup actions

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        if not tracker.get_slot('item'):
            dispatcher.utter_message(template="utter_no_item_selected")
            return []
        dispatcher.utter_message(image=user_cart.active_item.item_type.image)
        dispatcher.utter_message(template="utter_confirm_add")

        return []


class AddToCart(Action):
    """Class to add item to cart."""

    def name(self) -> Text:
        """Set action name to action_add_to_cart."""
        return "action_add_to_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Add item to cart.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: list of slotsets and followup actions

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        user_cart.add_item_instance(user_cart.active_item)
        return [FollowupAction("action_clear_slots"), SlotSet("num_cart_items", len(user_cart.cart_items)),
                SlotSet("cart_total", user_cart.sum_cost())]


class PrepareAddToCart(Action):
    """Class to add item to cart."""

    def name(self) -> Text:
        """Set action name to action_prepare_add_to_cart.

        Return:
            Text: name of action

        """
        return "action_prepare_add_to_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Get info from slots and create active item item_instance.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: list of slotsets and followup actions

        """
        # slots should all be validated at this point from validation step
        user_cart = cart.get_user_cart(tracker.sender_id)

        item = tracker.get_slot('item')
        size = tracker.get_slot('size')
        options = tracker.get_slot('options')
        user_cart.active_item = cart.ItemInstance.from_item_name(item, user_cart.menu)
        if tracker.get_slot('quantity'):
            user_cart.active_item.quantity = w2n.word_to_num(tracker.get_slot('quantity'))
        for opt in options:
            user_cart.active_item.options[opt] = user_cart.active_item.item_type.option_fields[opt]
            user_cart.active_item.options[opt].selected = True
        user_cart.active_item.options[size] = user_cart.active_item.item_type.option_fields[size]
        user_cart.active_item.options[size].selected = True

        return [SlotSet("item_to_add", user_cart.active_item.to_text()),
                SlotSet("image", user_cart.menu.menu_items[item].image)]


class ValidateItem(Action):
    """Validate item with menu."""

    def name(self) -> Text:
        """Create identifier for action."""
        return 'action_validate_item'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Check that the requested item is in the menu.

        Args:
            value (Text): value of the slot that you are validating
            user_cart (cart.Cart): The cart object for the specific user

        Return:
            Optional[Text]: A matching value from the menu or None

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        match = user_cart.menu.get_matching_menu_item(tracker.get_slot('item'))
        if match:
            return [SlotSet('item', match)]
        else:
            dispatcher.utter_message(template="utter_item_not_found")
            return [SlotSet('item', None), FollowupAction('action_listen')]


class ValidateSize(Action):
    """Validate size with menu item."""

    def name(self) -> Text:
        """Create identifier for action."""
        return 'action_validate_size'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Check that 'size' is a valid value (small, medium, or large).

        Args:
            dispatcher: Rasa collecting dispatcher
            tracker: Rasa tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: Set slots item and size

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        item_size_result = user_cart.validate_size(tracker.get_slot('item'), tracker.get_slot('size'))
        if not item_size_result[0]:
            dispatcher.utter_message(template='utter_invalid_item')
            return [SlotSet('item', None), SlotSet('size', None), FollowupAction('action_listen')]
        elif not item_size_result[1]:
            dispatcher.utter_message(template='utter_invalid_size')
            item_match = user_cart.menu.menu_items[user_cart.menu.get_matching_menu_item(tracker.get_slot('item'))]
            dispatcher.utter_message(item_match.describe_options('size'))
            return [SlotSet('item', item_size_result[0]), SlotSet('size', None), FollowupAction('action_listen')]
        return [SlotSet('item', item_size_result[0]), SlotSet('size', item_size_result[1])]


class ValidateOptions(Action):
    """Validate options with menu item."""

    def name(self) -> Text:
        """Create identifier for action."""
        return 'action_validate_options'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Check that all 'options' are valid for the requested menu item.

        Args:
            dispatcher: Rasa collecting dispatcher
            tracker: Rasa tracker
            domain: Rasa domain

        Return:
            List[Text]: A list of matching values from the menu or an empty list

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        options = tracker.get_slot('options')
        if options == []:
            return [SlotSet('options', options)]
        else:  # stop-gap solution for error when adding a single add-on ['c','r','e','a','m']
            if len(options[0]) == 1:
                options = ["".join(options)]
            valid, invalid = user_cart.validate_options(tracker.get_slot('item'), tracker.get_slot('options'))
            if invalid:
                dispatcher.utter_message(f"I couldn't find a matching option for {cart.list_to_string(invalid, join='or')}")
                return [SlotSet('options', valid), FollowupAction('action_listen')]
            return [SlotSet('options', valid)]


class ReadCart(Action):
    """Class to read out cart contents to user."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_read_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Read out cart contents.

        Check if current_cart is None, if so utter cart is empty
        Otherwise, read out current_cart.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: list of slotsets and followup actions

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        if user_cart.cart_items:
            readable_cart = ""
            dispatcher.utter_message(template="utter_cart_contents")
            for item in user_cart.cart_items:
                readable_cart += f'{item.quantity}x {item.item_type.name}:\t\t${item.cost()}\n'
            readable_cart += f"TOTAL\t\t${user_cart.sum_cost()}"
            dispatcher.utter_message(readable_cart)
        else:
            dispatcher.utter_message(template="utter_cart_is_empty")

        return []


class RemoveFromCart(Action):
    """Remove the item specified in target_cart_item slot."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_remove_from_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Get the index from target_cart_item, remove the item at that index.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: updated cart

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        to_remove = user_cart.get_matching_cart_item(tracker.get_slot("target_cart_item"))
        if to_remove:
            removed = user_cart.remove_item(to_remove)
            if removed:
                dispatcher.utter_message(template="utter_removed")
        else:
            dispatcher.utter_message(template="utter_cart_item_not_found")

        return [FollowupAction("action_clear_slots"), SlotSet("num_cart_items", len(user_cart.cart_items)),
                SlotSet("cart_total", user_cart.sum_cost())]


class GetCartItem(Action):
    """Find one matching item in the cart."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_get_cart_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Find a matching item in the cart and set target_cart_item."""
        user_cart = cart.get_user_cart(tracker.sender_id)
        match = user_cart.get_matching_cart_item(tracker.get_slot('item'))
        if match:
            return [SlotSet('target_cart_item', match)]
        else:
            return [SlotSet('target_cart_item', None)]


class ClearCart(Action):
    """Clear the entire cart, removing all items."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_clear_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Remove all items from the cart.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: updated cart

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        user_cart.clear()
        dispatcher.utter_message(template="utter_cart_cleared")

        return [SlotSet("num_cart_items", len(user_cart.cart_items)), SlotSet("cart_total", user_cart.sum_cost())]


class CheckoutCart(Action):
    """Checkout the entire cart.

    PLACEHOLDER until purchasing is possible

    """

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_checkout_cart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Purchase all items in the cart.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: updated cart

        """
        receipt = ''
        user_cart = cart.get_user_cart(tracker.sender_id)
        if user_cart.cart_items:
            # TODO: implement actual checkout functionality
            user_cart.checkout()
            for item in user_cart.cart_items:
                receipt += f'{item.quantity}x {item.item_type.name}:\t\t${item.cost()}\n'
            receipt += f"TOTAL\t\t${user_cart.sum_cost()}"
            user_cart.clear()
            dispatcher.utter_message(template='utter_checkout_complete')
        else:
            dispatcher.utter_message(template='utter_empty_cart_no_checkout')

        return[SlotSet("readable_cart", user_cart.list_contents()), SlotSet("receipt", receipt)]


class RequestRating(Action):
    """Ask for user rating of bot."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_request_rating"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Request rating of 1-5 from user.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        """
        dispatcher.utter_message(template='utter_request_rating')
        return[]


""" SLOT MANIPULATION """


class ClearSlots(Action):
    """Class to clear the temp slots, size, item, and options between items."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_clear_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Reset size, item, and options to None.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: slotset for each item -> None

        """
        return [SlotSet('size', None), SlotSet('item', None), SlotSet('quantity', None),
                SlotSet('options', None), SlotSet('target_cart_item', None), SlotSet('receipt', None)]


class SetOptionsNone(Action):
    """Class to set options to [] if user doesn't want any."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: Action name

        """
        return "action_set_options_none"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Set option slot to empty list."""
        return [SlotSet('options', [])]


""" MENU FUNCTIONALITY """


class SetMenu(Action):
    """Load menu for 'store' and put it in the 'menu' slot."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_set_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, Domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Create cart object and load selected menu into cart object.

        Check if there is a menu corresponding to the store slot
        if not, utter error message. If menu exists, load and store in cart.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: SlotSet('cart')

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        curr_store = tracker.get_slot('store')
        if curr_store is None:
            dispatcher.utter_message(template="utter_no_store_selected")
            return [FollowupAction('action_listen')]
        elif user_cart.menu is not None and curr_store == user_cart.menu.name:
            return []
        else:
            # TODO: move menus to a more permanent shared folder
            menu_match = user_cart.get_matching_menu(curr_store, MENU_PATH)
            if menu_match is not None:
                user_cart.menu = cart.Menu.load_menu(menu_match, MENU_PATH)
            if menu_match is None or user_cart.menu is None:
                dispatcher.utter_message(template="utter_menu_not_found")
                return[SlotSet('store', None), FollowupAction('action_listen')]
        return[]


class DescribeMenu(Action):
    """Display a general description of a menu, including its categories."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_describe_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, Domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Display each menu item name and price.

        Extract the menu from the menu slot (display error if no
        menu is selected). Display name and price.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: none

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        if not user_cart.menu:
            dispatcher.utter_message(template='utter_no_store_selected')
        else:
            dispatcher.utter_message(user_cart.menu.describe_menu())

        return []


class DescribeCategory(Action):
    """Display a general description of a menu, including its categories."""

    def name(self) -> Text:
        """Create identifier for action.

        Return:
            Text: action name

        """
        return "action_describe_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, Domain: Dict[Text, Any]
            ) -> List[Dict[Text, Any]]:
        """Display each menu item name and price.

        Extract the menu from the menu slot (display error if no
        menu is selected). Display name and price.

        Args:
            dispatcher: Rasa CollectingDispatcher
            tracker: Rasa Tracker
            domain: Rasa domain

        Return:
            List[Dict[Text, Any]]: none

        """
        user_cart = cart.get_user_cart(tracker.sender_id)
        if not user_cart.menu:
            dispatcher.utter_message(template='utter_no_store_selected')
            return []
        if not tracker.get_slot('category'):
            dispatcher.utter_message(template='utter_no_category_selected')
            return []

        cat_match = user_cart.menu.get_matching_menu_category(tracker.get_slot('category'))
        if cat_match:
            description = user_cart.menu.describe_category(cat_match).split('\n')
            while len(description) > 30:
                chunk = '\n'.join(description[:30])
                description = description[30:]
                dispatcher.utter_message(chunk)
            dispatcher.utter_message('\n'.join(description))
        else:
            dispatcher.utter_message(template='utter_category_not_found')

        return []
