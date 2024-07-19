from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import TransferForm, DepositForm
from .models import UserProfile, Transaction
from django.db import transaction as db_transaction

@login_required
def home(request):
    user_profile = UserProfile.objects.get(user=request.user)
    transactions = user_profile.user.transaction_set.all()
    return render(request, 'bankapp/home.html', {'user_profile': user_profile, 'transactions': transactions})

@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            recipient_username = form.cleaned_data['recipient_username']
            
            try:
                recipient = User.objects.get(username=recipient_username)
            except User.DoesNotExist:
                form.add_error('recipient_username', 'Пользователь не найден')
                return render(request, 'bankapp/transfer.html', {'form': form})

            sender_profile = UserProfile.objects.get(user=request.user)
            recipient_profile = UserProfile.objects.get(user=recipient)

            if sender_profile.balance >= amount:
                with db_transaction.atomic():
                    sender_profile.balance -= amount
                    recipient_profile.balance += amount
                    sender_profile.save()
                    recipient_profile.save()

                    # Создание транзакций для записи операции
                    Transaction.objects.create(user=request.user, recipient=recipient, amount=-amount)
                    Transaction.objects.create(user=recipient, recipient=request.user, amount=amount)

                return redirect('home')
            else:
                form.add_error('amount', 'Недостаточно средств на счете')
    else:
        form = TransferForm()

    return render(request, 'bankapp/transfer.html', {'form': form})

@login_required
def deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_profile = UserProfile.objects.get(user=request.user)
            with db_transaction.atomic():
                user_profile.balance += amount
                user_profile.save()

                # Создание транзакции для записи операции
                Transaction.objects.create(user=request.user, amount=amount, recipient=None)

            return redirect('home')  # Перенаправление на домашнюю страницу после пополнения
    else:
        form = DepositForm()

    context = {
        'form': form,
    }
    return render(request, 'bankapp/deposit.html', context)