import requests
from twilio.rest import Client

# the company we are interested
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything'

STOCK_API_KEY = "**********"
NEWS_API_KEY = '**********'
TWILIO_ACCOUNT_SIC = '**********'
TWILIO_AUTH_TOKEN = '**********'

PARAMETERS = {
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY,
}
r = requests.get(STOCK_ENDPOINT, params=PARAMETERS)
data = r.json()
daily_data = data["Time Series (Daily)"]

# using list comprehension to turn that long dictionary into lists
daily_data_list = [value for (key, value) in daily_data.items()]
latest_price = daily_data_list[0]['4. close']
the_day_before_price = daily_data_list[1]['4. close']

diff_percent = (float(latest_price) - float(the_day_before_price))/float(latest_price) * 100
# when the stock price changes 1 percent, get the first 3 news
up_down = None
if diff_percent > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
if abs(diff_percent) > 1:
    NEWS_PARAMETERS = {
        "qInTitle": COMPANY_NAME,
        "apikey": NEWS_API_KEY,
    }
    news_r = requests.get(NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    articles = news_r.json()["articles"]
    first_three_articles = articles[:3]

formatted_articles = [f"{STOCK_NAME}: {up_down}{round(abs(diff_percent),2)}% \nHeadline: {article['title']}, \nBrief: {article['description']}" for article in first_three_articles]

client = Client(TWILIO_ACCOUNT_SIC, TWILIO_AUTH_TOKEN)
for article in formatted_articles:
    message = client.messages \
        .create(
        body=article,
        from_='**********',
        to='**********',
    )

