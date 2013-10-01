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


from haystack import indexes

from p4l.models import Record
from p4l.utils import strip_accents, get_labels_for_uris, safe_cache_key

from django.core.cache import get_cache
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def get_organizations_label(uris):
    cache = get_cache('indexation')
    
    res = {}
    missing_uris = []
    
    for uri in uris: 
        label = cache.get(safe_cache_key(uri))
        if label is not None:
            res[uri] = label
        else:
            missing_uris.append(uri)
            
    new_labels = get_labels_for_uris(missing_uris, settings.RDF_SCHEMES['organizations'], None, True)
    for k,v in new_labels.iteritems():
        cache.set(safe_cache_key(k),v)
        res[k] = v
    
    return res


class RecordIndex(indexes.SearchIndex, indexes.Indexable):    

    text = indexes.CharField(document=True, use_template=True, stored=False)
    identifier = indexes.CharField(model_attr="identifier", stored=True)
    titles = indexes.MultiValueField(model_attr="get_titles", stored=False)
    titles_src = indexes.MultiValueField(model_attr="get_titles", stored=True, indexed=False)
    authors = indexes.MultiValueField(model_attr="all_authors", stored=False)
    
    years = indexes.MultiValueField(model_attr="get_imprints_years", indexed=False, stored=True)
    
    def prepare(self, obj):
        authors = obj.get_authors() + get_organizations_label(obj.get_corporate_authors()).values()
        obj.all_authors = [strip_accents(unicode(v)) for v in authors] 
        return indexes.SearchIndex.prepare(self, obj)
    
    def prepare_titles(self, obj):
        return [strip_accents(v) for v in obj.get_titles()]

    def get_model(self):
        return Record

    def get_updated_field(self):
        return "modification_date"
    
    def index_queryset(self, using=None):
        return Record.objects.using(using).all().prefetch_related("imprints","authors", "titles", "corporateAuthors")