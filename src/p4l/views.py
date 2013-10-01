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

import json
import logging
import time

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, View
from rest_framework.renderers import UnicodeJSONRenderer

from p4l.api.serializers import RecordSerializer
from p4l.models import Record
from p4l.utils import get_labels_for_uris


logger = logging.getLogger(__name__)

QUERY_FIELDS_TRANSLATION = {
    'url': 'dataurl',
    'filter': 'dataquery',
    'root': 'datarootquery',
    'childs': 'datachildsquery',
    'child-count': 'datachildcountquery'                            
}


def get_record_uri_labels(record, lang):
    uri_labels = get_labels_for_uris([s.uri for s in record.subjects.all()], settings.RDF_SCHEMES['subjects'], lang, False)
    uri_labels.update(get_labels_for_uris([s.uri for s in record.themes.all()], settings.RDF_SCHEMES['themes'], lang, False))
    uri_labels.update(get_labels_for_uris([s.uri for s in record.countries.all()], settings.RDF_SCHEMES['countries'], lang, False))
    uri_labels.update(get_labels_for_uris([record.language.uri] if record.language else [], settings.RDF_SCHEMES['languages'], lang, False))
    uri_labels.update(get_labels_for_uris([s.uri for s in record.otherLanguages.all()], settings.RDF_SCHEMES['languages'], lang, False))
    uri_labels.update(get_labels_for_uris([s.uri for s in record.projectNames.all()], settings.RDF_SCHEMES['projects'], None, True))
    uri_labels.update(get_labels_for_uris([s.uri for s in record.subjectCorporateBodies.all()], settings.RDF_SCHEMES['organizations'], None, True))
    uri_labels.update(get_labels_for_uris([s.uri for s in record.corporateAuthors.all()], settings.RDF_SCHEMES['organizations'], None, True))
    uri_labels.update(get_labels_for_uris([record.recordType] if record.recordType else [], settings.RDF_SCHEMES['types'], lang, False))
    uri_labels.update(get_labels_for_uris([s.uri for s in record.audiences.all()], settings.RDF_SCHEMES['audiences'], None, True))
    return uri_labels


class RecordDetailView(DetailView):
    
    model = Record
    template_name = "p4l/record_view.html"
    slug_field = "identifier"
    
    def get_context_data(self, **kwargs):
        context = DetailView.get_context_data(self, **kwargs)
        # We get the language, "fr" by default
        lang = "fr"
        if "lang" in self.request.GET:
            lang = self.request.GET["lang"]
        elif hasattr(self.request, "LANGUAGE_CODE") and self.request.LANGUAGE_CODE in ["fr","en","es"]:
            lang = self.request.LANGUAGE_CODE

        context['uri_labels'] = get_record_uri_labels(self.object,lang)
        
        
        return context

class RecordEditView(DetailView):
    http_method_names = ['get']
    template_name = 'p4l/record_update_form.html'
    model = Record
    slug_field = "identifier"
    is_create_view = False
    
    def get_empty_object(self):
        
        obj = Record()
        obj.id = -1
        obj.identifier = "T" + str(int(time.time()))
        obj.uri = "http://www.iiep.unesco.org/plan4learning/record/" + obj.identifier
        
        return obj
    
    
    def get_object(self, *args, **kwargs):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug` argument
        in the URLconf, but subclasses can override this to return any object.
        """
        if self.is_create_view:
            return self.get_empty_object()
        
        return super(RecordEditView, self).get_object(*args, **kwargs)
        

    def get_context_data(self, **kwargs):
        
        context = super(RecordEditView, self).get_context_data(**kwargs)
        
        if self.object:
            serializer = RecordSerializer(self.object)
            context['object_json'] = UnicodeJSONRenderer().render(serializer.data)
        else:
            context['object_json'] = "null"
        
        # We get the language, "fr" by default
        lang = "fr"
        if "lang" in self.request.GET:
            lang = self.request.GET["lang"]
        elif hasattr(self.request, "LANGUAGE_CODE") and self.request.LANGUAGE_CODE in ["fr","en","es"]:
            lang = self.request.LANGUAGE_CODE
        
        context['uri_labels'] = json.dumps(get_record_uri_labels(self.object,lang))
        
        # lang must be like "XX" in the sparql request 
        lang = '"' + lang + '"'

        query_dicts = dict([(k , dict([ (QUERY_FIELDS_TRANSLATION[key],value.format(lang=lang)) for key,value in v.items()  ])) for k,v in settings.SPARQL_REF_QUERIES.items()])
        context['query_dicts'] = json.dumps(query_dicts)
        
        # Languages list used in drop down list
        context['languages_list'] = json.dumps(settings.LANGUAGES_LIST)
        
        context['is_create_view'] = json.dumps(self.is_create_view)
                
        return context


class RecordDeleteView(View):
    def get(self, request, slug, **kwargs):
        rec = get_object_or_404(Record, identifier=slug)
        rec.delete()
        return redirect('p4l_home')
        