from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Setting, ToEmail
from .forms import SettingForm, ToEmailForm



class SettingAdmin(admin.ModelAdmin):
    form = SettingForm  # Use the custom form if additional validation is needed
    list_display = ('host', 'port', 'email', 'status')

    def has_add_permission(self, request):
        # Limit to only one instance of Setting
        if Setting.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Disable delete permission
        return False

    def save_model(self, request, obj, form, change):
        if not change and Setting.objects.exists():
            raise ValidationError('Only one instance of Setting is allowed. Please edit the existing instance.')
        super().save_model(request, obj, form, change)

# Register the Setting model with the custom admin class
admin.site.register(Setting, SettingAdmin)



class ToEmailAdmin(admin.ModelAdmin):
    form = ToEmailForm
    list_display = ('name', 'email', 'phonenumber', 'position', 'active_status')
    list_filter = ('active_status', 'position')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.pk == 1:
            return ['active_status']
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        if obj and obj.pk == 1:
            return False
        return super().has_delete_permission(request, obj)


admin.site.register(ToEmail, ToEmailAdmin)
