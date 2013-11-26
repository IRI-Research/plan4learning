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

import itertools
import os
import signal
from subprocess import PIPE, Popen, STDOUT
import time
import uuid

from django.conf import settings
from django.http.response import StreamingHttpResponse, HttpResponse
from django.utils.translation import ugettext
from django.views.generic.base import TemplateView, View


class ConfirmScriptView(TemplateView):
    template_name = "p4l/admin/confirm_run_script.html"
    
    def get_context_data(self, **kwargs):
        return {
            'command_line' : " ".join(getattr(settings,"ADMIN_SCRIPT", {}).get('args',"")),
            'env' : repr(getattr(settings,"ADMIN_SCRIPT", {}).get('env',{})),
            'cwd' : repr(getattr(settings,"ADMIN_SCRIPT", {}).get('cwd',"")),
        }

class RunScriptView(View):
    
    def __init__(self, **kwargs):
        View.__init__(self, **kwargs)
        self.boundary = "--BOUNDARY--==--%s" % str(uuid.uuid4())

    
    def get(self, request):
        resp = StreamingHttpResponse()
        
        command_kwargs = {
            'shell':False,
            'env':None,
            'cwd':None
        }
        admin_script = getattr(settings,"ADMIN_SCRIPT", {})
        command = admin_script.get('args',"")
        
        if not command:
            return resp

        command_kwargs.update(admin_script,
            stdout=PIPE,
            stderr=STDOUT,
            bufsize=0,
            close_fds=True,
            preexec_fn=os.setsid
        )

        resp['Connection'] = "Keep-Alive"
        doc_start = [
             '<!DOCTYPE html>',
             '<html lang="en">',
             '<head>',
             '<meta charset="utf-8">',
             '<title>output</title>',
             '<style>body {font-family: monospace; white-space: pre;}</style>',
             '</head>',
             '<body>',
        ]
        
        doc_end = [
             '<script>parent.done();</script>',
             '</html>',
             '</body>'
        ]
        
        scroll_to_bottom = '<script type="text/javascript">window.scrollBy(0,50);</script>'

        process = Popen(**command_kwargs)
         
        # Save the pid in the user's session (a thread-safe place)
        request.session['pid'] = process.pid
 
        def read_output():
            for line in iter(process.stdout.readline, b''):
                yield "%s%s" %(line, scroll_to_bottom)
             
        resp.streaming_content = itertools.chain(doc_start, read_output(), doc_end)
        
        return resp


def check_pid(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

class KillScriptView(View):
    
    def get(self, request):
        
        resp = HttpResponse()
        
        pid = request.session.get('pid', None)
        
        if not pid:
            resp.content = ugettext("No active process to kill")
        else:
            os.kill(pid, signal.SIGINT)
            i = 0
            while i <= settings.SCRIPT_MAX_WAIT and check_pid(pid):
                time.sleep(settings.SCRIPT_WAIT)
                i += 1

            if check_pid(pid):
                os.killpg(pid, signal.SIGKILL)
            
            resp.content = ugettext("Success: The process was killed successfully.")
            
        return resp
