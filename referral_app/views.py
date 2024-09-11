from django.contrib.auth import login
from django.http import HttpResponseForbidden
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
from .forms import UserProfileForm, AuthCodeForm, InviteCodeForm


def home(request):
    return render(request, "referral_app/home.html")


def register_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get("phone_number")

            if UserProfile.objects.filter(phone_number=phone_number).exists():
                return redirect(reverse("referral_app:login_by_phone"))

            else:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data.get("password"))
                user.save()

                # Генерация случайного кода для SMS
                code = random.randint(1000, 9999)
                user.auth_code = code
                user.save()

                # Логирование для отладки (вместо отправки SMS)
                print(f"Generated code: {code}")

                return redirect(reverse("referral_app:auth_code", args=[user.pk]))
    else:
        form = UserProfileForm()

    return render(request, "referral_app/register_view.html", {"form": form})


def login_by_phone(request):
    if request.method == "POST":
        phone_number = request.POST.get("phone_number")

        # Проверяем, есть ли пользователь с таким номером телефона
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
            # Если пользователь найден, отправляем новый код
            code = random.randint(1000, 9999)
            user.auth_code = code
            user.save()

            # Логирование для отладки (вместо отправки SMS)
            print(f"Generated code: {code}")

            return redirect(reverse("referral_app:auth_code", args=[user.pk]))
        except UserProfile.DoesNotExist:
            # Если пользователь не найден, перенаправляем на регистрацию
            return redirect(reverse("referral_app:register_view"))

    return render(request, "referral_app/login_by_phone.html")


def auth_code(request, pk):
    user = UserProfile.objects.get(pk=pk)
    if request.method == "POST":
        form = AuthCodeForm(request.POST, instance=user)
        if form.is_valid():
            login(request, user)
            return redirect(reverse("referral_app:retrieve_view", args=[user.pk]))
    else:
        form = AuthCodeForm(instance=user)

    return render(request, "referral_app/auth_code.html", {"form": form, "user": user})


def retrieve_view(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)

    # Проверяем, является ли текущий пользователь владельцем профиля
    if request.user != user:
        return HttpResponseForbidden("У вас нет прав для просмотра этого профиля.")

    if request.method == "POST":
        invite_form = InviteCodeForm(request.POST, instance=user)
        if invite_form.is_valid():
            invite_form.save()
            return redirect(reverse("referral_app:retrieve_view", args=[user.pk]))
    else:
        invite_form = InviteCodeForm(instance=user)

        # Получаем список пользователей, которые использовали инвайт-код данного пользователя
    users_with_my_invite_code = UserProfile.objects.filter(invite_used=user.invite_code)

    return render(
        request,
        "referral_app/retrieve_view.html",
        {
            "user": user,
            "invite_form": invite_form,
            "users_with_my_invite_code": users_with_my_invite_code,
        },
    )


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
