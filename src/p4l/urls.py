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

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import urls as auth_urls
from django.contrib.auth.decorators import login_required

from p4l.search.views import RecordSearchView
from p4l.views import RecordDetailView, RecordEditView, RecordDeleteView


js_info_dict = {
    'packages': ('p4l',),
    'domain': 'django',
}

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', login_required(RecordSearchView.as_view()), name='p4l_home'),
    url(r'^auth/', include(auth_urls)),
    url(r'^record/view/(?P<slug>\w+)$', login_required(RecordDetailView.as_view()), name='p4l_record_view'),
    url(r'^record/edit/(?P<slug>[\w\:]+)$', login_required(RecordEditView.as_view()), name='p4l_record_edit'),
    url(r'^record/new$', login_required(RecordEditView.as_view(is_create_view=True)), name='p4l_record_new'),
    url(r'^record/delete/(?P<slug>\w+)$', login_required(RecordDeleteView.as_view()), name='p4l_record_delete'),
    url(r'^api/', include('p4l.api.urls')),

    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    url(r'^admin/', include(admin.site.urls)),
    
)