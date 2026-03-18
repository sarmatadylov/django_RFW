from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'registration_source',
    )

    list_display = ('email', 'is_staff', 'is_active', 'registration_source')

    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'birthdate')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),

        ('Registration info', {'fields': ('registration_source', 'last_login')}),


    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'registration_source'),
        }),

    )

    #def save_model(self, request, obj, form, change):
    #    super().save_model(request, obj, form, change)
     #   if not change:
      #      ConfirmationCode.objects.create(user=obj)


#@admin.register(ConfirmationCode)
#class ConfirmationCodeAdmin(admin.ModelAdmin):
#    list_display = ('user', 'code', 'created_at')
#    search_fields = ('user__email', 'code')
