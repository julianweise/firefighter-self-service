from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from personal_data.models import DriverLicense, UserStatus, CategoryOfDriverLicense, Rank, RankAssignment, \
    Firefighter, Authority, Honor, HonorAssignment, Role, RoleAssignment


class CustomAuthorityAdmin(ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(Authority, CustomAuthorityAdmin)


class CustomCategoryOfDriverLicenseAdmin(ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(CategoryOfDriverLicense, CustomCategoryOfDriverLicenseAdmin)


class CustomRankAdmin(ModelAdmin):
    list_display = ("sorting_order", "name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("sorting_order", "name",)


admin.site.register(Rank, CustomRankAdmin)


class CustomRankAssignmentAdmin(ModelAdmin):
    list_display = ("rank", "firefighter", "issue_date", "issuer")
    list_filter = ("rank", "firefighter", "issuer")
    search_fields = ("rank", "firefighter", "issuer")
    ordering = ("issue_date", "firefighter",)


admin.site.register(RankAssignment, CustomRankAssignmentAdmin)


class CustomUserStatus(ModelAdmin):
    list_display = ("name", "active")
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("-active", "name",)


admin.site.register(UserStatus, CustomUserStatus)


class DriverLicenseInline(admin.TabularInline):
    max_num = 1
    model = DriverLicense


class RankAssignmentInline(admin.TabularInline):
    max_num = 1
    model = RankAssignment


class UserInline(admin.TabularInline):
    model = User


class CustomUserAdmin(UserAdmin):
    model = Firefighter
    list_display = ('first_name', 'last_name', 'staff_id', 'email', 'is_staff', 'is_active')
    list_filter = ('first_name', 'last_name', 'email', 'status')
    fieldsets = (
        (_("Basic information"), {
            'fields': ('first_name', 'last_name', 'email', 'password', 'date_of_birth', 'active_since')
        }),
        (_("Extended information"), {
            'fields': ('status', 'staff_id')
        }),
        (_("Address"), {
            'fields': ('street', 'zip', 'city', 'phone_number')
        }),
        (_("Equipment"), {
            'fields': ('pager', 'key', 'locker')
        }),
        (_("Permissions"), {
            'fields': ('is_staff', 'is_active')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'street', 'zip', 'city',
                       'phone_number', 'date_of_birth', 'is_staff', 'is_active')}
         )
    )
    search_fields = ('email', 'last_name', 'first_name')
    ordering = ('last_name', 'first_name')
    inlines = [DriverLicenseInline, RankAssignmentInline]


class CustomHonorAdmin(ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("sorting_order",)


admin.site.register(Honor, CustomHonorAdmin)


class CustomHonorAssignmentAdmin(ModelAdmin):
    list_display = ("honor", "firefighter", "issue_date", "issuer")
    list_filter = ("honor", "firefighter", "issue_date", "issuer")
    search_fields = ("honor", "firefighter", "issue_date", "issuer")
    ordering = ("honor", "firefighter", "issue_date", "issuer")


admin.site.register(HonorAssignment, CustomHonorAssignmentAdmin)


class CustomRoleAdmin(ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    ordering = ("sorting_order",)


admin.site.register(Role, CustomRoleAdmin)


class CustomRoleAssignmentAdmin(ModelAdmin):
    list_display = ("firefighter", "role", "start", "end", "issuer")
    list_filter = ("firefighter", "role", "issuer")
    search_fields = ("firefighter", "role", "issuer")
    ordering = ("role", "firefighter", "issuer")


admin.site.register(RoleAssignment, CustomRoleAssignmentAdmin)


class CustomDriverLicenseAdmin(ModelAdmin):
    list_display = ("owner", "license_id", "issue_date", "expiration_date")
    list_filter = ("owner",)
    search_fields = ("owner", "license_id")
    ordering = ("owner", "issue_date")


admin.site.register(DriverLicense, CustomDriverLicenseAdmin)

admin.site.register(Firefighter, CustomUserAdmin)
