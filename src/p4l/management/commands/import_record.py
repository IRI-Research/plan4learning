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
from optparse import make_option

from django.core.management import BaseCommand
from django.db import reset_queries, transaction
from rdflib import BNode

from p4l.mapping.constants import get_empty_graph, IIEP
from p4l.mapping.parsers import RecordParser, QueryCache
from p4l.utils import show_progress
import xml.etree.cElementTree as ET
from django.conf import settings


logger = logging.getLogger(__name__)


DEFAULT_LANGUAGE_URI = "http://psi.oasis-open.org/iso/639/#eng"

DEFAULT_LANGUAGE_QUERY =  """SELECT ( COALESCE(?lang, ?other_lang) as ?main_lang) WHERE {
    OPTIONAL { ?s dct:language ?lang }.
    OPTIONAL { ?s iiep:otherLanguage ?other_lang }.
}"""


class Command(BaseCommand):

    args = "record_url ..."

    help = "Import p4l record rdf format"

    option_list = BaseCommand.option_list + (
        make_option('-b', '--batch-size',
            dest= 'batch_size',
            type='int',
            default= 50,
            help= 'number of object to import in bulk operations' 
        ),
        make_option('-p', '--preserve',
            dest= 'preserve',
            action='store_true',
            default=False,
            help= 'preserve existing record' 
        ),
        make_option('-i', '--index',
            dest= 'index',
            action='store_true',
            default=False,
            help= 'index while importing' 
        ),
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.record_parser = RecordParser(query_cache=QueryCache())
        

    def filter_node(self, node, graph, res_graph):
        for p,o in graph[node]:
            res_graph.add((node,p,o))
            if isinstance(o, BNode):
                self.filter_node(o, graph, res_graph)



    def calculate_records_nb(self, records_url):
        context = ET.iterparse(records_url, events=("end",))
        i = 0
        for _,elem in context:
            if elem.tag == "{%s}Record" % IIEP:
                i += 1
        return i

    def process_url(self, records_url, options):

        total_records = self.calculate_records_nb(records_url)
        writer = None
        errors=[]

        context = ET.iterparse(records_url, events=("end",))
        i = 0
        for _,elem in context:
            if elem.tag == "{%s}Record" % IIEP:
                i += 1
                writer = show_progress(i, total_records, "Processing record nb %d " % i, 50, writer=writer)
                try:
                    record_graph = get_empty_graph()
                    record_graph.parse(data=ET.tostring(elem, encoding='utf-8'), format='xml')                    
                    self.record_parser.build_record(record_graph, delete=(not self.preserve))                    
                except Exception as e:
                    transaction.rollback()
                    msg = "Error processing resource %d in %s : %s" % (i, records_url, repr(e))
                    logger.exception(msg)
                    errors.append((i, records_url, msg))
                else:
                    transaction.commit()

                if i%self.batch_size == 0:                    
                    reset_queries()

        return errors


    # def process_url(self, records_url, options):
    #     #open graph with rdflib
    #             
    #     g = Graph()
    #     print("Loading %s" % records_url)
    #     g.parse(records_url)
    #     print("Parsing %s done" % records_url)
    #     for i,record_uri in enumerate(g[:RDF.type:IIEP.Record]):
    #         print(i, repr(record_uri))
    #         record_graph = self.get_empty_graph()
    #         self.filter_node(record_uri, g, record_graph)
    #         self.build_record(record_graph)
    #         if i > 3:
    #             break


    def handle(self, *args, **options):

        self.batch_size = options.get('batch_size', 50)
        self.preserve = options.get("preserve", False)
        self.index = options.get("index", False)
        
        if not self.index:
            old_realtime_indexing = getattr(settings, "REALTIME_INDEXING", None)
            #this is not recommended by the django manual, but in case of management command it seems to work
            settings.REALTIME_INDEXING = False 
        
        transaction.enter_transaction_management()
        transaction.managed(True)

        for records_url in args:
            print("Processing %s" % records_url)
            errors = self.process_url(records_url, options)
            print("Processing %s Done" % records_url)
            if errors:
                print("%d error(s) when processing %s, check your log file." % (len(errors), records_url))

        transaction.leave_transaction_management()
        
        if not self.index and old_realtime_indexing:
            settings.REALTIME_INDEXING = old_realtime_indexing

