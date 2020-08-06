## intent:quote_insurance
- I'd like to apply for travel insurance
- travel insurance
- may I please get a quote insurance for travel?
- travel insurance please

## intent:inform
- [Xuchen Yao](name)
- my name is [Xuchen Yao](name)
- i'm [Xuchen Yao](name)
- [04/07/1984](birthday)
- [01/01/1970](birthday)
- [10](insurance_day) days
- [ten](insurance_day) days
- [japan](travel_country: Japan)
- [thailand](travel_country: Thailand)
- [south korea](travel_country: South Korea)
- [taiwan](travel_country: Taiwan)
- [Cambodia](travel_country: Cambodia)
- [china](travel_country: China/HK/Macao)
- [Laos](travel_country: Laos)
- [Malaysia](travel_country: Malaysia)
- [Singapore](travel_country: Singapore)
- [Thailand](travel_country: Thailand)
- [The Philippines](travel_country: The Philippines)
- [Vietnam](travel_country: Vietnam)
- [Other Countries](travel_country: Other Countries)
- [none of them](travel_country: Other Countries)
- [usa](travel_country: Other Countries)
- [canada](travel_country: Other Countries)
- [russia](travel_country: Other Countries)
- [$1m](total_amount)
- [$1000](total_amount)
- [yaoxuchen@gmail.com](email)
- [xuchen@seasalt.ai](email)
- [asdfa@safd.com](email)
- [guoguo chen](name)
- [23/88/2341](birthday)
- [13](insurance_day)
- [Thailand](travel_country: Thailand)
- [$500,000](total_amount)
- [jlw@jlas.com](email)

## intent:explain
- why
- what's this?
- what's that?
- what is it?
- why is that
- why do you need it
- why do you need to know that?
- could you explain why you need it?

## intent:faq/ask_guardianship
- what is under guardianship?
- could you please explain under guardianship?

## intent:faq/ask_amount
- what is total insurance amount?
- could you please explain total insurance amount?

## intent:faq/ask_airlift
- what is air ambulance transport?
- what is air ambulance transport and does it add cost?
- could you please explain air ambulance transport?

## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there

## intent:goodbye
- bye
- goodbye
- see you around
- see you later

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct
- yes please

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really
- nope

## intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good

## intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?

## intent:out_of_scope
- I want to order food
- What is 2 + 2?
- Who’s the US President?
- I need a job
- Now?
- Pizza bot
- Recharge
- SEL ME SOMETHING
- The Try it out is not working
- The weather is good
- Today
- Try it out broken
- What day is it today?
- What did you eat yesterday?
- What do you prefer?
- What is todays date

## synonym: Cambodia
- Cambodia

## synonym: China/HK/Macao
- china
- hong kong
- hk
- macro

## synonym: Japan
- japan

## synonym: Laos
- Laos

## synonym: Malaysia
- Malaysia

## synonym: Other Countries
- Other Countries
- none of them
- usa
- canada
- russia

## synonym: Singapore
- Singapore

## synonym: South Korea
- south korea

## synonym: Taiwan
- taiwan

## synonym: Thailand
- thailand
- Thailand

## synonym: The Philippines
- The Philippines

## synonym: Vietnam
- Vietnam

## regex:birthday
- [0-9]{1,2}(/|-|\s+)[0-9]{1,2}(/|-|\s+)[0-9]{2,4}
- [0-9]{2,4}(/|-|\s+)[0-9]{1,2}(/|-|\s+)[0-9]{1,2}

## regex:email
- [^@]+@[^@]+\.[^@]+

## regex:insurance_days
- \d+

## regex:total_amount
- \$[\d,]+

## lookup:other_countries.txt
  data/other_countries.txt
