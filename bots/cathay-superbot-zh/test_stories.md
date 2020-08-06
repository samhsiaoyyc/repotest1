## Testing Resend email with G2-1-1 + resend email
* greet: 哈囉
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: c_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: c_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* resend_ebill: 補寄電子帳單
  - action_resend_ebill_api
  - utter_ebill_checkout
* resend: 補寄給我
  - resend_email_form
  - form{"name": "resend_email_form"}
  - utter_ask_resend_confirm
* form: affirm: 確認
  - form: resend_email_form
  - form{"name": null}
  - utter_resend_email_done
  - utter_help_resend
* usual: 常用功能
  - utter_usual

## Testing Resend email with G2-1-1 + resend email + change email
* greet: 哈囉
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: c_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: c_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* resend_ebill: 補寄電子帳單
  - action_resend_ebill_api
  - utter_ebill_checkout
* resend: 補寄給我
  - resend_email_form
  - form{"name": "resend_email_form"}
  - utter_ask_resend_confirm
* form: chage_mail: 改寄到另一個信箱
  - form: resend_email_form
  - form{"name": null}
  - reset_email_form
  - form{"name": "reset_email_form"}
  - utter_ask_new_email
* inform: @^*@#(@gmail.com
  - form: reset_email_form
  - utter_reset_email
  - form{"name": "reset_email_form"}
  - utter_ask_new_email
* inform: a4b5c6@gmail.com
  - form: reset_email_form
  - utter_ask_new_email_confirm
* form: chage_mail: 否，重新輸入
  - form: reset_email_form
  - form{"name": "reset_email_form"}
  - utter_ask_new_email
* inform: A456bc99@gmail.com
  - form: reset_email_form
  - utter_ask_new_email_confirm
* form: affirm: 是
  - form: reset_email_form
  - form{"name": null}
  - resend_email_form
  - form{"name": "resend_email_form"}
  - utter_ask_resend_confirm
* form: affirm: 確認
  - form: resend_email_form
  - form{"name": null}
  - utter_resend_email_done
  - utter_help_resend
* register_ebill: 申請電子帳單
  - utter_register_ebill


## Testing Resend email with G2-1-1-2 + ebill
* greet: 哈囉
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: b_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: b_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* resend_ebill: 補寄電子帳單
  - action_resend_ebill_api
  - utter_paper_bill_checkout
* ebill: 電子帳單
  - action_switch_ebill
  - resend_email_form
  - form{"name": "resend_email_form"}
  - utter_ask_resend_confirm
* form: affirm: 確認
  - form: resend_email_form
  - form{"name": null}
  - utter_resend_email_done
  - utter_help_resend
* usual: 常用功能
  - utter_usual

## Testing Resend email with G2-1-1-2 + recent bill details with twd + installment
* greet: 哈囉
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: b_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: b_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* resend_ebill: 補寄電子帳單
  - action_resend_ebill_api
  - utter_paper_bill_checkout
* recent: 近一期帳單消費明細
  - action_recent_detail_api
* installment: 我要分期
  - utter_installment

## Testing Resend email with G2-1-1-2 + non_resend
* greet: 哈囉
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: b_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: b_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* resend_ebill: 補寄電子帳單
  - action_resend_ebill_api
  - utter_paper_bill_checkout
* non_resend: 不用補寄
  - utter_help


## Testing Resend email with G2-1-2-2 + usual functionality
* greet: 哈囉
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: e_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: e_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* resend_ebill: 補寄電子帳單
  - action_resend_ebill_api
  - utter_paper_bill_uncheckout
  - utter_help_for_unbill_uncheckout
* usual: 常用功能
  - utter_usual

## Testing Resend email with G2-1-2 + recent bill details with frd  + installment
* greet: 哈囉
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: a_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: a_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* resend_ebill: 補寄電子帳單
  - action_resend_ebill_api
  - utter_ebill_uncheckout
  - utter_help_for_unbill_uncheckout
