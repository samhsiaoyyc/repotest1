## ask_menu
* ask_menu
	- action_utter_menu_categories
* ask_menu_category
	- action_utter_menu_category

## affirm out of context
* affirm
	- utter_confused

## deny out of context
* deny
	- utter_confused

## inform with empty product
* inform{"product": "Crunchy Taco"}
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* affirm
	- action_add_to_cart
	- utter_confirmed_add
* ask_cart_contents
	- action_cart_contents

## inform with empty slots
* inform{"product": "Crunchy Taco"}
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* affirm
	- action_add_to_cart
	- utter_confirmed_add
* ask_cart_contents
	- action_cart_contents

## inform with empty slots
* inform{"product": "Crunchy Taco"}
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* deny
	- utter_cancelled_add
	- action_cancel_add
* ask_cart_contents
	- action_cart_contents

## add_and_confirm
* add_item{"product": "Crunchy Taco"}
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* inform
	- form{"name": null}
	- utter_get_add_confirmation
* affirm
	- action_add_to_cart
	- utter_confirmed_add
* ask_cart_contents
	- action_cart_contents

## add_and_deny
* add_item{"item": "Crunchy Taco"}
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
	- form{"name": null}
	- utter_get_add_confirmation
* deny
	- utter_cancelled_add
	- action_cancel_add
	- slot{"product": null}
	- slot{"quantity": null}
	- slot{"size": null}
* ask_cart_contents
	- action_cart_contents

## add_and_deny_form
* add_item{"product": "Crunchy Taco"}
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* deny
	- form{"name": null}
	- action_cancel_add
	- slot{"product": null}
	- slot{"quantity": null}
	- slot{"size": null}

## add_and_ask_menu
* add_item{"product": "Crunchy Taco"}
	- order_form
	- form{"name": "order_form"}
* ask_menu
	- action_utter_menu_categories
* ask_menu_category
	- action_utter_menu_category
	- form{"name": null}
* inform
	- form{"name": null}
	- utter_get_add_confirmation
* affirm
	- action_add_to_cart
	- utter_confirmed_add
