import uuid

from phonenumber_field.modelfields import PhoneNumberField

from payments import models as pms
from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class profile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=12, default="")
    signup_confirmation = models.BooleanField(default=False)


    cus_id = models.CharField(max_length=30)

    current_plan = models.ForeignKey(pms.membership ,default=1, on_delete=models.PROTECT)

    # tracks = models.IntegerField(default=3)
    # unlimited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} profile'

# def profile_topoff(user):
#     print(user)
#     u_p = profile.objects.get(user=user)
#
#     if u_p.tracks < 3:
#         u_p.tracks = 3
#     else:
#         u_p.tracks = u_p.tracks + 3
#
#     u_p.save()
#
#     return