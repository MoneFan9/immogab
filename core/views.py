from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, KYCSubmissionSerializer
from .models import User
from .tasks import validate_kyc_task

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class KYCSubmissionView(generics.UpdateAPIView):
    serializer_class = KYCSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Trigger asynchronous validation
        validate_kyc_task.delay(instance.id)

        return Response(
            {"message": "KYC document submitted. Verification is in progress."},
            status=status.HTTP_202_ACCEPTED
        )
