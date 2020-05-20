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
from track import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', user_views.TrackerCreate.as_view(), name='trc'),
    path('dashboard/', user_views.Dashboard.as_view(), name='dashboard'),
    path('<uuid:pk>/', user_views.DetailInfo.as_view(), name='tracker-detail'),
    path('<uuid:pk>/delete/', user_views.DeleteView.as_view(), name='tracker-delete'),
    path('webhook', user_views.sms_hook, name='sms_hook'),

    path('test/', user_views.test, name='test')

]
