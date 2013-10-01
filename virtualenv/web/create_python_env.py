"""
Call this like ``python create_python_env.py``; it will
refresh the project-boot.py script

-prerequisite:

- virtualenv
- distribute
- psycopg2 requires the PostgreSQL libpq libraries and the pg_config utility

- python project-boot.py --distribute --no-site-packages --index-url=http://pypi.websushi.org/ --clear --type-install=local --ignore-packages=MYSQL <path_to_venv>
- python project-boot.py --no-site-packages --clear --ignore-packages=MYSQL  --type-install=local <path_to_venv>
- For Linux :
python project-boot.py --unzip-setuptools --no-site-packages --index-url=http://pypi.websushi.org/ --clear --type-install=local <path_to_venv>

Probleme avec mysql :

sudo install_name_tool -change libmysqlclient.18.dylib /usr/local/mysql/lib/libmysqlclient.18.dylib ~/dev/workspace/platform/virtualenv/web/env/venv_platform/lib/python2.7/site-packages/_mysql.so

"""

import os
import subprocess
import re
import sys


here = os.path.dirname(os.path.abspath(__file__))
base_dir = here
script_name = os.path.join(base_dir, 'project-boot.py')

import virtualenv

src_base = os.path.abspath(os.path.join(here,"..","res","src")).replace("\\","/")
lib_path = os.path.abspath(os.path.join(here,"..","res","lib")).replace("\\","/")
patch_path = os.path.abspath(os.path.join(here,"res","patch")).replace("\\","/")


EXTRA_TEXT  = "import sys\n"
EXTRA_TEXT += "sys.path.append('%s')\n" % (lib_path)
EXTRA_TEXT += "sys.path.append('%s')\n" % (os.path.abspath(os.path.join(here,"res")).replace("\\","/"))
EXTRA_TEXT += "from res_create_env import generate_install_methods\n"
EXTRA_TEXT += "adjust_options, extend_parser, after_install = generate_install_methods(path_locations, '%s', '%s', Logger, call_subprocess)\n" % (src_base, here)

def main():
    python_version = ".".join(map(str,sys.version_info[0:2]))
    text = virtualenv.create_bootstrap_script(EXTRA_TEXT, python_version=python_version)
    if os.path.exists(script_name):
        f = open(script_name)
        cur_text = f.read()
        f.close()
    else:
        cur_text = ''
    print 'Updating %s' % script_name
    if cur_text == 'text':
        print 'No update'
    else:
        print 'Script changed; updating...'
        f = open(script_name, 'w')
        f.write(text)
        f.close()

if __name__ == '__main__':
    main()

