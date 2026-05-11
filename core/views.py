from rest_framework import generics, permissions
from .serializers import KYCSubmissionSerializer, UserSerializer
from .tasks import validate_kyc_document_async

class KYCSubmitView(generics.UpdateAPIView):
    serializer_class = KYCSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save()
        # Trigger async validation
        validate_kyc_document_async.delay(user.id)

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
