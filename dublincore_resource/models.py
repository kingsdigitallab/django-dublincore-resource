from django.db import models
from django.conf import settings
from controlled_vocabulary.models import ControlledTermField

LENGTH_LABEL = 200
LENGTH_DATE = 30
LENGTH_IDENTIFIER = 50
# TODO: make that a config setting
LOCAL_VOCABULARY_BASE_URL = 'http://localhost:8000/vocabularies'

FIELD_OPTIONAL = dict(blank=True, null=False, default='')
DUBLINCORE_RESOURCE_ABSTRACT_ONLY = getattr(
    settings, 'DUBLINCORE_RESOURCE_ABSTRACT_ONLY', False)
DUBLINCORE_RESOURCE_UPLOAD_PATH = getattr(
    settings, 'DUBLINCORE_RESOURCE_UPLOAD_PATH',
    'uploads/dublin_core/'
)


def get_upload_path(instance, filename):
    # TODO: increase counter to avoid overwriting file with same name
    ret = '{}/{}'.format(
        DUBLINCORE_RESOURCE_UPLOAD_PATH.rstrip('/'),
        filename
    )
    return ret


class DublinCoreAgent(models.Model):
    '''A person or an association'''
    full_name = models.CharField(
        max_length=200
    )
    identifier = models.URLField(
        max_length=300, **FIELD_OPTIONAL
    )

    def __str__(self):
        return self.full_name


class DublinCoreRights(models.Model):
    '''Information about rights held in and over the resource.'''
    shorthand = models.CharField(
        max_length=LENGTH_IDENTIFIER, **FIELD_OPTIONAL
    )
    statement = models.TextField()

    def __str__(self):
        return self.short_hand or 'Rights record #{}'.format(self.id)


class AbstractDublinCoreResource(models.Model):
    '''
    Simplifications:
    * only a few DC elements are multi-valued

    '''
    identifier = models.CharField(
        max_length=LENGTH_LABEL, **FIELD_OPTIONAL,
        help_text='''A code or URL that uniquely identifies the resource within a referencial system. It should be compact, widely recognised and as stable as possible (i.e. it will never change in the future). e.g. ISBN:1-56592-149-6'''
    )
    title = models.CharField(
        max_length=300,
        help_text='''A name given to the resource.'''
    )
    date = models.CharField(
        max_length=LENGTH_DATE,
        help_text='''The point or period in time the resource was created or made available. Not necessarily the same as 'temporal' column (see below).''',
        **FIELD_OPTIONAL
    )
    bibliographic_citation = models.TextField(
        help_text='''A bibliographic reference for the resource.''',
        ** FIELD_OPTIONAL
    )

    # agents
    creators = models.ManyToManyField(
        DublinCoreAgent,
        blank=True,
        related_name='created_resources',
        help_text='''The person or organization primarily responsible for creating the intellectual content of the resource.'''
    )
    contributors = models.ManyToManyField(
        DublinCoreAgent,
        blank=True,
        related_name='contributed_resources',
        help_text='''A person or organization not specified in a Creator element who has made significant intellectual contributions to the resource but whose contribution is secondary to any person or organization specified in a Creator element'''
    )
    publisher = models.ForeignKey(
        DublinCoreAgent,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='published_resources',
        help_text='''An entity responsible for making the resource available.'''
    )

    rights = models.ForeignKey(
        DublinCoreRights,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='resources',
        help_text='''A rights management statement, an identifier that links to a rights management statement, or an identifier that links to a service providing information about rights management for the resource.'''
    )

    # content description
    # TODO: multivalued
    description = models.TextField(
        help_text='''An account of the resource (e.g. abstract, summary). One or more sentences.''',
        **FIELD_OPTIONAL
    )
    subject = ControlledTermField(
        '', null=True, blank=True,
        help_text='''The topic of the resource.'''
    )
    spatial = ControlledTermField(
        'geonames', null=True, blank=True,
        help_text='''The location or geographic scope of the resource's content.'''
    )
    temporal = models.CharField(
        max_length=LENGTH_LABEL, **FIELD_OPTIONAL,
        help_text='''The date or period in history the resource refers to.'''
    )
    language = ControlledTermField(
        'iso639-2', null=True, blank=True,
        help_text='''The primary language of the resource.'''
    )

    # type and formats
    type = ControlledTermField(
        'dcmitype', null=True, blank=True,
        help_text='''The nature or genre of the resource.'''
    )
    format = ControlledTermField(
        'format', null=True, blank=True,
        help_text='''The physical or digital manifestation of the resource.'''
    )
    # TODO: add this field
    # source = models.CharField(max_length=200)

    # NON DC fields:
    attachment = models.FileField(
        upload_to=get_upload_path, **FIELD_OPTIONAL
    )

    class Meta:
        abstract = True
        # ordering = ['prefix']
        # verbose_name_plural = 'Controlled vocabularies'

    def __str__(self):
        ret = self.title
        if self.date:
            ret += ' ({})'.format(self.date)
        return ret


if not DUBLINCORE_RESOURCE_ABSTRACT_ONLY:
    class DublinCoreResource(AbstractDublinCoreResource):
        pass
