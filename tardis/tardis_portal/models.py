#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2010, Monash e-Research Centre
#   (Monash University, Australia)
# Copyright (c) 2010, VeRSI Consortium
#   (Victorian eResearch Strategic Initiative, Australia)
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    *  Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    *  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    *  Neither the name of the VeRSI, the VeRSI Consortium members, nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import SafeUnicode


class UserProfile(models.Model):
    """
    UserProfile class is an extension to the Django standard user model.

    :attribute authcate_user: is the user an external user
    :attribute user: a forign key to the :class:`django.contrib.auth.models.User`
    """

    authcate_user = models.BooleanField()
    user = models.ForeignKey(User, unique=True)


class XSLT_docs(models.Model):

    xmlns = models.URLField(max_length=255, primary_key=True)
    data = models.TextField()

    def __unicode__(self):
        return self.xmlns


class Author(models.Model):
    """Author's are researchers associated with an experiment that do not have a TARDIS account.

Fields:

name
    Author's full name"""

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Experiment(models.Model):
    """The Experiment is TARDIS' top level representation of data.  Experiments are composed of a number of Datasets, each of which contains any number of Datafiles.

Fields:

url

approved

title
    Short name of the Experiment

institution_name
    The institution or facility where the Experiment was conducted.

description
    The description, or abstract, describing the Experiment.

start_time
    The timestamp indicating the date the experiment was started.

end_time
    The timestamp indicating the date the experiment was completed.
created_time
    Auto-generated, the timestamp indicating the date / time the experiment was created, typically when metadata was uploaded in to TARDIS.

update_time
    Auto-generated, the timestamp indicating the date / time that the experiment was last modified.

created_by
    The User account used to initially upload the Experiment.

handle
    ???

public
    Boolean flag indicating whether the Experiment is publically accessible."""

    url = models.URLField(verify_exists=False, max_length=255)
    approved = models.BooleanField()
    title = models.CharField(max_length=400)
    institution_name = models.CharField(max_length=400)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(null=True, blank=True,
        auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)
    handle = models.TextField(null=True, blank=True)
    public = models.BooleanField()

    def __unicode__(self):
        return self.title


class Experiment_Owner(models.Model):

    experiment = models.ForeignKey(Experiment)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return SafeUnicode(self.experiment.id) + ' | ' \
            + SafeUnicode(self.user.username)


class Author_Experiment(models.Model):

    experiment = models.ForeignKey(Experiment)
    author = models.ForeignKey(Author)
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return SafeUnicode(self.author.name) + ' | ' \
            + SafeUnicode(self.experiment.id) + ' | ' \
            + SafeUnicode(self.order)

    class Meta:
        ordering = ['order']
        unique_together = (('experiment', 'author'),)


class Dataset(models.Model):
    """The Dataset groups Datafiles together.  TARDIS doesn't place any interpretation on the meaning of the group, which should be meaningful to the researcher.

Examples of groups include:

 * Experimental Data, Derived Data, Final Data
 * Grouped by equipment
 * Grouped by configuration (equipment settings)
 * Time sequence

The description should include enough information for the researcher to interpret the grouping.

Fields:

experiment
    The Experiment to which the Dataset belongs

description
    A free-format description of the Dataset"""

    experiment = models.ForeignKey(Experiment)
    description = models.TextField()

    def __unicode__(self):
        return self.description


class Dataset_File(models.Model):
    """A Dataset_File record is created for each file contained in the Experiment, and belongs to a single Dataset.

Fields:

dataset
    Foreign key to the containing Dataset

filename
    The name of the file :-)

url
    The location of the file.  (Add note about plugable protocol handling)

size
    The file size (in bytes?)

protocol
    The protocol used to download the file

created_time
    The creation date of the file(?)"""

    dataset = models.ForeignKey(Dataset)
    filename = models.CharField(max_length=400)
    url = models.URLField(max_length=400)
    size = models.CharField(blank=True, max_length=400)
    protocol = models.CharField(blank=True, max_length=10)
    created_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.filename


