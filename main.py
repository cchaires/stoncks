import requests
import os
import dotenv
import datetime
from twilio.rest import Client


def get_api_key(api_name):
    """Returns API KEY from API_KEYS.env file"""
    dotenv.load_dotenv(dotenv_path="API_KEYS.env")
    return os.getenv(api_name)


def stonks_api():
    """Return a list of the closing values from yesterday and the day before yesterday for Tesla stock."""
    api_key_stonks = get_api_key('STOCK_API_KEY')
    stock = "TSLA"
    url_stonks = "https://www.alphavantage.co/query"
    params_stonks = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": stock,
        "outputsize": "compact",
        "datatype": "json",
        "apikey": api_key_stonks
    }
    r_stonks = requests.get(url_stonks, params=params_stonks)
    r_stonks.raise_for_status()
    r_data = r_stonks.json()

    stock_yesterday = float(r_data['Time Series (Daily)'][str(now)]['4. close'])
    stock_before_yesterday = float(r_data['Time Series (Daily)'][str(before)]['4. close'])
    return stock_yesterday, stock_before_yesterday


def percentage_change():
    yesterday, before_yesterday = stonks_api()
    percent_change = ((yesterday - before_yesterday) / before_yesterday) * 100
    return percent_change


def news_api():
    news_api_key = get_api_key('NEWS_API_KEY')
    company_name = "Tesla Inc"
    url_news = "https://newsapi.org/v2/everything"
    params_news = {
        "q": company_name,
        "from": now,
        "sortBy": "relevancy",
        "pageSize": 3,
        "apiKey": news_api_key
    }
    r_news = requests.get(url_news, params=params_news)
    r_news.raise_for_status()
    r_json = r_news.json()
    return r_json


def get_news(article_number):
    articles = news_api()['articles']
    if article_number < 1 or article_number > len(articles):
        return "Invalid article number"
    else:
        article = articles[article_number - 1]
        print(f"TESLA: {round(percentage_change(), 2)}% Title: {article['title']}")
        return f"TESLA: {round(percentage_change(), 2)}% Title: {article['title']}"


def sms_api():
    account_sid = get_api_key('TWILIO_ACCOUNT_SID')
    auth_token = get_api_key('TWILIO_AUTH_TOKEN')
    api_key = get_api_key('TWILIO_API_KEY')
    client = Client(account_sid, auth_token)
    return client


def send_sms():
    for i in range(1, 4):
        message = sms_api().messages \
            .create(
            body=get_news(i),
            from_='YOUR TWILIO PHONE NUMBER',
            to='+YOUR PHONE NUMBER'
        )


# Date:
now = datetime.date.today() - datetime.timedelta(days=1)
before = now - datetime.timedelta(days=1)

if abs(percentage_change()) >= 5:
    send_sms()
else:
    print("Nothing relevant")
