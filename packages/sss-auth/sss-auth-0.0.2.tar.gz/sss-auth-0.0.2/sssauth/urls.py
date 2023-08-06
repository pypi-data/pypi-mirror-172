from django.urls import path

from sssauth import views

app_name = 'sssauth'

urlpatterns = [
    path('login_api/', views.login_api, name='sssauth_login_api'),
    path('signup_api/', views.signup_api, name='sssauth_signup_api'),
]

