from django.contrib import admin
from .models import GalleryImages,Testimonial,ContactPage,TypesOfService,ServiceContent,TeamMember,OurFeature,AboutUs


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


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'designation',
        'is_active',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'is_active',
        'designation',
        'created_at',
    )

    search_fields = (
        'name',
        'designation',
    )

    ordering = ('name',)

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ("Basic Information", {
            'fields': (
                'name',
                'designation',
                'image',
                'is_active',
            )
        }),
        ("Social Media Links", {
            'fields': (
                'facebook',
                'twitter',
                'instagram',
            ),
            'description': "Optional social media profile links"
        }),
        ("Timestamps", {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

@admin.register(OurFeature)
class OurFeatureAdmin(admin.ModelAdmin):

    list_display = (
        'heading_quote',
        'sub_title1',
        'sub_title2',
        'sub_title3',
        'last_updated',
    )

    search_fields = (
        'heading_quote',
        'sub_title1',
        'sub_title2',
        'sub_title3',
    )

    ordering = ('-last_updated',)

    readonly_fields = (
        'last_updated',
    )

    fieldsets = (
        ("Main Content", {
            'fields': (
                'heading_quote',
                'image',
            )
        }),
        ("Feature 1", {
            'fields': (
                'sub_title1',
                'icon1',
                'short_description1',
            )
        }),
        ("Feature 2", {
            'fields': (
                'sub_title2',
                'icon2',
                'short_description2',
            )
        }),
        ("Feature 3", {
            'fields': (
                'sub_title3',
                'icon3',
                'short_description3',
            )
        }),
        ("Last Updated", {
            'fields': (
                'last_updated',
            )
        }),
    )

    # -------------------------------
    # Allow ONLY ONE instance
    # -------------------------------
    def has_add_permission(self, request):
        return not OurFeature.objects.exists()
    

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):

    list_display = (
        'heading_quote',
        'sub_title1',
        'sub_title2',
        'last_updated',
    )

    search_fields = (
        'heading_quote',
        'sub_title1',
        'sub_title2',
    )

    ordering = ('-last_updated',)

    readonly_fields = (
        'last_updated',
    )

    fieldsets = (
        ("Main Content", {
            'fields': (
                'heading_quote',
                'image',
                'short_description',
            )
        }),
        ("Feature 1", {
            'fields': (
                'sub_title1',
                'icon1',
                'short_description1',
            )
        }),
        ("Feature 2", {
            'fields': (
                'sub_title2',
                'icon2',
                'short_description2',
            )
        }),
        ("Detail Content", {
            'fields': (
                'detail_content',
            )
        }),
        ("Last Updated", {
            'fields': (
                'last_updated',
            )
        }),
    )

    # -------------------------------
    # Allow ONLY ONE instance
    # -------------------------------
    def has_add_permission(self, request):
        return not AboutUs.objects.exists()