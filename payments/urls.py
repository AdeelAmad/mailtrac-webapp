"""mailtrac URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from payments import views as user_views
from home import views as home
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', user_views.charge, name='charge'),
    path('hooks', user_views.hook, name='hook')
    # path('', user_views.pay, name='payments'),
    # path('bill', user_views.bill, name='createCustomer'),
    # path('charge/', user_views.charge, name='charge'),
    # path('cancel/', user_views.cancelSub, name='cancel')
]