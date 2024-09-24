from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication

from .serializers import UserSerializer

User = get_user_model()


class CreateUserView(generics.CreateAPIView):
    """
    Создание нового пользователя в системе
    """
    serializer_class = UserSerializer


class ListUsersView(generics.ListAPIView):
    """
    Получить список всех пользователей (для администраторов)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Получить или обновить профиль текущего пользователя
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
