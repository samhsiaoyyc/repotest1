## affirm out of context
* affirm: yeah
	- utter_confused

## deny out of context
* deny: no
	- utter_confused

## inform with empty product
* inform{"product": "Crunchy Taco"}: I'd like [a](quantity) [Crunchy Taco](product) please
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* affirm: yes
	- action_add_to_cart
	- utter_confirmed_add
* ask_cart_contents: What's in my cart?
	- action_cart_contents

## inform with empty slots
* inform{"product": "Crunchy Taco"}: I'll have [a](quantity) [crunchy taco](product)
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* affirm: yeah
	- action_add_to_cart
	- utter_confirmed_add
* ask_cart_contents: Ok, now what's in my cart?
	- action_cart_contents

## inform with empty slots
* inform{"product": "Crunchy Taco"}: [Crunchy Taco](product)
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* deny: no
	- utter_cancelled_add
	- action_cancel_add
* ask_cart_contents: What's on my order so far?
	- action_cart_contents

## add_and_confirm
* add_item{"product": "diet pepsi", "quantity": "1"}: I'd like [a](quantity) [Diet Pepsi](product) please
	- slot{"product": "diet pepsi", "quantity": "1"}
	- order_form
	- form{"name": "order_form"}
* inform{"size": "large"}: [large](size)
	- slot{"size": "large"}
	- form{"name": null}
	- utter_get_add_confirmation
* affirm: yes
	- action_add_to_cart
	- utter_confirmed_add
* ask_cart_contents: What's in my cart?
	- action_cart_contents

## add_and_deny
* add_item{"product": "Crunchy Taco"}: I'll have [a](quantity) [crunchy taco](product)
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
	- form{"name": null}
	- utter_get_add_confirmation
* deny: no
	- utter_cancelled_add
	- action_cancel_add
	- slot{"product": null}
	- slot{"quantity": null}
	- slot{"size": null}
* ask_cart_contents: Ok, what do I have so far?
	- action_cart_contents

## add_and_deny_form
* add_item{"product": "Crunchy Taco"}: I'll have [a](quantity) [crunchy taco](product)
	- order_form
	- slot{"product": "crunchy taco"}
	- form{"name": "order_form"}
* deny: no
	- form{"name": null}
	- action_cancel_add
	- slot{"product": null}
	- slot{"quantity": null}
	- slot{"size": null}

## ask_menu
* ask_menu: What's on the menu?
	- action_utter_menu_categories
* ask_menu_category{"menu_category": "drinks"}: [Drinks][menu_category]
	- slot{"menu_category": "drinks"}
	- action_utter_menu_category
