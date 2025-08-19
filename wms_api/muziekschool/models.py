# muziekschool/models.py
from django.db import models
from knack.models import Instrument
from tinymce.models import HTMLField

class BaseModel(models.Model):
    """Abstract base model with common fields"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Over(BaseModel):
    titel = models.CharField(max_length=128)
    info = HTMLField()

    class Meta:
        verbose_name = "Over ons"
        verbose_name_plural = "Over ons"

    def __str__(self):
        return self.titel

class Vacature(BaseModel):
    functie = models.CharField(max_length=128)
    beschrijving = HTMLField()
    instrumenten = models.ManyToManyField(Instrument, blank=True)
    deadline = models.DateField(null=True, blank=True)
    salaris = models.CharField(max_length=128, blank=True)

    class Meta:
        verbose_name = "Vacature"
        verbose_name_plural = "Vacatures"
        ordering = ["functie"]

    def __str__(self):
        return self.functie

    @property
    def is_open(self):
        if not self.deadline:
            return True
        from django.utils import timezone

        return self.deadline > timezone.now().date()


class Contact(BaseModel):
    organisatie = models.CharField(max_length=128)
    adres = models.CharField(max_length=128)
    postcode = models.CharField(max_length=6)
    plaats = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    telefoon = models.CharField(max_length=128)
    kvk_nr = models.CharField(max_length=128, null=True, blank=True)
    btw_nr = models.CharField(max_length=128, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contactgegevens"

    def __str__(self):
        return f"{self.organisatie} - {self.adres}"


class Header(BaseModel):
    titel = models.CharField(max_length=128)
    info = HTMLField()
    background_image = models.ImageField(upload_to="headers", null=True, blank=True)

    class Meta:
        verbose_name = "Header"
        verbose_name_plural = "Headers"
        ordering = ["titel"]

    def __str__(self):
        return self.titel
    
class Banner(BaseModel):
    titel = models.CharField(max_length=128)
    info = HTMLField()
    background_image = models.ImageField(upload_to="banners", null=True, blank=True)
    banner_type = models.CharField(max_length=32, blank=True)

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banners"
        ordering = ["titel"]

    def __str__(self):
        return self.titel