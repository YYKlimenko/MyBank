from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Account, Currency


class CurrencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Currency
        fields = ('name', 'value')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')


class AccountSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = Account
        fields = ('id', 'name', 'count', 'user_id', 'currency')


class CreatingAccountSerializer(serializers.ModelSerializer):
    currency_name = serializers.CharField(source='currency')
    user_id = serializers.IntegerField(source='user')

    class Meta:
        model = Account
        fields = ('id', 'name', 'count', 'user_id', 'currency_name')


class QuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()