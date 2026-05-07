from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Asset, Stock, CashAccount
from .forms import (AssetForm, AssetEditForm, AssetSellForm,
                    StockForm, StockEditForm, StockSellForm, CashAccountForm)
import yfinance as yf
from django.http import JsonResponse

# ── Assets ──────────────────────────────────────────
@login_required
def asset_list(request):
    active_assets = Asset.objects.filter(user=request.user, status='active')
    sold_assets = Asset.objects.filter(user=request.user, status='sold')
    return render(request, 'portfolio/asset_list.html', {
        'assets': active_assets,
        'sold_assets': sold_assets
    })

@login_required
def asset_add(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.save()
            messages.success(request, 'Asset added successfully!')
            return redirect('portfolio:asset_list')
    else:
        form = AssetForm()
    return render(request, 'portfolio/asset_form.html', {'form': form, 'title': 'Add Asset'})

@login_required
def asset_edit(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssetEditForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asset updated successfully!')
            return redirect('portfolio:asset_list')
    else:
        form = AssetEditForm(instance=asset)
    return render(request, 'portfolio/asset_form.html', {'form': form, 'title': 'Edit Asset'})

@login_required
def asset_sell(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AssetSellForm(request.POST, instance=asset)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.status = 'sold'
            asset.save()
            messages.success(request, f'{asset.name} marked as sold!')
            return redirect('portfolio:asset_list')
    else:
        form = AssetSellForm(instance=asset)
    return render(request, 'portfolio/sell_form.html', {
        'form': form,
        'title': f'Sell {asset.name}',
        'item_name': asset.name,
        'back_url': '/portfolio/assets/'
    })

@login_required
def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)
    asset.delete()
    messages.success(request, 'Asset deleted.')
    return redirect('portfolio:asset_list')


# ── Stocks ──────────────────────────────────────────
@login_required
def stock_list(request):
    active_stocks = Stock.objects.filter(user=request.user, status='active')
    sold_stocks = Stock.objects.filter(user=request.user, status='sold')
    stock_data = []
    for stock in active_stocks:
        try:
            ticker = yf.Ticker(stock.ticker)
            current_price = ticker.fast_info['lastPrice']
            current_value = current_price * float(stock.shares)
            gain_loss = current_value - float(stock.total_invested())
            gain_loss_percent = (gain_loss / float(stock.total_invested())) * 100
        except:
            current_price = None
            current_value = None
            gain_loss = None
            gain_loss_percent = None
        stock_data.append({
            'stock': stock,
            'current_price': current_price,
            'current_value': current_value,
            'gain_loss': gain_loss,
            'gain_loss_percent': gain_loss_percent,
        })
    return render(request, 'portfolio/stock_list.html', {
        'stock_data': stock_data,
        'sold_stocks': sold_stocks
    })

@login_required
def stock_add(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.user = request.user
            stock.save()
            messages.success(request, f'{stock.ticker} added to your portfolio!')
            return redirect('portfolio:stock_list')
    else:
        form = StockForm()
    return render(request, 'portfolio/stock_form.html', {'form': form, 'title': 'Add Stock'})

@login_required
def stock_edit(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StockEditForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock updated successfully!')
            return redirect('portfolio:stock_list')
    else:
        form = StockEditForm(instance=stock)
    return render(request, 'portfolio/stock_form.html', {'form': form, 'title': 'Edit Stock'})

@login_required
def stock_sell(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StockSellForm(request.user, request.POST, instance=stock)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.status = 'sold'
            convert = form.cleaned_data.get('convert_to_cash')
            cash_account = form.cleaned_data.get('cash_account')
            if convert and cash_account:
                proceeds = stock.sale_price * stock.shares
                cash_account.balance += proceeds
                cash_account.save()
                stock.sale_converted_to_cash = True
                messages.success(request, f'Sale proceeds of {proceeds} added to {cash_account.account_name}!')
            stock.save()
            messages.success(request, f'{stock.ticker} marked as sold!')
            return redirect('portfolio:stock_list')
    else:
        form = StockSellForm(request.user, instance=stock)
    return render(request, 'portfolio/sell_form.html', {
        'form': form,
        'title': f'Sell {stock.ticker}',
        'item_name': stock.ticker,
        'back_url': '/portfolio/stocks/',
        'is_stock': True
    })

@login_required
def stock_delete(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    stock.delete()
    messages.success(request, 'Stock removed.')
    return redirect('portfolio:stock_list')


# ── Cash ──────────────────────────────────────────
@login_required
def cash_list(request):
    accounts = CashAccount.objects.filter(user=request.user)
    return render(request, 'portfolio/cash_list.html', {'accounts': accounts})

@login_required
def cash_add(request):
    if request.method == 'POST':
        form = CashAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Cash account added!')
            return redirect('portfolio:cash_list')
    else:
        form = CashAccountForm()
    return render(request, 'portfolio/cash_form.html', {'form': form, 'title': 'Add Cash Account'})

@login_required
def cash_edit(request, pk):
    account = get_object_or_404(CashAccount, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CashAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated!')
            return redirect('portfolio:cash_list')
    else:
        form = CashAccountForm(instance=account)
    return render(request, 'portfolio/cash_form.html', {'form': form, 'title': 'Edit Cash Account'})

@login_required
def cash_delete(request, pk):
    account = get_object_or_404(CashAccount, pk=pk, user=request.user)
    account.delete()
    messages.success(request, 'Account removed.')
    return redirect('portfolio:cash_list')

def ticker_search(request):
    query = request.GET.get('q', '')
    if len(query) < 1:
        return JsonResponse([], safe=False)
    try:
        ticker = yf.Search(query, max_results=6)
        results = []
        for item in ticker.quotes:
            if 'symbol' in item and 'longname' in item or 'shortname' in item:
                results.append({
                    'ticker': item.get('symbol', ''),
                    'name': item.get('longname') or item.get('shortname', ''),
                })
        return JsonResponse(results, safe=False)
    except:
        return JsonResponse([], safe=False)