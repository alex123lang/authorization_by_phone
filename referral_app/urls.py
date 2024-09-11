from django.urls import path
from rest_framework.permissions import AllowAny
from referral_app.views import (
    CustomTokenObtainPairView,
    UserProfileCreateAPIView,
    UserProfileAuthCodeUpdateAPIView,
    RetrieveApiView,
)
from rest_framework_simplejwt.views import TokenRefreshView

from referral_app.apps import ReferralAppConfig
from . import views

app_name = ReferralAppConfig.name

urlpatterns = [
    path("", views.home, name="home"),
    path("register_view/", views.register_view, name="register_view"),
    path("login_by_phone/", views.login_by_phone, name="login_by_phone"),
    path("<int:pk>/auth_code/", views.auth_code, name="auth_code"),
    path("<int:pk>/retrieve_view/", views.retrieve_view, name="retrieve_view"),
    path("register/", UserProfileCreateAPIView.as_view(), name="register"),
    path(
        "<int:pk>/sign_up/",
        UserProfileAuthCodeUpdateAPIView.as_view(),
        name="sign_up",
    ),
    path("<int:pk>/", RetrieveApiView.as_view(), name="retrieve"),
    path(
        "login/",
        CustomTokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
