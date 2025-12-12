from django.contrib import admin
from .models import LogoSettings,CompanyDetails,ColorSettings

@admin.register(LogoSettings)
class LogoSettingsAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'last_updated')

    # Disable "Add" button in admin when one instance exists
    def has_add_permission(self, request):
        if LogoSettings.objects.exists():
            return False
        return True

    # Allow editing existing instance
    def has_delete_permission(self, request, obj=None):
        # Optional: Prevent deletion if you want
        return False  # remove delete option
    
@admin.register(CompanyDetails)
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = ('companyname', 'contact_number', 'email', 'last_updated')

    def has_add_permission(self, request):
        # Disable the Add button when one instance exists
        if CompanyDetails.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False  # Disable delete
    

@admin.register(ColorSettings)
class ColorSettingsAdmin(admin.ModelAdmin):
    list_display = ['primary', 'secondary', 'light', 'dark', 'last_updated']

    def has_add_permission(self, request):
        return not ColorSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
