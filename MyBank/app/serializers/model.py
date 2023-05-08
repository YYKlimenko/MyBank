from django.contrib.auth import get_user_model  # type: ignore
from django.contrib.auth.hashers import make_password  # type: ignore
from rest_framework import serializers  # type: ignore

from app.models import Asset, Account, Property, AssetCategory


class AssetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Asset
        fields = ('name', 'description', 'value', 'category_id', 'user_id')


class AssetCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetCategory
        fields = ('name', 'verbose_name', 'description')


class CreatingUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ('password', 'password2', 'username', 'first_name', 'last_name', 'email')

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError("Passwords don't match")
        data['password'] = make_password(data['password'])
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_active')


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('id', 'name', 'count', 'user_id', 'asset_id')


class CreatingAccountSerializer(serializers.ModelSerializer):
    asset_id = serializers.CharField()
    user_id = serializers.IntegerField()

    class Meta:
        model = Account
        fields = ('id', 'name', 'count', 'user_id', 'asset_id')


class PropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('id', 'name', 'user_id', 'value', 'description')


class CreatingPropertySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Property
        fields = ('name', 'user_id', 'value', 'description')


class UpdatingPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('name', 'value', 'description')
