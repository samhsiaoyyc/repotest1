# Example bot for E Call Bao - ch_zh

## TODO

- [ ] Complete form format handling and validation
- [ ] Complete the feature of redirecting to customer service
- [ ] Streaming the Twilio SMS service

## Get started

### Installation

The version of rasa x I tested is 0.26.3:

        pip install  rasa-x==0.26.3 --extra-index-url https://pypi.rasa.com/simple

This also installs rasa 1.8.3, rasa sdk 1.8.0 and tensorflow 2.1.0

### Run

        rasa run actions &
        rasa x

After running Rasa x, please train and active bot firstly. Then we can test this bot by "Talk to your bot" or having conversation after "share your bot".

## References:

- [Rasa SDK](https://rasa.com/docs/rasa/api/rasa-sdk/)
- [Cuztomized Actions](https://rasa.com/docs/rasa/core/actions/#custom-actions)
- [Form](https://rasa.com/docs/rasa/core/forms/#form-basics)

## Note: I have some requirement/questions about more detail of conversation:

1. 對話5: 依年齡宣讀投保金額範圍 => 需要投保金額對照表。
2. 對話8: 請問是否要附醫療專機 => 醫療專機對於保費是否有額外收費？有的話，需要費率表。
3. 對話9: 判斷是否為國泰世華卡友，且保費超過$1100，可贈送不便險 => 是指月繳1100?
4. 對話9: 若投保額度超過電話投保額度 = > 需要電話投保額度標準。
5. 對話10: 請問是否加收不便險? => 需要不便險的費率表。
6. 對話10: 請問是否加收不便險? => 電話投保額度是否包含不便險。
