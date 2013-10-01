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

import codecs
import logging
import math
import hashlib
import sys
import unicodedata

from django.conf import settings
from django.core.validators import URLValidator
from django.utils.http import urlquote_plus
import requests


logger = logging.getLogger(__name__)

def show_progress(current_line, total_line, label, width, writer=None):

    if writer is None:
        writer = sys.stdout
        if sys.stdout.encoding is not None:
            writer = codecs.getwriter(sys.stdout.encoding)(sys.stdout)

    percent = (float(current_line) / float(total_line)) * 100.0

    marks = math.floor(width * (percent / 100.0)) #@UndefinedVariable
    spaces = math.floor(width - marks) #@UndefinedVariable

    loader = u'[' + (u'=' * int(marks)) + (u' ' * int(spaces)) + u']'
        
    s = u"%s %3d%% %*d/%d - %*s\r" % (loader, percent, len(str(total_line)), current_line, total_line, width, label[:width])
    
    writer.write(s) #takes the header into account
    if percent >= 100:
        writer.write("\n")
    writer.flush()
    
    return writer

LANGUAGE_NS = u"http://psi.oasis-open.org/iso/639/#"
LANGUAGE_URI_MAP = {u'roh': u'rm', u'sco': u'sco', u'scn': u'scn', u'rom': u'rom', u'ron': u'ro', u'oss': u'os', u'ale': u'ale', u'mni': u'mni', u'nwc': u'nwc', u'osa': u'osa', u'mnc': u'mnc', u'mwr': u'mwr', u'ven': u'ven', u'uga': u'uga', u'mwl': u'mwl', u'fas': u'fa', u'fat': u'fat', u'fan': u'fan', u'fao': u'fo', u'din': u'din', u'hye': u'hy', u'dsb': u'dsb', u'srd': u'sc', u'iba': u'iba', u'div': u'div', u'tel': u'te', u'tem': u'tem', u'nbl': u'nr', u'ter': u'ter', u'tet': u'tet', u'sun': u'su', u'kut': u'kut', u'suk': u'suk', u'kur': u'ku', u'kum': u'kum', u'sus': u'sus', u'new': u'new', u'nep': u'ne', u'sux': u'sux', u'men': u'men', u'lez': u'lez', u'gla': u'gd', u'bos': u'bs', u'gle': u'ga', u'eka': u'eka', u'glg': u'gl', u'akk': u'akk', u'aka': u'aka', u'bod': u'bo', u'glv': u'gv', u'jrb': u'jrb', u'vie': u'vi', u'ipk': u'ik', u'uzb': u'uz', u'sga': u'sga', u'bre': u'br', u'bra': u'bra', u'aym': u'ay', u'cha': u'ch', u'chb': u'chb', u'che': u'ce', u'chg': u'chg', u'chk': u'chk', u'chm': u'chm', u'chn': u'chn', u'cho': u'cho', u'chp': u'chp', u'chr': u'chr', u'chu': u'cu', u'chv': u'cv', u'chy': u'chy', u'msa': u'ms', u'iii': u'ii', u'ndo': u'ng', u'ibo': u'ibo', u'car': u'car', u'xho': u'xh', u'deu': u'de', u'cat': u'ca', u'del': u'del', u'den': u'den', u'cad': u'cad', u'tat': u'tt', u'srn': u'srn', u'raj': u'raj', u'spa': u'es', u'tam': u'ta', u'tah': u'ty', u'afh': u'afh', u'eng': u'en', u'enm': u'enm', u'csb': u'csb', u'nyn': u'nyn', u'nyo': u'nyo', u'sid': u'sid', u'nya': u'ny', u'sin': u'si', u'afr': u'af', u'lam': u'lam', u'snd': u'sd', u'mar': u'mr', u'lah': u'lah', u'sna': u'sn', u'lad': u'lad', u'snk': u'snk', u'mad': u'mad', u'mag': u'mag', u'lat': u'la', u'mah': u'mh', u'mak': u'mak', u'mal': u'ml', u'man': u'man', u'egy': u'egy', u'znd': u'znd', u'zen': u'zen', u'kbd': u'kbd', u'ita': u'it', u'tsn': u'tn', u'tso': u'ts', u'tsi': u'tsi', u'byn': u'byn', u'fij': u'fj', u'fin': u'fi', u'eus': u'eu', u'non': u'non', u'ceb': u'ceb', u'dan': u'da', u'nym': u'nym', u'nob': u'nb', u'dak': u'dak', u'ces': u'cs', u'dar': u'dar', u'day': u'day', u'nor': u'no', u'kpe': u'kpe', u'guj': u'gu', u'mdf': u'mdf', u'mas': u'mas', u'lao': u'lo', u'mdr': u'mdr', u'gon': u'gon', u'goh': u'goh', u'sms': u'sms', u'smo': u'sm', u'smn': u'smn', u'smj': u'smj', u'got': u'got', u'sme': u'se', u'bla': u'bla', u'sma': u'sma', u'gor': u'gor', u'ast': u'ast', u'orm': u'om', u'que': u'qu', u'ori': u'or', u'bal': u'bal', u'asm': u'as', u'pus': u'ps', u'kik': u'ki', u'ltz': u'lb', u'wln': u'wa', u'isl': u'is', u'mai': u'mai', u'lav': u'lv', u'zap': u'zap', u'yid': u'yi', u'kok': u'kok', u'kom': u'kv', u'kon': u'kon', u'ukr': u'uk', u'ton': u'to', u'kos': u'kos', u'kor': u'ko', u'tog': u'tog', u'hun': u'hu', u'hup': u'hup', u'cym': u'cy', u'udm': u'udm', u'bej': u'bej', u'ben': u'bn', u'bel': u'be', u'bem': u'bem', u'aar': u'aa', u'nzi': u'nzi', u'sah': u'sah', u'san': u'sa', u'sam': u'sam', u'pro': u'pro', u'sag': u'sg', u'sad': u'sad', u'rar': u'rar', u'rap': u'rap', u'sas': u'sas', u'sat': u'sat', u'min': u'min', u'lim': u'li', u'lin': u'ln', u'lit': u'lt', u'efi': u'efi', u'btk': u'btk', u'kac': u'kac', u'kab': u'kab', u'kaa': u'kaa', u'kan': u'kn', u'kam': u'kam', u'kal': u'kl', u'kas': u'ks', u'kar': u'kar', u'kaw': u'kaw', u'kau': u'kau', u'kat': u'ka', u'kaz': u'kk', u'tyv': u'tyv', u'awa': u'awa', u'urd': u'ur', u'doi': u'doi', u'tpi': u'tpi', u'mri': u'mi', u'abk': u'ab', u'tkl': u'tkl', u'nld': u'nl', u'oji': u'oji', u'oci': u'oc', u'wol': u'wo', u'jav': u'jv', u'hrv': u'hr', u'mga': u'mga', u'hit': u'hit', u'gez': u'gez', u'ssw': u'ss', u'hil': u'hil', u'him': u'him', u'hin': u'hi', u'bas': u'bas', u'gba': u'gba', u'bad': u'bad', u'kua': u'kj', u'cre': u'cre', u'ban': u'ban', u'crh': u'crh', u'bam': u'bam', u'bak': u'ba', u'shn': u'shn', u'arp': u'arp', u'arw': u'arw', u'ara': u'ar', u'arc': u'arc', u'sel': u'sel', u'arn': u'arn', u'lus': u'lus', u'mus': u'mus', u'lua': u'lua', u'lub': u'lub', u'lug': u'lug', u'lui': u'lui', u'lun': u'lun', u'luo': u'luo', u'iku': u'iu', u'tur': u'tr', u'tuk': u'tk', u'tum': u'tum', u'mkd': u'mk', u'cop': u'cop', u'cos': u'co', u'ile': u'ie', u'ilo': u'ilo', u'gwi': u'gwi', u'und': u'und', u'tli': u'tli', u'tlh': u'tlh', u'por': u'pt', u'pon': u'pon', u'pol': u'pl', u'ang': u'ang', u'tgk': u'tg', u'tgl': u'tl', u'fra': u'fr', u'fre': u'fr', u'dum': u'dum', u'swa': u'sw', u'dua': u'dua', u'swe': u'sv', u'yap': u'yap', u'frm': u'frm', u'tiv': u'tiv', u'yao': u'yao', u'xal': u'xal', u'fry': u'fy', u'gay': u'gay', u'ota': u'ota', u'hmn': u'hmn', u'hmo': u'ho', u'an': u'arg', u'gaa': u'gaa', u'fur': u'fur', u'mlg': u'mg', u'slv': u'sl', u'fil': u'fil', u'mlt': u'mt', u'slk': u'sk', u'ful': u'ful', u'jpn': u'ja', u'vol': u'vo', u'vot': u'vot', u'ind': u'id', u'ave': u'ae', u'jpr': u'jpr', u'ava': u'ava', u'pap': u'pap', u'ewo': u'ewo', u'pau': u'pau', u'ewe': u'ewe', u'pag': u'pag', u'pal': u'pal', u'pam': u'pam', u'pan': u'pa', u'nog': u'nog', u'phn': u'phn', u'kir': u'ky', u'nia': u'nia', u'dgr': u'dgr', u'syr': u'syr', u'kin': u'rw', u'niu': u'niu', u'epo': u'eo', u'jbo': u'jbo', u'mic': u'mic', u'tha': u'th', u'hai': u'hai', u'gmh': u'gmh', u'ell': u'el', u'ady': u'ady', u'elx': u'elx', u'ada': u'ada', u'nav': u'nv', u'hat': u'ht', u'hau': u'ha', u'haw': u'haw', u'bin': u'bin', u'amh': u'am', u'bik': u'bik', u'bih': u'bh', u'mos': u'mos', u'moh': u'moh', u'mon': u'mn', u'bho': u'bho', u'mol': u'mo', u'bis': u'bi', u'tvl': u'tvl', u'ijo': u'ijo', u'est': u'et', u'kmb': u'kmb', u'peo': u'peo', u'umb': u'umb', u'tmh': u'tmh', u'fon': u'fon', u'hsb': u'hsb', u'run': u'rn', u'rus': u'ru', u'pli': u'pi', u'ace': u'ace', u'ach': u'ach', u'nde': u'nd', u'dzo': u'dz', u'kru': u'kru', u'srr': u'srr', u'ido': u'io', u'srp': u'sr', u'kro': u'kro', u'krc': u'krc', u'nds': u'nds', u'zun': u'zun', u'zul': u'zu', u'twi': u'tw', u'sog': u'sog', u'nso': u'nso', u'fro': u'fro', u'som': u'so', u'son': u'son', u'sot': u'st', u'vai': u'vai', u'her': u'hz', u'lol': u'lol', u'heb': u'he', u'loz': u'loz', u'gil': u'gil', u'was': u'was', u'war': u'war', u'bul': u'bg', u'wal': u'wal', u'bua': u'bua', u'bug': u'bug', u'aze': u'az', u'zha': u'za', u'zho': u'zh', u'nno': u'nn', u'uig': u'ug', u'myv': u'myv', u'inh': u'inh', u'khm': u'km', u'kho': u'kho', u'mya': u'my', u'kha': u'kha', u'ina': u'ia', u'nah': u'nah', u'tir': u'ti', u'nap': u'nap', u'grb': u'grb', u'grc': u'grc', u'nau': u'na', u'grn': u'gn', u'tig': u'tig', u'yor': u'yo', u'cor': u'kw', u'sqi': u'sq', u'dyu': u'dyu'}

