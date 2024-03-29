from __future__ import print_function
import re
import os
import django
from django.db import transaction
from google_auth_httplib2 import Request

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mailtrac.settings")
django.setup()
from celery import shared_task
import google
import base64
from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.models import User
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import easypost
from track.models import tracker as tr
easypost.api_key = ''


@shared_task
def scan(token, token_secret):

    creds = None

    creds = google.oauth2.credentials.Credentials(
        client_id='',
        client_secret='',
        refresh_token=token_secret,
        scopes={
            'profile',
            'email',
            'https://www.googleapis.com/auth/gmail.modify'
        },
        token=token,
        token_uri="https://oauth2.googleapis.com/token",
    )

    if not creds.valid:
        creds.refresh(Request())

    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)

    response = service.users().messages().list(userId='me', maxResults=15, q='tracking number').execute()

    messages = []

    if 'messages' in response:
        messages.extend(response['messages'])


    for message in messages:
        email_seach.delay(message, token, token_secret)



@shared_task
def email_seach(message, token, token_secret):


    user = SocialToken.objects.get(token_secret=token_secret).account.user

    number_found = False
    creds = None
    body = None

    fedex = re.compile(r'(\b96\d{20}\b)|(\b\d{15}\b)|(\b\d{12}\b)')
    usps = re.compile(r'(EA\d{9}US)|(9\d{15,21})')
    ups = re.compile(r'(1Z ?[0-9A-Z]{3} ?[0-9A-Z]{3} ?[0-9A-Z]{2} ?[0-9A-Z]{4} ?[0-9A-Z]{3} ?[0-9A-Z])')

    creds = google.oauth2.credentials.Credentials(
        client_id='',
        client_secret='',
        refresh_token=token_secret,
        scopes={
            'profile',
            'email',
            'https://www.googleapis.com/auth/gmail.modify'
        },
        token=token,
        token_uri="https://oauth2.googleapis.com/token",
    )

    if not creds.valid:
        creds.refresh(Request())

    service = build('gmail', 'v1', credentials=creds, cache_discovery=False)


    message_return = service.users().messages().get(userId='me', id=message['id']).execute()

    try:
        if message_return['payload']['parts'][0]['body']['data'] is not None:
            body = decode_base64(message_return)
    except:
        pass

    for headers in message_return['payload']['headers']:
        if headers['name'] == 'Subject':
            subject = str(headers['value'])

            if subject is not None:
                if number_found == False:
                    results = tracking_search(subject, fedex, usps, ups)
                    if results is not None:

                        result = createTracker(user, results['tracking_number'], results['carrier'], number_found)

                        print(result)

    if number_found == False:
        if body:
            results = tracking_search(body, fedex, usps, ups)
            if results is not None:
                result = createTracker(user, results['tracking_number'], results['carrier'], number_found)
                print(result)



def tracking_search(word, fedex, usps, ups):

    results = {}

    if fedex.search(word):
        match = fedex.search(word).groups()

        tracking_number = extract_num(match)

        results.update({'tracking_number': tracking_number})
        results.update({'carrier': 'FedEx'})
        return results

    if usps.search(word):
        match = usps.search(word).groups()

        tracking_number = extract_num(match)

        results.update({'tracking_number':tracking_number})
        results.update({'carrier':'USPS'})
        return results

    if ups.search(word):
        match = ups.search(word).groups()

        tracking_number = extract_num(match)

        results.update({'tracking_number': tracking_number})
        results.update({'carrier': 'UPS'})
        return results

def extract_num(match):
    for group in match:
        if group is not None:
            return str(group)


def decode_base64(msg):
    return base64.urlsafe_b64decode(msg['payload']['parts'][0]['body']['data'].encode("ASCII")).decode("utf-8")

@transaction.atomic
def createTracker(user, num, car, number_found):

    tracker_exists = tr.objects.all().filter(user=user, tracking_number=num)


    if not tracker_exists:
        try:
            tracker = easypost.Tracker.create(
                tracking_code=num,
                carrier=car
            ).to_dict()

            if tracker['status'] == 'unknown':
                error = '{} is too old'.format(num)
                return error
            else:

                track = tr(user=user, name='Feature is currently in testing', description='Automatically added shipment.',
                           tracking_number=num, carrier=car)
                track.save()
                number_found = True
                print('tracker created')
                return number_found

        except:
            pass
    else:
        error = 'tracker already exists'
        return error
