from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    ASSET_TYPES = [
        ('real_estate', 'Real Estate'),
        ('vehicle', 'Vehicle'),
        ('land', 'Land'),
        ('other', 'Other'),
    ]
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('NGN', 'Nigerian Naira'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    purchase_value = models.DecimalField(max_digits=15, decimal_places=2)
    current_value = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    purchase_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sale_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def appreciation(self):
        return self.current_value - self.purchase_value

    def appreciation_percent(self):
        if self.purchase_value > 0:
            return ((self.current_value - self.purchase_value) / self.purchase_value) * 100
        return 0

    def profit_loss(self):
        if self.sale_price:
            return self.sale_price - self.purchase_value
        return None

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Stock(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    company_name = models.CharField(max_length=200)
    shares = models.DecimalField(max_digits=15, decimal_places=4)
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sale_date = models.DateField(null=True, blank=True)
    sale_converted_to_cash = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_invested(self):
        return self.shares * self.purchase_price

    def profit_loss(self):
        if self.sale_price:
            return (self.sale_price - self.purchase_price) * self.shares
        return None

    def __str__(self):
        return f"{self.ticker} - {self.shares} shares ({self.user.username})"


class CashAccount(models.Model):
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('NGN', 'Nigerian Naira'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=200)
    balance = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='NGN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_name} - {self.balance} {self.currency} ({self.user.username})"
    
class PortfolioSnapshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    net_worth = models.DecimalField(max_digits=15, decimal_places=2)
    total_assets = models.DecimalField(max_digits=15, decimal_places=2)
    total_stocks = models.DecimalField(max_digits=15, decimal_places=2)
    total_cash = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')

    class Meta:
        unique_together = ['user', 'date', 'currency']
        ordering = ['date']

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.net_worth}"