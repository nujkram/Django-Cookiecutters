from rest_framework import serializers
from accounts.models import Account as Master


class AccountPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'username',
        )


class AccountPublicCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'email',
            'username',
            'password',
        )


class LoginWithCredentialsSerializer(serializers.Serializer):
    class Meta:
        fields = (
            'email',
            'password'
        )
