from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import MyTokenObtainPairView, KYCSubmitView, UserProfileView

urlpatterns = [
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('kyc/submit/', KYCSubmitView.as_view(), name='kyc_submit'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
