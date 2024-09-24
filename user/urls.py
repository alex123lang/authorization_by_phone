from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import CreateUserView, ListUsersView, UserProfileView

app_name = 'user'


urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('users_list/', ListUsersView.as_view(), name='list_users'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
