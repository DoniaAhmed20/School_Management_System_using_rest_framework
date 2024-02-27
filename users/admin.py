from django.contrib import admin
from .models import CustomUser

# admin.site.register(CustomUser)
from django.contrib import admin
from rest_framework.authtoken.models import Token

admin.site.register(Token)


# admin.py
from django.contrib import admin
from .models import CustomUser

def activate_users(modeladmin, request, queryset):
    queryset.update(is_active=True)

activate_users.short_description = "Activate selected users"

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active')
    actions = [activate_users]

admin.site.register(CustomUser, CustomUserAdmin)
