# activiteiten/admin.py
from django.contrib import admin
from .models import (
    Cursus,
    Workshop,
    Project,
    Groep,
)

admin.site.site_header = "WMS Admin"
admin.site.site_title = "WMS Admin Portal"
admin.site.index_title = "Welkom bij WMS Admin Portal"


@admin.register(Cursus)
class CursusAdmin(admin.ModelAdmin):
    list_display = ["naam", "prijs", "duur", "is_active", "created_at"]
    list_filter = ["is_active", "instrumenten", "created_at"]
    search_fields = ["naam", "beschrijving"]
    filter_horizontal = ["instrumenten"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active", "prijs"]


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ["naam", "prijs", "duur", "is_active", "created_at"]
    list_filter = ["is_active", "instrumenten", "created_at"]
    search_fields = ["naam", "beschrijving"]
    filter_horizontal = ["instrumenten"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active", "prijs"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'naam',
        'start',
        'end',
        'prijs',
        'duur',
        'is_upcoming',
        'is_ongoing',
    )

    list_filter = (
        'start',
        'end',
    )

    search_fields = (
        'naam',
        'beschrijving',
    )

    readonly_fields = (
        'is_upcoming',
        'is_ongoing',
    )

    fieldsets = (
        (None, {
            'fields': ('naam', 'instrumenten', 'beschrijving', 'image', 'link')
        }),
        ('Project Details', {
            'fields': ('start', 'end', 'prijs', 'duur')
        }),
        ('Status', {
            'fields': ('is_upcoming', 'is_ongoing'),
            'description': 'Current status of the project based on dates.',
        }),
    )


@admin.register(Groep)
class GroepAdmin(admin.ModelAdmin):
    list_display = ["naam", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["naam", "beschrijving"]
    readonly_fields = ["created_at", "updated_at"]
    list_editable = ["is_active"]
    