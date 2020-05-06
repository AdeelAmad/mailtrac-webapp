from allauth.account.views import AjaxCapableProcessFormViewMixin
from allauth.socialaccount.forms import DisconnectForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as dlog
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import FormView
from twilio.rest import Client
from users.tokens import account_activation_token
from . import models
import stripe
from sentry_sdk import last_event_id
from .forms import SignUpForm, UserUpdateForm

stripe.api_key = "sk_test_3wr5teXSikqaAdP42VYJiERm"
account_sid = 'AC0d8c64f616fe81480e93a4b3f17f27f7'
auth_token = 'da712819ec5328e2d9b6d09c4d3fb29b'
client = Client(account_sid, auth_token)

def prsent(request):
    messages.success(request, "Your password reset link has been sent. Check your email for it.")
    return redirect('login')

def prcomplete(request):
    messages.success(request, "Your password has been reseted successfully.")
    return redirect('login')



@login_required
def logout(request):
    dlog(request)
    messages.info(request, "You are now logged out.")
    return redirect('login')

@transaction.atomic
def register(request):

    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            user = form.save()
            user.refresh_from_db()
            user.profile.phonenumber = form.cleaned_data.get('phonenumber')

            customer = stripe.Customer.create(
                email = form.cleaned_data.get('email')
            )

            user.profile.cus_id = customer["id"]

            # user.is_active = False
            user.save()


            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            messages.success(request, f'Account created for {username}!')




            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('activation_sent')
    else:

        form = SignUpForm()

    return render(request, 'users/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'users/activation_invalid.html')

@login_required
def activation_sent_view(request):

    if request.method == "POST":

        user = request.user
        profile = models.profile.objects.get(user=user)
        phonenumber = profile.phonenumber
        code = '{}{}{}{}{}{}'.format(request.POST['1'], request.POST['2'], request.POST['3'], request.POST['4'], request.POST['5'], request.POST['6'])

        try:

            verification_check = client.verify \
                .services('VAdd3709671c61d204fc5847f31e039f77') \
                .verification_checks \
                .create(to=phonenumber, code=code)


            if verification_check.status != "approved":
                messages.warning(request, "Incorrect code. It has been resent to you.")
                return redirect('activation_sent')
            else:
                profile.signup_confirmation = True
                profile.save()
                messages.success(request, "Your account has been verified.")
                return redirect('profile')
        except:
            messages.warning(request, "An error occured. Please try again in a few minutes.")

    else:
        user = request.user
        profile = models.profile.objects.get(user=user)
        phonenumber = profile.phonenumber

        if profile.signup_confirmation == False:

            verification = client.verify \
                .services('VAdd3709671c61d204fc5847f31e039f77') \
                .verifications \
                .create(to=phonenumber, channel='sms')



            return render(request, 'users/activation_sent.html')

        else:
            return redirect('dashboard')











def login_user(request):
    print(UserCreationForm(request.POST))
    return render(request, 'users/login.html')
    # logout(request)
    # username = password = ''
    # if request.POST:
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #
    #     user = authenticate(username=username, password=password)
    #     if user is not None:
    #         if user.is_active:
    #             login(request, user)
    #             return HttpResponseRedirect('/main/')
    # return render_to_response('users/login.html', context_instance=RequestContext(request))








@transaction.atomic
@login_required
def profile(request):

    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid():

            u_form.save()
            # p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:

        u_form = UserUpdateForm(instance=request.user)
        # p_form = ProfileUpdateForm(instance=request.user.profile)

    user = request.user
    profile = models.profile.objects.get(user=user)

    context = {
        'u_form': u_form,
        'profile': profile,
        'user': user
    }

    return render(request, 'users/profile.html', context)

def handler500(request, *args, **argv):
    return render(request, "users/500.html", {
        'sentry_event_id': last_event_id(),
    }, status=500)