class Schema(models.Model):
    """A TARDIS schema is a named collection of Parameters that can be attached to an Experiment, Dataset or Datafile with a many-to-many relationship, e.g. each Experiment can have multiple ParameterSets, and each ParameterSet can be attached to multiple Experiments.

Fields:

namespace
    A URL that uniquely identifies the Schema.

name
    A user friendly name identifying the Schema.

type
    One of:

    * EQUIPMENT
    * DATASET
    * DATAFILE
    * GENERAL

    General Schema's may be attached to Equipment, Datasets or Datafiles.

subtype
    Used to group schema together when searching."""

    EXPERIMENT = 1
    DATASET = 2
    DATAFILE = 3
    GENERAL = 6
    _SCHEMA_TYPES = (
        (EXPERIMENT, 'Experiment schema'),
        (DATASET, 'Dataset schema'),
        (DATAFILE, 'Datafile schema'),
        (GENERAL, 'General schema'),
    )

    namespace = models.URLField(verify_exists=False, max_length=400)
    name = models.CharField(blank=True, null=True, max_length=50)
    type = models.IntegerField(
        choices=_SCHEMA_TYPES, default=EXPERIMENT)

    # subtype will be used for categorising the type of experiment, dataset
    # or datafile schemas. for example, the type of beamlines are usually used
    # further categorise the experiment, dataset, and datafile schemas. the
    # subtype might then allow for the following values: 'mx', 'ir', 'saxs'
    subtype = models.CharField(blank=True, null=True, max_length=30)

    def _getSchemaTypeName(self, typeNum):
        return dict(self._SCHEMA_TYPES)[typeNum]

    @classmethod
    def getSubTypes(cls):
        return set([schema.subtype for schema in Schema.objects.all() \
            if schema.subtype])

    @classmethod
    def getNamespaces(cls, type, subtype=None):
        """Return the list of namespaces for equipment, sample, and experiment
        schemas.

        """
        return [schema.namespace for schema in 
            Schema.objects.filter(type=type, subtype=subtype or '')]

    def __unicode__(self):
        return self._getSchemaTypeName(self.type) + (self.subtype and ' for ' +
            self.subtype.upper() or '') + ': ' + self.namespace

    def displayName(self):
        """displayName() returns a string that is user friendly to display"""
        if self.name is None:
            return self.namespace
        else:
            return self.name


    class UnsupportedType(Exception):
        def __init__(self, msg):
            Exception.__init__(self, msg)


class DatafileParameterSet(models.Model):
    schema = models.ForeignKey(Schema)

    # many to many link is needed so that sample and equipment parametersets
    # will be able to find datafiles they are linked to
    dataset_file = models.ManyToManyField(Dataset_File)

    def __unicode__(self):
        return "Datafile ParameterSet on " + self.schema.displayName()

    class Meta:
        ordering = ['id']


class DatasetParameterSet(models.Model):
    schema = models.ForeignKey(Schema)

    # many to many link is needed so that sample and equipment parametersets
    # will be able to find datasets they are linked to
    dataset = models.ManyToManyField(Dataset)

    def __unicode__(self):
        return "Dataset ParameterSet on " + self.schema.displayName()

    class Meta:
        ordering = ['id']


class ExperimentParameterSet(models.Model):
    schema = models.ForeignKey(Schema)

    # many to many link is needed so that sample and equipment parametersets
    # will be able to find experiments they are linked to
    experiment = models.ManyToManyField(Experiment)

    def __unicode__(self):
        return "Experiment ParameterSet on " + self.schema.displayName()

    class Meta:
        ordering = ['id']


