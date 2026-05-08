import requests
from django.conf import settings

def convert_currency(amount, from_currency, target_currency='USD'):
    if from_currency == target_currency:
        return amount 
    
    # make the API call here
    # the URL format is:
    # https://v6.exchangerate-api.com/v6/YOUR_KEY/pair/FROM_CURRENCY/USD
    api_key = settings.EXCHANGE_RATE_API_KEY
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{from_currency}/{target_currency}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code == 200 and data.get('result') == 'success':
            conversion_rate = data.get('conversion_rate')
            return amount * conversion_rate

        return amount

    except (requests.RequestException, ValueError, KeyError):
        return amount