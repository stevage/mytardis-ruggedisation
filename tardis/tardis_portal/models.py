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
    """
    Author's are researchers associated with an experiment that do not have a TARDIS account.

    Fields:

    :attribute name: Author's full name
    """

    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Experiment(models.Model):
    """
    The Experiment is TARDIS' top level representation of data.  Experiments are composed of a number of Datasets, each of which contains any number of Datafiles.

    An Experiment is a self-contained entity so that it may be transferred to other federated instances of TARDIS.

    Fields:

    :attribute url: Description needed.
    :attribute approved: Description needed.
    :attribute title:
        Short name of the Experiment
    :attribute institution_name:
        The institution or facility where the Experiment was conducted.
    :attribute description:
        The description, or abstract, describing the Experiment.
    :attribute start_time:
        The timestamp indicating the date the experiment was started.
    :attribute end_time:
        The timestamp indicating the date the experiment was completed.
    :attribute created_time:
        Auto-generated, the timestamp indicating the date / time the experiment was created, typically when metadata was uploaded in to TARDIS.
    :attribute update_time:
        Auto-generated, the timestamp indicating the date / time that the experiment was last modified.
    :attribute created_by:
        The User account used to initially upload the Experiment.
    :attribute handle: ???
    :attribute public:
        Boolean flag indicating whether the Experiment is publically accessible.
    """

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
    """
    The Dataset groups Datafiles together.  TARDIS doesn't place any interpretation on the meaning of the group, which should be meaningful to the researcher.

    Examples of groups include:

     * Experimental Data, Derived Data, Final Data
     * Grouped by equipment
     * Grouped by configuration (equipment settings)
     * Time sequence

    The description should include enough information for the researcher to interpret the grouping.

    Fields:

    :attribute experiment: The Experiment to which the Dataset belongs
    :attribute description: A free-format description of the Dataset
    """

    experiment = models.ForeignKey(Experiment)
    description = models.TextField()

    def __unicode__(self):
        return self.description


class Dataset_File(models.Model):
    """
    A Dataset_File record, commonly referred to as a Datafile, is created for each file contained in the Experiment, and belongs to a single Dataset.

    Fields:

    :attribute dataset: Foreign key to the containing Dataset
    :attribute filename: The name of the file :-)
    :attribute url: The location of the file.  (Add note about plugable protocol handling)
    :attribute size: The file size (in bytes?)
    :attribute protocol: The protocol used to download the file
    :attribute created_time: The creation date of the file(?)
    """

    dataset = models.ForeignKey(Dataset)
    filename = models.CharField(max_length=400)
    url = models.URLField(max_length=400)
    size = models.CharField(blank=True, max_length=400)
    protocol = models.CharField(blank=True, max_length=10)
    created_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.filename


class Schema(models.Model):
    """
    A TARDIS schema is a named collection of Parameters that can be attached to an Experiment, Dataset or Datafile.  A schema is instantiated as a parameter set, one of ExperimentParameterSet, DatasetParameterSet or DatafileParameterSet.

    Fields:

    :attribute namespace: A URL that uniquely identifies the Schema.
    :attribute name: A user friendly name identifying the Schema.
    :attribute subtype: Used to group schema together when searching.
    :attribute description: A free format text description of the schema.
    """

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
    description = models.TextField()

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
    """DatafileParameterSet is the instantiation of a schema attached to a Datafile.  Each Datafile may have multiple DatafileParameterSets, and a DatafileParameterSet may be attached to multiple Datafiles within an experiment."""

    schema = models.ForeignKey(Schema)
    dataset_file = models.ManyToManyField(Dataset_File)

    def __unicode__(self):
        return "Datafile ParameterSet on " + self.schema.displayName()

    class Meta:
        ordering = ['id']


class DatasetParameterSet(models.Model):
    """
    DatasetParameterSet is the instantiation of a schema attached to a Dataset.  Each Dataset may have multiple DatasetParameterSets, and a DatasetParameterSet may be attached to multiple Datasets within an experiment.
    """

    schema = models.ForeignKey(Schema)
    dataset = models.ManyToManyField(Dataset)

    def __unicode__(self):
        return "Dataset ParameterSet on " + self.schema.displayName()

    class Meta:
        ordering = ['id']


class ExperimentParameterSet(models.Model):
    """
    ExperimentParameterSet is the instantiation of a schema attached to an Experiment.  Each Experiment may have multiple ExperimentParameterSets.  However, unlike DatasetParameterSets and DatafileParameterSets, an ExperimentParameterSet may only be attached to one Experiment.
    """

    schema = models.ForeignKey(Schema)
    experiment = models.ForeignKey(Experiment)

    def __unicode__(self):
        return "Experiment ParameterSet on " + self.schema.displayName()

    class Meta:
        ordering = ['id']


class ParameterName(models.Model):
    """
    A ParameterName defines an item of metadata that may be stored as part of a ParameterSet.

    Fields:

    :attribute schema: The schema to which this Parameter belongs.
    :attribute name: A short name used to identify the parameter.
    :attribute full_name: The display name used to identify the parameter to a user.
    :attribute units: The units of the parameter.  This is only used for display purposes.  TARDIS doesn't place any interpretation on the units.
    :attribute is_numeric: Flag whether the parameter is a string or number (Float).
    :attribute comparison_type: An enumerated value indicating what type of match the search engine should perform.
    :attribute is_searchable: Flag whether to display the parameter on the search page.
    :attribute choices: ???
    :attribute description: A free format description of the parameter.
    """

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
    description = models.TextField()

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
