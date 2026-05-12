from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from portfolio.models import Asset, Stock, CashAccount
import yfinance as yf
from decimal import Decimal
from portfolio.utils import convert_currency
import plotly.graph_objects as go
import plotly.utils
import json
from news.utils import fetch_financial_news, get_ai_recommendations, analyse_sentiment
from django.core.cache import cache
import markdown
from portfolio.models import Asset, Stock, CashAccount, PortfolioSnapshot
from datetime import date

@login_required
def dashboard_view(request):
    active_assets = Asset.objects.filter(user=request.user, status='active')
    accounts = CashAccount.objects.filter(user=request.user)
    active_stocks = Stock.objects.filter(user=request.user, status='active')
    display_currency = request.GET.get('currency', 'NGN')
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

    #portfolio snapshot. update or create will create a list of objects everyday
    PortfolioSnapshot.objects.update_or_create(
        user=request.user,
        date=date.today(),
        currency=display_currency,
        defaults={
            'net_worth': net_worth,
            'total_assets': total_assets,
            'total_stocks': total_stock,
            'total_cash': total_cash,
        }
    )

    snapshots = PortfolioSnapshot.objects.filter(user=request.user, currency=display_currency)
    if snapshots.count() > 1:
        snap_dates = [str(s.date) for s in snapshots]
        snap_values = [float(s.net_worth) for s in snapshots]

        line_fig = go.Figure()
        line_fig.add_trace(go.Scatter(
            x=snap_dates,
            y=snap_values,
            mode='lines',
            fill='tozeroy',
            name='Net Worth',
            line=dict(color='#a8e63d', width=2),
            fillcolor='rgba(168, 230, 61, 0.1)'
        ))
        line_fig.update_layout(
            paper_bgcolor='#1b1e20',
            plot_bgcolor='#1b1e20',
            font=dict(color='#ffffff'),
            margin=dict(l=40, r=20, t=30, b=40),
            xaxis=dict(gridcolor='#2c3034'),
            yaxis=dict(gridcolor='#2c3034'),
        )
        portfolio_line_json = json.dumps(line_fig, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        portfolio_line_json = None

    if any([total_assets, total_stock, total_cash]):
        fig = go.Figure(data=[go.Pie(
            labels=['Assets', 'Stocks', 'Cash'],
            values=[total_assets, total_stock, total_cash]
        )])
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graph_json=None

    cache_key = f'news_ai_{request.user.id}'
    cached_data = cache.get(cache_key)

    if cached_data:
        news_articles = cached_data['news_articles']
        ai_recommendation = cached_data['ai_recommendation']
    else:
        news_articles = fetch_financial_news()
        ai_recommendation = get_ai_recommendations(news_articles)
        cache.set(cache_key, {
            'news_articles': news_articles,
            'ai_recommendation': ai_recommendation,
        }, timeout=86400)  # 86400 seconds = 24 hours

    ai_recommendation = markdown.markdown(ai_recommendation)
    news_articles, overall_label = analyse_sentiment(news_articles)

    return render(request, 'dashboard/dashboard.html', {
        'user': request.user,
        'total_assets' : total_assets, 
        'total_cash' : total_cash, 
        'total_stock' : total_stock,
        'net_worth' : net_worth,
        'display_currency': display_currency,
        'currency_symbol' : currency_symbol,
        'graph_json': graph_json,
        'portfolio_line_json': portfolio_line_json,
        'news_articles': news_articles,
        'ai_recommendation': ai_recommendation,
    })