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
        max_length=LENGTH_LABEL, **FIELD_OPTIONAL
    )
    title = models.CharField(max_length=300)
    date = models.CharField(max_length=LENGTH_DATE, **FIELD_OPTIONAL)
    creators = models.ManyToManyField(
        DublinCoreAgent,
        blank=True,
        related_name='created_resources'
    )
    contributors = models.ManyToManyField(
        DublinCoreAgent,
        blank=True,
        related_name='contributed_resources'
    )
    publisher = models.ForeignKey(
        DublinCoreAgent,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='published_resources',
    )
    rights = models.ForeignKey(
        DublinCoreRights,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='resources',
    )
    # TODO: multivalued
    subject = ControlledTermField(
        'controlled_vocabulary.ControlledTerm',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    description = models.TextField(**FIELD_OPTIONAL)
    spatial = ControlledTermField(
        'controlled_vocabulary.ControlledTerm',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    temporal = models.CharField(max_length=LENGTH_LABEL, **FIELD_OPTIONAL)
    type = ControlledTermField(
        'controlled_vocabulary.ControlledTerm',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    language = ControlledTermField(
        'controlled_vocabulary.ControlledTerm',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    bibliographic_citation = models.TextField(
        **FIELD_OPTIONAL
    )
    format = ControlledTermField(
        'controlled_vocabulary.ControlledTerm',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )
    # TODO: add this field
    # source = models.CharField(max_length=200)

    # NON DC fields:
    attachment = models.FileField(upload_to=get_upload_path, **FIELD_OPTIONAL)

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
