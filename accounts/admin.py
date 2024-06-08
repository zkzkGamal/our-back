from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
admin.site.register(models.DrugCategory)
admin.site.register(models.Profile)
admin.site.register(models.Organizations)
admin.site.register(models.Doctor)
admin.site.register(models.Drugs_Data)
admin.site.register(models.Patient)
admin.site.register(models.Suppliers)
admin.site.register(models.Warhouse_Managments)
admin.site.register(models.Warhouse_Places)
admin.site.register(models.Specialites)



class CustomUserAdmin(BaseUserAdmin):
    # List of fields to display in the User change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups')}),
        # ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

#List of fields to display in the User add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    # List of fields to display in the User list view
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_verified')

#List of fields to use in the search bar
    search_fields = ('email', 'first_name', 'last_name')

    # List of fields to use for filtering
    list_filter = ('is_active', 'is_staff', 'is_verified', 'groups')

#Register the User model with the custom admin
admin.site.register(models.User , CustomUserAdmin)
