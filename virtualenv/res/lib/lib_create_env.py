import sys
import os
import os.path
import shutil
import tarfile
import zipfile
import urllib
import platform
import patch
import struct
import glob
import re

join = os.path.join
system_str = platform.system()

URLS = {
    #'': {'setup': '', 'url':'', 'local':''},
    'DISTRIBUTE': {'setup': 'distribute', 'url':'http://pypi.python.org/packages/source/d/distribute/distribute-0.6.34.tar.gz', 'local':"distribute-0.6.34.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'DJANGO': {'setup': 'django', 'url': 'https://github.com/IRI-Research/django/archive/1.5.4+IRI.tar.gz', 'local':"django-1.5.4-IRI.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'SIX' : {'setup':'six', 'url':'https://pypi.python.org/packages/source/s/six/six-1.3.0.tar.gz', 'local': 'six-1.3.0.tar.gz', 'install' : {'method':'pip', 'option_str': None, 'dict_extra_env': None}},
    'DJANGO-EXTENSIONS': { 'setup': 'django-extensions', 'url':'https://github.com/django-extensions/django-extensions/archive/1.1.1.tar.gz', 'local':"django-extensions-1.1.1.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'SOUTH': { 'setup': 'South', 'url':'http://www.aeracode.org/releases/south/south-0.7.6.tar.gz', 'local':"south-0.7.6.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'RDFLIB' : {'setup':'rdflib', 'url':'https://github.com/RDFLib/rdflib/archive/4.0.1.tar.gz', 'local': 'rdflib-4.0.1.tar.gz', 'install' : {'method':'pip', 'option_str': None, 'dict_extra_env': None}},
    'REQUESTS': {'setup': 'requests', 'url':'https://github.com/kennethreitz/requests/archive/v1.2.3.tar.gz', 'local':'requests-1.2.3.tar.gz', 'install' : {'method':'pip', 'option_str': None, 'dict_extra_env': None}},
    'SIMPLEJSON': {'setup': 'simplejson','url':'https://github.com/simplejson/simplejson/archive/v3.3.0.tar.gz', 'local': 'simplejson-3.3.0.tar.gz', 'install' : {'method':'pip', 'option_str': None, 'dict_extra_env': None}},
    'ISODATE': {'setup': 'isodate','url':'https://pypi.python.org/packages/source/i/isodate/isodate-0.4.9.tar.gz', 'local': 'isodate-0.4.9.tar.gz', 'install' : {'method':'pip', 'option_str': None, 'dict_extra_env': None}},
    'PYPARSING': {'setup': 'pyparsing','url':'http://downloads.sourceforge.net/project/pyparsing/pyparsing/pyparsing-1.5.7/pyparsing-1.5.7.tar.gz', 'local': 'pyparsing-1.5.7.tar.gz', 'install' : {'method':'pip', 'option_str': None, 'dict_extra_env': None}},
    'SPARQLWRAPPER': {'setup': 'sparqlwrapper','url':'http://downloads.sourceforge.net/project/sparql-wrapper/sparql-wrapper-python/1.5.2/SPARQLWrapper-1.5.2.tar.gz', 'local': 'SPARQLWrapper-1.5.2.tar.gz', 'install' : {'method':'pip', 'option_str': None, 'dict_extra_env': None}},
    'HTML5LIB': {'setup': 'html5lib','url':'https://github.com/html5lib/html5lib-python/archive/1.0b3.tar.gz', 'local': 'html5lib-1.0b3.tar.gz', 'install' : {'method':'pip', 'option_str': None, 'dict_extra_env': None}},
    'PSYCOPG2': {'setup': 'psycopg2','url': 'http://initd.org/psycopg/tarballs/PSYCOPG-2-5/psycopg2-2.5.tar.gz', 'local':"psycopg2-2.5.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'DEFUSEDXML': {'setup': 'defusedxml','url': 'https://pypi.python.org/packages/source/d/defusedxml/defusedxml-0.4.1.tar.gz', 'local':"defusedxml-0.4.1.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'DJANGO-CORS-HEADERS': {'setup': 'django-cors-headers','url': 'https://pypi.python.org/packages/source/d/django-cors-headers/django-cors-headers-0.11.tar.gz', 'local':"django-cors-headers-0.11.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'DJANGO-FILTER': {'setup': 'django-filter','url': 'https://github.com/alex/django-filter/archive/v0.7.tar.gz', 'local':"django-filter-0.7.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'DJANGO-REST-FRAMEWORK': {'setup': 'djangorestframework','url': 'https://pypi.python.org/packages/source/d/djangorestframework/djangorestframework-2.3.7.tar.gz', 'local':"djangorestframework-2.3.7.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'MARKDOWN': {'setup': 'markdown','url': 'https://pypi.python.org/packages/source/M/Markdown/Markdown-2.3.1.tar.gz', 'local':"Markdown-2.3.1.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'WSGIREF': {'setup': 'wsgiref','url': 'https://pypi.python.org/packages/source/w/wsgiref/wsgiref-0.1.2.zip', 'local':"wsgiref-0.1.2.zip", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'HAYSTACK': {'setup': 'django-haystack','url': 'https://github.com/toastdriven/django-haystack/archive/v2.1.0.tar.gz', 'local':"django-haystack-2.1.0.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'PYELASTICSEARCH': {'setup': 'pyelasticsearch','url': 'https://pypi.python.org/packages/source/p/pyelasticsearch/pyelasticsearch-0.6.tar.gz', 'local':"pyelasticsearch-0.6.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
    'WHOOSH': {'setup': 'whoosh','url': 'https://pypi.python.org/packages/source/W/Whoosh/Whoosh-2.5.3.tar.gz', 'local':"Whoosh-2.5.3.tar.gz", 'install': {'method': 'pip', 'option_str': None, 'dict_extra_env': None}},
}

class ResourcesEnv(object):

    def __init__(self, src_base, run_base, urls, normal_installs):
        self.src_base = src_base
        self.run_base = run_base
        self.URLS = {}
        self.__init_url(urls)
        self.NORMAL_INSTALL = normal_installs

    def get_src_base_path(self, fpath):
        return os.path.abspath(os.path.join(self.src_base, fpath)).replace("\\","/")

    def get_run_res_base_path(self, fpath):
        return os.path.abspath(os.path.join(self.run_base, 'res', fpath)).replace("\\","/")    
    
    def __add_package_def(self, key, dict):
        self.URLS[key] = dict
        
    def __init_url(self, urls):
        for key, url_dict in urls.items():
            url_dict_copy = url_dict.copy()
            if url_dict.get('install', {}).get('method','pip') == 'pip-req':
                get_base_path = self.get_run_res_base_path
            else:
                get_base_path = self.get_src_base_path                                
            if not url_dict['url'].startswith("http://"):
                url_dict_copy['url'] = get_base_path(url_dict['url'])
            url_dict_copy['local'] = get_base_path(url_dict['local'])

            self.__add_package_def(key, url_dict_copy )

def ensure_dir(dir, logger):
    logger.notify('Check directory %s' % dir)
    if not os.path.exists(dir):
        logger.notify('Creating directory %s' % dir)
        os.makedirs(dir)

def extend_parser(parser):    
    parser.add_option(
        '--index-url',
        metavar='INDEX_URL',
        dest='index_url',
        default='http://pypi.python.org/simple/',
        help='base URL of Python Package Index')
    parser.add_option(
        '--type-install',
        metavar='type_install',
        dest='type_install',
        help='type install : local, url, setup - default : local')
    parser.add_option(
        '--ignore-packages',
        metavar='ignore_packages',
        dest='ignore_packages',
        default=None,
        help='list of comma separated keys for package to ignore')    

def install_psycopg2(option_str, extra_env, res_source_key, home_dir, lib_dir, tmp_dir, src_dir, res_env, logger, call_subprocess, filter_python_develop):
    psycopg2_src = os.path.join(src_dir,"psycopg2.zip")
    shutil.copy(res_env.URLS['PSYCOPG2'][res_source_key], psycopg2_src)
    #extract psycopg2
    zf = zipfile.ZipFile(psycopg2_src)
    psycopg2_base_path = os.path.join(src_dir,"psycopg2")
    zf.extractall(psycopg2_base_path)
    zf.close()
    
    psycopg2_src_path = os.path.join(psycopg2_base_path, os.listdir(psycopg2_base_path)[0])
    shutil.copytree(os.path.join(psycopg2_src_path, 'psycopg2'), os.path.abspath(os.path.join(home_dir, 'Lib/site-packages', 'psycopg2')))
    shutil.copy(os.path.join(psycopg2_src_path, 'psycopg2-2.4.5-py2.7.egg-info'), os.path.abspath(os.path.join(home_dir, 'Lib/site-packages', 'site-packages')))
    

def install_mysql(option_str, extra_env, res_source_key, home_dir, lib_dir, tmp_dir, src_dir, res_env, logger, call_subprocess, filter_python_develop):
    
    args = [os.path.abspath(os.path.join(home_dir, 'bin', 'pip')), 'install', res_env.URLS['MYSQL'][res_source_key]]                
    if option_str :
        args.insert(4,option_str)
    call_subprocess(args,
            cwd=os.path.abspath(tmp_dir),
            filter_stdout=filter_python_develop,
            show_stdout=True,
            extra_env=extra_env)

    mysqlconfig_output = []
    
    call_subprocess(['mysql_config', '--libmysqld-libs'],
        cwd=os.path.abspath(tmp_dir),
        filter_stdout=lambda line: mysqlconfig_output.append(line),
        show_stdout=True)
        
    mysqlconfig_output = "".join(mysqlconfig_output)
    m = re.search("\-L[\'\"]?([\w\/]+)[\'\"]?", mysqlconfig_output)
    if m:
        repdylibpath = m.group(1)
    else:
        repdylibpath = '/usr/local/mysql/lib'
        
    dyliblist = glob.glob(repdylibpath+"/libmysqlclient.*.dylib")
    def key_func(s):
        m = re.match(repdylibpath+"/libmysqlclient\.([\d]+)\.dylib", s)
        if m:
            return int(m.group(1))
        else:
            return sys.maxint
    dyliblist.sort(key=key_func)
    
    if dyliblist:
        dylibpath = dyliblist[0]
    else:
        dylibpath = '/usr/local/mysql/lib/libmysqlclient.18.dylib'
        
    dylibname = os.path.basename(dylibpath)    
    sopath = os.path.join(os.path.abspath(lib_dir), 'site-packages', '_mysql.so')
    
    call_subprocess(['install_name_tool', '-change', dylibname, dylibpath, sopath],
        cwd=os.path.abspath(tmp_dir),
        filter_stdout=filter_python_develop,
        show_stdout=True)


def gen_install_comp_lib(lib_name, lib_key, configure_options=[]):
    
    def install_lib(option_str, extra_env, res_source_key, home_dir, lib_dir, tmp_dir, src_dir, res_env, logger, call_subprocess, filter_python_develop):
        lib_src = os.path.join(src_dir,lib_name+".tar.gz")
        logger.notify("Copy %s to %s " % (res_env.URLS[lib_key][res_source_key],lib_src))
        shutil.copy(res_env.URLS[lib_key][res_source_key], lib_src)
        tf = tarfile.open(lib_src,'r:gz')
        lib_base_path = os.path.join(src_dir, lib_name) 
        logger.notify("Extract %s to %s " % (lib_name,lib_base_path))
        tf.extractall(lib_base_path)
        tf.close()
        
        lib_src_path = os.path.join(lib_base_path, os.listdir(lib_base_path)[0])
    
        logger.notify(lib_name + " configure in " + lib_src_path)
        call_subprocess(['./configure', '--prefix='+os.path.abspath(home_dir)] + configure_options,
                        cwd=os.path.abspath(lib_src_path),
                        filter_stdout=filter_python_develop,
                        show_stdout=True)
        
        logger.notify(lib_name + " make in " + lib_src_path)
        call_subprocess(['make'],
                        cwd=os.path.abspath(lib_src_path),
                        filter_stdout=filter_python_develop,
                        show_stdout=True)
    
        logger.notify(lib_name + "make install in " + lib_src_path)
        call_subprocess(['make', 'install'],
                        cwd=os.path.abspath(lib_src_path),
                        filter_stdout=filter_python_develop,
                        show_stdout=True)
    return install_lib

install_libjpeg = gen_install_comp_lib("libjpeg", "LIBJPEG", ['--enable-shared'])
install_zlib = gen_install_comp_lib("zlib", "ZLIB", [])
    

def lib_generate_install_methods(path_locations, src_base, run_base, Logger, call_subprocess, normal_installs, options_to_add=None, urls= None):
    
    all_urls = URLS.copy()
    if urls is not None:
        all_urls.update(urls)
        
    res_env = ResourcesEnv(src_base, run_base, all_urls, normal_installs)

    def filter_python_develop(line):
        if not line.strip():
            return Logger.DEBUG
        for prefix in ['Searching for', 'Reading ', 'Best match: ', 'Processing ',
                       'Moving ', 'Adding ', 'running ', 'writing ', 'Creating ',
                       'creating ', 'Copying ']:
            if line.startswith(prefix):
                return Logger.DEBUG
        return Logger.NOTIFY
    
    
    def normal_install(key, res_path, method, option_str, extra_env, res_source_key, home_dir, tmp_dir, res_env, logger, call_subprocess):
        logger.notify("Install %s from %s with %s" % (key,res_path,method))
        if method == 'pip':
            if sys.platform == 'win32':
                args = [os.path.abspath(os.path.join(home_dir, 'Scripts', 'pip')), 'install', res_path]
            else:
                args = [os.path.abspath(os.path.join(home_dir, 'bin', 'pip')), 'install', res_path]
            if option_str :
                args.append(option_str)
            if res_source_key == 'local':
                if extra_env is None:
                    extra_env = {}
                extra_env["PIP_DOWNLOAD_CACHE"] = res_env.get_src_base_path("")
                args.insert(2, '-f')
                args.insert(3, res_env.get_src_base_path(""))
                args.insert(4, '--no-index')
            logger.notify("Install %s from %s with %s args %s " % (key,res_path,method, repr(args)))
            call_subprocess(args,
                    cwd=os.path.abspath(tmp_dir),
                    filter_stdout=filter_python_develop,
                    show_stdout=True,
                    extra_env=extra_env)
        if method == 'pip-req':
            if sys.platform == 'win32':
                args = [os.path.abspath(os.path.join(home_dir, 'Scripts', 'pip')), 'install', '-r', res_path]
            else:
                args = [os.path.abspath(os.path.join(home_dir, 'bin', 'pip')), 'install', '-r', res_path]
            if option_str :
                args.append(option_str)
            if res_source_key == 'local':
                if extra_env is None:
                    extra_env = {}
                extra_env["PIP_DOWNLOAD_CACHE"] = res_env.get_src_base_path("")
                args.insert(2, '-f')
                args.insert(3, res_env.get_src_base_path(""))
                args.insert(4, '--no-index')
            logger.notify("Install %s from %s with %s args %s " % (key,res_path,method, repr(args)))
            call_subprocess(args,
                    cwd=os.path.abspath(tmp_dir),
                    filter_stdout=filter_python_develop,
                    show_stdout=True,
                    extra_env=extra_env)
        else:
            if sys.platform == 'win32':
                args = [os.path.abspath(os.path.join(home_dir, 'Scripts', 'easy_install')), res_path]
            else:
                args = [os.path.abspath(os.path.join(home_dir, 'bin', 'easy_install')), res_path]
            if option_str :
                args.insert(1,option_str)
            call_subprocess(args,
                    cwd=os.path.abspath(tmp_dir),
                    filter_stdout=filter_python_develop,
                    show_stdout=True,
                    extra_env=extra_env)            
 
    
    def after_install(options, home_dir):
        
        global logger
        
        verbosity = options.verbose - options.quiet
        logger = Logger([(Logger.level_for_integer(2-verbosity), sys.stdout)])

        
        home_dir, lib_dir, inc_dir, bin_dir = path_locations(home_dir)
        base_dir = os.path.dirname(home_dir)
        src_dir = os.path.join(home_dir, 'src')
        tmp_dir = os.path.join(home_dir, 'tmp')
        ensure_dir(src_dir, logger)
        ensure_dir(tmp_dir, logger)
        system_str = platform.system()
                
        res_source_key = getattr(options, 'type_install') if hasattr(options, 'type_install') else 'local' #.get('type_install', 'local')
        if res_source_key is None:
            res_source_key = 'local'
        
        ignore_packages = []
        
        if system_str == 'Windows':
            default_install_options = {'method': 'easy_install', 'option_str': None, 'dict_extra_env': {}}
        else:
            default_install_options = {'method': 'pip', 'option_str': None, 'dict_extra_env': {}}
            
        if options.ignore_packages :
            ignore_packages = options.ignore_packages.split(",")
        
        logger.indent += 2
        try:    
            for key in res_env.NORMAL_INSTALL:
                install_options = None
                if isinstance(key, dict):
                    install_options = key.get('install', default_install_options)
                    install_options['method'] = 'pip-req'
                    res_path = res_env.get_run_res_base_path(key['requirement'])
                else:
                    if key not in res_env.URLS:
                        logger.notify("%s not found in def : passing" % (key,))
                    install_options = res_env.URLS[key].get('install', None)
                    res_path = res_env.URLS[key][res_source_key]
                if install_options is None:
                    install_options = default_install_options
                method = install_options.get('method', default_install_options['method'])
                option_str = install_options.get('option_str', default_install_options['option_str'])
                extra_env = install_options.get('dict_extra_env', default_install_options['dict_extra_env'])
                if not extra_env:
                    extra_env = {}
                    
                if 'TMPDIR' not in extra_env:
                    extra_env['TMPDIR'] = os.path.abspath(tmp_dir)          
                #isinstance(lst, (list, tuple))
                if key not in ignore_packages:
                    logger.notify("install %s with method %s" % (key, repr(method)))
                    if callable(method):
                        method(option_str, extra_env, res_source_key, home_dir, lib_dir, tmp_dir, src_dir, res_env, logger, call_subprocess, filter_python_develop)
                    elif method in globals() and callable(globals()[method]) and method not in ['pip', 'easy_install']:  
                        globals()[method](option_str, extra_env, res_source_key, home_dir, lib_dir, tmp_dir, src_dir, res_env, logger, call_subprocess, filter_python_develop)
                    else:
                        normal_install(key, res_path, method, option_str, extra_env, res_source_key, home_dir, tmp_dir, res_env, logger, call_subprocess)
                            
            logger.notify("Clear source dir")
            shutil.rmtree(src_dir)
    
        finally:
            logger.indent -= 2
        script_dir = join(base_dir, bin_dir)
        logger.notify('Run "%s Package" to install new packages that provide builds'
                      % join(script_dir, 'easy_install'))
    
    def adjust_options(options, args):
        if not options_to_add:
            pass
        for opt in options_to_add:
            test_opt = opt.split('=',1)[0]
            #if not hasattr(options,test_opt) or getattr(options, test_opt) is None:
            setattr(options, test_opt,opt.split('=',1)[1] if "=" in opt else True)

    return adjust_options, extend_parser, after_install
