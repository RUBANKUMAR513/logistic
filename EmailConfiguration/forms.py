from django import forms
from django.core.exceptions import ValidationError
from .models import Setting, ToEmail

class SettingForm(forms.ModelForm):
    class Meta:
        model = Setting
        fields = ['host', 'port', 'email', 'password', 'status']

    def clean(self):
        cleaned_data = super().clean()
        
        # Ensure only one Setting instance exists
        if not self.instance.pk and Setting.objects.exists():
            raise forms.ValidationError({
                '__all__': 'Only one instance of Setting is allowed. Please edit the existing one instead of creating a new instance.'
            })
        
        return cleaned_data



class ToEmailForm(forms.ModelForm):
    class Meta:
        model = ToEmail
        fields = ['name', 'email', 'phonenumber', 'position', 'active_status']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if ToEmail.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                f'A ToEmail entry with the name "{name}" already exists.'
            )
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if ToEmail.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                f'A ToEmail entry with the email "{email}" already exists.'
            )
        return email

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        if ToEmail.objects.filter(phonenumber=phonenumber).exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                f'A ToEmail entry with the phone number "{phonenumber}" already exists.'
            )
        return phonenumber

    def clean(self):
        cleaned_data = super().clean()
        # ❌ Removed 5-instance limit check
        return cleaned_data
