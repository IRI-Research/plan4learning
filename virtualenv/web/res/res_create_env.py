import platform

from lib_create_env import lib_generate_install_methods

system_str = platform.system()


INSTALLS = [ #(key,method, option_str, dict_extra_env)
    {'requirement':'requirement.txt', 'install': {'option_str': None, 'dict_extra_env': None}}, 
#      'SIX',
#      'WSGIREF',
#      'REQUESTS',
#      'SIMPLEJSON',
#      'ISODATE',
#      'PYPARSING',
#      'HTML5LIB',
#      'PSYCOPG2',
#      'DJANGO',
#      'DJANGO-EXTENSIONS',
#      'SOUTH',
#      'RDFLIB',
#      'SPARQLWRAPPER',
#      'DEFUSEDXML',
#      'DJANGO-CORS-HEADERS',
#      'DJANGO-FILTER',
#      'MARKDOWN',
#      'DJANGO-REST-FRAMEWORK',
#      'DJANGO-HAYSTACK',
#      'PYELASTICSEARCH',
#      'WHOOSH'    
]

if system_str == "Linux":
    INSTALLS.insert(2, 'DISTRIBUTE')

OPTIONS_TO_ADD = ['clear', 'type_install=local', 'unzip_setuptools']
if system_str != 'Linux':
    OPTIONS_TO_ADD.append('use_distribute')

def generate_install_methods(path_locations, src_base, run_base, Logger, call_subprocess):    
    return lib_generate_install_methods(path_locations, src_base, run_base, Logger, call_subprocess, INSTALLS, OPTIONS_TO_ADD)
