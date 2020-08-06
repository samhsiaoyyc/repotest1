## greet
* greet
  - utter_greet

## thank
* thank
  - utter_noworries

## goodbye
* goodbye
  - utter_goodbye

## question from FAQ
* faq
    - respond_faq

## hello + select store
* select_store{"store": "Starbucks"}
    - store_form
    - form{"name": "store_form"}
    - slot{"store": "Starbucks"}
    - form{"name": null} 
    - action_set_menu
> select_store

## describe menu
* describe_menu
    - action_describe_menu
> describe_menu

## describe category
* describe_category{"category": "Hot Drinks"}
    - action_describe_category
> describe_category

## describe category, store not selected first
* describe_category{"store": "starbucks", "category": "hot drinks"}
    - store_form
    - form{"name": "store_form"}
    - action_set_menu
    - form{"name": null}
    - action_describe_category

## describe menu, store not selected first
* describe_menu{"store": "starbucks"}
    - store_form
    - form{"name": "store_form"}
    - slot{"store": "starbucks"}
    - form{"name": null}
    - action_set_menu
    - action_describe_menu

## interactive_story_1
* greet
    - utter_greet
* select_store{"store": "Starbucks"}
    - store_form
    - action_set_menu
* goodbye
    - utter_goodbye

## select store, ask info, select item w/checkpoints
> select_store
> describe_menu
> describe_category
> add_item

## skip select store
* select_item{"item": "Americano", "size": "Venti"}
    - store_form
    - form{"name": "store_form"}
    - slot{"requested_slot": "store"}
