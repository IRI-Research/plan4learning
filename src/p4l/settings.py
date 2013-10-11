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

# Django settings for p4l project.
from django.conf import global_settings
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

ugettext = lambda s: s

LANGUAGES = ( 
    ('fr', ugettext('French')),
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
)


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'p4l.templateloaders.Loader'
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'p4l.urls'

AUTH_USER_MODEL = 'p4l.User'
INITIAL_CUSTOM_USER_MIGRATION = "0001_initial"


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'p4l.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django_extensions',
    'south',
    'rest_framework',
    'haystack',
    'p4l'
)

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'p4l.context_processors.version',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

NB_RECORDS_BY_PAGE = 20

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': '',
        'INDEX_NAME': 'p4l',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'p4l.search.signals.P4lSignalProcessor'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = NB_RECORDS_BY_PAGE

REALTIME_INDEXING = True

CACHES = {
    'default' : {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'indexation': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'p4l-indexation',
        'TIMEOUT': 300,
    }
}




RDF_SCHEMES = { 
    'organizations': 'http://www.iiep.unesco.org/plan4learning/scheme/Organizations',
    'audiences': '',
    'languages': 'http://www.iiep.unesco.org/plan4learning/scheme/Languages',
    'types': 'http://www.iiep.unesco.org/plan4learning/scheme/DocumentType',
    'subjects': 'http://skos.um.es/unescothes/CS000',
    'themes': 'http://www.iiep.unesco.org/plan4learning/scheme/Themes',
    'countries': 'http://skos.um.es/unescothes/CS000/Countries',    
    'projects': 'http://www.iiep.unesco.org/plan4learning/scheme/Projects'
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
                  
    'PAGINATE_BY': 20,
    'PAGINATE_BY_PARAM': 'page_size' 
}

