from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from stock.models import Stock, AccountCurrency, AccountStock
from stock.forms import BuySellForm

# Create your views here.
def stock_list(request):
    stocks = Stock.objects.all()
    context = {
        "stocks": stocks,
    }
    return render(request, "stocks.html", context)

@login_required
def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    context = {
        "stock": stock,
        "form": BuySellForm(initial={"price":stock.get_random_price()})
    }
    return render(request, "stock.html", context)

@login_required
def stock_buy(request, pk):
    if request.method != "POST":
        return redirect("stock:detail", pk=pk)

    stock = get_object_or_404(Stock, pk=pk)
    form = BuySellForm(request.POST)

    if form.is_valid():
        amount = form.cleaned_data["amount"]
        price = form.cleaned_data["price"]
        buy_cost = price * amount

        acc_stock, created = AccountStock.objects.get_or_create(
            account=request.user.account, stock=stock,
            defaults={"average_buy_cost":0,"amount":0}
        )
        current_cost = acc_stock.average_buy_cost * acc_stock.amount

        total_cost = current_cost + buy_cost
        total_amount = acc_stock.amount + amount

        acc_stock.amount = total_amount
        acc_stock.average_buy_cost = total_cost / total_amount

        acc_currency, created = AccountCurrency.objects.get_or_create(
            account=request.user.account, currency=stock.currency,
            defaults={"amount":0}
        )

        if acc_currency.amount < buy_cost:
            form.add_error(
                None,
                f"На счёте недостаточно средств в валюте {stock.currency.sign}"
            )
        else:
            acc_currency.amount = acc_currency.amount - buy_cost
            acc_stock.save()
            acc_currency.save()
            return redirect("stock:list")

    context = {
        "stock": get_object_or_404(Stock, pk=pk),
        "form": form
    }

    return render(request, "stock.html", context)

@login_required
def account(request):
    currencies = cache.get(f"currencies_{request.user.username}")
    stocks = cache.get(f"stocks_{request.user.username}")

    if currencies is None:
        print(currencies)
        currencies = [
            {
                "name": acc_currency.currency.name,
                "amount": acc_currency.amount,
                "sign": acc_currency.currency.sign
            } for acc_currency in request.user.account.accountcurrency_set.select_related("currency")
        ]
        cache.set(f"currencies_{request.user.username}", currencies, 300)

    if stocks is None:
        stocks = [
            {
                "pk": acc_stock.pk,
                "ticker": acc_stock.stock.ticker,
                "amount": acc_stock.amount,
                "avg": acc_stock.average_buy_cost,
                "currency": acc_stock.stock.currency.sign
            } for acc_stock in request.user.account.accountstock_set.select_related("stock").all()
        ]
        cache.set(f"stocks_{request.user.username}", stocks, 300)

    context = {
        "currencies": currencies,
        "stocks": stocks
    }

    return render(request, template_name="account.html", context=context)

@login_required
def acc_stock(request, pk):
    acc_stock = get_object_or_404(AccountStock, pk=pk)

    form = BuySellForm(max_count=acc_stock.amount, initial={"price":acc_stock.stock.get_random_price()})

    context = {
        "acc_stock": acc_stock,
        "form": form
    }

    return render(request, template_name="acc_stock.html", context=context)

@login_required
def stock_sell(request, pk):
    if request.method != "POST":
        return redirect("stock:acc_stock", pk=pk)

    acc_stock = get_object_or_404(AccountStock, pk=pk)
    form = BuySellForm(request.POST, max_count=acc_stock.amount)

    if form.is_valid():
        amount = form.cleaned_data["amount"]
        price = form.cleaned_data["price"]

        acc_currency, created = AccountCurrency.objects.get_or_create(
            account=request.user.account, currency=acc_stock.stock.currency,
            defaults={"amount":0}
        )

        sell_cost = price * amount
        total_amount = acc_stock.amount - amount

        acc_stock.amount = total_amount
        acc_currency.amount = acc_currency.amount + sell_cost

        acc_stock.save()
        acc_currency.save()
        return redirect("stock:account")

    context = {
        "acc_stock": acc_stock,
        "form": form
    }

    return render(request, template_name="acc_stock.html", context=context)