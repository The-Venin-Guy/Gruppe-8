from django import forms
from .models import Asset, Stock, CashAccount

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'purchase_value', 'current_value', 'currency', 'purchase_date', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class AssetEditForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'purchase_value', 'current_value', 'currency', 'purchase_date', 'notes']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class AssetSellForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['sale_price', 'sale_date']
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sale_price'].required = True
        self.fields['sale_date'].required = True

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker', 'company_name', 'shares', 'purchase_price', 'purchase_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class StockEditForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['ticker', 'company_name', 'shares', 'purchase_price', 'purchase_date']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

class StockSellForm(forms.ModelForm):
    convert_to_cash = forms.BooleanField(required=False, label='Convert proceeds to cash account?')
    cash_account = forms.ModelChoiceField(queryset=CashAccount.objects.none(), required=False, label='Select cash account')

    class Meta:
        model = Stock
        fields = ['sale_price', 'sale_date']
        widgets = {
            'sale_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cash_account'].queryset = CashAccount.objects.filter(user=user)
        self.fields['sale_price'].required = True
        self.fields['sale_date'].required = True

class CashAccountForm(forms.ModelForm):
    class Meta:
        model = CashAccount
        fields = ['account_name', 'balance', 'currency']