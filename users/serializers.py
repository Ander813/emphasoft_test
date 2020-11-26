from django.contrib.auth.models import User
from rest_framework import serializers


class ReadOnlyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'is_active', 'last_login', 'is_superuser')


class WriteOnlyUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'is_active')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.set_password(password)
        instance.save()

        return instance
