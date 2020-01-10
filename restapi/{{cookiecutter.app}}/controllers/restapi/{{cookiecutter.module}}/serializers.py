from rest_framework import serializers

from {{cookiecutter.app}}.models.{{cookiecutter.module}} import {{cookiecutter.model}} as Master


class {{cookiecutter.model}}PublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )

class {{cookiecutter.model}}PrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )

class {{cookiecutter.model}}PrivateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )

class {{cookiecutter.model}}PrivateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'id',
        )