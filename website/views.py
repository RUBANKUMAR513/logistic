from django.shortcuts import render
from settings.models import LogoSettings,ColorSettings,CompanyDetails


# Helper function to get common context
def get_common_context():
    logo_settings = LogoSettings.objects.first()
    company = CompanyDetails.objects.first()
    colors = ColorSettings.objects.first()
    return {
        "logo_settings": logo_settings,
        "company": company,
        "colors": colors,
    }

# Home page
def home(request):
    context = get_common_context()
    return render(request, "index.html", context)

# About page
def about(request):
    context = get_common_context()
    return render(request, "about.html", context)

# Service page
def service(request):
    context = get_common_context()
    return render(request, "service.html", context)

# Gallery page
def gallery(request):
    context = get_common_context()
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
    return render(request, "contact.html", context)

# 404 error page
def error_404(request, exception):
    context = get_common_context()
    return render(request, "404.html", context)

