from django import forms

class TransferForm(forms.Form):
    recipient_username = forms.CharField(label='Имя получателя', max_length=100)
    amount = forms.DecimalField(label='Сумма перевода', max_digits=10, decimal_places=2)

class DepositForm(forms.Form):
    amount = forms.DecimalField(label='Сумма пополнения', max_digits=10, decimal_places=2)