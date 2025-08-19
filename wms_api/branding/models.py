from django.db import models

class BrandingAsset(models.Model):
    logo = models.ImageField(upload_to="branding/logos/")
    icon = models.ImageField(upload_to="branding/icons/", null=True, blank=True)
    font_file = models.FileField(upload_to="branding/fonts/", null=True, blank=True)

    def __str__(self):
        return f'{self.logo}'.split('/')[-1]

class DesignPattern(models.Model):
    name = models.CharField(max_length=64, default="schema")
    primary_color = models.CharField(max_length=7, default="#000000")
    secondary_color = models.CharField(max_length=7, default="#FFFFFF")
    accent_color = models.CharField(max_length=7, blank=True, null=True)
    font_family = models.CharField(max_length=100, default="Arial")

    def __str__(self):
        return f'{self.name}_{self.pk}'