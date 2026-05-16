from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User, KYCDocument

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['is_kyc_verified'] = user.is_kyc_verified
        token['id_card_type'] = user.id_card_type

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'id_card_number', 'id_card_type', 'is_kyc_verified')
        read_only_fields = ('is_kyc_verified',)

class KYCDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCDocument
        fields = ('id', 'document', 'status', 'submitted_at', 'reviewed_at', 'rejection_reason')
        read_only_fields = ('status', 'submitted_at', 'reviewed_at', 'rejection_reason')
