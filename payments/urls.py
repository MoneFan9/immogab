from django.urls import path
from .views import MobileMoneyWebhookView

urlpatterns = [
    path('webhook/<str:provider>/', MobileMoneyWebhookView.as_view(), name='mobile_money_webhook'),
]
