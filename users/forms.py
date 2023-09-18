from django.contrib.auth.forms import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField
from twilio.rest import Client
from .models import profile

account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
from users.models import profile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    phonenumber = forms.CharField(max_length=12)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phonenumber']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already registered to another account.")
        return email

    def clean_phonenumber(self):
        def lookup(phonenumber):
            if profile.objects.filter(phonenumber=phonenumber).exists():
                raise ValidationError('Phone number is already registered to another account.')
            print(phonenumber)
            try:
                client.lookups.phone_numbers(phonenumber)
            except:
                raise ValidationError('Phone number is invalid')
            return phonenumber

        phonenumber = self.cleaned_data["phonenumber"]
        if phonenumber.isdigit():
            if len(phonenumber) == 10:
                phonenumber = "+1{}".format(phonenumber)
                lookup(phonenumber)
            else:
                raise ValidationError('Phone number is invalid')
        elif len(phonenumber) == 11 and phonenumber[0] == "1":
            phonenumber = "+{}".format(phonenumber)
            lookup(phonenumber)
        elif len(phonenumber) == 12 and phonenumber[0:1] == "+1":
            phonenumber = phonenumber
            lookup(phonenumber)
        else:
            raise ValidationError('Phone number is invalid')
        return phonenumber


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

# class ProfileUpdateForm(forms.ModelForm):
#
#     class Meta:
#         model = profile
#         fields = ['cus_id']
