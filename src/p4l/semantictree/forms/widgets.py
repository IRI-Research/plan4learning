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

from django import forms
from django.core.exceptions import ValidationError
from django.forms.util import flatatt
from django.utils.html import format_html
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

import logging
logger = logging.getLogger(__name__)

class SemanticTreeWidget(forms.TextInput):
    """
    A widget that enables to request semantic trees
    """
    
    class Media:
        css = {
            'all': ('semantictree/semantictree.css',)
        }
        js = ('semantictree/semantictree.js',)
    
    # The user can add css classes but we always add "semantic-tree" class
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        # Test if class attr is here
        if "class" in final_attrs:
            final_attrs["class"] += " semantic-tree"
        else:
            final_attrs["class"] = "semantic-tree"
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        final_attrs['placeholder'] = _("Search")
        input_res = format_html('<input{0} />', flatatt(final_attrs))
        
        if "data-url" not in final_attrs or "data-query" not in final_attrs or "data-root-query" not in final_attrs or "data-childs-query" not in final_attrs or "data-child-count-query" not in final_attrs:
            raise ValidationError(_('"data-url", "data-query", "data-root-query", "data-childs-query" and "data-child-count-query" must be set in CharField configuration'))
        dialog_text = _("Browse")
        
        dialog_res = "<span id=\"dialog-link-container-" + final_attrs["name"] + "\" class=\"dialog-link-container ui-state-default ui-corner-all\"><a href=\"#\" id=\"dialog-link-" + final_attrs["name"] + "\" class=\"dialog-link\" title=\"%s\">%s</a></span>" % (dialog_text,dialog_text)
        dialog_res += '<span id="dialog-' + final_attrs["name"] + '" class="dialog" title="Select term"><span id="term-tree-' + final_attrs["name"] + '"></span></span>'
        
        return input_res + " " + _("or") + " " + dialog_res


class SemanticTagItWidget(forms.TextInput):
    """
    A widget that enables to request semantic trees
    """
    
    class Media:
        css = {
            'all': ('semantictree/semantictree.css',)
        }
        js = ('semantictree/semantictree.js',)
    
    # The user can add css classes but we always add "semantic-tree" class
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        # Test if class attr is here
        if "class" in final_attrs:
            final_attrs["class"] += " semantic-tree-tagit"
        else:
            final_attrs["class"] = "semantic-tree-tagit"
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        
        input_res = format_html('<input{0} />', flatatt(final_attrs))
        
        if "data-url" not in final_attrs or "data-query" not in final_attrs or "data-root-query" not in final_attrs or "data-childs-query" not in final_attrs or "data-child-count-query" not in final_attrs:
            raise ValidationError(_('"data-url", "data-query", "data-root-query", "data-childs-query" and "data-child-count-query" must be set in CharField configuration'))
        dialog_text = _("Browse")
        
        dialog_res = "<span id=\"dialog-link-container-" + final_attrs["name"] + "\" class=\"dialog-link-container ui-state-default ui-corner-all\"><a href=\"#\" id=\"dialog-link-" + final_attrs["name"] + "\" class=\"dialog-link\" title=\"%s\">%s</a></span>" % (dialog_text,dialog_text)
        dialog_res += '<span id="dialog-' + final_attrs["name"] + '" class="dialog" title="Select term"><span id="term-tree-' + final_attrs["name"] + '"></span></span>'
        
        return input_res + " " + _("or") + " " + dialog_res