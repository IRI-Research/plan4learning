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

@author: ymh
'''

from django.conf.urls import patterns, url
from django.contrib.admin import AdminSite as DjangoAdminSite

from p4l.admin.views import RunScriptView, ConfirmScriptView, KillScriptView
from p4l.decorators import is_staff


class AdminSite(DjangoAdminSite):
    
    login_template = "registration/login.html"

    
    def get_urls(self):
        urlpatterns = DjangoAdminSite.get_urls(self)
        
        urlpatterns += patterns('',
            url(r'^confirm_script$', is_staff(ConfirmScriptView.as_view()), name='confirm_script'),
            url(r'^run_script$', is_staff(RunScriptView.as_view()), name='run_script'),
            url(r'^kill_script$', is_staff(KillScriptView.as_view()), name='kill_script')
        )
        
        return urlpatterns

site = AdminSite()

