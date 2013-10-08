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

from rdflib.namespace import RDFS
from rdflib.term import URIRef, Literal

from p4l.mapping.constants import IIEP, DCT
from p4l.mapping.serializers import (ModelSerializer, SimpleFieldSerializer, 
    BooleanFieldSerializer, RelatedFieldSerializer)


def uri_convert(s):
    try:
        return URIRef(unicode(s)) if s else None
    except:
        return Literal(unicode(s)) if s else None

class ImprintSerializer(ModelSerializer):
    
    imprintCity = SimpleFieldSerializer(predicate=IIEP.imprintCity, lang_field='lang')
    publisher = SimpleFieldSerializer(predicate=DCT.publisher, lang_field='lang')
    imprintDate = SimpleFieldSerializer(predicate=IIEP.imprintDate, lang_field='lang')


class VolumeIssueSerializer(ModelSerializer):
    volume = SimpleFieldSerializer(predicate=IIEP.volume, lang_field='lang')
    number = SimpleFieldSerializer(predicate=IIEP.number, lang_field='lang')


class MeetingSerializer(ModelSerializer):
    label = SimpleFieldSerializer(predicate=RDFS.label, lang_field='lang')
    meetingNumber = SimpleFieldSerializer(predicate=IIEP.meetingNumber, lang_field='lang')
    meetingPlace = SimpleFieldSerializer(predicate=IIEP.meetingPlace, lang_field='lang')
    meetingDate = SimpleFieldSerializer(predicate=IIEP.meetingDate, lang_field='lang')
    meetingYear = SimpleFieldSerializer(predicate=IIEP.meetingYear, lang_field='lang')

class SubjectMeetingSerializer(ModelSerializer):
    label = SimpleFieldSerializer(predicate=RDFS.label)
    meetingNumber = SimpleFieldSerializer(predicate=IIEP.meetingNumber)
    meetingPlace = SimpleFieldSerializer(predicate=IIEP.meetingPlace)
    meetingDate = SimpleFieldSerializer(predicate=IIEP.meetingDate)
    meetingYear = SimpleFieldSerializer(predicate=IIEP.meetingYear)


class SerieSerializer(ModelSerializer):
    title = SimpleFieldSerializer(predicate=DCT.title, lang_field='lang')
    volume = SimpleFieldSerializer(predicate=IIEP.volume, lang_field='lang')


class UrlSerializer(ModelSerializer):
    address = SimpleFieldSerializer(predicate=IIEP.address)
    display = SimpleFieldSerializer(predicate=IIEP.display)



class RecordSerializer(ModelSerializer):
    
    identifier = SimpleFieldSerializer(predicate=DCT.identifier)
    notes = SimpleFieldSerializer(predicate=IIEP.notes)
    editionStatement = SimpleFieldSerializer(predicate=IIEP.editionStatement)
    corporateAuthorLabel = SimpleFieldSerializer(predicate=IIEP.corporateAuthorLabel)
    recordType = SimpleFieldSerializer(predicate=DCT.type, convert=uri_convert)
    isDocumentPart = BooleanFieldSerializer(predicate=IIEP.isDocumentPart)
    hidden = BooleanFieldSerializer(predicate=IIEP.hidden)
    restricted = BooleanFieldSerializer(predicate=IIEP.restricted)    

    language = RelatedFieldSerializer(many=False, value_field='uri', predicate=DCT.language, convert=uri_convert) 
    otherLanguages = RelatedFieldSerializer(many=True, value_field='uri', predicate=IIEP.otherLanguage, convert=uri_convert)
    subjects = RelatedFieldSerializer(many=True, value_field='uri', predicate=DCT.subject, convert=uri_convert)
    themes = RelatedFieldSerializer(many=True, value_field='uri', predicate=IIEP.theme, convert=uri_convert)
    countries = RelatedFieldSerializer(many=True, value_field='uri', predicate=IIEP.country, convert=uri_convert)
    projectNames = RelatedFieldSerializer(many=True, value_field='uri', predicate=IIEP.projectName, convert=uri_convert)
    subjectCorporateBodies = RelatedFieldSerializer(many=True, value_field='uri', predicate=IIEP.subjectCorporateBody, convert=uri_convert) 
    corporateAuthors = RelatedFieldSerializer(many=True, value_field='uri', predicate=IIEP.corporateAuthor, convert=uri_convert)
    audiences = RelatedFieldSerializer(many=True, value_field='uri', predicate=IIEP.audience, convert=uri_convert)
    
    isbns = RelatedFieldSerializer(many=True, value_field='isbn', predicate=IIEP.isbn, lang_field='lang')
    issns = RelatedFieldSerializer(many=True, value_field='issn', predicate=IIEP.issn, lang_field='lang')
    collations = RelatedFieldSerializer(many=True, value_field='collation', predicate=IIEP.collation, lang_field='lang')
    documentCodes = RelatedFieldSerializer(many=True, value_field='documentCode', predicate=IIEP.documentCode, lang_field='lang')
    titles = RelatedFieldSerializer(many=True, value_field='title', predicate=DCT.title, lang_field='lang')
    addedTitles = RelatedFieldSerializer(many=True, value_field='title', predicate=IIEP.addedTitle, lang_field='lang')
    titlesMainDocument = RelatedFieldSerializer(many=True, value_field='title', predicate=IIEP.titleMainDocument, lang_field='lang')
    abstracts = RelatedFieldSerializer(many=True, value_field='abstract', predicate=DCT.abstract, lang_field='lang')
    periodicals = RelatedFieldSerializer(many=True, value_field='label', predicate=IIEP.periodical, lang_field='lang')
    authors = RelatedFieldSerializer(many=True, value_field='name', predicate=IIEP.author)
    subjectPersons = RelatedFieldSerializer(many=True, value_field='name', predicate=IIEP.subjectPerson)
    
    imprints = ImprintSerializer(many=True, predicate=IIEP.imprint)
    volumeIssues = VolumeIssueSerializer(many=True, predicate=IIEP.volumeIssue)
    meetings = MeetingSerializer(many=True, predicate=IIEP.meeting)
    subjectMeetings = SubjectMeetingSerializer(many=True, predicate=IIEP.subjectMeeting)
    series = SerieSerializer(many=True, predicate=IIEP.serie)
    urls = UrlSerializer(many=True, predicate=IIEP.url)
    
    
    class Meta:
        type = IIEP.Record
        uri_fieldname = "uri"
