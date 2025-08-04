from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import mixins, generics, status
from auth_dipesh.api.serializers import CustomUserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework.permissions import BasePermission

CustomUser = get_user_model()

class UserListCreateAPIView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class UserDetailAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class UserLoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "incorrect username or password"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SayHelloAPIView(APIView):
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    
    def get(self, request):
        #note that I used
        content = {'message': 'hello' }
        return Response(content)

#creating custom permissions
# class IsOwner(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return bool(obj.user and request.user)

# class EditProfileView(mixins.UpdateModelMixin,generics.GenericAPIView):
#     has_permissions = [IsOwner]

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

