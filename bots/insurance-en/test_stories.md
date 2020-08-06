## greet + goodbye
* greet: Hi!
  - utter_greet
* bye: Bye
  - utter_bye

## greet + thanks
* greet: Hello there
  - utter_greet
* thank: thanks a bunch
  - utter_noworries

## greet + thanks + goodbye
* greet: Hey
  - utter_greet
* thank: thank you
  - utter_noworries
* bye: bye bye
  - utter_bye
  
## ask guardianship
* faq: what is under guardianship??
  - respond_faq

## ask insurance 
* faq: what is total insurance amount?
  - respond_faq

## ask 
* faq: what is air ambulance transport?
  - respond_faq

## insurance form
* greet: hello
    - utter_greet
* quote_insurance: I'd like to quote insurance
    - insurance_form
    - form{"name":"insurance_form"}
    - utter_ask_name
* inform: [xuchen yao](name)
    - insurance_form
    - utter_ask_is_under_guardianship
* faq: what is under guardianship
    - respond_faq
    - insurance_form
    - utter_ask_is_under_guardianship
* explain: explain this 
    - utter_explain_guardianship
    - insurance_form
    - utter_ask_is_under_guardianship
* deny: nope
    - insurance_form
    - form{"name":"insurance_form"}
    - utter_ask_birthday
* inform: [01/01/1970](birthday)
    - insurance_form
    - form{"name":"insurance_form"}
    - utter_ask_insurance_day
* inform: [10](insurance_day) days
    - insurance_form
    - form{"name":"insurance_form"}
    - utter_ask_travel_country
* inform: [Japan](travel_country)
    - insurance_form
    - form{"name":"insurance_form"}
    - utter_ask_total_amount
* inform: [$1000000](total_amount)
    - insurance_form
    - utter_ask_need_airlift
* affirm: yes
    - insurance_form
    - utter_ask_email
* inform: [yaoxuchen@gmail.com](email)
    - insurance_form
    - form{"name":null}

