from django.urls import path
from .views import WebhookView

urlpatterns = [
    path('webhook/<str:provider>/', WebhookView.as_view(), name='payment_webhook'),
]
