## hello + ask volli
* greet: Hello!
    - utter_greet
* faq: what does this app do?
    - respond_faq
    
## ask how to + ask find shop
* faq: how does this app work?
    - respond_faq
* faq: how do I find a store I want to order from?
    - respond_faq
    
## ask find item + ask select item
* faq: how can I look for an item?
    - respond_faq
* faq: how do I select an item?
    - respond_faq
    
## ask add cart
* faq: how do I add something to my cart?
    - respond_faq
    
## ask remove cart
* faq: how can I take something out of my cart?
    - respond_faq
    
## ask purchase + ask multiple orders
* faq: how do I check out?
    - respond_faq
* faq: can I place more than one order at once?
    - respond_faq
    
## hello + select store + describe
* greet: Hello
    - utter_greet
* select_store: Open the menu for Starbucks.
    - slot{"store": "starbucks"}
    - store_form
    - action_set_menu
* describe_menu: What's on the menu?
    - action_describe_menu
* describe_category: What's in the [Hot Drinks](category) category?
    - action_describe_category
    
## hello + select store + add item
* greet: Hi there
    - utter_greet
* select_store: show me the [starbucks](store) menu
    - slot{"store": "starbucks"}
    - store_form
    - form{"name": "store_form"}
    - action_set_menu
* select_item{"size": "small", "item": "Caffe Americano"}: I'll have a [small](size) [caffe americano](item)
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "add_on"}
* deny: no thank you
    - form{"name":null}
    - slot{"item_to_add": "small Caffe Americano"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* affirm: yup
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* ask_cart_contents: What's in my cart now?
    - action_read_cart
    
## select store + how to add + add item + add item
* select_store: open [starbucks](store)
    - slot{"store": "starbucks"}
    - store_form
    - action_set_menu
* faq: how do I add something to my cart?
    - respond_faq
* select_item{"size": "venti", "item": "flat white"}: give me a [large](size) [flat white](item)
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "add_on"}
* inform{"add_on": "nutmeg"}: add some [nutmeg](add_on)
    - form{"name": null}
    - slot{"item_to_add": "venti flat white with nutmeg"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add 
* affirm: sure
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
* select_item{"quantity": "2", item": "caffe latte"}: I'd also like [2](quantity) [caffe lattes](item)
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* inform{"size": "grande"}: Make it a [grande](size)
    - slot{"requested_slot": "add_on"}
* deny
    - form{"name": null}
    - slot{"item_to_add": "2 grande caffe lattes"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* affirm: yes please
    - action_add_to_cart
    - slot{"num_cart_items": 3}
    - slot{"cart_total": 8.00}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status

## select store + add item + cancel add item
* select_store: open [starbucks](store)
    - slot{"store": "starbucks"}
    - store_form
    - action_set_menu
* select_item{"size": "large", "item": "mocha"}: How about a [large](size) [mocha](item)
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "add_on"}
* inform{"add_on": "whipped cream"}: sure, [whipped cream](add_on)
    - form{"name": null}
    - slot{"item_to_add": "large mocha with whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add 
* affirm: sure
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 4.00}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* select_item{"item": "caffe latte"}: I'd also like a [caffe latte](item)
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* inform{"size": "grande"}: Make it a [grande](size)
    - slot{"requested_slot": "add_on"}
* deny
    - form{"name": null}
    - slot{"item_to_add": "grande caffe latte"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* deny: actually, nevermind
    - utter_deny_add
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status

## Guoguo convo 5/8
* select_store: open [starbucks](store)
    - slot{"store": "starbucks"}
    - store_form
    - action_set_menu
* select_item{"item": "Espresso"}: I'd like to have an [Espresso](item)
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* inform{"size": "large"}: [large](size)
    - slot{"requested_slot": "add_on"}
* deny
    - form{"name": null}
    - slot{"item_to_add": "large Espresso"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* affirm: yes please
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 4.00}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* select_item{"item": "mocha", "add_on": "8 pump"}: Can you also add a [8 pump](add_on) [mocha](item)
    - action_confirm_add
* affirm: yes
    - action_add_to_cart
    - slot{"num_cart_items": 2}
    - slot{"cart_total": 8.00}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* select_item{"item": "caffe latte"}: I'd like to order [caffe latte](item) for my wife as well
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* inform{"size": "large"}: [large](item)
    - slot{"requested_slot": "add_on"}
* deny
    - form{"name": null}
    - slot{"item_to_add": "large caffe latte"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* affirm: sure
    - action_add_to_cart
    - slot{"num_cart_items": 3}
    - slot{"cart_total": 10.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* ask_cart_contents: could you check the cart for me?
    - action_read_cart
* checkout_cart: checkout please
    - utter_confirm_checkout
* affirm: yes
    - action_checkout_cart
    - action_request_rating
* inform{"rating": "10"}: 10
    - slot{"rating": "10"}
    - utter_thank
    
## item_form interrupt
* select_store: open [starbucks](store)
    - slot{"store": "starbucks"}
    - store_form
    - action_set_menu
* select_item{"item": "espresso"}: I'd like to have an [Espresso](item)
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* ask_cart_contents: what's in my cart?
    - action_read_cart
    - item_form
    - slot{"requested_slot": "size"}
* inform{"size": "small"}: [small](size) please
    - slot{"requested_slot": "add_on"}
* deny: no thanks
    - form{"name": null}
    - slot{"item_to_add": "small caramel macchiato"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* affirm: sure
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 2.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* ask_cart_contents: tell me what's in my cart
    - action_read_cart

## add item + checkout
* select_store: open the [starbucks](store) menu
    - slot{"store": "starbucks"}
    - store_form
    - action_set_menu
* select_item{"size": "grande", "item": "Caffe Mocha", "add_on": "['whipped cream']"}: I'd like to have a [grande](size) [Caffe Mocha](item) with [whipped cream](add_on)
    - item_form
    - slot{"item_to_add": "large Espresso"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* affirm: sure
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 4.00}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* checkout_cart: checkout please
    - utter_confirm_checkout
* affirm: yep
    - action_checkout_cart
    - action_request_rating
* inform{"rating": "10"}: 10
    - slot{"rating": "10"}
    - utter_thank

## add item + remove item
* select_store: open the [starbucks](store) menu
    - slot{"store": "starbucks"}
    - store_form
    - action_set_menu
* select_item{"size": "small", "item": "Latte", "add_on": "['nutmeg']"}: I'd like to have a [small](size) [Latte](item) with [nutmeg](add_on)
    - item_form
    - slot{"item_to_add": "small latte with nutmeg"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* affirm: sure
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.00}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* remove_item: actually, I don't want that [latte](item)
    - cart_item_form
    - form{"name": "cart_item_form"}
    - slot{"target_cart_item": "latte"}
    - form{"name": null}
    - action_remove_from_cart
    - slot{"num_cart_items": 0}
    - slot{"cart_total": 0}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"item": null}
    - slot{"target_cart_item": null}
    - utter_cart_status

## add item + clear cart
* select_store: I'll order from [starbucks](store)
    - slot{"store": "starbucks"}
    - store_form
    - action_set_menu
* select_item{"size": "medium", "item": "cappuccino", "add_on": "['Extra foam']"}: Gimme a [medium](size) [cappuccino](item) with [extra foam](add_on)
    - item_form
    - slot{"item_to_add": "medium cappuccino with extra foam"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - action_confirm_add
* affirm: sure
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.00}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"add_on": null}
    - slot{"quantity": null}
    - utter_cart_status
* clear_cart: Actually, empty my cart
    - utter_confirm_clear_cart
* affirm
    - action_clear_cart