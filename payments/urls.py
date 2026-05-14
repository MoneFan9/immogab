from django.urls import path
from .views import mock_payment_webhook

app_name = 'payments'

urlpatterns = [
    path('webhook/mock/', mock_payment_webhook, name='mock-webhook'),
]
