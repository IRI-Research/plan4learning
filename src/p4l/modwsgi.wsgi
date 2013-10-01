import os, sys, site

def application(environ, start_response):
    
    global g_env_set
    
    if 'g_env_set' not in globals() or not g_env_set:
        os.environ['DJANGO_SETTINGS_MODULE'] = environ['DJANGO_SETTINGS_MODULE']
    
        prev_sys_path = list(sys.path)
    
        sys.path.append(environ['PROJECT_PATH'])
        for path in environ.get('PYTHON_PATH',"").split(os.pathsep):
            if path:
                site.addsitedir(path)  # @UndefinedVariable
    
        new_sys_path = [] 
        for item in list(sys.path): 
            if item not in prev_sys_path and item not in new_sys_path: 
                new_sys_path.append(item) 
                sys.path.remove(item)
        sys.path[:0] = new_sys_path
        g_env_set = True 

    import django.core.handlers.wsgi

    _application = django.core.handlers.wsgi.WSGIHandler()
    
    if environ.get('PYDEV_DEBUG', "False").lower() in ["true", "1", "t"]:
        import pydevd #@UnresolvedImport
        pydevd.settrace(suspend=False)


    return _application(environ, start_response)
        
