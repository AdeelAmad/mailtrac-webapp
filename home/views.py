import collections

from django.shortcuts import render

# Create your views here.
from users import models
from payments import models as pmodels
import stripe
from twilio.rest import Client

stripe.api_key = ""
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


def home(request):
    return render(request, 'home/home.html')

def pricing(request):
    return render(request, 'home/pricing.html')

def privacy(request):
    return render(request, 'home/privacy.html')

def howwork(request):
    return render(request, 'home/how.html')

def updates(request):
    return render(request, 'home/updates.html')

def notready(request):
    return render(request, 'home/not.html')

def billing(request):


    # Invoice lists
    invoices = []
    invoiceElement = collections.namedtuple('invoiceElement', ['number', 'amount', 'status', 'date', 'link', 'badge'])

    user = request.user
    profile = models.profile.objects.get(user=user)

    cus_id = profile.cus_id

    cancel = False
    if profile.current_plan == "Unlimited":
        cancel = True

    try:
        customer_method = stripe.Customer.retrieve(cus_id).to_dict()['invoice_settings']['default_payment_method']

        pay_meth = stripe.PaymentMethod.retrieve(customer_method).to_dict()['card']['last4']

        brand = pay_meth['card']['brand']

        if brand == 'visa':
            brand = 'Visa'


        for invoice in stripe.Invoice.list(customer = cus_id).to_dict()['data']:

            amount = '${}.{}'.format(str(invoice['amount_due'])[0], str(invoice['amount_due'])[1:])
            status = invoice['status']

            if status == 'paid':
                badge = 'success'
            if status == 'open':
                badge = 'info'
            if status == 'draft':
                badge = 'secondary'
            if status == 'uncollectible':
                badge = 'warning'
            if status == 'void':
                badge = 'danger'

            invoices.append(invoiceElement(invoice['number'], amount, status, invoice['created'], invoice['hosted_invoice_url'], badge))

            print(invoice['number'], amount, invoice['status'], invoice['created'], invoice['hosted_invoice_url'], badge)
    except:
        brand = ""
        pay_meth = ""
        invoices = ""


    context = {
        'plan': profile.current_plan,
        'brand': brand,
        'last4': pay_meth,
        'invoices': invoices,
        'cancel': cancel
    }

    return render(request, 'home/billing.html', context)
