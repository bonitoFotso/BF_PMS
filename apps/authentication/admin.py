from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm

# Register your models here.
from .models import User

admin.site.site_header = "BF_PMS"


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_helpdesk','is_technicien','active')
    list_filter = ('admin', 'is_helpdesk','is_technicien', 'active')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password',)}),
        ('Personal Info', {'fields': ()}),
        ('Permissions', {'fields': ('admin', 'is_helpdesk','is_technicien', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)}
        ),
    )
    search_fields = ('email', 'name', )
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
