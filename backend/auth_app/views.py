from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_app.serializers import userInfoInitSerializer, LoginSerializer, Registererializer


# Create your views here.
class CheckUser(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = userInfoInitSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(data=userInfoInitSerializer(user).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@extend_schema(
    request=None,
    responses={200: None},
)
@ensure_csrf_cookie
def get_csrf_token(request):
    return Response(status=status.HTTP_200_OK)


class LoginView(CreateAPIView):
    serializer_class = LoginSerializer

    def perform_create(self, serializer):
        phone_number = serializer.validated_data.get('phone_number')
        password = serializer.validated_data.get('password')
        print(password)
        user = authenticate(username=phone_number, password=password)
        print(user)
        if user is not None:
            login(request=self.request, user=user)
        else:
            raise ValidationError("Phone number or Password or Both are wrong.")


class RegisterView(CreateAPIView):
    serializer_class = Registererializer

    def perform_create(self, serializer):
        serializer.save(active=True)
