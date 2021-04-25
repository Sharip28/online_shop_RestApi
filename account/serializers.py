from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, required=True)
    password_confirmation = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with given email does not exist')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        user = get_object_or_404(MyUser, email=email)
        password = attrs.get('password')
        password_confirmation = attrs.get('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        password = data.get('password')
        try:
            user = MyUser.objects.get(email=email, is_active=True)
        except:
            raise serializers.ValidationError('User not found')
        user.set_password(password)
        user.save()
        return user