LANGUAGES_LIST = [
(u"French", "fr"),
(u"English", "en"),
(u"Spanish; Castilian", "es"),
(u"", ""),
(u"Abkhaz", "ab"),
(u"Afar", "aa"),
(u"Afrikaans", "af"),
(u"Akan", "ak"),
(u"Albanian", "sq"),
(u"Amharic", "am"),
(u"Arabic", "ar"),
(u"Aragonese", "an"),
(u"Armenian", "hy"),
(u"Assamese", "as"),
(u"Avaric", "av"),
(u"Avestan", "ae"),
(u"Aymara", "ay"),
(u"Azerbaijani", "az"),
(u"Bambara", "bm"),
(u"Bashkir", "ba"),
(u"Basque", "eu"),
(u"Belarusian", "be"),
(u"Bengali; Bangla", "bn"),
(u"Bihari", "bh"),
(u"Bislama", "bi"),
(u"Bosnian", "bs"),
(u"Breton", "br"),
(u"Bulgarian", "bg"),
(u"Burmese", "my"),
(u"Catalan", "ca"),
(u"Chamorro", "ch"),
(u"Chechen", "ce"),
(u"Chichewa; Chewa; Nyanja", "ny"),
(u"Chinese", "zh"),
(u"Chuvash", "cv"),
(u"Cornish", "kw"),
(u"Corsican", "co"),
(u"Cree", "cr"),
(u"Croatian", "hr"),
(u"Czech", "cs"),
(u"Danish", "da"),
(u"Divehi; Dhivehi; Maldivian;", "dv"),
(u"Dutch", "nl"),
(u"Dzongkha", "dz"),
(u"English", "en"),
(u"Esperanto", "eo"),
(u"Estonian", "et"),
(u"Ewe", "ee"),
(u"Faroese", "fo"),
(u"Fijian", "fj"),
(u"Finnish", "fi"),
(u"French", "fr"),
(u"Fula; Fulah; Pulaar; Pular", "ff"),
(u"Galician", "gl"),
(u"Ganda", "lg"),
(u"Georgian", "ka"),
(u"German", "de"),
(u"Greek Modern", "el"),
(u"Guarani", "gn"),
(u"Gujarati", "gu"),
(u"Haitian; Haitian Creole", "ht"),
(u"Hausa", "ha"),
(u"Hebrew", "he"),
(u"Herero", "hz"),
(u"Hindi", "hi"),
(u"Hiri Motu", "ho"),
(u"Hungarian", "hu"),
(u"Icelandic", "is"),
(u"Ido", "io"),
(u"Igbo", "ig"),
(u"Indonesian", "id"),
(u"Interlingua", "ia"),
(u"Interlingue", "ie"),
(u"Inuktitut", "iu"),
(u"Inupiaq", "ik"),
(u"Irish", "ga"),
(u"Italian", "it"),
(u"Japanese", "ja"),
(u"Javanese", "jv"),
(u"Kalaallisut; Greenlandic", "kl"),
(u"Kannada", "kn"),
(u"Kanuri", "kr"),
(u"Kashmiri", "ks"),
(u"Kazakh", "kk"),
(u"Khmer", "km"),
(u"Kikuyu; Gikuyu", "ki"),
(u"Kinyarwanda", "rw"),
(u"Kirundi", "rn"),
(u"Komi", "kv"),
(u"Kongo", "kg"),
(u"Korean", "ko"),
(u"Kurdish", "ku"),
(u"Kwanyama; Kuanyama", "kj"),
(u"Kyrgyz", "ky"),
(u"Lao", "lo"),
(u"Latin", "la"),
(u"Latvian", "lv"),
(u"Limburgish; Limburgan; Limburger", "li"),
(u"Lingala", "ln"),
(u"Lithuanian", "lt"),
(u"Luba-Katanga", "lu"),
(u"Luxembourgish; Letzeburgesch", "lb"),
(u"Macedonian", "mk"),
(u"Malagasy", "mg"),
(u"Malay", "ms"),
(u"Malayalam", "ml"),
(u"Maltese", "mt"),
(u"Manx", "gv"),
(u"Marathi", "mr"),
(u"Marshallese", "mh"),
(u"Mongolian", "mn"),
(u"Maori", "mi"),
(u"Nauru", "na"),
(u"Navajo; Navaho", "nv"),
(u"Ndonga", "ng"),
(u"Nepali", "ne"),
(u"North Ndebele", "nd"),
(u"Northern Sami", "se"),
(u"Norwegian", "no"),
(u"Norwegian Bokmal", "nb"),
(u"Norwegian Nynorsk", "nn"),
(u"Nuosu", "ii"),
(u"Occitan", "oc"),
(u"Ojibwe; Ojibwa", "oj"),
(u"Church Slavic; Church Slavonic", "cu"),
(u"Oriya", "or"),
(u"Oromo", "om"),
(u"Ossetian; Ossetic", "os"),
(u"Panjabi; Punjabi", "pa"),
(u"Pashto; Pushto", "ps"),
(u"Persian", "fa"),
(u"Polish", "pl"),
(u"Portuguese", "pt"),
(u"Pali", "pi"),
(u"Quechua", "qu"),
(u"Romanian; Moldavian", "ro"),
(u"Romansh", "rm"),
(u"Russian", "ru"),
(u"Samoan", "sm"),
(u"Sango", "sg"),
(u"Sanskrit (Samskrta),sa"),
(u"Sardinian", "sc"),
(u"Scottish Gaelic; Gaelic", "gd"),
(u"Serbian", "sr"),
(u"Shona", "sn"),
(u"Sindhi", "sd"),
(u"Sinhala; Sinhalese", "si"),
(u"Slovak", "sk"),
(u"Slovene", "sl"),
(u"Somali", "so"),
(u"South Azerbaijani", "az"),
(u"South Ndebele", "nr"),
(u"Southern Sotho", "st"),
(u"Spanish; Castilian", "es"),
(u"Sundanese", "su"),
(u"Swahili", "sw"),
(u"Swati", "ss"),
(u"Swedish", "sv"),
(u"Tagalog", "tl"),
(u"Tahitian", "ty"),
(u"Tajik", "tg"),
(u"Tamil", "ta"),
(u"Tatar", "tt"),
(u"Telugu", "te"),
(u"Thai", "th"),
(u"Tibetan", "bo"),
(u"Tigrinya", "ti"),
(u"Tonga", "to"),
(u"Tsonga", "ts"),
(u"Tswana", "tn"),
(u"Turkish", "tr"),
(u"Turkmen", "tk"),
(u"Twi", "tw"),
(u"Ukrainian", "uk"),
(u"Urdu", "ur"),
(u"Uyghur; Uighur", "ug"),
(u"Uzbek", "uz"),
(u"Venda", "ve"),
(u"Vietnamese", "vi"),
(u"Volapuk", "vo"),
(u"Walloon", "wa"),
(u"Welsh", "cy"),
(u"Western Frisian", "fy"),
(u"Wolof", "wo"),
(u"Xhosa", "xh"),
(u"Yiddish", "yi"),
(u"Yoruba", "yo"),
(u"Zhuang; Chuang", "za"),
(u"Zulu", "zu")]

