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


class DublinCoreResourceAdminForm(forms.ModelForm):
    class Meta:
        model = DublinCoreResource
        fields = ['title', 'type', 'language', 'identifier', 'description',
                  'creators', 'contributors', 'publisher']
        widgets = {
            'language': ControlledTermWidget(
                DublinCoreResource.language.field.remote_field,
                admin.site,
                'iso639-2'
            ),
            'type': ControlledTermWidget(
                DublinCoreResource.type.field.remote_field,
                admin.site,
                'dcmitype'
            )
        }


@admin.register(DublinCoreResource)
class DublinCoreResource(admin.ModelAdmin):
    form = DublinCoreResourceAdminForm

    list_display = ['id', 'title', 'date', 'type']
    list_display_links = ['id', 'title']
    search_fields = ['identifier', 'title', 'description']
    list_filter = ['type', 'language']

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
            'fields': ('description', 'subject', 'spatial', 'temporal',
                       'language')
        }),
        ('Type & format', {
            'fields': ('type', 'format')
        }),
        ('Rights', {
            'fields': ('rights',)
        }),
    )
