# agenda/admin.py
from django.contrib import admin
from .models import Post, Event, Vakantie


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["titel", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["titel", "content"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["titel", "datum", "aanvang", "start"]
    list_filter = ["datum", "created_at"]
    search_fields = ["titel", "beschrijving"]
    date_hierarchy = "datum"
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Vakantie)
class VakantieAdmin(admin.ModelAdmin):
    list_display = ["naam", "start", "eind"]
    list_filter = ["start", "eind"]
    search_fields = ["naam"]
    date_hierarchy = "start"
