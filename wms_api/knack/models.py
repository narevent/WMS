# knack/models.py
from django.db import models
from PIL import Image
from tinymce.models import HTMLField


class Instrument(models.Model):
    naam = models.CharField(max_length=128, unique=True)
    beschrijving = HTMLField(blank=True)
    image = models.ImageField(default="default.jpg", upload_to="instrument")
    link = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["naam"]
        verbose_name_plural = 'Instrumenten'

    def __str__(self):
        return self.naam


class LesType(models.Model):
    naam = models.CharField(max_length=128, blank=True, unique=True)
    soort = models.CharField(max_length=12)
    duur = models.PositiveSmallIntegerField(default=30)
    aantal = models.PositiveSmallIntegerField(default=38)
    prijs_ex = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prijs_inc = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    beschrijving = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["soort", "duur"]

    def __str__(self):
        return f"{self.naam}"


class LesTarief(models.Model):
    type = models.ForeignKey(LesType, on_delete=models.CASCADE)
    prijs_ex = models.DecimalField(max_digits=10, decimal_places=2)
    prijs_inc = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "lestarieven"
        ordering = ["type__soort", "prijs_ex"]

    def __str__(self):
        return f"{self.type} - €{self.prijs_inc}"


class Locatie(models.Model):
    naam = models.CharField(max_length=128, blank=True, null=True)
    adres = models.CharField(max_length=128, blank=True, null=True)
    kaart = models.URLField(max_length=256, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["naam"]

    def __str__(self):
        return self.naam


class Docent(models.Model):
    naam = models.CharField(max_length=128)
    instrumenten = models.ManyToManyField(Instrument, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="docenten")
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["naam"]
        verbose_name_plural = 'Docenten'

    def __str__(self):
        return self.naam

