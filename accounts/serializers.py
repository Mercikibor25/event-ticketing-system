from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser
from .gava import verify_kra_pin_by_id

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    national_id = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'national_id', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})

        # Verify National ID with GAVA KRA API
        national_id = data.get('national_id')
        result = verify_kra_pin_by_id(national_id)

        if not result['valid']:
            raise serializers.ValidationError({
                "national_id": "Invalid National ID. KRA PIN verification failed."
            })

        # Store KRA details
        data['kra_pin'] = result.get('kra_pin', '')
        data['taxpayer_name'] = result.get('taxpayer_name', '')

        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone_number',
                 'national_id', 'kra_pin', 'taxpayer_name', 'role']
        read_only_fields = ['role', 'kra_pin', 'taxpayer_name']