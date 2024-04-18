from django.contrib import admin
from .models import post, Like
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(post)
admin.site.register(Like)