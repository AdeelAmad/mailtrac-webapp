from __future__ import print_function

import base64
import email

import google
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from googleapiclient import http as https
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.contrib import messages as dmes
from .tasks import scan as tscan


@login_required
def scan(request):

    user = request.user
    try:
        user_num = SocialAccount.objects.get(user=user).id
        social_token = SocialToken.objects.get(account=user_num)

        tscan.delay(social_token.token, social_token.token_secret)

        dmes.success(request, 'Your email is now being scanned')
        return redirect('dashboard')

    except:
        dmes.warning(request, 'You need to link your account to gmail first!')
        return redirect('profile')

def refresh_token(request):
    pass