# cf http://docs.python.org/2/library/subprocess.html#popen-constructor 
ADMIN_SCRIPT = {}

SCRIPT_WAIT = .250
SCRIPT_MAX_WAIT = 40 # * SCRIPT_WAIT = 10 sec

from config import *  # @UnusedWildImport

if not "SRC_BASE_URL" in locals():
    SRC_BASE_URL = BASE_URL + __name__.split('.')[0] + '/'
if not "LOGIN_URL" in locals():
    LOGIN_URL = SRC_BASE_URL + 'auth/login/'
if not "LOGOUT_URL" in locals():
    LOGOUT_URL = SRC_BASE_URL + 'auth/disconnect/'
if not "LOGIN_REDIRECT_URL" in locals():
    LOGIN_REDIRECT_URL = SRC_BASE_URL
if not "LOGOUT_REDIRECT_URL" in locals():
    LOGOUT_REDIRECT_URL = SRC_BASE_URL + 'auth/login'

if not "SPARQL_QUERY_ENDPOINT" in locals():    
    SPARQL_QUERY_ENDPOINT = "http://localhost:8080/openrdf-sesame/repositories/plan4learning"

if not "SPARQL_REF_QUERIES" in locals():
    SPARQL_REF_QUERIES = {
        'subjects': {
            'url' : SPARQL_QUERY_ENDPOINT,
            'filter' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                    "?uri a skos:Concept. "
                    "?uri skos:inScheme <http://skos.um.es/unescothes/CS000> . "
                    "?uri skos:prefLabel ?label. "
                    "FILTER (lang(?label) = {lang}). "
                    "?uri skos:prefLabel ?lab. "
                    "FILTER regex (str(?lab), ?reg, 'i'). "
                    "FILTER (lang (?lab) = {lang}). "
                    "BIND (STRLEN(STRBEFORE (str(?lab), ?reg)) AS ?place). "
                    "BIND (STRLEN(STR(?lab)) AS ?len) "
                "}} "
                "ORDER BY ?place ?len ?lab"
            ),
            "root" : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label ?type "
                "WHERE {{ "
                    "?uri a skos:Collection ; "
                         "skos:inScheme <http://skos.um.es/unescothes/CS000> ; "
                         "skos:prefLabel|rdfs:label ?label ; "
                         "rdf:type ?type . "
                    "FILTER (lang(?label) = {lang}). " 
                    "FILTER NOT EXISTS {{ [skos:member ?uri] }}. "
                "}} "
                "ORDER BY ?label"
            ),
            "childs" : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label ?type "
                "WHERE {{ "
                  "?uri skos:inScheme <http://skos.um.es/unescothes/CS000> . "
                  "{{ ?uri a ?type "
                    "FILTER (?type = skos:Collection || ?type = skos:Concept) }}. "
                  "?root skos:narrower|skos:member ?uri. "
                  "?uri skos:prefLabel|rdfs:label ?label. "
                  "FILTER (lang(?label) = {lang}). "
                "}} "
                "ORDER BY ?label"
            ),
            "child-count" : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT (COUNT(?uri) as ?nb) "
                "WHERE {{ "
                    "?uri skos:inScheme <http://skos.um.es/unescothes/CS000> . "
                    "?root skos:narrower|skos:member ?uri. "
                "}}"
            )
        },
        'themes': {
            'url' : SPARQL_QUERY_ENDPOINT,
            'filter' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                    "?uri a skos:Concept. "
                    "?uri skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Themes> . "
                    "?uri skos:prefLabel ?label. "
                    "FILTER (lang(?label) = {lang}). "
                    "?uri skos:prefLabel ?lab. "
                    "FILTER regex (str(?lab), ?reg, 'i'). "
                    "FILTER (lang (?lab) = {lang}). "
                    "BIND (STRLEN(STRBEFORE (str(?lab), ?reg)) AS ?place). "
                    "BIND (STRLEN(STR(?lab)) AS ?len) "
                "}} "
                "ORDER BY ?place ?len ?lab"
            ),
            'root' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label ?type "
                "WHERE {{ "
                    "?uri a skos:Collection ; "
                         "skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Themes> ; "    
                         "skos:prefLabel|rdfs:label ?label ; "
                         "rdf:type ?type . "
                    "FILTER (lang(?label) = {lang}). " 
                    "FILTER NOT EXISTS {{ [skos:member ?uri] }} "
                "}} "
                "ORDER BY ?label"
            ),
            'childs' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label ?type "
                "WHERE {{ "
                  "?uri skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Themes> . "
                  "{{ ?uri a ?type "
                    "FILTER (?type = skos:Collection || ?type = skos:Concept) }}. "
                  "?root skos:narrower|skos:member ?uri. "
                  "?uri skos:prefLabel|rdfs:label ?label. "
                  "FILTER (lang(?label) = {lang}). "
                "}} "
                "ORDER BY ?label "
            ),
            'child-count' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT (COUNT(?uri) as ?nb) "
                "WHERE {{ "
                    "?uri skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Themes> . "
                    "?root skos:narrower|skos:member ?uri. "
                "}} "
            )
        },
        'countries': {
            'url' : SPARQL_QUERY_ENDPOINT,
            'filter' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                    "?uri a skos:Concept. "
                    "?uri skos:inScheme <http://skos.um.es/unescothes/CS000/Countries> . "
                    "?uri skos:prefLabel ?label. "
                    "FILTER (lang(?label) = {lang}). "
                    "?uri skos:prefLabel ?lab. "
                    "FILTER regex (str(?lab), ?reg, 'i'). "
                    "FILTER (lang (?lab) = {lang}). "
                    "BIND (STRLEN(STRBEFORE (str(?lab), ?reg)) AS ?place). "
                    "BIND (STRLEN(STR(?lab)) AS ?len) "
                "}} "
                "ORDER BY ?place ?len ?lab"
            ),
            'root' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                    "?uri a skos:Concept ; "
                         "skos:inScheme <http://skos.um.es/unescothes/CS000/Countries> ; "    
                         "skos:prefLabel ?label . "
                    "FILTER (lang(?label) = {lang}). " 
                    "FILTER NOT EXISTS {{ [skos:narrower ?uri] }} "
                "}} "
                "ORDER BY ?label "
            ),
            'childs' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                  "?uri skos:inScheme <http://skos.um.es/unescothes/CS000/Countries> . "
                  "{{ ?uri a ?type "
                    "FILTER (?type = skos:Collection || ?type = skos:Concept) }}. "
                  "?root skos:narrower|skos:member ?uri. "
                  "?uri skos:prefLabel|rdfs:label ?label. "
                  "FILTER (lang(?label) = {lang}). "
                "}} "
                "ORDER BY ?label"
            ),
            'child-count' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT (COUNT(?uri) as ?nb) "
                "WHERE {{ "
                    "?uri skos:inScheme <http://skos.um.es/unescothes/CS000/Countries> . "
                    "?root skos:narrower|skos:member ?uri. "
                "}}"
            )
        },
        'languages': {
            'url' : SPARQL_QUERY_ENDPOINT,
            'filter' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                    "?uri a skos:Concept. "
                    "?uri skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Languages> . "
                    "?uri skos:prefLabel ?label. "
                    "FILTER (lang(?label) = {lang}). "
                    "?uri skos:prefLabel ?lab. "
                    "FILTER regex (str(?lab), ?reg, 'i'). "
                    "FILTER (lang (?lab) = {lang}). "
                    "BIND (STRLEN(STRBEFORE (str(?lab), ?reg)) AS ?place). "
                    "BIND (STRLEN(STR(?lab)) AS ?len) "
                "}} "
                "ORDER BY ?place ?len ?lab"
            ),
            'root' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                    "?uri a skos:Concept ; "
                         "skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Languages> ;     "
                         "skos:prefLabel ?label . "
                    "FILTER (lang(?label) = {lang}).  "
                    "FILTER NOT EXISTS {{ [skos:narrower ?uri] }} "
                "}} "
                "ORDER BY ?label"
            )
        },
        'projects': {
            'url' : SPARQL_QUERY_ENDPOINT,
            'filter' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label ?acro "
                "WHERE {{ "
                    "?uri a skos:Concept. "
                    "?uri skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Projects> . "
                    "?uri skos:prefLabel ?label. "
                    "?uri skos:prefLabel ?lab. "
                    "OPTIONAL {{ ?uri skos:altLabel ?acro }}. "
                    "FILTER regex (str(?lab), ?reg, 'i'). "
                    "BIND (STRLEN(STRBEFORE (str(?lab), ?reg)) AS ?place). "
                    "BIND (STRLEN(STR(?lab)) AS ?len) "
                "}} "
                "ORDER BY ?place ?len ?lab"
            ),
            'root' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label ?acro "
                "WHERE {{ "
                    "?uri a skos:Concept ; "
                    "skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Projects> ;     "
                    "skos:prefLabel ?label . "
                    "OPTIONAL {{ ?uri skos:altLabel ?acro }} "
                "}} "
                "ORDER BY ?label"
            )
        },
        'organizations': {
            'url' : SPARQL_QUERY_ENDPOINT,
            'filter' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label ?acro "
                "WHERE {{ "
                    "?uri a skos:Concept. "
                    "?uri skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Organizations> . "
                    "?uri skos:prefLabel ?label. "
                    "?uri skos:prefLabel ?lab. "
                    "OPTIONAL {{ ?uri skos:altLabel ?acro }}. "
                    "FILTER regex (str(?lab), ?reg, 'i'). "
                    "BIND (STRLEN(STRBEFORE (str(?lab), ?reg)) AS ?place). "
                    "BIND (STRLEN(STR(?lab)) AS ?len) "
                "}} "
                "ORDER BY ?place ?len ?lab"
            ),
            'root' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label ?acro "
                "WHERE {{ "
                    "?uri a skos:Concept ; "
                         "skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/Organizations> ;     "
                         "skos:prefLabel ?label . "
                    "OPTIONAL {{ ?uri skos:altLabel ?acro }} "
                "}} "
                "ORDER BY ?label"
            )
        },
        'types': {
            'url' : SPARQL_QUERY_ENDPOINT,
            'filter' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                    "?uri a skos:Concept. "
                    "?uri skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/DocumentType> . "
                    "?uri skos:prefLabel ?label. "
                    "FILTER (lang(?label) = {lang}). "
                    "?uri skos:prefLabel ?lab. "
                    "FILTER regex (str(?lab), ?reg, 'i'). "
                    "FILTER (lang (?lab) = {lang}). "
                    "BIND (STRLEN(STRBEFORE (str(?lab), ?reg)) AS ?place). "
                    "BIND (STRLEN(STR(?lab)) AS ?len) "
                "}} "
                "ORDER BY ?place ?len ?lab"
            ),
            'root' : (
                "PREFIX skos:<http://www.w3.org/2004/02/skos/core#> "
                "PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#> "
                "PREFIX owl:<http://www.w3.org/2002/07/owl#> "
                "PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> "
                "SELECT DISTINCT ?uri ?label "
                "WHERE {{ "
                    "?uri a skos:Concept ; "
                         "skos:inScheme <http://www.iiep.unesco.org/plan4learning/scheme/DocumentType> ;     "
                         "skos:prefLabel ?label . "
                    "FILTER (lang(?label) = {lang}).  "
                    "FILTER NOT EXISTS {{ [skos:narrower ?uri] }} "
                "}} "
                "ORDER BY ?label "
            )
        },
        'audiences': {
            'url' : SPARQL_QUERY_ENDPOINT,
            "filter" : "",
            "root" : "",
            "childs" : "",
            "child-count" : ""
        }
    }         
