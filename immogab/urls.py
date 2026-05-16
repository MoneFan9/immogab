from django.contrib import admin
from django.urls import path
from payments.views import payment_webhook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/payments/webhook/<str:provider>/", payment_webhook, name="payment-webhook"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
