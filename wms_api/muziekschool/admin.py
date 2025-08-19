# muziekschool/admin.py
from django.contrib import admin
from .models import (
    Over,
    Vacature,
    Contact,
    Header,
    Banner,
)

admin.site.site_header = "WMS Admin"
admin.site.site_title = "WMS Admin Portal"
admin.site.index_title = "Welkom bij WMS Admin Portal"


@admin.register(Over)
class OverAdmin(admin.ModelAdmin):
    list_display = ["titel", "is_active", "created_at", "updated_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["titel", "info"]
    readonly_fields = ["created_at", "updated_at"]

@admin.register(Vacature)
class VacatureAdmin(admin.ModelAdmin):
    list_display = ["functie", "deadline", "is_active", "is_open", "created_at"]
    list_filter = ["is_active", "instrumenten", "deadline", "created_at"]
    search_fields = ["functie", "beschrijving"]
    filter_horizontal = ["instrumenten"]
    readonly_fields = ["created_at", "updated_at", "is_open"]
    list_editable = ["is_active", "deadline"]

    def is_open(self, obj):
        return obj.is_open

    is_open.boolean = True
    is_open.short_description = "Open"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["organisatie", "adres", "plaats", "email", "telefoon", "is_active"]
    list_filter = ["is_active", "plaats"]
    search_fields = ["organisatie", "adres", "plaats", "email"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active"]


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ["titel", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["titel", "info"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active"]

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ["titel", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["titel", "info"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active"]