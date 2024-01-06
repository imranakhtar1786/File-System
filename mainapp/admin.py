from django.contrib import admin
from .models import userDetail,Files

@admin.register(userDetail)
class userDetailadmin(admin.ModelAdmin):
    list_display = ["id","username","name","email","staff"]

@admin.register(Files)
class Filesadmin(admin.ModelAdmin):
    list_display = ["id","file"]
