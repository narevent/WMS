# stichting/models.py
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

class Overeenkomst(BaseModel):
    naam = models.CharField(max_length=128)
    beschrijving = HTMLField()
    document = models.FileField(upload_to="overeenkomsten", null=True, blank=True)

    class Meta:
        verbose_name = "Overeenkomst"
        verbose_name_plural = "Overeenkomsten"
        ordering = ["naam"]

    def __str__(self):
        return self.naam

class Sponsor(BaseModel):
    naam = models.CharField(max_length=128)
    link = models.URLField(null=True, blank=True)
    beschrijving = HTMLField()
    image = models.ImageField(default="default.jpg", upload_to="sponsor")
    priority = models.IntegerField(
        default=0, help_text="Hogere waarde = hogere prioriteit"
    )

    def __str__(self):
        return self.naam

    class Meta:
        verbose_name = "Sponsor"
        verbose_name_plural = "Sponsors"
        ordering = ["-priority"]


class Anbi(BaseModel):
    beleidsplan = models.FileField(upload_to="anbi", blank=True)
    beschrijving = HTMLField()
    jaar = models.IntegerField(help_text="Jaar van het beleidsplan")

    class Meta:
        verbose_name = "ANBI"
        verbose_name_plural = "ANBI documenten"
        ordering = ["-jaar"]

    def __str__(self):
        return f"ANBI {self.jaar}"

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)