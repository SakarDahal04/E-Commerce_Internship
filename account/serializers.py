from rest_framework import serializers

from django.contrib.auth.models import User

from account.mixins import PasswordValidationMixin

class RegistrationSerializer(PasswordValidationMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError({"User already exist": "User with this username already exists"})

        return value
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')

        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            is_active = False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()



class PasswordResetConfirmSerializer(PasswordValidationMixin, serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def save(self, user):
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