def get_code_from_language_uri(lang_uri):

    if not lang_uri:
        return None
    if lang_uri.startswith(LANGUAGE_NS):
        lang_uri = lang_uri[len(LANGUAGE_NS):]

    return LANGUAGE_URI_MAP.get(lang_uri, None)



def get_labels_for_uris(uri_list, scheme_uri, lang, acronyms=False):
    query_without_acronym = """
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
SELECT ?uri ?label
WHERE {
    ?uri skos:inScheme <%s> .
    ?uri skos:prefLabel|skos:label ?label .
    FILTER (%s)
}
"""
    query_with_acronym = """
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
SELECT ?uri ?label ?acro
WHERE {
    ?uri skos:inScheme <%s> .
    ?uri skos:prefLabel|skos:label ?label .
    OPTIONAL { ?uri skos:altLabel ?acro }
    FILTER (%s)
}
"""
    if acronyms:
        query = query_with_acronym
    else:
        query = query_without_acronym
    res_dict = {}
    if not uri_list:
        return res_dict
    # We build the filter string
    filter_str = ""
    validate = URLValidator()
    for i,uri in enumerate(uri_list):
        res_dict[uri] = ""
        # We test if the uri is correct. If not, all the sparql request fails
        try:
            validate(uri)
        except:
            continue
        uri = uri.replace(" ", "") # avoid bug when only few urls are not good
        filter_str += (" || ?uri = <" + uri + ">") if i else ("?uri = <" + uri + ">")
    # We request the labels
    res = requests.get(
        settings.SPARQL_QUERY_ENDPOINT,
        params={'query':query % (scheme_uri, filter_str), 'timeout':10},#, '$root' : "<"+uri+">"},
        headers={'accept':'application/sparql-results+json'},
    )
    if res.ok and res.text:
        json_res = res.json()
        if 'results' in json_res and 'bindings' in json_res['results'] and len(json_res['results']['bindings'])>0:
            # json_res['results']['bindings'] has several languages. If we find french, we save the french label.
            # If not, we save the first one.
            tmp_dict = {}
            first_label = None
            # We create a temporary dict with the lang code and the label
            for b in json_res['results']['bindings']:
                if lang:
                    if 'label' in b and 'value' in b['label'] and 'xml:lang' in b['label']:
                        tmp_dict[b['label']['xml:lang']] = b['label']['value']
                        if not first_label:
                            first_label = b['label']['value']
                else:
                    if 'acro' in b and 'value' in b['acro']:
                        first_label = b['acro']['value'] + ". " + b['label']['value']
                    else:
                        first_label = b['label']['value']
                if lang in tmp_dict or first_label:
                    if lang in tmp_dict:
                        label = tmp_dict[lang]
                    else:
                        label = first_label
                    res_dict[b['uri']['value']] = label
    return res_dict

    
    
