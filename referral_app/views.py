from django.urls import reverse
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from referral_app.models import UserProfile
from referral_app.utils import send_sms  # Импортируем функцию отправки SMS
from referral_app.serializers import UserProfileSerializer
import random  # Для генерации случайного кода
from rest_framework_simplejwt.views import TokenViewBase
from referral_app.serializers import CustomTokenObtainPairSerializer
from django.shortcuts import render, redirect, get_object_or_404
import requests
from django.conf import settings


def home(request):
    return render(request, "referral_app/home.html")


class UserProfileCreateAPIView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Сохраняем пользователя
        user = serializer.save()
        user.set_password(user.password)
        user.save()

        # Генерируем новый случайный код для SMS
        code = random.randint(1000, 9999)

        # Формируем сообщение для отправки
        message = f"Ваш код для подтверждения: {code}"

        # Преобразуем номер телефона в целое число перед отправкой SMS
        user.phone_number = int(user.phone_number)

        # Отправляем SMS с кодом
        # response = send_sms(user.phone_number, message)

        # Для тестирования
        response = code
        print(response)

        # Сохраняем новый код в модели пользователя
        user.auth_code = code
        user.save()

        # Логируем отправку SMS
        """if "error" in response:
            print(f"Ошибка при отправке SMS: {response['error']}")
        else:
            print(f"SMS успешно отправлено на номер {user.phone_number}.")"""


class UserProfileAuthCodeUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (AllowAny,)

    def perform_update(self, serializer):
        if "phone_number" in serializer.validated_data:
            serializer.validated_data.pop("phone_number", None)
        user = serializer.save()
        # Генерируем новый случайный код для SMS
        code = random.randint(1000, 9999)

        # Формируем сообщение для отправки
        message = f"Ваш код для подтверждения: {code}"

        # Преобразуем номер телефона в целое число перед отправкой SMS
        user.phone_number = int(user.phone_number)

        # Отправляем SMS с кодом
        # response = send_sms(user.phone_number, message)

        # Для тестирования
        response = code
        print(response)

        # Сохраняем новый код в модели пользователя
        user.auth_code = code
        user.save()

        # Логируем отправку SMS
        """if "error" in response:
            print(f"Ошибка при отправке SMS: {response['error']}")
        else:
            print(f"SMS успешно отправлено на номер {user.phone_number}.")"""


class RetrieveApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user  # Возвращаем текущего пользователя

    def retrieve(self, request, *args, **kwargs):
        """
        Переопределение метода для вывода списка пользователей, которые ввели инвайт-код текущего пользователя.
        """
        user = self.get_object()

        # Список пользователей, которые ввели инвайт-код текущего пользователя
        users_with_my_invite_code = UserProfile.objects.filter(
            invite_used=user.invite_code
        ).values_list("phone_number", flat=True)

        # Дефолтное поведение retrieve с добавлением пользователей, использовавших инвайт-код
        response_data = self.get_serializer(user).data
        response_data["users_with_my_invite_code"] = list(users_with_my_invite_code)

        return Response(response_data, status=200)


class CustomTokenObtainPairView(TokenViewBase):
    serializer_class = CustomTokenObtainPairSerializer
