from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()
from shared_features.mixins import ModelAdminMixin

from .models import JobSeeker, Company, IndustryArea, Address, FileStore


# @admin.register(User)
class UserModelAdmin(ModelAdminMixin):
    """
    handle User class instance in Django admin panel
    """

    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("username", "email", "first_name", "last_name")
    ordering = ("username", "email", "first_name", "last_name")


admin.site.register(User, UserModelAdmin)
admin.site.register(JobSeeker)
admin.site.register(Company)
admin.site.register(IndustryArea)
admin.site.register(Address)
admin.site.register(FileStore)
