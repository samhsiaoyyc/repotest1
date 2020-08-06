# Example bot for Cathay Superbot zh version

## TODO

- [x] Fix reset_email_form form action can't re-input email after input chage_mail intent at new_email_confirm
- [x] Build docker image of API Mock Server
- [x] Refactor code
- [x] Add Mock Server created by Flask
- [x] E2E Testing

## Get started

### Installation

The version of rasa x I tested is 0.26.3:

        pip install  rasa-x==0.26.3 --extra-index-url https://pypi.rasa.com/simple
        

This also installs rasa 1.8.3, rasa sdk 1.8.0 and tensorflow 2.1.0


Install Flask:

        pip install flask

### Run

Train model:

        cd ngChat/
        PYTHONPATH=./:$PYTHONPATH rasa train --data bots/cathay-superbot-zh/data/ --config bots/cathay-superbot-zh/config.yml --domain bots/cathay-superbot-zh/domain.yml --out bots/cathay-superbot-zh/models

Run rasa action server:

        cd bots/cathay-superbot-zh/
        rasa run actions

Run Mock API Server:

        python mock_server.py

Run rasa conversation:
        
        cd ngChat/
        rasa shell -m bots/cathay-superbot-zh/models/ --endpoints bots/cathay-superbot-zh/endpoints.yml


for e2e testing:

        cd ngChat/
        PYTHONPATH=./$PYTHONPATH rasa test --e2e -s bots/cathay-superbot-zh/test_stories.md -m bots/cathay-superbot-zh/models/ -c bots/cathay-superbot-zh/config.yml -u bots/cathay-superbot-zh/data/nlu.md --out bots/cathay-superbot-zh/results/

### Test bot

There are 5 test_user for different path:

| user_id | user_password | 查詢未出帳明細 | 近一期帳單明細 | 補寄電子帳單 |
| ------- | ------------- | -------------- | -------------- | ------------ |
| a_user  | a_user        | 台幣           | 外幣           | G2-1-2       |
| b_user  | b_user        | 外幣           | 台幣           | G2-1-1-2     |
| c_user  | c_user        | 台/外幣        | 外幣           | G2-1-1       |
| d_user  | d_user        | 查無           | 查無           | G2-1-3       |
| e_user  | e_user        | 查無           | 台幣           | G2-1-2-2     |


Insert greet saying to trigger service:

> Your input ->  哈囉
> > 嗨我是阿發! 你好嗎?
> 
> > 請輸入您的帳號
> 
> Your input -> c_user
> 
> > 請輸入您的密碼
> 
> Your input -> c_user
> 
> > 請選擇服務?
> 
> > 1: 查詢消費明細 (查詢消費明細)
> > 2: 補寄電子帳單 (補寄電子帳單)
