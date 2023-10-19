from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email']
# Register your models here.
admin.site.register(User,UserAdmin)