from .views import CurrencyView, AccountView, UserCRUDView, UserSumView, PropertyView
from django.urls import path

from .views.model import MoexStockView

urlpatterns = [
    path('api/v1/accounts/', AccountView.as_view()),

    path('api/v1/users/', UserCRUDView.as_view()),

    path('api/v1/sum/', UserSumView.as_view()),

    path('api/v1/currencies/', CurrencyView.as_view()),

    path('api/v1/moex_stocks/', MoexStockView.as_view()),

    path('api/v1/properties/', PropertyView.as_view()),
]
