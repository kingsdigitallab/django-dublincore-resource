from django.db import models
from django.conf import settings
from .settings import get_var
from controlled_vocabulary.models import (
    ControlledTermField, ControlledTermsField
)

LENGTH_LABEL = 200
LENGTH_LABEL_LONG = 500
LENGTH_DATE = 30
LENGTH_IDENTIFIER = 50

FIELD_OPTIONAL = dict(blank=True, null=False, default='')


def get_upload_path(instance, filename):
    # TODO: increase counter to avoid overwriting file with same name
    ret = '{}/{}'.format(
        get_var('UPLOAD_PATH').rstrip('/'),
        filename
    )
    return ret


class DublinCoreAgent(models.Model):
    '''A person or an association'''
    full_name = models.CharField(
        max_length=LENGTH_LABEL
    )
    identifier = models.URLField(
        max_length=LENGTH_LABEL_LONG, **FIELD_OPTIONAL
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Dublin Core Agent'
        verbose_name_plural = 'Dublin Core Agents'


class DublinCoreRights(models.Model):
    '''Information about rights held in and over the resource.'''
    shorthand = models.CharField(
        max_length=LENGTH_IDENTIFIER, **FIELD_OPTIONAL
    )
    statement = models.TextField()

    def __str__(self):
        return self.shorthand or 'Rights record #{}'.format(self.id)

    class Meta:
        verbose_name = 'Dublin Core Rights'
        verbose_name_plural = 'Dublin Core Rights'


class AbstractDublinCoreResource(models.Model):
    '''
    A Dublin Core Resource
    https://www.dublincore.org/specifications/dublin-core/dcmi-terms/

    https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    Almost all Dublin Core Elements (dc:) are represented by a Django field of
    the same name.
    Except for the use of plural for multi-valued fields, e.g. creators.

    https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-2
    Some additional terms are also implemented as fields:
    dcterms:issued, dcterms:isPartOf, dcterms:spatial, dcterms:temporal,
    dcterms:bibliographicCitation
    '''

    # Identifying information
    # dc:identifier
    identifier = models.CharField(
        max_length=LENGTH_LABEL, **FIELD_OPTIONAL,
        help_text='''A code or URL that uniquely identifies the resource within a referencial system. It should be compact, widely recognised and as stable as possible (i.e. it will never change in the future). e.g. ISBN:1-56592-149-6'''
    )
    # dc:title
    title = models.CharField(
        max_length=LENGTH_LABEL_LONG,
        help_text='''A name given to the resource.'''
    )
    # dc:date
    date = models.CharField(
        max_length=LENGTH_DATE,
        help_text='''The point or period in time the resource was created or made available. Not necessarily the same as 'temporal' column (see below).''',
        **FIELD_OPTIONAL
    )
    # dc:issued
    issued = models.CharField(
        max_length=LENGTH_DATE,
        help_text='''Date of formal issuance (e.g., publication) of the resource.''',
        **FIELD_OPTIONAL
    )
    # dcterms:isPartOf
    # Useful for bibliographic citations (e.g. article in a journal)
    # We don't use a foreign key as the referenced resource may not be recorded
    # in this database.
    is_part_of = models.CharField(
        max_length=LENGTH_LABEL,
        help_text='''A related resource in which the described resource is physically or logically included.''',
        **FIELD_OPTIONAL
    )
    # dcterms:bibliographicCitation (refinement of dc:identifier)
    bibliographic_citation = models.TextField(
        help_text='''A bibliographic reference for the resource.''',
        ** FIELD_OPTIONAL
    )

    # Agents
    # dc:creator
    creators = models.ManyToManyField(
        DublinCoreAgent,
        blank=True,
        related_name='created_resources',
        help_text='''The person or organization primarily responsible for creating the intellectual content of the resource.'''
    )
    # dc:contributor
    contributors = models.ManyToManyField(
        DublinCoreAgent,
        blank=True,
        related_name='contributed_resources',
        help_text='''A person or organization not specified in a Creator element who has made significant intellectual contributions to the resource but whose contribution is secondary to any person or organization specified in a Creator element'''
    )
    # dc:publisher
    publisher = models.ForeignKey(
        DublinCoreAgent,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='published_resources',
        help_text='''An entity responsible for making the resource available.'''
    )

    # dc:rights
    rights = models.ForeignKey(
        DublinCoreRights,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='resources',
        help_text='''A rights management statement, an identifier that links to a rights management statement, or an identifier that links to a service providing information about rights management for the resource.'''
    )

    # Content description
    # dc:description
    description = models.TextField(
        help_text='''An account of the resource (e.g. abstract, summary). One or more sentences.''',
        **FIELD_OPTIONAL
    )
    # dc:subject
    subjects = ControlledTermsField(
        'fast-topic', blank=True,
        help_text='''The topic of the resource.'''
    )
    # dc:coverage
    # Note: better to split temporal and spatial coverage into the
    # refined fields instead of using this field.
    coverage = models.CharField(
        max_length=LENGTH_LABEL, **FIELD_OPTIONAL,
        help_text='''The spatial or temporal topic of the resource.'''
    )
    # dcterms:spatial (refinement of dc:coverage)
    spatial = ControlledTermField(
        'wikidata', null=True, blank=True,
        help_text='''The location or geographic scope of the resource's content.'''
    )
    # dcterms:temporal (refinement of dc:coverage)
    temporal = models.CharField(
        max_length=LENGTH_LABEL, **FIELD_OPTIONAL,
        help_text='''The date or period in history the resource refers to.'''
    )
    # dc:language
    languages = ControlledTermsField(
        'iso639-2', blank=True,
        help_text='''The primary language of the resource.'''
    )

    # dc:type
    type = ControlledTermField(
        'dcmitype', null=True, blank=True,
        help_text='''The nature or genre of the resource.'''
    )
    # dc:format
    format = ControlledTermField(
        'mime', null=True, blank=True,
        help_text='''The physical or digital manifestation of the resource.'''
    )

    # Other terms
    # dc:source
    # Note that this and dc:related are very vague. It is usually better
    # to use more specific properties, e.g. dcterms:isPartOf
    source = models.CharField(
        max_length=LENGTH_LABEL, **FIELD_OPTIONAL,
        help_text='''A related resource from which the described resource is derived.'''
    )

    # NON DC fields:
    attachment = models.FileField(
        upload_to=get_upload_path, **FIELD_OPTIONAL
    )

    class Meta:
        abstract = True
        verbose_name = 'Dublin Core Resource'
        verbose_name_plural = 'Dublin Core Resources'

    def __str__(self):
        ret = self.title
        if self.date:
            ret += ' ({})'.format(self.date)
        return ret


if not get_var('ABSTRACT_ONLY'):
    class DublinCoreResource(AbstractDublinCoreResource):
        pass
