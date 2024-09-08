from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from referral_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "phone_number", "auth_code", "invite_code", "invite_used"]

    def validate_invite_used(self, value):
        """
        Проверка существования инвайт-кода и того, что пользователь уже его не активировал.
        """
        if not value:
            return value  # Если пользователь не вводит инвайт-код, пропускаем проверку

        # Проверка, активировал ли пользователь уже инвайт-код
        if self.instance and self.instance.invite_used:
            raise serializers.ValidationError("Вы уже активировали инвайт-код.")

        # Проверка существования инвайт-кода в базе данных
        try:
            inviter = UserProfile.objects.get(invite_code=value)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Инвайт-код не найден.")

        return value


class CustomTokenObtainPairSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    auth_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        auth_code = attrs.get("auth_code")

        # Проверка, что пользователь с таким номером телефона существует
        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError(
                "Пользователь с таким номером телефона не найден."
            )

        # Проверка правильности кода
        if user.auth_code != auth_code:
            raise serializers.ValidationError("Неверный код.")

        refresh = RefreshToken.for_user(user)

        user.auth_code = None
        user.save()

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
