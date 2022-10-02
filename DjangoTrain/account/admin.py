from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

UserAdmin.fieldsets [2][1]['fields'] = (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "Is_author",
                    "Special_user",
                    "groups",
                    "user_permissions",
)

UserAdmin.fieldsets [1][1]["fields"] = (
                    "first_name", 
                    "last_name", 
                    "email",
                    "Profile_Avatar",
)

UserAdmin.list_display += ("Is_author" , "is_special_user")


admin.site.register(User, UserAdmin)