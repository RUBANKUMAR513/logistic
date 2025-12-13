from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
import os
from io import BytesIO
from django.core.files.base import ContentFile

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