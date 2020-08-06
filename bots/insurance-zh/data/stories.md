## Guardianship:Yes + eCallBao:End
> answer_guardianship
> answer_guardianship_again
* yes
  - utter_thanks

  - utter_is_guardianship
  - utter_bye

## Guardianship:No
> answer_guardianship
> answer_guardianship_again
* no
  - utter_thanks
> fill_form

## Guardianship:What
> answer_guardianship
* what
  - utter_explain_guardianship
  - utter_ask_guardianship
> answer_guardianship_again

## Fill_Form
> fill_form
  - utter_check_insurance_content
  - slot{"repeat_count": 0}
  - action_fill_eCallBao_form

## eCallBao:Begin + Guardianship:Yes
* pickup
  - utter_greetings
  
  - utter_check_guardianship
> answer_guardianship

## eCallBao:Transfer
> answer_guardianship_again
* what
  - action_tranfer_to_servicer
