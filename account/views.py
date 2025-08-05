from django.shortcuts import render, redirect

from rest_framework import generics, views, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator


from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse

from account.serializers import RegistrationSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from account.utils import send_activation_email, send_password_reset_email


def activate_email_forward(request, user):
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    activation_path = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
    activation_url = request.build_absolute_uri(activation_path)

    send_activation_email(user.email, activation_url)     


# Create your views here.
class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
    # template_name = 'account/registration.html'

    # def get(self, request):
    #     return render(request, self.template_name)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)     # providing incoming data to the serializer for validation
        serializer.is_valid(raise_exception=True)              # if not validated raise exceptions

        user = serializer.save(is_active=False)

        activate_email_forward(request, user)

        return Response({
            "message": "Registration successful. Please check your email to activate your account.",
            "user": serializer.data,
        })

class ActivateAccountView(views.APIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if user.is_active:
                return Response(
                    {"detail": "User already exists and is an active user"},
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(
                    {'detail': 'Your account has been activated successfully'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Invalid Activation Link"},
                    status = status.HTTP_400_BAD_REQUEST
                )

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"detail": "Invalid activation link"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    # template_name = 'account/login.html'

    # def get(self, request):
    #     return render(request, self.template_name)

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid email or password"},
                status = status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not user.is_active:
                activate_email_forward(request, user)

                return Response({
                    "detail": "Account is Inactive. Please activate your account. Activation email has been sent"
                })

            refresh = RefreshToken.for_user(user)

            login(request, user)

            # response = redirect('list-cart')
            # response.set_cookie("access_token", str(refresh.access_token))
            # response.set_cookie("refresh_token", str(refresh))
            # return response

            return Response(
                {
                    "detail": "Login Successful",
                    'access': str(refresh.access_token),
                    "refresh": str(refresh) 
                },
                status = status.HTTP_200_OK
            )

        return Response(
            {"detail": "Invalid email or password"},
            status = status.HTTP_401_UNAUTHORIZED
        )


class PasswordResetview(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    # template_name = "account/password_reset.html"

    # def get(self, request):
    #     return render(request, self.template_name)

    def post(self, request):
        serializer = PasswordResetSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = default_token_generator.make_token(user)

            reset_url = reverse("password-reset-confirm", kwargs={'uidb64': uidb64, 'token': token})
            absoulute_reset_url = request.build_absolute_uri(reset_url)

            send_password_reset_email(user.email, absoulute_reset_url)

        return Response(
            {"detail": "If the user with this email exists, the email has been sent"},
            status = status.HTTP_200_OK
        )
    
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, User.DoesNotExist, OverflowError):
            return Response(
                {"detail": "Invalid reset link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Reset Link has been expired or is invalid"},
                status = status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=user)
            return Response(
                {"detail": "Password is reset successfully"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": f"Errors: {serializer.errors}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        