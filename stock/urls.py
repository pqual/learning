from django.urls import path

from stock.views import stock_list, stock_detail, stock_buy, account


urlpatterns = [
    path("list/", stock_list, name="list"),
    path("account/", account, name="account"),
    path("detail/<int:pk>/", stock_detail, name="detail"),
    path("buy/<int:pk>/", stock_buy, name="buy")
]