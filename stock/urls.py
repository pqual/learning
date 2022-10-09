from django.urls import path

from stock.views import (
    stock_list, stock_detail, stock_buy,
    account, acc_stock, stock_sell
)


urlpatterns = [
    path("list/", stock_list, name="list"),
    path("account/", account, name="account"),
    path("detail/<int:pk>/", stock_detail, name="detail"),
    path("buy/<int:pk>/", stock_buy, name="buy"),
    path("acc_stock/<int:pk>/", acc_stock, name="acc_stock"),
    path("sell/<int:pk>/", stock_sell, name="sell")
]