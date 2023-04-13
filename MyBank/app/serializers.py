from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.models import Asset, Account, Property


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ('name', 'value')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'name', 'count', 'user_id', 'currency_id')


class CreatingAccountSerializer(serializers.ModelSerializer):
    currency_id = serializers.CharField(source='currency')
    user_id = serializers.IntegerField(source='user')

    class Meta:
        model = Account
        fields = ('id', 'name', 'count', 'user_id', 'currency_id')


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'name', 'user_id', 'value', 'description')


class CreatingPropertySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user')

    class Meta:
        model = Property
        fields = ('name', 'user_id', 'value', 'description')
