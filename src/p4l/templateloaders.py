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

'''
Created on Oct 9, 2013

From http://djangosnippets.org/snippets/1376/

@author: ymh
'''
from os.path import dirname, join, abspath, isdir

from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_app
from django.template import TemplateDoesNotExist
from django.template.loaders.filesystem import Loader as FilesystemLoader


def get_template_vars(template_name):
    app_name, template_name = template_name.split(":", 1)
    try:
        template_dir = abspath(join(dirname(get_app(app_name).__file__), 'templates'))
    except ImproperlyConfigured:
        raise TemplateDoesNotExist()
    
    return template_name, template_dir

class Loader(FilesystemLoader):
    
    is_usable = True
    
    def get_template_sources(self, template_name, template_dirs=None):
        if ":" not in template_name:
            raise TemplateDoesNotExist()
        template_name, template_dir = get_template_vars(template_name)
        
        if not isdir(template_dir):
            raise TemplateDoesNotExist()

        return [join(template_dir, template_name)]
 