def fill_label_for_model(model, property_uri, scheme_uri):
    query = """
PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
SELECT ?uri ?label 
WHERE {
    ?uri skos:inScheme <%s> .
    ?uri skos:prefLabel|skos:label ?label .
    FILTER (?uri = $root)
}
"""
    # Loads Models label from sparkl query
    objs = model.objects.filter(label=None)
    total_objs = len(objs)
    writer = None
    i = 0
    found = 0
    for o in objs:
        i += 1
        res = requests.get(
            settings.SPARQL_QUERY_ENDPOINT,
            params={'query':query % scheme_uri, 'timeout':10, '$root' : "<"+getattr(o, property_uri)+">"},
            headers={'accept':'application/sparql-results+json'},
        )
        if not res.ok:
            continue
        elif res.text:
            json_res = res.json()
            if 'results' in json_res and 'bindings' in json_res['results'] and len(json_res['results']['bindings'])>0:
                # json_res['results']['bindings'] has several languages. If we find french, we save the french label.
                # If not, we save the first one.
                tmp_dict = {}
                first_label = None
                # We create a temporary dict with the lang code and the label
                for b in json_res['results']['bindings']:
                    if 'label' in b and 'value' in b['label'] and 'xml:lang' in b['label']:
                        tmp_dict[b['label']['xml:lang']] = b['label']['value']
                        if not first_label:
                            first_label = b['label']['value']
                if 'fr' in tmp_dict or first_label:
                    if 'fr' in tmp_dict:
                        o.label = tmp_dict['fr']
                    else:
                        o.label = first_label
                    l = o.label
                    o.save()
                    found += 1
                    writer = show_progress(i, total_objs, l, 50, writer=writer)
    print("Processing Sparql Done. %d found on %d" % (found, total_objs))

def strip_accents(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value)
                  if unicodedata.category(c) != 'Mn')
    
    
def safe_cache_key(value):
    '''Returns an md5 hexdigest of value if len(value) > 250. Replaces invalid memcache
       control characters with an underscore. Also adds the CACHE_MIDDLEWARE_KEY_PREFIX
       to your keys automatically.
    '''
    value = urlquote_plus(value)
    for char in value:
        if ord(char) < 33:
            value = value.replace(char, '_')
    
    value = "%s_%s" % (settings.CACHE_MIDDLEWARE_KEY_PREFIX, value)
    
    if len(value) <= 250:
        return value
    
    return hashlib.md5(value).hexdigest()


    