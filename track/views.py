import collections
from datetime import datetime

import pytz
from geoip import geolite2
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from twilio.rest import Client
from django.contrib import messages
from .models import tracker
from users import models as umod
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
import easypost

easypost.api_key = " "
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class TrackerCreate(LoginRequiredMixin, CreateView):
    model = tracker
    fields = ['name', 'description', 'tracking_number', 'carrier']
    success_url = '/'


    @transaction.atomic
    def form_valid(self, form):
        user = self.request.user
        u_profile = umod.profile.objects.get(user=user)
        verified = umod.profile.objects.get(user=user).signup_confirmation

        if verified:
            form.instance.user = self.request.user
            self.object = form.save()

            if self.object.carrier != 'Other':
                tracker = easypost.Tracker.create(
                    tracking_code=self.object.tracking_number,
                    carrier=self.object.carrier
                )
            else:
                print('created without carrier')
                tracker = easypost.Tracker.create(
                    tracking_code=self.object.tracking_number
                )

            return redirect('tracker-detail', self.object.id)
        else:
            messages.warning(self.request, 'Please verify your account before adding a package')
            return redirect('profile')


class Dashboard(LoginRequiredMixin, ListView):
    template_name = 'track/dashboard.html'
    context_object_name = 'codes'

    def get_queryset(self):
        resultList = []

        dataElement = collections.namedtuple('dataElement',
                                             ['name', 'number', 'status', 'description', 'public_url', 'id', 'a', 'mute'])

        filter = self.request.GET.get('status')

        for o in tracker.objects.all().filter(user=self.request.user):
            if o.carrier != 'Other':
                ts = easypost.Tracker.all(
                    tracking_code=o.tracking_number,
                    carrier=o.carrier
                ).to_dict().get('trackers')
            else:
                ts = easypost.Tracker.all(
                    tracking_code=o.tracking_number
                ).to_dict().get('trackers')

            status = self.extratValue(ts, 'status', 'pending')
            url = self.extratValue(ts, 'public_url', 'http://google.com')
            display = 'a'
            mute = ''

            if status == 'pre_transit':
                status = 'Pre Shipment'
            if status == 'out_for_delivery':
                status = 'Out For Delivery'
            if status == 'return_to_sender':
                status = 'Return To Sender'
            if status == 'failure':
                status = 'Faliure'
            if status == 'unknown':
                status = 'Unknown'
                mute = 'text-muted'
                display = 'p'
            if status == 'in_transit':
                status = 'In Transit'
            if status == 'delivered':
                status = 'Delivered'
            if status == 'pending':
                status = 'Pending'
                mute = 'text-muted'
                display = 'p'

            if filter == None or status == filter:
                resultList.append(dataElement(o.name, o.tracking_number, status, o.description, url, o.id, display, mute))

        return resultList

    def extratValue(self, ts, key, defaultValue=None):
        return ts[0].get(key) if len(ts) > 0 else defaultValue


