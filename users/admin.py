from django.contrib import admin
from users.models import User, Code


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass
