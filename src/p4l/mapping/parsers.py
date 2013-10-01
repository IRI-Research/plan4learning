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

from rdflib.plugins.sparql.processor import prepareQuery
from rdflib.term import URIRef
from p4l.models.data import Language, Record
from p4l.models import signals


class QueryCache(object):
    def __init__(self, *args, **kwargs):
        self.__query_cache = {}

    def get_sparql_query(self, query, namespaces_dict):
        return self.__query_cache.get(query, False) \
            or self.__query_cache.setdefault(query, prepareQuery(query, initNs=namespaces_dict))
    

def convert_bool(val):
    if val == True or val == False:
        return val
    if val is None:
        return False
    if isinstance(val, basestring):
        if len(val) == 0:
            return False
        if val[0].lower() in ['t','y','1','o']:
            return True
        else:
            return False        
    return bool(val)

class RecordParser(object):

    
    def __init__(self, query_cache = None):
        self.query_cache = None
        if self.query_cache is None:
            self.query_cache = QueryCache()        
    
    def extract_single_value_form_graph(self, graph, q, bindings={}, index=0, convert=lambda v:unicode(v) if v is not None else None, default=None):
        return next(self.extract_multiple_values_from_graph(graph, q, bindings, index, convert), default)

    def extract_multiple_values_from_graph(self, graph, q, bindings={}, index=0, convert=lambda v:unicode(v) if v is not None else None):

        index_list = index
        if isinstance(index, int):
            index_list = range(index+1)

        if hasattr(convert, '__call__'):
            convert_dict = dict((k, convert) for k in index_list)
        else:
            convert_dict = convert

        convert_dict = dict((k, f if hasattr(f,'__call__') else lambda v:unicode(v) if v is not None else None) for k,f in convert_dict.iteritems())

        for row in graph.query(self.query_cache.get_sparql_query(q, dict(graph.namespaces())), initBindings=bindings):
            if len(row) < len(index_list):
                break
            else:
                res = dict([ (k, convert_dict.get(k, lambda v:unicode(v) if v is not None else None)(v)) for k, v in zip(index_list, row)])
                if isinstance(index, int):
                    yield res[index]
                else:
                    yield res


    def convert_bool(self, val):
        if val == True or val == False:
            return val
        if val is None:
            return False
        if isinstance(val, basestring):
            if len(val) == 0:
                return False
            if val[0].lower() in ['t','y','1','o']:
                return True
            else:
                return False        
        return bool(val)


    def add_to_related_collection(self, coll, graph, fields, q, bindings={},  convert=lambda v: unicode(v) if v is not None else None, through_fields=None):
        
        for val in self.extract_multiple_values_from_graph(graph, q, bindings=bindings, index=fields, convert=convert):

            if through_fields:                
                new_obj_val = dict([(k,v) for k,v in val.iteritems() if k not in through_fields])
            else:
                new_obj_val = val

            if hasattr(coll, 'through'):
                new_obj_rel, _ = coll.model.objects.get_or_create(**new_obj_val)
                if through_fields:
                    through_vals = {coll.source_field_name: coll.instance, coll.target_field_name: new_obj_rel}
                    through_vals.update(dict([(k,v) for k,v in val.iteritems() if k in through_fields]))
                    coll.through.objects.create(**through_vals)
                    new_obj = None
                else:
                    new_obj = new_obj_rel

            else:
                new_obj = coll.create(**new_obj_val)
            
            if new_obj:
                coll.add(new_obj)




    def build_record(self, graph, delete=True):

        record_uri = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?s WHERE { ?s rdf:type iiep:Record .}")
        record_identifier = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s dct:identifier ?o .}", bindings={'s':URIRef(record_uri)})
        
        if delete:
            Record.objects.filter(identifier=record_identifier).delete()

        record = Record()
        record.uri = record_uri
        record.identifier = record_identifier
        record.notes = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s iiep:notes ?o .}", bindings={'s':URIRef(record.uri)})
        record.recordType = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s dct:type ?o .}", bindings={'s':URIRef(record.uri)})
        record.isDocumentPart = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s iiep:isDocumentPart ?o .}", bindings={'s':URIRef(record.uri)}, convert=self.convert_bool, default=False)
        record.hidden = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s iiep:hidden ?o .}", bindings={'s':URIRef(record.uri)}, convert=self.convert_bool, default=False)
        record.restricted = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s iiep:restricted ?o .}", bindings={'s':URIRef(record.uri)}, convert=self.convert_bool, default=False)
        record.editionStatement = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s iiep:editionStatement ?o .}", bindings={'s':URIRef(record.uri)})
        record.corporateAuthorLabel = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s iiep:corporateAuthorLabel ?o .}", bindings={'s':URIRef(record.uri)})

        language = self.extract_single_value_form_graph(graph,"SELECT DISTINCT ?o WHERE { ?s dct:language ?o .}", bindings={'s':URIRef(record.uri)})
        if language:
            record.language, _ = Language.objects.get_or_create(uri=language)

        record.save()

        self.add_to_related_collection(record.otherLanguages, graph,  ['uri'], "SELECT ?o WHERE { ?s iiep:otherLanguage ?o .}", bindings={'s':URIRef(record.uri)})
        self.add_to_related_collection(record.subjects, graph, ['uri'], "SELECT ?o WHERE { ?s dct:subject ?o .}", bindings={'s':URIRef(record.uri)})
        self.add_to_related_collection(record.themes, graph, ['uri'], "SELECT ?o WHERE { ?s iiep:theme ?o .}", bindings={'s':URIRef(record.uri)})
        self.add_to_related_collection(record.countries, graph,  ['uri'], "SELECT ?o WHERE { ?s iiep:country ?o .}", bindings={'s':URIRef(record.uri)})
        self.add_to_related_collection(record.authors, graph, ['name'], "SELECT ?o WHERE { ?s iiep:author ?o .}", bindings={'s':URIRef(record.uri)})
        self.add_to_related_collection(record.subjectPersons, graph, ['name'], "SELECT ?o WHERE { ?s iiep:subjectPerson ?o .}", bindings={'s':URIRef(record.uri)})
        self.add_to_related_collection(record.projectNames, graph, ['uri'], "SELECT ?o WHERE { ?s iiep:projectName ?o . }")
        self.add_to_related_collection(record.audiences, graph,  ['uri'], "SELECT ?o WHERE { ?s dct:audience ?o .}", bindings={'s':URIRef(record.uri)})

        self.add_to_related_collection(
            record.periodicals,
            graph, 
            ['label','lang'],
            "SELECT DISTINCT ?o  ( lang(?o) as ?l) WHERE { ?s iiep:periodical ?o .}",
            bindings={'s':URIRef(record.uri)}
        )

        self.add_to_related_collection(
            record.meetings,
            graph, 
            ['label', 'meetingNumber', 'meetingPlace', 'meetingDate', 'meetingYear', 'lang'],
            "SELECT ?l ?mn ?mp ?md ?my (lang(COALESCE(?l,?nm, ?mp,?md,?my)) as ?lang) WHERE { [iiep:meeting ?bnode]. OPTIONAL { ?bnode rdfs:label ?l }. OPTIONAL { ?bnode iiep:meetingNumber ?mn }. OPTIONAL { ?bnode iiep:meetingPlace ?mp }.  OPTIONAL { ?bnode iiep:meetingDate ?md }. OPTIONAL { ?bnode iiep:meetingYear ?my }}",
            convert={'meetingYear' : lambda y: int(y) if y is not None else None}
        )

        self.add_to_related_collection(
            record.series,
            graph, 
            ['title', 'volume', 'lang'],
            "SELECT ?t ?vol (lang(COALESCE(?t,?vol)) as ?lang) WHERE { [iiep:serie ?bnode]. OPTIONAL { ?bnode dct:title ?t }. OPTIONAL { ?bnode iiep:volume ?vol } }",
        )

        self.add_to_related_collection(
            record.subjectCorporateBodies,
            graph,
            ['uri'],
            "SELECT ?o WHERE { ?s iiep:subjectCorporateBody ?o. }",
            bindings={'s':URIRef(record.uri)}
        )

        self.add_to_related_collection(
            record.subjectMeetings,
            graph,
            ['label', 'meetingNumber', 'meetingPlace', 'meetingDate', 'meetingYear'],
            "SELECT ?l ?mn ?mp ?md ?my WHERE { [iiep:subjectMeeting ?bnode]. OPTIONAL { ?bnode rdfs:label ?l }. OPTIONAL { ?bnode iiep:meetingNumber ?mn }. OPTIONAL { ?bnode iiep:meetingPlace ?mp }.  OPTIONAL { ?bnode iiep:meetingDate ?md }. OPTIONAL { ?bnode iiep:meetingYear ?my }}",            
            convert={'meetingYear' : lambda y: int(y) if y is not None else None}
        )

        self.add_to_related_collection(
            record.corporateAuthors,
            graph,
            ['uri'],
            "SELECT ?o WHERE { ?s iiep:corporateAuthor ?o.}",
            bindings={'s':URIRef(record.uri)}            
        )

        self.add_to_related_collection(
            record.issns,
            graph,
            ['issn', 'lang'],
            "SELECT ?issn (lang(COALESCE(?issn)) as ?lang) WHERE { ?s iiep:issn ?issn . }",
            bindings={'s':URIRef(record.uri)},
        )

        self.add_to_related_collection(
            record.isbns,
            graph,
            ['isbn', 'lang'],
            "SELECT ?isbn (lang(COALESCE(?isbn)) as ?lang) WHERE { ?s iiep:isbn ?isbn . }",
            bindings={'s':URIRef(record.uri)},
        )

        self.add_to_related_collection(
            record.documentCodes,
            graph,
            ['documentCode', 'lang'],
            "SELECT ?c (lang(COALESCE(?c)) as ?lang) WHERE { ?s iiep:documentCode ?c . }",
            bindings={'s':URIRef(record.uri)},
        )

        self.add_to_related_collection(
            record.titles,
            graph,
            ['title', 'lang'],
            "SELECT ?t (lang(COALESCE(?t)) as ?lang) WHERE { ?s dct:title ?t . }",
            bindings={'s':URIRef(record.uri)},
        )

        self.add_to_related_collection(
            record.abstracts,
            graph,
            ['abstract', 'lang'],
            "SELECT ?t (lang(COALESCE(?t)) as ?lang) WHERE { ?s dct:abstract ?t . }",
            bindings={'s':URIRef(record.uri)},
        )

        self.add_to_related_collection(
            record.addedTitles,
            graph,
            ['title', 'lang'],
            "SELECT ?t (lang(COALESCE(?t)) as ?lang) WHERE { ?s iiep:addedTitle ?t . }",
            bindings={'s':URIRef(record.uri)},
        )

        self.add_to_related_collection(
            record.titlesMainDocument,
            graph,
            ['title', 'lang'],
            "SELECT ?t (lang(COALESCE(?t)) as ?lang) WHERE { ?s iiep:titleMainDocument ?t . }",
            bindings={'s':URIRef(record.uri)},
        )

        self.add_to_related_collection(
            record.imprints,
            graph,
            ['imprintCity', 'publisher', 'imprintDate', 'lang'],
            "SELECT ?c ?p ?d (lang(COALESCE(?c, ?p, ?d)) as ?lang) WHERE { [ iiep:imprint ?bnode ]. OPTIONAL { ?bnode iiep:imprintCity ?c }. OPTIONAL { ?bnode dct:publisher ?p }. OPTIONAL { ?bnode iiep:imprintDate ?d }}",
        )

        self.add_to_related_collection(
            record.collations,
            graph,
            ['collation', 'lang'],
            "SELECT ?c (lang(COALESCE(?c)) as ?lang) WHERE { ?s iiep:collation ?c . }",
            bindings={'s':URIRef(record.uri)},
        )

        self.add_to_related_collection(
            record.volumeIssues,
            graph,
            ['volume', 'number', 'lang'],
            "SELECT ?v ?n (lang(COALESCE(?v, ?n)) as ?lang) WHERE { [ iiep:volumeIssue ?bnode ]. OPTIONAL { ?bnode iiep:volume ?v }. OPTIONAL { ?bnode iiep:number ?n }}",
        )

        self.add_to_related_collection(
            record.urls,
            graph,
            ['address', 'display'],
            "SELECT ?a ?d WHERE { [ iiep:url ?bnode ]. OPTIONAL { ?bnode iiep:address ?a }. OPTIONAL { ?bnode iiep:display ?d }.}",
        )
        
        signals.record_saved.send(Record, instance=record, created=True)

        return record
