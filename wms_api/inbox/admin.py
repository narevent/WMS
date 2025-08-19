# inbox/admin.py
from django.contrib import admin
from .models import Bericht, Proefles, Betalingsplichtige, Inschrijving


@admin.register(Bericht)
class BerichtAdmin(admin.ModelAdmin):
    list_display = ["naam", "email", "created_at", "is_read"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["naam", "email", "bericht"]
    readonly_fields = ["created_at"]
    actions = ["mark_as_read"]

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_as_read.short_description = "Mark selected messages as read"


@admin.register(Proefles)
class ProeflesAdmin(admin.ModelAdmin):
    list_display = ["naam", "instrument", "email", "telefoon", "status", "created_at"]
    list_filter = ["status", "instrument", "created_at"]
    search_fields = ["naam", "email", "telefoon"]
    readonly_fields = ["created_at"]


@admin.register(Betalingsplichtige)
class BetalingsplichtigenAdmin(admin.ModelAdmin):
    list_display = ["initialen", "achternaam", "plaats", "haarlempas", "akkoord"]
    list_filter = ["haarlempas", "akkoord", "plaats"]
    search_fields = ["initialen", "achternaam", "adres", "plaats"]


@admin.register(Inschrijving)
class InschrijvingAdmin(admin.ModelAdmin):
    list_display = [
        "voornaam",
        "achternaam",
        "instrument",
        "lestype",
        "status",
        "created_at",
    ]
    list_filter = ["status", "instrument", "lestype", "huren", "created_at"]
    search_fields = ["voornaam", "achternaam", "email", "telefoon"]
    readonly_fields = ["created_at"]
