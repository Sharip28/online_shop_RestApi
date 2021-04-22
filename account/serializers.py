from django.contrib.auth import authenticate
from rest_framework import serializers

from account.models import MyUser
from account.utils import send_activation_email


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6,write_only=True)
    password_confirmation = serializers.CharField(min_length=6,write_only=True)


    class Meta:
        model = MyUser
        fields = ('email','password','password_confirmation')

    def validate_email(self,email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('user already  exists')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Password do no match')
        return attrs

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = MyUser.objects.create_user(email=email,password=password)

        send_activation_email(email=email,
                              activation_code=user.activation_code)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self,attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email,password=password)
            if not user:
                message = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(message,code='authorisation')
        else:
            message = 'must include "email" and "password"'
            raise serializers.ValidationError(message, code='authorisation')

        attrs['user'] = user
        return attrs
