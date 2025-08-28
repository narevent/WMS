# agenda/models.py
from django.db import models
from PIL import Image
from tinymce.models import HTMLField


class Post(models.Model):
    titel = models.CharField(max_length=100)
    image = models.ImageField(default="default.jpg", upload_to="agenda", blank=True, null=True)
    content = HTMLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titel

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        resolution = 1024
        if img.height > resolution or img.width > resolution:
            output_size = (resolution, resolution)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Event(models.Model):
    titel = models.CharField(max_length=100)
    datum = models.DateField()
    aanvang = models.TimeField()
    start = models.TimeField()
    image = models.ImageField(default="default.jpg", upload_to="event")
    beschrijving = HTMLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titel

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        resolution = 1024
        if img.height > resolution or img.width > resolution:
            output_size = (resolution, resolution)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Vakantie(models.Model):
    naam = models.CharField(max_length=128)
    start = models.DateField(auto_now=False, auto_now_add=False)
    eind = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.naam
