# inbox/models.py
from django.db import models
from knack.models import Instrument, LesType


class Bericht(models.Model):
    naam = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    bericht = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "berichten"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.naam} - {self.email}"


class Proefles(models.Model):
    naam = models.CharField(max_length=100)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, null=True)
    telefoon = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "In behandeling"),
            ("scheduled", "Ingepland"),
            ("completed", "Voltooid"),
            ("cancelled", "Geannuleerd"),
        ],
        default="pending",
    )

    class Meta:
        verbose_name_plural = "proeflessen"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.naam} - {self.instrument}"


class Betalingsplichtige(models.Model):
    initialen = models.CharField(max_length=10)
    achternaam = models.CharField(max_length=100)
    adres = models.CharField(max_length=100)
    postcode = models.CharField(max_length=6)
    iban = models.CharField(max_length=100)
    plaats = models.CharField(max_length=100)
    haarlempas = models.BooleanField(default=False)
    akkoord = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "betalingsplichtigen"
        ordering = ["achternaam", "initialen"]

    def __str__(self):
        return f"{self.initialen} {self.achternaam}"


class Inschrijving(models.Model):
    voornaam = models.CharField(max_length=100)
    achternaam = models.CharField(max_length=100)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, null=True)
    lestype = models.ForeignKey(LesType, on_delete=models.CASCADE, null=True)
    email = models.EmailField(max_length=100)
    telefoon = models.CharField(max_length=20)
    geboortedatum = models.DateField(auto_now=False, auto_now_add=False)
    huren = models.BooleanField(default=False)
    betalingsplichtige = models.ForeignKey(Betalingsplichtige, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "In behandeling"),
            ("approved", "Goedgekeurd"),
            ("rejected", "Afgewezen"),
            ("active", "Actief"),
            ("inactive", "Inactief"),
        ],
        default="pending",
    )

    class Meta:
        verbose_name_plural = "inschrijvingen"
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.voornaam} {self.achternaam} - {self.instrument.naam if self.instrument else "Geen instrument"}'