class DetailInfo(DetailView):
    model = tracker



    def get_context_data(self, **kwargs):

        # ip = get_client_ip(self.request)
        ip = '184.23.215.122'
        location = geolite2.lookup(ip)

        if location != None:
            time_zone = location.to_dict()['timezone']


        detailList = {}

        dataElement = collections.namedtuple('dataElement',
                                             ['est_deliv_date', 'status', 'carrier', 'tracking_number', 'name',
                                              'shipped', 'transit', 'delivery', 'delivered'])
        eventElement = collections.namedtuple('eventElement', ['message', 'location', 'date', 'time'])

        tracker = self.get_object()

        if tracker.carrier != 'Other':
            ts = easypost.Tracker.all(
                tracking_code=tracker.tracking_number,
                carrier=tracker.carrier
            ).to_dict().get('trackers')
        else:
            ts = easypost.Tracker.all(
                tracking_code=tracker.tracking_number,
            ).to_dict().get('trackers')

        est_deliv = self.extratValue(ts, 'est_delivery_date', 'pending')
        status = self.extratValue(ts, 'status', 'pending')

        carrier = self.extratValue(ts, 'carrier', 'Other')

        shipped = ''
        transit = ''
        delivery = ''
        delivered = ''
        est_deliv_date = ''

        if est_deliv:
            est_deliv_year = est_deliv[2:4]
            est_deliv_month = est_deliv[6:7]
            est_deliv_day = est_deliv[9:10]
            est_deliv_date = 'Expected Arrival {}/{}/{}'.format(est_deliv_month, est_deliv_day, est_deliv_year)

        elif status == 'delivered':
            est_deliv_date = 'Delivered'
        else:
            est_deliv_date = 'Expected Arrival N/A'

        if status == 'pre_transit':
            shipped = 'active'

        if status == 'in_transit':
            shipped = 'active'
            transit = 'active'

        if status == 'out_for_delivery':
            shipped = 'active'
            transit = 'active'
            delivery = 'active'

        if status == 'delivered':
            shipped = 'active'
            transit = 'active'
            delivery = 'active'
            delivered = 'active'

        events = []

        AM = 'AM'

        for item in reversed(ts[0]['tracking_details']):

            year = item['datetime'][2:4]
            month = int(item['datetime'][6:7])
            if month < 10:
                month = '0{}'.format(month)
            day = int(item['datetime'][8:10])
            if day < 10:
                day = '0{}'.format(day)

            hour = item['datetime'][11:13]
            minute = item['datetime'][14:16]



            if tracker.carrier == 'FedEx':

                date_str = datetime.strptime('20{}-{}-{} {}:{}'.format(year, month, day, hour, minute), "%Y-%m-%d %H:%M")
                print(date_str)
                date_str_utc = date_str.replace(tzinfo=pytz.timezone('UTC'))
                converted = str(date_str_utc.astimezone(pytz.timezone(time_zone)))

                year = converted[2:4]
                month = converted[5:7]
                day = converted[8:10]

                hour = converted[11:13]
                minute = converted[14:16]

                print('{}/{}/{}, {}:{}'.format(month, day, year, hour, minute))

            if int(hour) > 13:
                hour = int(hour) - 12
                AM = 'PM'


            date = '{}/{}/{}'.format(month, day, year)
            time = '{}:{} {}'.format(hour, minute, AM)

            city = item['tracking_location']['city']
            state = item['tracking_location']['state']
            country = item['tracking_location']['country']

            if country == None and state == None and city == None:
                location = 'N/A'
            elif country == None and state == None:
                location = city
            elif country == None:
                location = '{}, {}'.format(city, state)
            else:
                location = '{}, {} {}'.format(city, state, country)

            events.append(
                eventElement(item['message'], location, date, time))

        detailList.update({'dataElement': dataElement(est_deliv_date, status, carrier, tracker.tracking_number,
                                                      tracker.name, shipped, transit, delivery, delivered)})

        detailList['events'] = events

        return detailList

    def extratValue(self, ts, key, defaultValue=None):
        return ts[0].get(key) if len(ts) > 0 else defaultValue


class DeleteTracker(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    DeleteView.model = tracker
    DeleteView.success_url = '/track/dashboard'

    def test_func(self):
        tracker = self.get_object()
        if self.request.user == tracker.user:
            return True
        return False




def sms_hook(request):
    if request.method == 'POST':

        webhook = request.body.to_dict()

        if webhook.description == 'tracker.updated':
            if webhook.previous_attributes != webhook.result.status:
                tracking_code = webhook.result.tracking_code

                tracker_int = tracker.objects.all().get.filter(tracking_number=tracking_code)

                if tracker_int.sms == True:
                    user = tracker_int.user
                    profile = umod.profile.objects.get(user=user)

                    message = client.messages \
                        .create(
                        body="Your order {} is now {}".format(tracker_int.name, webhook.status),
                        from_='+12512702330',
                        to=profile.phone
                    )
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=200)
            else:
                return HttpResponse(status=200)
        else:
            return HttpResponse(status=200)
        return HttpResponse(status=200)