* recent: 近一期帳單明細
  - action_recent_detail_api
  - action_bill_detail_api
  - utter_unbill_detail
* installment: 我要分期
    - utter_installment

## Testing Resend email with G2-1-3 + usual functionality
* greet: 哈囉
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: d_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: d_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* resend_ebill: 補寄電子帳單
  - action_resend_ebill_api
  - utter_fallback
  - utter_help
* usual: 常用功能
  - utter_usual

## Testing Consum Details with query recent bill + unfound details + history bill 
* greet: 你好
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: d_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: d_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* search_consum_detail: 查詢消費明細
  - utter_search_detail
* recent: 近一期帳單明細
  - action_recent_detail_api
  - utter_unfound_detail
* history: 歷史帳單明細
  - utter_history
## Testing Consum Details with query recent bill + unfound details + query unbill detail
* greet: 你好
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: d_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: d_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* search_consum_detail: 查詢消費明細
  - utter_search_detail
* recent: 近一期帳單明細
  - action_recent_detail_api
  - utter_unfound_detail
* unbill: 未出帳明細
  - action_unbill_detail_api
  - utter_exception
## Testing Consum Details with query unbill detail + unfound details
* greet: 你好
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: d_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: d_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* search_consum_detail: 查詢消費明細
  - utter_search_detail
* unbill: 尚未出帳明細
  - action_unbill_detail_api
  - utter_exception
## Testing Consum Details with query unbill detail + found twd details + installment
* greet: 你好
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: a_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: a_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* search_consum_detail: 查詢消費明細
  - utter_search_detail
* unbill: 尚未出帳明細
  - action_unbill_detail_api
  - action_bill_detail_api
  - utter_recent_bill_detail
* installment: 我要分期
  - utter_installment
## Testing Consum Details with query unbill detail + found twd details + history bill
* greet: 你好
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: a_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: a_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* search_consum_detail: 查詢消費明細
  - utter_search_detail
* unbill: 尚未出帳明細
  - action_unbill_detail_api
  - action_bill_detail_api
  - utter_recent_bill_detail
* history: 歷史帳單明細
  - utter_history
## Testing Consum Details with query unbill detail + found frd details + query bill details
* greet: 你好
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: b_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: b_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* search_consum_detail: 查詢消費明細
  - utter_search_detail
* unbill: 尚未出帳明細
  - action_unbill_detail_api
  - action_bill_detail_api
  - utter_unbill_detail
* detail: 帳單明細
    - action_recent_detail_api
    - action_bill_detail_api
    - utter_unbill_detail
* installment: 我要分期
    - utter_installment
## Testing Consum Details with query unbill detail + found both currency type details + frd details + recent bill details
* greet: 你好
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: c_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: c_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* search_consum_detail: 查詢消費明細
  - utter_search_detail
* unbill: 尚未出帳明細
  - action_unbill_detail_api
  - action_bill_detail_api
  - utter_detail
* search_detail_frd: 查詢外幣明細
  - action_frd_detail_api
  - utter_unbill_detail
* detail: 帳單明細
  - action_recent_detail_api
  - action_bill_detail_api
  - utter_unbill_detail
* installment: 我要分期
  - utter_installment
## Testing Consum Details with query unbill detail + found both currency type details + twd details + pay
* greet: 你好
  - utter_greet
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_id
* inform: c_user
  - login_form
  - form{"name": "login_form"}
  - utter_ask_user_password
* inform: c_user
  - form: login_form
  - form{"name": null}
  - utter_begin_action
* search_consum_detail: 查詢消費明細
  - utter_search_detail
* unbill: 尚未出帳明細
  - action_unbill_detail_api
  - action_bill_detail_api
  - utter_detail
* search_detail_twd: 查詢台幣明細
  - action_twd_detail_api
  - utter_recent_bill_detail
* pay: 我要繳費
  - utter_pay



