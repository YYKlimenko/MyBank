from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from app.models import Asset, Account, Property


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ('name', 'value')


class CreatingUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('password', 'username', 'first_name', 'last_name', 'email')

    def validate_password(self, value: str) -> str:
        return make_password(value)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active')


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'name', 'count', 'user_id', 'asset_id')


class CreatingAccountSerializer(serializers.ModelSerializer):
    asset_id = serializers.CharField(source='asset')
    user_id = serializers.IntegerField(source='user')

    class Meta:
        model = Account
        fields = ('id', 'name', 'count', 'user_id', 'asset_id')


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'name', 'user_id', 'value', 'description')


class CreatingPropertySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user')

    class Meta:
        model = Property
        fields = ('name', 'user_id', 'value', 'description')
