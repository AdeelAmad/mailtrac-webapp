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
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from home import urls, views
from track import urls as trurls
from payments import urls as purls
from gmail import urls as gurls

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('', include(urls)),
    path('track/', include(trurls)),
    path('payments/', include(purls)),
    path('admin/', admin.site.urls),
    path('accounts/register/', user_views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('accounts/logout/', user_views.logout, name='logout'),
    path('accounts/profile/', user_views.profile, name='profile'),
    path('accounts/billing/', views.billing, name='billing'),

    path('gmail/', include(gurls)),

    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done', user_views.prsent, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete', user_views.prcomplete, name='password_reset_complete'),

    path('sent/', user_views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', user_views.activate, name='activate'),

    path('sentry-debug/', trigger_error),

    url(r'^accounts/', include('allauth.urls')),

]

handler500 = user_views.handler500
