
from django.urls import path
from .views import email_messages

urlpatterns = [
    path('', email_messages, name='email_messages'),
]