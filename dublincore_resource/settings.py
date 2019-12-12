from django.conf import settings
import os

'''
Default settings for the dublincore-resource app
All settings variables can be overridden in your django project settings.py
'''

# Set to True to disable the DublinCoreResource model and define your own
DUBLINCORE_RESOURCE_ABSTRACT_ONLY = False

# The path where resource file are uploaded, relative to your MEDIA path
DUBLINCORE_RESOURCE_UPLOAD_PATH = 'uploads/dublin_core/'


def get_var(name):
    '''
    Returns the value of a settings variable.
    The full name is DUBLINCORE_RESOURCE_ + name.
    First look into django settings.
    If not found there, use the value defined in this file.
    '''
    full_name = 'DUBLINCORE_RESOURCE_' + name
    ret = globals().get(full_name, None)
    ret = getattr(settings, full_name, ret)
    return ret
