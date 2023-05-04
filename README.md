Stonks API and News API
This Python script retrieves the closing values of Tesla's stock for yesterday and the day before yesterday from Alpha Vantage's API and calculates the percentage change. It also retrieves the three most relevant news articles related to Tesla Inc. from News API.

If the percentage change is greater than or equal to 5%, the script sends an SMS message using Twilio's API with the percentage change and the title of the most relevant news article.

To use this script, you'll need to obtain API keys for Alpha Vantage, News API, and Twilio and save them in an API_KEYS.env file. The file should contain the following variables:

STOCK_API_KEY
NEWS_API_KEY
TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_API_KEY
Make sure to replace YOUR TWILIO PHONE NUMBER and YOUR PHONE NUMBER with your actual phone numbers.

Note: This script requires the requests, os, dotenv, datetime, and twilio libraries.