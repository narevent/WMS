# stichting/admin.py
from django.contrib import admin
from .models import (
    Overeenkomst,
    Sponsor,
    Anbi,
    Document,
)

admin.site.site_header = "WMS Admin"
admin.site.site_title = "WMS Admin Portal"
admin.site.index_title = "Welkom bij WMS Admin Portal"

@admin.register(Overeenkomst)
class OvereenkomstAdmin(admin.ModelAdmin):
    list_display = ["naam", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["naam", "beschrijving"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active"]


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ["naam", "priority", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["naam", "beschrijving"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active", "priority"]


@admin.register(Anbi)
class AnbiAdmin(admin.ModelAdmin):
    list_display = ["jaar", "is_active", "created_at"]
    list_filter = ["is_active", "jaar", "created_at"]
    search_fields = ["beschrijving"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active"]

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "created_at"]
    list_filter = ["title", "created_at"]
    readonly_fields = ["created_at", "updated_at"]
    