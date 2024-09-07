from django.core.management import BaseCommand

from referral_app.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = UserProfile.objects.create(phone_number="9999999999")
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password("123")
        user.save()
