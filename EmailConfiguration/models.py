from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_migrate
from django.dispatch import receiver



class Setting(models.Model):
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and Setting.objects.exists():
            raise ValidationError('There can be only one instance of Settings.')
        super(Setting, self).save(*args, **kwargs)

    def __str__(self):
        return self.email


@receiver(post_migrate)
def create_default_setting(sender, **kwargs):
    # Only create default if `Setting` model exists and has no entries
    if sender.name == 'EmailConfiguration':  # Replace 'your_app_name' with your app's name
        if not Setting.objects.exists():
            Setting.objects.create(
                host='smtp.gmail.com',
                port=587,
                email='rubanfebinosolutions@gmail.com',
                password='aijb eiho aoqo gvmf',
                status=True
            )

    

class ToEmail(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    phonenumber = models.CharField(max_length=15, unique=True)
    position = models.CharField(max_length=100)
    active_status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Ensure default instance behavior
        if self.pk == 1:
            self.active_status = True

        # Duplicate validation (safe for updates)
        if ToEmail.objects.filter(name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(f'A ToEmail entry with the name "{self.name}" already exists.')

        if ToEmail.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError(f'A ToEmail entry with the email "{self.email}" already exists.')

        if ToEmail.objects.filter(phonenumber=self.phonenumber).exclude(pk=self.pk).exists():
            raise ValidationError(f'A ToEmail entry with the phone number "{self.phonenumber}" already exists.')

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.pk == 1:
            raise ValidationError("The default ToEmail instance cannot be deleted.")
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

# Signal to create default instance after migration
@receiver(post_migrate)
def create_default_toemail_instance(sender, **kwargs):
    if sender.name == 'EmailConfiguration':  # Replace 'your_app_name' with the actual app name
        if not ToEmail.objects.exists():
            ToEmail.objects.create(
                name="RUBAN KUMAR K",
                email="ceeeerubankumark513@gmail.com",
                phonenumber="6383817659",
                position="Developer",
                active_status=True
            )

class ClientMessage(models.Model):
    client_name = models.CharField(max_length=100)
    client_mail = models.EmailField()

    company_name = models.CharField(max_length=150, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    # No choices → fully dynamic
    service_type = models.CharField(max_length=50, null=True, blank=True)

    messages = models.TextField()
    receive_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} - {self.service_type or 'No Service'}"

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError("Updating ClientMessage is not allowed.")
        super().save(*args, **kwargs)

