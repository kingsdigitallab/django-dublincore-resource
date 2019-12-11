from django.contrib import admin
from .models import DublinCoreResource, DublinCoreAgent, DublinCoreRights
from django import forms
from controlled_vocabulary.models import ControlledTermWidget

# TODO: define a ControlledTermField which this widget by default


@admin.register(DublinCoreAgent)
class DublinCoreAgentAdmin(admin.ModelAdmin):
    search_fields = ['full_name']


@admin.register(DublinCoreRights)
class DublinCoreRightsAdmin(admin.ModelAdmin):
    search_fields = ['shorthand']


@admin.register(DublinCoreResource)
class DublinCoreResource(admin.ModelAdmin):

    list_display = ['id', 'title', 'date', 'type']
    list_display_links = ['id', 'title']
    search_fields = ['identifier', 'title', 'description']
    list_filter = ['type', 'languages']

    autocomplete_fields = ['creators', 'contributors', 'publisher', 'rights']

    save_on_top = True

    fieldsets = (
        ('Identification', {
            'fields': ('identifier', 'title', 'date', 'bibliographic_citation')
        }),
        ('Agents', {
            'fields': ('creators', 'contributors', 'publisher')
        }),
        ('Content', {
            'fields': ('description', 'subjects', 'spatial', 'temporal',
                       'languages')
        }),
        ('Type & format', {
            'fields': ('type', 'format')
        }),
        ('Rights', {
            'fields': ('rights',)
        }),
    )
