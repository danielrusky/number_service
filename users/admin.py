from django.contrib import admin
from users.models import User, Code, Referrals


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'phone'
    )
    search_fields = ("phone", )


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Referrals)
class ReferralsAdmin(admin.ModelAdmin):
    pass
