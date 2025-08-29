from tinymce.models import HTMLField
from django.utils import timezone
from django.db import models
from knack.models import Instrument
from muziekschool.models import BaseModel

class Cursus(BaseModel):
    naam = models.CharField(max_length=128)
    instrumenten = models.ManyToManyField(Instrument, blank=True)
    beschrijving = HTMLField()
    prijs = models.FloatField()
    duur = models.CharField(max_length=128)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="cursus")

    class Meta:
        verbose_name = "Cursus"
        verbose_name_plural = "Cursussen"
        ordering = ["naam"]

    def __str__(self):
        return self.naam


class Workshop(BaseModel):
    naam = models.CharField(max_length=128)
    instrumenten = models.ManyToManyField(Instrument, blank=True)
    beschrijving = HTMLField()
    prijs = models.FloatField()
    duur = models.CharField(max_length=128)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="workshop")

    class Meta:
        verbose_name = "Workshop"
        verbose_name_plural = "Workshops"
        ordering = ["naam"]

    def __str__(self):
        return self.naam


class Project(models.Model):
    naam = models.CharField(max_length=128)
    instrumenten = models.ManyToManyField(Instrument, blank=True)
    beschrijving = HTMLField()
    prijs = models.FloatField()
    duur = models.CharField(max_length=128)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(default="branding/default.jpg", upload_to="project")
    start = models.DateField()
    end = models.DateField()

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projecten"
        ordering = ["start", "naam"]

    def __str__(self):
        return self.naam

    @property
    def is_upcoming(self):
        if self.start:
            return self.start > timezone.now().date()
        return False

    @property
    def is_ongoing(self):
        today = timezone.now().date()
        if self.start and self.end:
            return self.start <= today <= self.end
        return False

class Groep(BaseModel):
    naam = models.CharField(max_length=128)
    beschrijving = HTMLField()
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="groep")

    class Meta:
        verbose_name = "Groep"
        verbose_name_plural = "Groepen"
        ordering = ["naam"]

    def __str__(self):
        return self.naam