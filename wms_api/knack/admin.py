# knack/admin.py
from django.contrib import admin
from .models import Instrument, LesType, LesTarief, Locatie, Docent


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ["naam", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["naam", "beschrijving"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(LesType)
class LesTypeAdmin(admin.ModelAdmin):
    list_display = ["naam", "soort", "duur", "aantal", "beschrijving", "is_active"]
    list_filter = ["is_active", "duur"]
    search_fields = ["soort", "beschrijving"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(LesTarief)
class LesTariefAdmin(admin.ModelAdmin):
    list_display = ["type", "prijs_ex", "prijs_inc", "is_active"]
    list_filter = ["is_active", "type"]
    search_fields = ["type__soort"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Locatie)
class LocatieAdmin(admin.ModelAdmin):
    list_display = ["naam", "adres", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["naam", "adres"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Docent)
class DocentAdmin(admin.ModelAdmin):
    list_display = ["naam", "is_active", "created_at"]
    list_filter = ["is_active", "instrumenten", "created_at"]
    search_fields = ["naam", "bio"]
    filter_horizontal = ["instrumenten"]
    readonly_fields = ["created_at", "updated_at"]
