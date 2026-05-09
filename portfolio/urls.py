from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/add/', views.asset_add, name='asset_add'),
    path('assets/edit/<int:pk>/', views.asset_edit, name='asset_edit'),
    path('assets/sell/<int:pk>/', views.asset_sell, name='asset_sell'),
    path('assets/delete/<int:pk>/', views.asset_delete, name='asset_delete'),
    path('stocks/', views.stock_list, name='stock_list'),
    path('stocks/add/', views.stock_add, name='stock_add'),
    path('stocks/edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('stocks/sell/<int:pk>/', views.stock_sell, name='stock_sell'),
    path('stocks/delete/<int:pk>/', views.stock_delete, name='stock_delete'),
    path('cash/', views.cash_list, name='cash_list'),
    path('cash/add/', views.cash_add, name='cash_add'),
    path('cash/edit/<int:pk>/', views.cash_edit, name='cash_edit'),
    path('cash/delete/<int:pk>/', views.cash_delete, name='cash_delete'),
    path('ticker-search/', views.ticker_search, name='ticker_search'),
    path('stocks/<int:pk>/', views.stock_detail, name='stock_detail'),
]