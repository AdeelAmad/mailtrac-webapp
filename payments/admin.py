from django.contrib import admin

# Register your models here.
from payments.models import membership, subscription

admin.site.register(membership)
admin.site.register(subscription)