from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class PasswordValidationMixin:
    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm-password": "Passwords doesn't match"}
            )

        validate_password(password)
        
        return data