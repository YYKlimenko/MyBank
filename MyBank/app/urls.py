from .views import CurrencyView, AccountView, UserView, count_sum, PropertyView
from django.urls import path

urlpatterns = [
    path('api/v1/accounts/', AccountView.as_view()),

    path('api/v1/users/', UserView.as_view()),

    path('api/v1/sum/<int:user_id>/', count_sum),

    path('api/v1/currencies/', CurrencyView.as_view()),

    path('api/v1/properties/', PropertyView.as_view()),



]
