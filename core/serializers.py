from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'cni_number', 'is_kyc_verified', 'kyc_document')
        read_only_fields = ('is_kyc_verified',)

class KYCSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('cni_number', 'kyc_document')
        extra_kwargs = {
            'cni_number': {'required': True},
            'kyc_document': {'required': True},
        }
