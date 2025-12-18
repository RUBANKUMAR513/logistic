from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile
import re

def validate_1920x1080(image):
    img = Image.open(image)
    width, height = img.size
    if width != 1920 or height != 1080:
        raise ValidationError("Image must be exactly 1920 x 1080 pixels.")
    
class HomePageSlider(models.Model):
    title = models.CharField(
        max_length=30,
        help_text="Enter slider title"
    )

    description = models.TextField(
        help_text="Short description for the slider",
        max_length=200
    )

    quote_before = models.CharField(
        max_length=20,
        help_text="Quote text shown on slider"
    )
    
    highlight_word = models.CharField(
        max_length=10,
        help_text="Word to highlight inside the quote"
    )

    quote_after = models.CharField(
        max_length=10,
        help_text="Quote text shown on slider",
        default="& Solution"
    )

    image = models.ImageField(
        upload_to='sliders/',
        validators=[validate_1920x1080],
        help_text="Upload image (Exact size: 1920 x 1080 px)"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Enable or disable this slider"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class GalleryImages(models.Model):
    ORIENTATION_CHOICES = [
        ('portrait', 'Portrait'),
        ('landscape', 'Landscape'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery_images/')
    enable = models.BooleanField(default=True)  # Checkbox for enable/disable
    orientation = models.CharField(max_length=10, choices=ORIENTATION_CHOICES)
    update_date_time = models.DateTimeField(auto_now=True)  # Automatically set the date/time on update

    def clean(self):
        # Limit to 25 instances
        if GalleryImages.objects.count() >= 25 and not self.pk:
            raise ValidationError('You can only create up to 25 Gallery Image Containers.')

    def save(self, *args, **kwargs):
        # Process the image for WebP format
        if self.image:
            # Open the image file
            img = Image.open(self.image)
            img = img.convert("RGB")  # Ensure compatibility with WebP format

            # Determine target size based on orientation
            if self.orientation == 'portrait':
                target_size = (1080, 1920)  # Example size for portrait
            else:
                target_size = (1920, 1080)  # Example size for landscape

            img.thumbnail(target_size, Image.Resampling.LANCZOS)  # Use LANCZOS for high-quality resizing

            # Save the image in WebP format
            output = BytesIO()
            img.save(output, format='WEBP', quality=80)  # Adjust quality for performance
            output.seek(0)

            # Replace the old image with the new WebP image
            new_image_name = os.path.splitext(self.image.name)[0] + '.webp'
            self.image = ContentFile(output.read(), name=new_image_name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class Testimonial(models.Model):
    client_name = models.CharField(
        max_length=30,
        help_text="Maximum 30 characters"
    )

    client_picture = models.ImageField(
        upload_to='testimonials/',
        help_text="Recommended size: 100 × 100 pixels"
    )

    profession = models.CharField(
        max_length=20,
        help_text="Maximum 20 characters"
    )

    description = models.TextField(
        max_length=100,
        help_text="Maximum 100 characters"
    )

    enable = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name
    

class ContactPage(models.Model):
    maincontent = models.CharField(max_length=200)
    
    locationtodisplay = models.TextField(
        help_text="Paste Google Maps iframe OR only the src URL"
    )
    last_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        # Allow only one instance
        if not self.pk and ContactPage.objects.exists():
            raise ValidationError("Only one ContactPage instance is allowed.")

    def save(self, *args, **kwargs):
        # Extract src if full iframe is pasted
        if self.locationtodisplay:
            match = re.search(r'src="([^"]+)"', self.locationtodisplay)
            if match:
                self.locationtodisplay = match.group(1)

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Contact Page Content"
    
def validate_image_500x300(image):
    img = Image.open(image)
    width, height = img.size
    if width != 500 or height != 300:
        raise ValidationError(
            "Image must be exactly 500 x 300 pixels."
        )

class TypesOfService(models.Model):
    service_name = models.CharField(
        max_length=30,
        unique=True,
        help_text="Enter service name"
    )

    image = models.ImageField(
        upload_to='services/',
        validators=[validate_image_500x300],
        default='services/default.png',
        help_text="Upload image with exact size 500 x 300 px"
    )

    description = models.TextField(
        max_length=100,
        
        help_text="Short description about the service"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Enable or disable this service"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name

def validate_1920_1080(image):
    img = Image.open(image)
    width, height = img.size
    if width != 1920 or height != 1080:
        raise ValidationError(
            "Page header image must be exactly 1920 x 1080 pixels."
        )

class ServiceContent(models.Model):
    service = models.OneToOneField(
        TypesOfService,
        on_delete=models.CASCADE,
        related_name='content'
    )
    
    # NEW FIELD
    page_header_image = models.ImageField(
        upload_to='services/headers/',
        validators=[validate_1920_1080],
        blank=True,
        null=True,
        help_text="Upload service page header image (Exact size: 1920 x 1080)"
    )

    description_1 = models.TextField(null=True)
    description_2 = models.TextField(null=True)
    description_3 = models.TextField(null=True)
    description_4 = models.TextField(null=True)
    

    image_1 = models.ImageField(upload_to='services/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='services/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='services/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='services/', blank=True, null=True)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.service.service_name} Content"
    
def validate_team_image(image):
    """
    Validate image size to be exactly 400x400 pixels
    """
    img = Image.open(image)
    width, height = img.size

    if width != 400 or height != 400:
        raise ValidationError(
            "Image must be exactly 400 x 400 pixels."
        )


class TeamMember(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Enter team member full name"
    )

    designation = models.CharField(
        max_length=100,
        help_text="Enter team member designation (e.g., Manager, Developer)"
    )

    image = models.ImageField(
        upload_to='team/',
        validators=[validate_team_image],
        help_text="Upload square image (400 x 400 pixels)"
    )

    facebook = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text="Facebook profile link"
    )

    twitter = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text="Twitter (X) profile link"
    )

    instagram = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text="Instagram profile link"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this member from website"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last updated time"
    )

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['name']

    def __str__(self):
        return self.name
    
# -------------------------------
# Image size validation (800x800)
# -------------------------------
def validate_800x800(image):
    img = Image.open(image)
    if img.width != 800 or img.height != 800:
        raise ValidationError("Image must be exactly 800 x 800 pixels.")


class OurFeature(models.Model):
    heading_quote = models.CharField(
        max_length=200,
        help_text="Main heading or quote"
    )

    image = models.ImageField(
        upload_to="features/",
        validators=[validate_800x800],
        help_text="Upload image with size 800 x 800 pixels"
    )

    # -------- Feature 1 --------
    sub_title1 = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique subtitle 1"
    )
    icon1 = models.CharField(
        max_length=30,
        help_text="Font Awesome icon name only (example: truck, clock, shield)"
    )
    short_description1 = models.CharField(
        max_length=150,
        help_text="Short description 1"
    )

    # -------- Feature 2 --------
    sub_title2 = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique subtitle 2"
    )
    icon2 = models.CharField(
        max_length=30,
        help_text="Font Awesome icon name only"
    )
    short_description2 = models.CharField(
        max_length=150,
        help_text="Short description 2"
    )

    # -------- Feature 3 --------
    sub_title3 = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique subtitle 3"
    )
    icon3 = models.CharField(
        max_length=30,
        help_text="Font Awesome icon name only"
    )
    short_description3 = models.CharField(
        max_length=150,
        help_text="Short description 3"
    )

    last_updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.pk and OurFeature.objects.exists():
            raise ValidationError("Only one OurFeature instance is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()  # ensures clean() runs always
        super().save(*args, **kwargs)


    def __str__(self):
        return self.heading_quote
    

class AboutUs(models.Model):
    heading_quote = models.CharField(
        max_length=200,
        help_text="Main heading or quote"
    )

    # Short description at the end (STRICT 30 chars)
    short_description = models.CharField(
        max_length=150,
        help_text="Short description about the company (shown at the end)"
    )

    image = models.ImageField(
        upload_to="about/",
        validators=[validate_800x800],
        help_text="Upload image with size 800 x 800 pixels"
    )

    # -------- Feature 1 --------
    sub_title1 = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique subtitle 1"
    )
    icon1 = models.CharField(
        max_length=30,
        help_text="Font Awesome icon name only (example: truck, clock)"
    )
    short_description1 = models.CharField(
        max_length=150,
        help_text="Short description 1"
    )

    # -------- Feature 2 --------
    sub_title2 = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique subtitle 2"
    )
    icon2 = models.CharField(
        max_length=30,
        help_text="Font Awesome icon name only"
    )
    short_description2 = models.CharField(
        max_length=150,
        help_text="Short description 2"
    )

    # Detailed About Content
    why_choose_us = models.TextField(
        help_text="Detailed content for About Us section"
    )

    last_updated = models.DateTimeField(auto_now=True)

    # -------------------------------
    # Allow ONLY ONE instance
    # -------------------------------
    def clean(self):
        if not self.pk and AboutUs.objects.exists():
            raise ValidationError("Only one AboutUs instance is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "About Us Section"




def validate_1920_1080(image):
    img = Image.open(image)
    width, height = img.size
    if width != 1920 or height != 1080:
        raise ValidationError(
            "Image must be exactly 1920 x 1080 pixels."
        )



class NavbarPageImages(models.Model):

    about_page_image = models.ImageField(
        upload_to='navbar/',
        validators=[validate_1920_1080],
        help_text="Upload About page banner image (Exact size: 1920 x 1080)",
        null=True,
        blank=True
    )
    about_page_description = models.TextField(
        null=True,
        blank=True,
        help_text="Optional description for About page banner"
    )

    gallery_page_image = models.ImageField(
        upload_to='navbar/',
        validators=[validate_1920_1080],
        help_text="Upload Gallery page banner image (Exact size: 1920 x 1080)",
        null=True,
        blank=True
    )
    gallery_page_description = models.TextField(
        null=True,
        blank=True,
        help_text="Optional description for Gallery page banner"
    )

    contact_page_image = models.ImageField(
        upload_to='navbar/',
        validators=[validate_1920_1080],
        help_text="Upload Contact page banner image (Exact size: 1920 x 1080)",
        null=True,
        blank=True
    )
    contact_page_description = models.TextField(
        null=True,
        blank=True,
        help_text="Optional description for Contact page banner"
    )
    error_page_image = models.ImageField(
        upload_to='navbar/',
        validators=[validate_1920_1080],
        help_text="Upload error page banner image (Exact size: 1920 x 1080)",
        null=True,
        blank=True
    )
    error_page_description = models.TextField(
        null=True,
        blank=True,
        help_text="Optional description for error page banner"
    )

    why_choose_us_image = models.ImageField(
        upload_to='navbar/',
        validators=[validate_1920_1080],
        help_text="Upload 'Why Choose Us' section image (Exact size: 1920 x 1080)",
        null=True,
        blank=True
    )
    why_choose_us_description = models.TextField(
        null=True,
        blank=True,
        help_text="Optional description for 'Why Choose Us' section"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.pk and NavbarPageImages.objects.exists():
            raise ValidationError("Only one Navbar Page Images instance is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return "Navbar Page Images"