from django.contrib import admin

from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(User)

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username')
