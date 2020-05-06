import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from mailtrac import settings
from users import models
from . import models as pmods

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = 'whsec_ltFQE1US2SRRLoJu1G1KvtZ6re3UDtCB'


def handle_checkout_session(session):
    cus_is = session["customer"]

    user_profile = models.profile.objects.get(cus_id=cus_is)

    product = session['display_items'][0]['custom']['name']

    print(product)

    tracks = user_profile.tracks

    if product == "10 tracks":
        user_profile.tracks = user_profile.tracks + 10

    if product == "25 tracks":
        user_profile.tracks = user_profile.tracks + 25

    if product == "65 tracks":
        user_profile.tracks = user_profile.tracks + 65

    user_profile.save()
    print(user_profile.tracks)



@csrf_exempt
def hook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Fulfill the purchase...
        handle_checkout_session(session)

    return HttpResponse(status=200)


def charge(request):
    package = int(request.GET.get('p'))

    user = request.user
    profile_model = models.profile
    profile = profile_model.objects.get(user=user)


    if package == 65:
        name = "65 tracks"
        amount = 500
    if package == 25:
        name = "25 tracks"
        amount = 250
    if package == 10:
        name = "10 tracks"
        amount = 100

    session = stripe.checkout.Session.create(
        customer = profile.cus_id,
        payment_method_types=['card'],
        line_items=[{
            'name': name,
            'amount': amount,
            'currency': 'usd',
            'quantity': 1,
        }],
        success_url='https://mailtracc.com/accounts/billing',
        cancel_url='https://mailtracc.com/accounts/billing',
    )
    return render(request, "payments/charge.html", context={"CHECKOUT_SESSION_ID": session.id})

# Subscription System (To release with full release)
# @login_required
# def bill(request):
#
#     if request.method == 'POST':
#
#         # get how user pays
#         user = request.user
#         payment_method = json.loads(request.body)['result']['paymentMethod']['id']
#
#         # get what product to bill for
#         print(json.loads(request.body)['plan'])
#
#         # get product data
#         membership_plan = pmods.membership.objects.get(membership_type=json.loads(request.body)['plan'])
#
#         #get user profile
#         profile_model = models.profile
#         query = profile_model.objects.get(user=user)
#
#         # check if user already has customer id
#         if query.cus_id[0:3] != 'cus':
#             customer = stripe.Customer.create(
#                 payment_method=payment_method,
#                 email=user.email,
#                 invoice_settings={
#                     'default_payment_method': payment_method,
#                 },
#             ).to_dict()
#
#
#             # put customer id into profile and save
#             new_cus_id = customer.get('id')
#
#             query.cus_id = new_cus_id
#             query.save()
#
#
#
#
#
#         #generate subscription
#         subscription = stripe.Subscription.create(
#             customer=query.cus_id,
#             items=[
#                 {
#                     'plan': membership_plan.stripe_plan_id,
#                 },
#             ],
#             expand=['latest_invoice.payment_intent'],
#         ).to_dict()
#
#         # Create subscription object for record / cancellations
#         subcription_model = pmods.subscription(sub_id=subscription['id'], active=True, membership=membership_plan)
#         subcription_model.save()
#
#         subcription_model.user.add(user)
#         subcription_model.save()
#
#
#         #update user profile with membership
#         query.current_plan = membership_plan
#         query.unlimited = True
#         query.save()
#
#         return redirect('billing')
#     else:
#         return redirect('/')
#
# def cancelSub(request):
#     if request.method == 'POST':
#
#         user = request.user
#         profile = models.profile.objects.get(user=user)
#         subscribtion = pmods.subscription.objects.get(user=user, active=True)
#
#         updated = stripe.Subscription.modify(
#             subscribtion.sub_id,
#             cancel_at_period_end = True
#         )
#
#         profile.current_plan = pmods.membership.objects.get(membership_type = 'Basic')
#         profile.unlimited = False
#
#         subscribtion.end_date = timezone.now()
#         subscribtion.active = False
#         subscribtion.save()
#
#         profile.save()
#
#         return redirect('billing')
#     else:
#         return redirect('/')
