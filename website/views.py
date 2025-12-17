from django.shortcuts import render
from settings.models import LogoSettings,ColorSettings,CompanyDetails
from website.models import GalleryImages,Testimonial,ContactPage,TypesOfService,TeamMember,OurFeature,AboutUs,NavbarPageImages,ServiceContent,HomePageSlider
from django.shortcuts import render, get_object_or_404

def get_common_context():
    logo_settings = LogoSettings.objects.first()
    company = CompanyDetails.objects.first()
    colors = ColorSettings.objects.first()
    nav_services = TypesOfService.objects.filter(is_active=True)

    return {
        "logo_settings": logo_settings,
        "company": company,
        "colors": colors,
        "nav_services": nav_services,  # ✅ Added
    }

# Home page
def home(request):
    context = get_common_context()
    context['testimonials'] = Testimonial.objects.filter(enable=True)
    context['team_members'] = TeamMember.objects.filter(
        is_active=True
    )
    context['feature'] = OurFeature.objects.first()
    context['sliders'] = HomePageSlider.objects.filter(is_active=True)
    context['services'] = TypesOfService.objects.filter(is_active=True)
    contact = ContactPage.objects.first()
    context['contact'] = contact
    context['about'] = AboutUs.objects.first()
    return render(request, "index.html", context)

# About page
def about(request):
    context = get_common_context()

    context['team_members'] = TeamMember.objects.filter(
        is_active=True
    )
    context['feature'] = OurFeature.objects.first()
    context['about'] = AboutUs.objects.first()
    context['navbar_images'] = NavbarPageImages.objects.first()
    return render(request, "about.html", context)


def about_detail(request):
    context = get_common_context()  
    context['about'] = AboutUs.objects.first()
    context['testimonials'] = Testimonial.objects.filter(enable=True)
    context['navbar_images'] = NavbarPageImages.objects.first()
    return render(request, "about-detail.html", context)

# Service page
def service(request):
    context = get_common_context()
    return render(request, "service.html", context)

# Gallery page
def gallery(request):
    context = get_common_context()
    gallery_images = GalleryImages.objects.filter(enable=True)

    context['gallery_images'] = gallery_images
    context['testimonials'] = Testimonial.objects.filter(enable=True)
    context['navbar_images'] = NavbarPageImages.objects.first()
    return render(request, "gallery.html", context)


# Pricing page
def pricing(request):
    context = get_common_context()
    return render(request, "price.html", context)

# Feature page
def feature(request):
    context = get_common_context()
    return render(request, "feature.html", context)

# Quote page
def quote(request):
    context = get_common_context()
    return render(request, "quote.html", context)

# Team page
def team(request):
    context = get_common_context()
    return render(request, "team.html", context)

# Testimonial page
def testimonial(request):
    context = get_common_context()
    return render(request, "testimonial.html", context)

# Contact page
def contact(request):
    context = get_common_context()
    contact = ContactPage.objects.first()
    context['contact'] = contact
    context['navbar_images'] = NavbarPageImages.objects.first()
    context['services'] = TypesOfService.objects.filter(is_active=True)
    return render(request, "contact.html", context)

# 404 error page
def error_404(request, exception):
    context = get_common_context()
    return render(request, "404.html", context)

def service_detail(request, service_id):
    # Get the active service
    service = get_object_or_404(
        TypesOfService,
        id=service_id,
        is_active=True
    )

    # Get related ServiceContent (if exists)
    try:
        service_content = service.content  # OneToOne relation
    except ServiceContent.DoesNotExist:
        service_content = None

    # Common context
    context = get_common_context()
    context['testimonials'] = Testimonial.objects.filter(enable=True)
    context.update({
        "service": service,
        "service_content": service_content,  # Pass page header image and descriptions
    })

    return render(request, "service-content.html", context)
