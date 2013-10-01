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


from django.conf import settings
from haystack.query import SQ
from whoosh.qparser import (SimpleParser, FieldsPlugin, OperatorsPlugin, 
    PhrasePlugin, SingleQuotePlugin, GroupPlugin, PrefixPlugin, GtLtPlugin, 
    RangePlugin)
from whoosh.query import (Term, And, AndMaybe, Or, AndNot, Not, Phrase, Prefix, 
    TermRange)

HAYSTACK_DEFAULT_OPERATOR = getattr(settings,'HAYSTACK_DEFAULT_OPERATOR','AND')

class QueryParser(object):


    def __init__(self, fieldname):
        '''
        Constructor
        '''
        self.w_parser = SimpleParser(fieldname, None)
        self.w_parser.add_plugin(FieldsPlugin())
        self.w_parser.add_plugin(OperatorsPlugin())
        self.w_parser.add_plugin(PhrasePlugin())
        self.w_parser.add_plugin(SingleQuotePlugin())
        self.w_parser.add_plugin(GroupPlugin())
        self.w_parser.add_plugin(PrefixPlugin())
        self.w_parser.add_plugin(GtLtPlugin())
        self.w_parser.add_plugin(RangePlugin())
        self.query = None
        self.current_node_stack = []        
        
    def parse(self, query):
        
        self.query = SQ()
        self.current_node_stack = [(self.query, HAYSTACK_DEFAULT_OPERATOR)]

        wquery = self.w_parser.parse(query)
        
        self.visit(wquery)
        
        if len(self.query) == 1 and isinstance(self.query.children[0], SQ):
            return self.query.children[0]
        else:
            return self.query 
        
        
    def visit(self, q):
        
        if isinstance(q, Term):
            current_node, current_connector = self.current_node_stack.pop() 
            current_node.add(SQ(**{q.fieldname:q.text}), current_connector)
            self.current_node_stack.append((current_node,current_connector))
        elif isinstance(q, And):
            self._add_compound_query(q, SQ.AND)
        elif isinstance(q, AndMaybe):
            self._add_andmaybe(q)
        elif isinstance(q, Or):
            self._add_compound_query(q, SQ.OR)
        elif isinstance(q, AndNot):
            self._add_andnot(q)
        elif isinstance(q, Not):
            self._add_not(q)
        elif isinstance(q, Phrase):
            self._add_phrase(q)
        elif isinstance(q, Prefix):
            self._add_prefix(q)
        elif isinstance(q, TermRange):
            self._add_range(q)
            
    def _add_compound_query(self, q, connector):

        new_node = SQ()
        self.current_node_stack.append((new_node, connector))
        for subquery in q.subqueries:
            self.visit(subquery)
        self.current_node_stack.pop()
                        
        if len(new_node)==1 and isinstance(new_node.children[0], SQ) :
            new_node = new_node.children[0]
        
        current_node, current_connector = self.current_node_stack[-1]
        current_node.add(new_node, current_connector)
        
        
    def _add_andnot(self, q):
        
        new_node = SQ()
        self.current_node_stack.append((new_node, SQ.AND))
        self.visit(q.a)
        self.visit(Not(q.b))
        self.current_node_stack.pop()
        
        if len(new_node)==1 and isinstance(new_node.children[0], SQ) :
            new_node = new_node.children[0]
        
        current_node, current_connector = self.current_node_stack[-1]
        current_node.add(new_node, current_connector)

    def _add_andmaybe(self, q):
        
        new_node = SQ()
        self.current_node_stack.append((new_node, SQ.AND))
        self.visit(q.a)
        self.visit(q.b)
        self.current_node_stack.pop()
        
        if len(new_node)==1 and isinstance(new_node.children[0], SQ) :
            new_node = new_node.children[0]
        
        current_node, current_connector = self.current_node_stack[-1]
        current_node.add(new_node, current_connector)

        
    def _add_not(self, q):
        
        new_node = SQ()
        self.current_node_stack.append((new_node, SQ.AND))
        self.visit(q.query)
        self.current_node_stack.pop()
        
        if len(new_node)==1 and isinstance(new_node.children[0], SQ) :
            new_node = new_node.children[0]
            
        current_node, current_connector = self.current_node_stack[-1]
        current_node.add(~new_node, current_connector)
        
    def _add_phrase(self, q):
        new_node = SQ(**{q.fieldname+"__exact":" ".join(q.words)})            
        current_node, current_connector = self.current_node_stack[-1]
        current_node.add(new_node, current_connector)

    def _add_prefix(self, q):
        new_node = SQ(**{q.fieldname+"__startswith":q.text})            
        current_node, current_connector = self.current_node_stack[-1]
        current_node.add(new_node, current_connector)

    def _add_range(self, q):
        
        if q.start is None:
            if q.endexcl:
                postfix = "__lt"
            else:
                postfix = "__lte"
            new_node = SQ(**{q.fieldname+postfix:self.__convert_nb(q.end)})
        elif q.end is None:
            if q.startexcl:
                postfix = "__gt"
            else:
                postfix = "__gte"
            new_node = SQ(**{q.fieldname+postfix:self.__convert_nb(q.start)})
        else:
            new_node = SQ(**{q.fieldname+"__range":[self.__convert_nb(q.start),self.__convert_nb(q.end)]})
        
        current_node, current_connector = self.current_node_stack[-1]
        current_node.add(new_node, current_connector)

    def __convert_nb(self, str_nb):        
        try:
            res = int(str_nb)
            return res
        except ValueError:
            try:
                res = float(str_nb)
                return res
            except ValueError:
                return str_nb
        
        
        