* inform{"store": "starbucks"}
    - slot{"store": "starbucks"}    
    - action_set_menu
    - form{"name": null}
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "options"}
    - slot{"item_to_add": "Venti Americano"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
* deny
    - form{"name": null}
    - action_confirm_add
* deny
    - utter_deny_add

## order item right away
* select_item{"item": "caramel macchiato"}
    - store_form
    - form{"name": "store_form"}
    - slot{"requested_slot": "store"}
* inform{"store": "starbucks"}
    - slot{"store": "starbucks"}
    - action_set_menu
    - form{"name": null}
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* inform{"size": "small"}
    - slot{"requested_slot": "options"}
* inform{"options": "['whipped cream']"}
    - slot{"requested_slot": null}
    - slot{"item_to_add": "small caramel macchaito with whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"quantity": null}
    - slot{"options": null}
    - utter_cart_status

## interactive order right away
* select_item{"item": "caramel macchiato"}
    - slot{"item": "caramel macchiato"}
    - store_form
    - form{"name": "store_form"}
    - slot{"requested_slot": "store"}
* form: inform{"store": "starbucks"}
    - slot{"store": "starbucks"}
    - form: store_form
    - slot{"store": "starbucks"}
    - form: followup{"name": "action_set_menu"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_set_menu
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caramel macchiato"}
    - slot{"requested_slot": "size"}
* form: inform{"size": "20oz"}
    - slot{"size": "20oz"}
    - form: item_form
    - slot{"size": "20oz"}
    - slot{"requested_slot": "options"}
* form: deny
    - form: item_form
    - slot{"options": ["20oz"]}
    - slot{"item_to_add": "20oz caramel macchiato"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form: followup{"name": "action_confirm_add"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"quantity": null}
    - slot{"options": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart
    
## hello + select store + add item
* greet
    - utter_greet
> select_store
* select_item{"item": "Flat White", "size": "small"}
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "options"}
* inform{"options": "['foam']"}
    - slot{"item_to_add": "small Flat White with foam"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"quantity": null}
    - slot{"options": null}
    - utter_cart_status

## select store + how to add + add item
> select_store
* faq
    - respond_faq
* select_item{"size": "medium", "item": "Caffe Americano"}
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "options"}
* affirm
    - slot{"requested_slot": "options"}
    - slot{"options": "['room']"}
    - slot{"item_to_add": "Medium Caffe Americano with room"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - utter_cart_status

## select store + add item + read cart
> select_store
* select_item{"item": "Latte", "options": "['Whipped Cream']"}
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* inform{"size": "large"}
    - slot{"item_to_add": "Large latte with whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart

## hello + read cart (empty)
* greet
    - utter_greet
* ask_cart_contents
    -action_read_cart

## add item + confirm + deny
* select_item{"size": "medium", "item": "Caffe Mocha", "options": "['whole milk']"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item_to_add": "medium caffe mocha with whole milk"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - action_confirm_add
> add_item
* deny
    - utter_deny_add
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}

## Rasa X story
* greet
    - utter_greet
> select_store
* select_item{"item": "Caffe Americano"}
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* inform{"size": "medium"}
    - slot{"requested_slot": "options"}
* deny
    - slot{"options": "[]"}
    - slot{"item_to_add": "medium caffe americano"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name":null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart

## select store + add item w/ 2 add-ons
> select_store
> describe_menu
> describe_category
* select_item{"item": "Caffe Americano", "options": "['cream', 'room']"}
    - item_form
    - form{"name": "item_form"}
    - slot{"requested_slot": "size"}
* inform
    - slot{"size": "venti"}
    - slot{"item_to_add": "venti americano with cream and room"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name":null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}

## interactive_story_1
* greet
    - utter_greet
* faq
    - respond_faq
> select_store
* faq
    - respond_faq
* select_item{"size": "venti", "item": "caffe americano", "options": "sugar"}
    - slot{"options": ["cream", "sugar"]}
    - slot{"item": "caffe americano"}
    - slot{"size": "venti"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caffe americano"}
    - slot{"size": "venti"}
    - slot{"options": ["cream", "sugar"]}
    - slot{"item_to_add": "Venti Americano with cream and sugar"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
* ask_cart_contents
    - action_read_cart
* select_item{"item": "cappuccino"}
    - slot{"item": "cappuccino"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "cappuccino"}
    - slot{"item": "cappuccino"}
    - slot{"requested_slot": "size"}
* form: inform{"size": "small"}
    - slot{"size": "small"}
    - form: item_form
    - slot{"size": "small"}
    - slot{"requested_slot": "options"}
* form: inform{"options": "foam"}
    - slot{"options": ["foam"]}
    - form: item_form
    - slot{"options": ["extra foam"]}
    - slot{"item_to_add": "small cappuccino with foam"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 2}
    - slot{"cart_total": 6.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
* ask_cart_contents
    - action_read_cart
    
## interactive_story_2 + remove from cart
* greet
    - utter_greet
* faq
    - respond_faq
> select_store
* faq
    - respond_faq
> describe_menu
> describe_category
* select_item{"size": "venti", "item": "caffe americano", "options": "sugar"}
    - slot{"options": ["cream", "sugar"]}
    - slot{"item": "caffe americano"}
    - slot{"size": "venti"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caffe americano"}
    - slot{"size": "venti"}
    - slot{"options": ["cream", "sugar"]}
    - slot{"item_to_add": "Venti Americano with cream and sugar"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
* ask_cart_contents
    - action_read_cart
* select_item{"item": "cappuccino"}
    - slot{"item": "cappuccino"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "cappuccino"}
    - slot{"requested_slot": "size"}
* form: inform{"size": "small"}
    - slot{"size": "small"}
    - form: item_form
    - slot{"size": "small"}
    - slot{"requested_slot": "options"}
* form: inform{"options": "foam"}
    - slot{"options": ["foam"]}
    - form: item_form
    - slot{"options": ["extra foam"]}
    - slot{"item_to_add": "small cappuccino with foam"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
* ask_cart_contents
    - action_read_cart
* remove_from_cart
    - slot{"target_cart_item": "caffe americano"}
    - form{"name": "cart_item_form"}
    - form{"name": null}
    - action_remove_from_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"item": null}
    - slot{"target_cart_item": null}
    - utter_cart_status

## interactive_story_3 + remove from cart
> select_store
* select_item{"item": "caramel macchiato"}
    - slot{"item": "caramel macchiato"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caramel macchiato"}
    - slot{"item": "caramel macchiato"}
    - slot{"requested_slot": "size"}
* form: inform{"size": "medium"}
    - slot{"size": "medium"}
    - form: item_form
    - slot{"size": "medium"}
    - slot{"requested_slot": "options"}
* form: deny
    - form: item_form
    - slot{"options": []}
    - slot{"item_to_add": "medium caramel macchiato"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* describe_category{"category": "Hot Teas"}
    - action_describe_category
* select_item{"size": "small", "item": "espresso"}
    - slot{"item": "espresso"}
    - slot{"size": "small"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "espresso"}
    - slot{"size": "small"}
    - slot{"item": "espresso"}
    - slot{"size": "small"}
    - slot{"requested_slot": "options"}
* form: deny
    - form: item_form
    - slot{"options": []}
    - slot{"item_to_add": "small espresso"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* remove_from_cart{"target_cart_item": "espresso"}
    - cart_item_form
    - form{"name": "cart_item_form"}
    - slot{"target_cart_item": "espresso"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_remove_from_cart
    - slot{"num_cart_items": 0}
    - slot{"cart_total": 0}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart
* thank
    - utter_noworries

## interactive_story_4
* greet
    - utter_greet
> select_store
* select_item{"item": "caffe americano", "options": "room"}
    - slot{"options": ["room"]}
    - slot{"item": "caffe americano"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caffe americano"}
    - slot{"options": ["room"]}
    - slot{"item": "caffe americano"}
    - slot{"options": ["room"]}
    - slot{"requested_slot": "size"}
* form: inform{"size": "12oz"}
    - slot{"size": "12oz"}
    - form: item_form
    - slot{"size": "12oz"}
    - slot{"item_to_add": "12oz caffe Americano with room"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* describe_menu
    - action_describe_menu
* select_item{"size": "16oz", "item": "caffe mocha", "options": "whipped cream"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "caffe mocha"}
    - slot{"size": "16oz"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caffe mocha"}
    - slot{"size": "16oz"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "caffe mocha"}
    - slot{"size": "16oz"}
    - slot{"options": ["whipped cream"]}
    - slot{"item_to_add": "16oz caffe mocha with whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart
* remove_from_cart{"target_cart_item": "caffe mocha"}
    - slot{"target_cart_item": "caffe mocha"}
    - cart_item_form
    - form{"name": "cart_item_form"}
    - slot{"requested_slot": "target_cart_item"}
    - form{"name": null}
    - action_remove_from_cart
    - slot{"num_cart_items": 0}
    - slot{"cart_total": 0}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status

## interactive_story_5
> select_store
* select_item{"item": "caffe latte", "options": "whipped cream"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "caffe latte"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "smoked butterscotch latte"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "smoked butterscotch latte"}
    - slot{"options": ["whipped cream"]}
    - slot{"requested_slot": "size"}
* form: inform{"size": "12oz"}
    - slot{"size": "12oz"}
    - form: item_form
    - slot{"size": "12oz"}
    - slot{"item_to_add": "12oz smoked butterscotch latte with whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart
* select_item{"size": "16oz", "item": "americano", "options": "cream"}
    - slot{"options": ["room", "cream"]}
    - slot{"item": "americano"}
    - slot{"size": "16oz"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caffe americano"}
    - slot{"size": "16oz"}
    - slot{"options": ["room", "whipped cream"]}
    - slot{"item": "caffe americano"}
    - slot{"size": "16oz"}
    - slot{"options": ["room", "whipped cream"]}
    - slot{"item_to_add": "16oz caffe americano with room and whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart
* thank
    - utter_noworries

## Interactive story 5 + clear cart, affirm
> select_store
* select_item{"item": "caffe latte", "options": "whipped cream"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "caffe latte"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "smoked butterscotch latte"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "smoked butterscotch latte"}
    - slot{"options": ["whipped cream"]}
    - slot{"requested_slot": "size"}
* form: inform{"size": "12oz"}
    - slot{"size": "12oz"}
    - form: item_form
    - slot{"size": "12oz"}
    - slot{"item_to_add": "12oz smoked butterscotch latte with whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart
* select_item{"size": "16oz", "item": "americano", "options": "cream"}
    - slot{"options": ["room", "cream"]}
    - slot{"item": "americano"}
    - slot{"size": "16oz"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caffe americano"}
    - slot{"size": "16oz"}
    - slot{"options": ["room", "whipped cream"]}
    - slot{"item": "caffe americano"}
    - slot{"size": "16oz"}
    - slot{"options": ["room", "whipped cream"]}
    - slot{"item_to_add": "16oz caffe americano with room and whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* clear_cart
    - utter_confirm_clear_cart
* affirm
    - action_clear_cart

## interactive story 5 + clear cart, deny
> select_store
> describe_menu
* select_item{"item": "caffe latte", "options": "whipped cream"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "caffe latte"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "smoked butterscotch latte"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "smoked butterscotch latte"}
    - slot{"options": ["whipped cream"]}
    - slot{"requested_slot": "size"}
* form: inform{"size": "12oz"}
    - slot{"size": "12oz"}
    - form: item_form
    - slot{"size": "12oz"}
    - slot{"item_to_add": "12oz smoked butterscotch latte with whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart
* select_item{"size": "16oz", "item": "americano", "options": "cream"}
    - slot{"options": ["room", "cream"]}
    - slot{"item": "americano"}
    - slot{"size": "16oz"}
    - item_form
    - form{"name": "item_form"}
    - slot{"item": "caffe americano"}
    - slot{"size": "16oz"}
    - slot{"options": ["room", "whipped cream"]}
    - slot{"item": "caffe americano"}
    - slot{"size": "16oz"}
    - slot{"options": ["room", "whipped cream"]}
    - slot{"item_to_add": "16oz caffe americano with room and whipped cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/f12bc8af498d45ed92c5d6f1dac64062.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 3.50}
    - followup{"name": "action_clear_slots"}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"options": null}
    - slot{"quantity": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* clear_cart
    - utter_confirm_clear_cart
* deny
    - utter_deny_clear_cart

## describe menu + describe category
> select_store
* describe_category{"category": "Hot Drinks"}
    - slot{"category": "Hot Drinks"}
    - action_describe_category
* describe_menu
    - action_describe_menu
* describe_category{"category": "Hot Teas"}
    - slot{"category": "Hot Teas"}
    - action_describe_category

## checkout
> select_store
> describe_category
> add_item
* checkout_cart
    - utter_confirm_checkout
* affirm
    - action_checkout_cart
    - action_request_rating
* inform{"rating": "10"}
    - slot{"rating": "10"}
    - utter_thank

## checkout deny
> select_store
> describe_menu
> add_item
* checkout_cart
    - utter_confirm_checkout
* deny
    - utter_cancel_checkout
    - action_request_rating
* inform{"rating": "10"}
    - slot{"rating": "10"}
    - utter_thank

## interactive_story
* select_store{"store": "starbucks"}
    - slot{"store": "starbucks"}
    - store_form
    - form{"name": "store_form"}
    - slot{"store": "starbucks"}
    - slot{"store": "starbucks"}
    - form: followup{"name": "action_set_menu"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_set_menu
* describe_menu
    - action_describe_menu
* describe_category{"category": "cold drinks"}
    - slot{"category": "cold drinks"}
    - action_describe_category
* select_item{"item": "violet drink", "options": ["whipped cream"]}
    - item_form
    - form{"name": "item_form"}
    - slot{"store": "starbucks"}
    - slot{"item": "violet drink"}
    - slot{"options": []}
    - slot{"requested_slot": "size"}
* form: inform{"size": "venti"}
    - slot{"size": "venti"}
    - form: item_form
    - slot{"size": "Venti"}
    - form: followup{"name": "action_confirm_add"}
    - slot{"item_to_add": "a Venti Violet Drink"}
    - slot{"image": "https://globalassets.starbucks.com/assets/cec54d35a8f84706b86c3a2ae839fa7e.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - followup{"name": "action_clear_slots"}
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 0.0}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"quantity": null}
    - slot{"options": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* checkout_cart
    - utter_confirm_checkout
* affirm
    - action_checkout_cart
    - slot{"readable_cart": "The cart is empty."}
    - action_request_rating
* inform{"rating": "10"}
    - slot{"rating": "10"}
    - utter_thank

## interactive_story_1
* select_store{"store": "starbucks"}
    - slot{"store": "starbucks"}
    - store_form
    - form{"name": "store_form"}
    - slot{"store": "starbucks"}
    - slot{"store": "starbucks"}
    - form: followup{"name": "action_set_menu"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_set_menu
* describe_menu
    - action_describe_menu
* describe_category{"category": "hot coffees"}
    - slot{"category": "hot coffees"}
    - action_describe_category
* select_item{"size": "grande", "item": "white chocolate mocha", "options": "whipped cream"}
    - slot{"options": ["whipped cream"]}
    - slot{"item": "white chocolate mocha"}
    - slot{"size": "grande"}
    - item_form
    - form{"name": "item_form"}
    - slot{"store": "starbucks"}
    - slot{"item": "white chocolate mocha"}
    - slot{"size": "Grande"}
    - slot{"options": ["with Whipped Cream"]}
    - slot{"item": "white chocolate mocha"}
    - slot{"size": "Grande"}
    - slot{"options": ["with Whipped Cream", "Grande"]}
    - form: followup{"name": "action_confirm_add"}
    - slot{"item_to_add": "a Grande White Chocolate Mocha with with Whipped Cream"}
    - slot{"image": "https://globalassets.starbucks.com/assets/4b621e63f6ba4c19a8618055284eca8d.jpg?impolicy=1by1_wide_1242"}
    - form{"name": null}
    - slot{"requested_slot": null}
    - action_confirm_add
* affirm
    - action_add_to_cart
    - followup{"name": "action_clear_slots"}
    - slot{"num_cart_items": 1}
    - slot{"cart_total": 0.0}
    - action_clear_slots
    - slot{"size": null}
    - slot{"item": null}
    - slot{"quantity": null}
    - slot{"options": null}
    - slot{"target_cart_item": null}
    - utter_cart_status
* ask_cart_contents
    - action_read_cart
* checkout_cart
    - utter_confirm_checkout
* affirm
    - action_checkout_cart
    - action_request_rating
* inform{"rating": "10"}
    - slot{"rating": "10"}
    - utter_thank



