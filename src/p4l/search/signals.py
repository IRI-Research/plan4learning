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
from django.db import models
from haystack import signals

import p4l.models.signals


class P4lSignalProcessor(signals.BaseSignalProcessor):
    
    def handle_delete(self, sender, instance, **kwargs):
        if getattr(settings, "REALTIME_INDEXING", True):
            signals.BaseSignalProcessor.handle_delete(self, sender, instance, **kwargs)
    
    def handle_save(self, sender, instance, **kwargs):
        if getattr(settings, "REALTIME_INDEXING", True):
            signals.BaseSignalProcessor.handle_save(self, sender, instance, **kwargs)
    
    def __connect_signals(self, klass):        
        p4l.models.signals.record_saved.connect(self.handle_save, sender=klass)
        models.signals.post_delete.connect(self.handle_delete, sender=klass)        

    def __disconnect_signals(self, klass):
        p4l.models.signals.record_saved.disconnect(self.handle_save, sender=klass)
        models.signals.post_delete.disconnect(self.handle_delete, sender=klass)

    
    def setup(self):
        #put import here to avoid circular         
        from p4l.models.data import Record
        self.__connect_signals(Record)



    def teardown(self):

        from p4l.models.data import Record
        self.__disconnect_signals(Record)
        