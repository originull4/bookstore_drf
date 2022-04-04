from django.contrib.auth.hashers import make_password
from rest_framework.serializers import (CharField, HyperlinkedIdentityField,
                                        ModelSerializer, ValidationError)

from .models import Account


class AccountSerializer(ModelSerializer):
    user_detail_url = HyperlinkedIdentityField(view_name='account-detail', read_only=True, lookup_field='id')

    class Meta:
        model = Account
        exclude = ('groups', 'user_permissions', 'password',)


class AccountUpdateSerializer(ModelSerializer):
    username = CharField(required=False)

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar', 'gender')

    def validate_username(self, value):
        if Account.objects.filter(username=value).exists():
            raise ValidationError('an account with this username already exists')
        return value

    def validate_email(self, value):
        lower_email = value.lower()
        if Account.objects.filter(email__iexact=lower_email).exists():
            raise ValidationError('an account with this email already exists')
        return lower_email


class AccountCreateSerializer(ModelSerializer):
    password = CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        account = Account(**validated_data)
        account.is_staff = True
        account.save()
        return account

    def validate_password(self, value):
        if len(value) < 6:
            raise ValidationError('password must be more than 6 character.')
        return make_password(value)
        
    def validate_email(self, value):
        lower_email = value.lower()
        if Account.objects.filter(email__iexact=lower_email).exists():
            raise ValidationError('an account with this email already exists')
        return lower_email


class PasswordChangeSerializer(ModelSerializer):
    old_password = CharField(write_only=True, required=True)
    password1 = CharField(write_only=True, required=True)
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = Account
        fields = ('old_password', 'password1', 'password2')

    def validate_old_password(self, value):
        account = self.context['request'].user
        if not account.check_password(value):
            raise ValidationError("Old password is not correct")
        return value

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError({"password": "password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password1'])
        instance.save()
        return instance

