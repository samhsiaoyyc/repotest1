"""Actions for the Taco Bell bot."""

from typing import Any, Text, Dict, List, Union
import json
import os

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

from fuzzywuzzy import process

MENU_PATH = os.environ['MENU_PATH']  # Type: Text
if not MENU_PATH:
    raise ValueError('The MENU_PATH environment variable must be defined.')

with open(MENU_PATH) as f:
    MENU = {k.lower(): v for k, v in json.load(f).items()}


class OrderDetailForm(FormAction):
    """Form action for specifying additional item options.

    Details required for each product are specified by the menu data.
    """

    def name(self) -> Text:
        """Return FormAction's unique identifier."""
        return "order_detail_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """Get a list of required slots.

        The return value of this method specifies this FormAction's required
        slots. As these are accessed a dict stored in the menu slot, this
        menu slot must always be filled prior to calling this form action.

        TODO: There should be a graceful failure path to exit this form and
        call the StoreForm action if the menu slot is not filled.
        """
        product_info = MENU.get(tracker.get_slot("product").lower())
        if product_info and product_info.get('sizes'):
            return ['size', 'quantity']
        else:
            return ['quantity']

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """Get a dict mapping form slots to inputs.

        This method's return value is a dictionary specifying the
        mapping between required slots (dict keys) and, corresponding
        (dict values) extracted entities, intent-value pairs, messages,
        or a list of the above, with priority assigned according to
        list order.
        """
        return {
            "size": [
                self.from_entity(entity="size"),
                self.from_text(not_intent=["ask_menu",
                                           "ask_menu_category"])
            ],
            "quantity": [
                self.from_entity(entity="quantity"),
                self.from_text(not_intent=["ask_menu",
                                           "ask_menu_category"])
            ]
        }

    def validation_helper(
        self,
        product: Text,
        value: Text,
        dispatcher: CollectingDispatcher,
        addon_key: Text,
        slot_key: Text,
    ) -> Dict[Text, Any]:
        """Validate that an addon is in the list for a product."""
        product_info = MENU.get(product.lower())
        if product_info and product_info.get(addon_key):
            if value.lower() in [
                    addon.lower()
                    for addon in product_info[addon_key]
            ]:
                return {slot_key: value}
            else:
                message = "{} isn't an option for {}".format(value, product)
        else:
            message = "{} doesn't come with {}".format(product, addon_key)
        dispatcher.utter_message(message)
        return {slot_key: None}

    def validate_addon(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate addon value."""
        product = tracker.get_slot("product")
        return self.validation_helper(
            product,
            value,
            dispatcher,
            'addons',
            'addon'
        )

    def validate_sauce(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate sauce value."""
        product = tracker.get_slot("product")
        return self.validation_helper(
            product,
            value,
            dispatcher,
            'sauces',
            'sauce'
        )

    def validate_size(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate product value."""
        product = tracker.get_slot("product")
        product_info = MENU.get(product.lower())

        if product_info and product_info.get('sizes'):
            if value.lower() in [
                    size.lower()
                    for size in product_info['sizes'].keys()
            ]:
                return {'size': value}
            else:
                size_string = ', '.join(list(product_info.get('sizes').keys()))
                message = ("{} isn't a size option for {}. "
                           "Please select from {}")
                message = message.format(value, product, size_string)
                dispatcher.utter_message(message)
                return {'size': None}
        else:
            message = "{} doesn't come in different sizes".format(product)
            dispatcher.utter_message("message")
            return {"size": None}

    def validate_quantity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate product value."""
        try:
            return {"quantity": str(int(value))}
        except ValueError:
            message = "Sorry, I don't understand the quantity {}".format(value)
            dispatcher.utter_message(message)
            return {"quantity": None}

    def submit(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """Return action to be taken when all required slots are filled.

        In this case, 'utter_get_add_confirmation' is set as a followup action.
        """
        return [FollowupAction('utter_get_add_confirmation')]


class OrderForm(FormAction):
    """Form action for selecting the current product.

    Valid products are specified by the menu data. As the product
    must be selected and validated before the required set of details are
    identified from the menu, this is separate from the ItemDetail form and
    calls that form as a follow-up action.
    """

    def name(self) -> Text:
        """Return FormAction's unique identifier."""
        return "order_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """Return FormAction's required slots."""
        return ["product"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """Get a dict mapping form slots to inputs.

        This method's return value is a dictionary specifying the
        mapping between required slots (dict keys) and, corresponding
        (dict values) extracted entities, intent-value pairs, messages,
        or a list of the above, with priority assigned according to
        list order.

        TODO:
        I notice that the response to an incorrect product set in the
        validate_product method is returned twice. Is it returned once
        for each value mapped to the product key as these are evaluated?
        """
        return {"product": [self.from_entity(entity="product"),
                self.from_text()]}

    def validate_product(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate that product value's key is in the loaded menu."""
        options = [name.lower() for name in MENU.keys()]
        if value.lower() in options:
            return {"product": value}
        else:
            candidate = process.extractOne(value.lower(), options)
            if candidate[1] > 80:
                return {"product": candidate[0]}
            else:
                message = ("Sorry, I don't see {} on the menu."
                           "Please make another selection.")
                message = message.format(value)
                dispatcher.utter_message(message)
                return {"product": None}

    def submit(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """Return the action to be taken when all required slots are filled.

        In this case, the 'order_detail_form' action is invoked as a follow-up
        to collect slots for any remaining details required by the product.
        """
        return [FollowupAction('order_detail_form')]


class ActionAddToCart(Action):
    """Add the current order to the cart, then clear the slot data."""

    def name(self) -> Text:
        """Return this Action's unique identifier."""
        return "action_add_to_cart"

    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """Add the current product to the cart, then clear the slots."""
        cart = tracker.get_slot('cart') or []

        cart.append({
            "product": tracker.get_slot("product"),
            "size": tracker.get_slot("size"),
            "addon": tracker.get_slot("addon"),
            "sauce": tracker.get_slot("sauce"),
            "quantity": tracker.get_slot("quantity")
        })

        return [SlotSet('cart', cart),
                SlotSet('product', None),
                SlotSet('size', None),
                SlotSet('quantity', None),
                SlotSet('addon', None),
                SlotSet('sauce', None)]


class ActionCancelAdd(Action):
    """Cancel adding the current item, clearing the slots."""

    def name(self) -> Text:
        """Return this Action's unique identifier."""
        return "action_cancel_add"

    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """Clear the current product from the slots."""
        return [SlotSet('product', None),
                SlotSet('size', None),
                SlotSet('quantity', None),
                SlotSet('addon', None),
                SlotSet('sauce', None)]


class RemoveItem(Action):
    """Remove all items with a matching name from the cart.

    TODO: It should be possible to remove a both single and all
    products: "remove the crunchy tacos from my cart" vs. "remove one
    of the crunchy tacos from my cart."
    """

    def name(self) -> Text:
        """Return this Action's unique identifier."""
        return "action_remove_product"

    def run(
        self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """Remove all items with a matching name from the cart."""
        cart = tracker.get_slot('cart')
        if not cart:
            dispatcher.utter_message("Your cart is empty")
        else:
            cart = [entry for entry in cart
                    if entry["product"] != tracker.get_slot("product")]

        message = "Ok, I removed the {} from your cart."
        message = message = message.format(tracker.get_slot("product"))
        dispatcher.utter_message(message)
        return [SlotSet('cart', cart),
                SlotSet('product', None),
                SlotSet('size', None),
                SlotSet('quantity', None),
                SlotSet('addon', None),
                SlotSet('sauce', None)]


class ActionCartContents(Action):
    """Build and utter string representation of the current cart."""

    def name(self) -> Text:
        """Return this Action's unique identifier."""
        return "action_cart_contents"

    def cart_entry_to_string(self, cart_entry) -> Text:
        """Convert the dict representing a cart product to a string.

        TODO: This currently only shows the quantity and product name, not
        size.
        """
        return "{} {}".format(cart_entry['quantity'], cart_entry['product'])

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """Convert the cart list to a string and utter it."""
        if not tracker.get_slot('cart'):
            dispatcher.utter_message("Your cart is empty")
        else:
            product_strings = [self.cart_entry_to_string(entry)
                               for entry in tracker.get_slot('cart')]
            if len(product_strings) > 1:
                product_strings.insert(len(product_strings) - 1, ', and')
            dispatcher.utter_message(' '.join(product_strings))

        return []

# class ActionUtterOptions(Action):
#    """
#    This action lists available options for the current slot.
#    """
#
#    def name(self) -> Text:
#        """
#        The return value of this method specifies this Action's unique
#        identifier.
#        """
#        return "action_utter_menu_options"
#
#
#    def run(self,dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#        """
#        When invoked, this lists available options for the current requested
#        slot.
#        """
#
#        # If we're not in a form with a requested slot, and/or
#        # the product slot isn't set, assume that the user is
#        # asking about menu options.
#        product = tracker.get_slot("product")
#        if not tracker.get_slot('requested_slot') or not product:
#            return [FollowupAction('action_utter_menu_categories')]
#        else:
#            product_info = MENU.get(product.lower())
#            if tracker.get_slot('requested_slot') == "size":
#                options = MENU[menu_category].keys()
#                message = "The options are: {}"
#                message = message.format(', '.join(options))
#                dispatcher.utter_message(message)
#            elif tracker.get_slot('requested_slot') == "quantity":
#                pass # TODO
#        return []


class ActionUtterMenuCategories(Action):
    """List available menu categories."""

    def name(self) -> Text:
        """Return this Action's unique identifier."""
        return "action_utter_menu_categories"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """List available menu categories."""
        categories = MENU['menu_categories'].keys()
        message = ("Which menu category would you like to hear?"
                   "The options are: {}")
        message = message.format(', '.join(categories))
        dispatcher.utter_message(message)

        return []


class ActionUtterMenuCategory(Action):
    """List the items in a menu category."""

    def name(self) -> Text:
        """Return this Action's unique identifier."""
        return "action_utter_menu_category"

    def format_menu_string(self, menu):
        """Convert the menu to a string."""
        return ', \n'.join([item for item in menu])

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        """List items in the specified menu category."""
        menu_category = tracker.get_slot('menu_category')
        candidate = process.extractOne(
            menu_category,
            list(MENU['menu_categories'].keys())
        )
        if candidate[1] > 80:
            menu_category = MENU['menu_categories'][candidate[0]]
            message = self.format_menu_string(menu_category)
            dispatcher.utter_message(message)
            return []
        else:
            dispatcher.utter_message("I don't recognize that menu category")
            return [FollowupAction("action_utter_menu_categories")]

        return []
