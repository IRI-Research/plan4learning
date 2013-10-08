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


import bz2
import codecs
import gzip
import logging
from optparse import make_option
from xml.sax.saxutils import XMLGenerator
from xml.sax.xmlreader import AttributesNSImpl

from django.core.management import BaseCommand
from django.core.management.base import CommandError
from django.db.models.fields.related import ForeignKey

from p4l.mapping.constants import GRAPH_NAMESPACES, RDF, get_empty_graph
from p4l.mapping import RecordSerializer
from p4l.models.data import Record
from p4l.utils import show_progress


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    args = "file_path..."

    help = "Export p4l record rdf format"

    option_list = BaseCommand.option_list + (
        make_option('-l', '--limit',
            dest= 'limit',
            type='int',
            default=-1,
            help= 'number of record to export. -1 is all (default)' 
        ),
        make_option('-s', '--skip',
            dest= 'skip',
            type='int',
            default=0,
            help= 'number of record to skip before export. default 0.' 
        ),
        make_option('-b', '--batch',
            dest= 'batch',
            type='int',
            default=100,
            help= 'query batch default 100.' 
        ),
        make_option('-j', '--bzip2',
            dest= 'bzip2',
            action='store_true',
            default=False,
            help= 'bz2 compress' 
        ),
        make_option('-z', '--gzip',
            dest= 'gzip',
            action='store_true',
            default=False,
            help= 'gzip compress' 
        ),
    )


    def get_graph_from_object(self, obj):
        g = get_empty_graph()
        
        serializer = RecordSerializer()        
        serializer.to_graph(None, obj, None, g)
        
        return g
    
    
    def handle(self, *args, **options):
        
        if len(args) != 1:
            raise CommandError("This command takes exactly one argument")
        
        filepath = args[0]

        bzip2 = options.get('bzip2', False)
        gzip_opt = options.get('gzip', False)
        
        if bzip2 and not filepath.endswith(".bz2"):
            filepath += ".bz2"
        elif gzip_opt and not filepath.endswith(".gz"):
            filepath += ".gz"            
        
        limit = options.get("limit", -1)
        skip = options.get("skip", 0)
        batch = options.get("batch", 100)
        
        qs = Record.objects.all().select_related(*[field.name for field in Record._meta.fields if isinstance(field, ForeignKey)]).prefetch_related(*([field.name for field in Record._meta.many_to_many] + [obj.get_accessor_name() for obj in Record._meta.get_all_related_objects()])).order_by('identifier')  # @UndefinedVariable
        
        if limit>=0:
            qs = qs[skip:skip+limit]
        else:
            qs = qs[skip:]
        
        open_method = None
        open_args = []
        decode_method = lambda s: s
        
        if bzip2:
            open_method = bz2.BZ2File
            open_args = [filepath, 'wb', 9]
        elif gzip_opt:
            open_method = gzip.GzipFile
            open_args = [filepath, 'wb', 9]
        else:
            open_method = codecs.open
            open_args = [filepath, 'wb', "utf-8"]
            decode_method = lambda s: s.decode("utf-8")
        
        total_records = qs.count()
        
        print("Total record to export : %d" % total_records)
        progress_writer = None
        
        with open_method(*open_args) as dest_file:
            writer = XMLGenerator(dest_file, "UTF-8")
            writer.startDocument()
            for prefix,uri in GRAPH_NAMESPACES.items():
                writer.startPrefixMapping(prefix, uri)
            writer.startElementNS((RDF, 'RDF'), 'RDF', AttributesNSImpl({}, {}))
            writer.characters("\n")
            for n in range((total_records/batch)+1):
                for i,r in enumerate(qs[n*batch:((n+1)*batch)]):
                    progress_writer = show_progress(i+(n*batch)+1, total_records, "Exporting record %s" % r.identifier, 50, progress_writer) 
                    graph = self.get_graph_from_object(r)
                    do_write = False
                    for line in graph.serialize(format="pretty-xml", encoding="utf-8").splitlines(True):
                        if "<iiep:Record" in line:
                            do_write = True
                        if do_write:
                            dest_file.write(decode_method(line))
                        if "</iiep:Record>" in line:
                            break
                
            writer.endElementNS((RDF, 'RDF'), 'RDF')
            writer.endDocument()
            dest_file.write("\n")
