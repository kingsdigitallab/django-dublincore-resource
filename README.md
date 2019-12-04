# Django Dublin Core Resource

A Django model and admin interface to manage metadata about your resources using Dublin Core (DC) standard.

The approach taken by this app is to centralise all your resource metadata into a single table.

Most DC elements accepts only a single value to keep things simple.

# Data Models

* DublinCoreResource
  * each DC element is represented by a field
* DublinCoreAgent
  * represents a person or organisation
* DublinCoreRights
  * represents Rights statements that can be shared among your resources

# Features

* One centralised table for all your resource
* Standard Dublin Core elements/fields
* Easy lookup into authority lists / controlled vocabularies
* [TODO] smart bulk import/update from CSV
* [TODO] advanced input validations
* [TODO] customisable model
* [TODO] API / export into various standard formats
* [TODO] support for file attachment
* [TODO] support for geonames
* [TODO] support for bibliographic citation parsin
* [TODO] support for EDTF dates

# Set up

## Installation

TODO

## Configuration

TODO
