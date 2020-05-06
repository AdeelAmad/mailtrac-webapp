
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from users import models as umodels

# Create your models here.
MEMBERSHIPS = (
    ('Basic', 'Basic'),
    ('Pro', 'Pro'),
    ('Unlimited', 'Unlimited')
)


class membership(models.Model):

    membership_type = models.CharField(choices=MEMBERSHIPS, max_length=10, default='Basic')
    price = models.CharField(max_length=3)
    stripe_plan_id = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type

class subscription(models.Model):

    sub_id = models.CharField(max_length=40)
    user = models.ManyToManyField(User)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    membership = models.ForeignKey(membership, on_delete=models.SET_NULL, null=True)