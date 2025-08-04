from rest_framework import serializers
from auth_dipesh.models import CustomUser
from auth_dipesh.models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False)
    class Meta:
        model = CustomUser
        fields = '__all__'
    # so here we have method called create, 
    # what we are going to do is first we pop that data we passed into postman out.
    # we unpack it and with the thelp of that we create a new address
    # since postman expects to give address id when creating user, again put that address id that we created
    def create(self, validated_data):
        address_data = validated_data.pop('address')
        raw_password = validated_data.pop('password')
        address_id = Address.objects.create(**address_data)
        user = CustomUser.objects.create_user(password=raw_password, address=address_id, **validated_data)
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()