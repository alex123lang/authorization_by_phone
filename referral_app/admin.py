from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # List of fields to display in the admin list view
    list_display = ["phone_number", "invite_code", "invite_used"]

    # Enable searching by phone number and invite code
    search_fields = ["phone_number", "invite_code", "invite_used"]

    # Fields that can be edited directly from the list view
    list_editable = ["invite_used"]
