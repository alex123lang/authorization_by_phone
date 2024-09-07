import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    username = None

    phone_number = models.CharField(max_length=15, unique=True)
    auth_code = models.CharField(max_length=100, blank=True, null=True)
    invite_code = models.CharField(max_length=6, unique=True, blank=True, null=True)
    invite_used = models.CharField(max_length=6, blank=True, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        # Automatically assign invite code if it's a new user
        if not self.invite_code:
            self.generate_invite_code()
        super().save(*args, **kwargs)

    def generate_invite_code(self):
        # Generate a random 6-digit invite code consisting of numbers and symbols
        self.invite_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
