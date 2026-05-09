from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from portfolio.models import Asset, Stock, CashAccount
import yfinance as yf
from decimal import Decimal
from portfolio.utils import convert_currency
import plotly.graph_objects as go
import plotly.utils
import json
from news.utils import fetch_financial_news, get_ai_recommendations

@login_required
def dashboard_view(request):
    active_assets = Asset.objects.filter(user=request.user, status='active')
    accounts = CashAccount.objects.filter(user=request.user)
    active_stocks = Stock.objects.filter(user=request.user, status='active')
    display_currency = request.GET.get('currency', 'USD')
    currency_symbols = {'USD': '$', 'NGN': '₦'}
    currency_symbol = currency_symbols.get(display_currency, '$')
    stock_data = []
    for stock in active_stocks:
        try:
            ticker = yf.Ticker(stock.ticker)
            current_price = ticker.fast_info['lastPrice']
            current_value = current_price * float(stock.shares)
        except:
            current_price = None
            current_value = None
        stock_data.append({
            'stock': stock,
            'current_price': current_price,
            'current_value': current_value
        })
    
    total_stock = sum(Decimal(str(item['current_value'])) for item in stock_data if item['current_value'] is not None)
    total_stock = convert_currency(total_stock, 'USD', display_currency)

    total_assets = sum(convert_currency(asset.current_value, asset.currency, display_currency) for asset in active_assets)

    total_cash = sum(convert_currency(account.balance, account.currency, display_currency) for account in accounts) 

    net_worth = total_assets + total_cash + total_stock



    fig = go.Figure(data=[go.Pie(
        labels=['Assets', 'Stocks', 'Cash'],
        values=[total_assets, total_stock, total_cash]
    )])
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    news_articles = fetch_financial_news()
    ai_recommendation = get_ai_recommendations(news_articles)

    return render(request, 'dashboard/dashboard.html', {
        'user': request.user,
        'total_assets' : total_assets, 
        'total_cash' : total_cash, 
        'total_stock' : total_stock,
        'net_worth' : net_worth,
        'display_currency': display_currency,
        'currency_symbol' : currency_symbol,
        'graph_json': graph_json,
        'news_articles': news_articles,
        'ai_recommendation': ai_recommendation
    })