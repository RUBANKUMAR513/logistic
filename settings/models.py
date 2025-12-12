from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from colorfield.fields import ColorField
import re


def validate_png(file):
    if not file.name.lower().endswith('.png'):
        raise ValidationError("Only PNG files are allowed.")

class LogoSettings(models.Model):
    company_name = models.CharField(
        max_length=100,
        default="Capricon",
        help_text="Enter your company name"
    )

    logo = models.ImageField(
        upload_to='logos/',
        validators=[validate_png],
        help_text="Upload your logo (PNG only)"
    )

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Logo Setting"
        verbose_name_plural = "Logo Settings"

    def __str__(self):
        return self.company_name or "Site Logo"

    def save(self, *args, **kwargs):
        if not self.pk and LogoSettings.objects.exists():
            raise ValidationError("Only one LogoSettings instance allowed.")
        return super().save(*args, **kwargs)






def validate_contact_number(value):
    """
    Indian + International phone numbers
    """
    indian_pattern = r'^[6-9][0-9]{9}$'
    international_pattern = r'^\+?[0-9\s\-]{7,20}$'

    if not re.fullmatch(indian_pattern, value) and not re.fullmatch(international_pattern, value):
        raise ValidationError(
            "Enter a valid phone number (Indian 10-digit or international format)."
        )

def validate_email_address(value):
    """Allow any valid email address"""
    email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

    if not re.fullmatch(email_pattern, value):
        raise ValidationError("Enter a valid email address.")

def validate_url(value):
    if value and not value.startswith(("http://", "https://")):
        raise ValidationError("Enter a valid URL starting with http:// or https://")


class CompanyDetails(models.Model):
    companyname = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, validators=[validate_contact_number])
    email = models.EmailField(validators=[validate_email_address])

    twitter = models.URLField(blank=True, null=True, validators=[validate_url])
    instagram = models.URLField(blank=True, null=True, validators=[validate_url])
    youtube = models.URLField(blank=True, null=True, validators=[validate_url])
    linkedin = models.URLField(blank=True, null=True, validators=[validate_url])
    facebook = models.URLField(blank=True, null=True, validators=[validate_url])

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Detail"
        verbose_name_plural = "Company Details"

    def __str__(self):
        return self.companyname

    def save(self, *args, **kwargs):
        if not self.pk and CompanyDetails.objects.exists():
            raise ValidationError("Only one CompanyDetails instance is allowed.")
        return super().save(*args, **kwargs)


class ColorSettings(models.Model):
    primary = ColorField(default='#FF3E41')      # from :root
    secondary = ColorField(default='#51CFED')    # from :root
    light = ColorField(default='#F8F2F0')        # from :root
    dark = ColorField(default='#060315')         # from :root

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Color Setting"
        verbose_name_plural = "Color Settings"

    def __str__(self):
        return "Website Color Theme"

    def save(self, *args, **kwargs):
        # Allow only one instance
        if not self.pk and ColorSettings.objects.exists():
            raise ValidationError("Only one ColorSettings instance is allowed.")
        return super().save(*args, **kwargs)