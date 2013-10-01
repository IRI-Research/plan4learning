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

import logging

from rdflib.namespace import RDF
from rdflib.term import URIRef, Literal, BNode
from collections import OrderedDict


logger = logging.getLogger(__name__)

class BaseSerializer(object):
    
    creation_counter = 0
    
    def __init__(self, predicate=None, many=False):
        self.predicate = predicate
        self.creation_counter = BaseSerializer.creation_counter
        self.many = many
        BaseSerializer.creation_counter += 1
        if self.predicate and not isinstance(self.predicate, URIRef):
            self.predicate = URIRef(predicate)
    

class FieldSerializer(BaseSerializer):
        
    def __init__(self, predicate=None, convert=None, source=None, many=False):
        super(FieldSerializer, self).__init__(predicate=predicate, many=many)
        self.convert = convert or (lambda x: Literal(unicode(x)) if x else None)
        self.source = source


    def get_rdf_object(self, obj, fieldname):
        raise NotImplemented()
        
    def to_graph(self, subject, obj, fieldname, graph):
        o = self.get_rdf_object(obj, fieldname)
        if o:
            graph.add((subject, self.predicate, o))
        

class SimpleFieldSerializer(FieldSerializer):
    
    def __init__(self, predicate=None, convert=None, source=None, lang_field=None):
        super(SimpleFieldSerializer, self).__init__(predicate=predicate, convert=convert, source=source, many=False)
        self.lang_field = lang_field
    
    def get_rdf_object(self, obj, fieldname):
        res = self.convert(getattr(obj, self.source or fieldname))
        if res is None:
            return
        if not isinstance(res, Literal):
            res = Literal(unicode(res))        
        lang = getattr(obj, self.lang_field, None) if self.lang_field else None
        
        return Literal(res.value, lang) if lang else res

class BooleanFieldSerializer(SimpleFieldSerializer):

    def bool_convert(self, value):
        return (Literal('TRUE') if value else Literal('FALSE')) if value is not None else None

    def __init__(self, predicate=None, convert=None, source=None, lang_field=None):
        super(BooleanFieldSerializer, self).__init__( predicate, convert=convert, source=source, lang_field=lang_field)
        self.convert = lambda x: self.bool_convert(x)


class RelatedFieldSerializer(SimpleFieldSerializer):
        
    def __init__(self, value_field, predicate=None, convert=None, source=None, many=False, lang_field=None):
        super(RelatedFieldSerializer, self).__init__(predicate, convert, source, lang_field=lang_field)
        self.many = many
        self.value_field = value_field

    def to_graph(self, subject, obj, fieldname, graph):
        value = getattr(obj, fieldname, None)
        if not value:
            return
        
        values_to_add = []
        if self.many:
            for related_obj in value.all():
                values_to_add.append(self.get_rdf_object(related_obj, self.value_field))
        else:
            values_to_add.append(self.get_rdf_object(value, self.value_field))
        for o in values_to_add:
            if o:
                graph.add((subject, self.predicate, o))

    

# Directly adapted from serializers in rest_framework 
def _get_declared_fields(bases, attrs):
    """
    Create a list of serializer field instances from the passed in 'attrs',
    plus any fields on the base classes (in 'bases').

    Note that all fields from the base classes are used.
    """
    fields = [(field_name, attrs.pop(field_name))
              for field_name, obj in list(attrs.iteritems())
              if isinstance(obj, BaseSerializer)]
    fields.sort(key=lambda x: x[1].creation_counter)

    # If this class is subclassing another Serializer, add that Serializer's
    # fields.  Note that we loop over the bases in *reverse*. This is necessary
    # in order to maintain the correct order of fields.
    for base in bases[::-1]:
        if hasattr(base, 'base_serializers'):
            fields = list(base.base_serializers.items()) + fields

    return OrderedDict(fields)


class SerializerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['base_serializers'] = _get_declared_fields(bases, attrs)
        return super(SerializerMetaclass, cls).__new__(cls, name, bases, attrs)


class ModelSerializerOptions(object):
    
    def __init__(self, meta):
        self.type = getattr(meta, 'type', None)
        if self.type and not isinstance(self.type, URIRef):
            self.type = URIRef(self.type)
        self.uri_fieldname = getattr(meta, 'uri_fieldname', None)

class ModelSerializer(BaseSerializer):
    
    __metaclass__ =  SerializerMetaclass
      
    class Meta(object):
        pass

    def get_serializers(self):
        return []
        
    def get_uri(self, obj):
        uri = None
        if self.opts.uri_fieldname:
            uri = getattr(obj, self.opts.uri_fieldname, None)            
        return URIRef(uri) if uri else None
    
    def object_to_graph(self, subject, uri, obj, graph):
        
        if self.predicate:
            graph.add((subject, self.predicate, uri))
        
        for serializer_fieldname, field_serializer in self.base_serializers.iteritems():
            field_serializer.to_graph(uri, obj, serializer_fieldname, graph)

    
    def to_graph(self, subject, obj, fieldname, graph):        

        uri = self.get_uri(obj)
        if self.opts.type:
            graph.add((uri, RDF.type, self.opts.type))
            
        obj_to_add = []
        if fieldname:
            field_value = getattr(obj, fieldname, None)
            if field_value:
                if self.many:
                    obj_to_add = [(nested_obj, BNode()) for nested_obj in field_value.all()]
                else:
                    obj_to_add = [(field_value, BNode())]
        else:
            obj_to_add = [(obj, uri)]
        
        for nested_obj, nested_uri in obj_to_add:
            self.object_to_graph( subject, nested_uri, nested_obj, graph)
            
    
    def __init__(self, predicate=None, many=False):
        BaseSerializer.__init__(self, predicate=predicate, many=many)
        self.opts = ModelSerializerOptions(self.Meta)        
    
