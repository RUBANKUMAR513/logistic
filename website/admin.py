from django.contrib import admin
from .models import GalleryImages,Testimonial,ContactPage,TypesOfService,ServiceContent


@admin.register(GalleryImages)
class GalleryImagesAdmin(admin.ModelAdmin):
    list_display = ('name', 'enable', 'orientation', 'update_date_time')
    list_filter = ('enable', 'orientation')
    search_fields = ('name',)

    # Disable "Add" button if 25 images already exist
    def has_add_permission(self, request):
        if GalleryImages.objects.count() >= 25:
            return False
        return True


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'profession', 'enable', 'last_updated')
    list_editable = ('enable',)
    search_fields = ('client_name', 'profession')
    list_filter = ('enable', 'last_updated')


@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("short_maincontent", "last_updated")
    fields = ("maincontent", "locationtodisplay")

    def has_add_permission(self, request):
        return not ContactPage.objects.exists()

    def short_maincontent(self, obj):
        return obj.maincontent[:40] + "..." if len(obj.maincontent) > 40 else obj.maincontent

    short_maincontent.short_description = "Main Content"


class ServiceContentInline(admin.StackedInline):
    model = ServiceContent
    extra = 0


@admin.register(TypesOfService)
class TypesOfServiceAdminPanel(admin.ModelAdmin):
    inlines = [ServiceContentInline]
    list_display = ('service_name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('service_name',)
    ordering = ('-created_at',)
    list_editable = ('is_active',)