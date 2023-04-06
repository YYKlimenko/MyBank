import abc

from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Account, Currency, Property


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


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'name', 'count', 'user_id', 'value', 'description')


class CreatingPropertySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user')

    class Meta:
        model = Account
        fields = ('name', 'count', 'user_id', 'value', 'description')


class QuerySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