class ParameterName(models.Model):

    EXACT_VALUE_COMPARISON = 1
    NOT_EQUAL_COMPARISON = 2
    RANGE_COMPARISON = 3
    GREATER_THAN_COMPARISON = 4
    GREATER_THAN_EQUAL_COMPARISON = 5
    LESS_THAN_COMPARISON = 6
    LESS_THAN_EQUAL_COMPARISON = 7
    CONTAINS_COMPARISON = 8
    __COMPARISON_CHOICES = (
        (EXACT_VALUE_COMPARISON, 'Exact value'),
        (CONTAINS_COMPARISON, 'Contains'),
        # TODO: enable this next time if i figure out how to support
        #(NOT_EQUAL_COMPARISON, 'Not equal'),
        (RANGE_COMPARISON, 'Range'),
        (GREATER_THAN_COMPARISON, 'Greater than'),
        (GREATER_THAN_EQUAL_COMPARISON, 'Greater than or equal'),
        (LESS_THAN_COMPARISON, 'Less than'),
        (LESS_THAN_EQUAL_COMPARISON, 'Less than or equal'),
    )

    schema = models.ForeignKey(Schema)
    name = models.CharField(max_length=60)
    full_name = models.CharField(max_length=60)
    units = models.CharField(max_length=60, blank=True)
    is_numeric = models.BooleanField()
    comparison_type = models.IntegerField(
        choices=__COMPARISON_CHOICES, default=EXACT_VALUE_COMPARISON)
    is_searchable = models.BooleanField(default=False)
    # TODO: we'll need to rethink the way choices for drop down menus are
    #       represented in the DB. doing it this way is just a bit wasteful.
    choices = models.CharField(max_length=500, blank=True)

    def __unicode__(self):
        return (self.schema.name or self.schema.namespace) + ": " + self.name

    class Meta:
        unique_together = (('schema', 'name'),)


class DatafileParameter(models.Model):

    parameterset = models.ForeignKey(DatafileParameterSet)
    name = models.ForeignKey(ParameterName)
    string_value = models.TextField(null=True, blank=True)
    numerical_value = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        if self.name.is_numeric:
            return 'Datafile Param: %s=%s' % (self.name.name,
                self.numerical_value)
        return 'Datafile Param: %s=%s' % (self.name.name, self.string_value)

    class Meta:
        ordering = ['id']


class DatasetParameter(models.Model):

    parameterset = models.ForeignKey(DatasetParameterSet)
    name = models.ForeignKey(ParameterName)
    string_value = models.TextField(null=True, blank=True)
    numerical_value = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        if self.name.is_numeric:
            return 'Dataset Param: %s=%s' % (self.name.name,
                self.numerical_value)
        return 'Dataset Param: %s=%s' % (self.name.name, self.string_value)

    class Meta:
        ordering = ['id']


class ExperimentParameter(models.Model):
    parameterset = models.ForeignKey(ExperimentParameterSet)
    name = models.ForeignKey(ParameterName)
    string_value = models.TextField(null=True, blank=True)
    numerical_value = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        if self.name.is_numeric:
            return 'Experiment Param: %s=%s' % (self.name.name,
                self.numerical_value)
        return 'Experiment Param: %s=%s' % (self.name.name, self.string_value)

    class Meta:
        ordering = ['id']


class XML_data(models.Model):
    datafile = models.OneToOneField(Dataset_File, null=True, blank=True)
    dataset = models.OneToOneField(Dataset, null=True, blank=True)
    experiment = models.OneToOneField(Experiment, null=True, blank=True)
    xmlns = models.URLField(max_length=400)
    data = models.TextField()

    def __unicode__(self):
        return self.xmlns


class Equipment(models.Model):
    key = models.CharField(unique=True, max_length=30)
    dataset = models.ManyToManyField(Dataset, null=True, blank=True)
    description = models.TextField(blank=True)
    make = models.CharField(max_length=60, blank=True)
    model = models.CharField(max_length=60, blank=True)
    type = models.CharField(max_length=60, blank=True)
    serial = models.CharField(max_length=60, blank=True)
    comm = models.DateField(null=True, blank=True)
    decomm = models.DateField(null=True, blank=True)
    url = models.URLField(null=True, blank=True, verify_exists=False, max_length=255)

    def __unicode__(self):
        return self.key
