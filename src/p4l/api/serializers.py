# -*- coding: utf-8 -*-
#
# Copyright IRI (c) 2013
#
# contact@iri.centrepompidou.fr
#
# This software is governed by the CeCILL-B license under French law and
# abiding by the rules of distribution of free software.  You can  use, 
# modify and/ or redistribute the software under the terms of the CeCILL-B
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info". 
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability. 
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security. 
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
#

from django.core.exceptions import ValidationError
from p4l.models import Record
from rest_framework import serializers
import logging
from rest_framework.serializers import NestedValidationError
import copy
from django.db.models.fields.related import ForeignKey

logger = logging.getLogger(__name__)

class ThesaurusSerializer(serializers.SlugRelatedField):
    
    def __init__(self, *args, **kwargs):
        kwargs.update({                       
            'read_only': False,
        })
        serializers.SlugRelatedField.__init__(self, *args, **kwargs)
        
    def from_native(self, data):
        if self.queryset is None:
            raise Exception('Writable related fields must include a `queryset` argument')
        try:
            res, _ = self.queryset.get_or_create(**{self.slug_field: data})
            return res
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise ValidationError(msg)


class P4lModelSerializer(serializers.ModelSerializer):
    
    
    def get_nested_field(self, model_field, related_model, to_many):
        field_exclude = ()
        if model_field is None:
            fk = [f.name for f in related_model._meta.fields if (isinstance(f, ForeignKey) and f.rel.to == Record)][0]
            field_exclude = ('id', fk)
        class NestedModelSerializer(P4lModelSerializer):
            class Meta:
                model = related_model
                depth = self.opts.depth - 1
                exclude = field_exclude

        return NestedModelSerializer(many=to_many)

        
    def field_from_native(self, data, files, field_name, into):
        """
        Override default so that the serializer can be used as a writable
        nested field across relationships.
        """        
        if self.read_only:
            return
        
        try:
            value = data[field_name]
        except KeyError:
            if self.default is not None and not self.partial:
                # Note: partial updates shouldn't set defaults
                value = copy.deepcopy(self.default)
            else:
                if self.required:
                    raise ValidationError(self.error_messages['required'])
                return

        # Set the serializer object if it exists
        obj = getattr(self.parent.object, field_name) if self.parent.object else None

        if self.source == '*':
            if value:
                into.update(value)
        else:
            if value in (None, ''):
                into[(self.source or field_name)] = None
            elif self.many and hasattr(value, '__iter__'):
                if obj is not None:
                    obj.all().delete()
                nested_items = []
                for val in value:
                    kwargs = {
                        'instance': None,
                        'data': val,
                        'context': self.context,
                        'partial': self.partial,
                        'many': False
                    }
                    serializer = self.__class__(**kwargs)
                    nested_items.append(serializer.from_native(val, files))
                into[self.source or field_name] = nested_items
            else:
                kwargs = {
                    'instance': obj,
                    'data': value,
                    'context': self.context,
                    'partial': self.partial,
                    'many': self.many
                }
                serializer = self.__class__(**kwargs)

                if serializer.is_valid():
                    into[self.source or field_name] = serializer.object
                else:
                    # Propagate errors up to our parent
                    raise NestedValidationError(serializer.errors)





class RecordSerializer(P4lModelSerializer):
    '''
    Serializer for record
    '''
    language = ThesaurusSerializer(many=False, required=False, slug_field='uri') 
    otherLanguages = ThesaurusSerializer(many=True, required=False, slug_field='uri')
    subjects = ThesaurusSerializer(many=True, required=False, slug_field='uri')
    themes = ThesaurusSerializer(many=True, required=False, slug_field='uri')
    countries = ThesaurusSerializer(many=True, required=False, slug_field='uri')
    projectNames = ThesaurusSerializer(many=True, required=False, slug_field='uri')
    subjectCorporateBodies = ThesaurusSerializer(many=True, required=False, slug_field='uri') 
    corporateAuthors = ThesaurusSerializer(many=True, required=False, slug_field='uri')
    audiences = ThesaurusSerializer(many=True, required=False, slug_field='uri')

    class Meta:
        model = Record
        depth = 1
        fields = ("identifier", "uri", "subjects", "notes", "otherLanguages",
                  "language", "editionStatement", "recordType", "isDocumentPart",
                  "hidden", "restricted", "themes", "countries", "projectNames", 
                  "subjectCorporateBodies", "corporateAuthors", "corporateAuthorLabel", 
                  "imprints", "titles", "addedTitles", "issns", "isbns", "documentCodes",
                  "abstracts", "titlesMainDocument", "collations", "volumeIssues",
                  "periodicals", "meetings", "subjectMeetings", "series",
                  "authors", "subjectPersons", "urls", "audiences")

    
