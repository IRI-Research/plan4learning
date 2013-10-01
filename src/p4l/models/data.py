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

from django.db import models

from p4l.models.common import P4lModel, P4lModelLang
from p4l.models.user import User


class Imprint(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="imprints")
    imprintCity = models.CharField(max_length=512, blank=True, null=True, db_index=True)
    publisher = models.CharField(max_length=512, blank=True, null=True, db_index=True)
    imprintDate = models.CharField(max_length=512, blank=True, null=True, db_index=True)    


class Serie(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="series")
    title = models.CharField(max_length=2048, blank=False, null=False, db_index=True)
    volume = models.CharField(max_length=2048, blank=True, null=True, db_index=True)


class ProjectName(P4lModel):
    uri = models.URLField(max_length=2048, unique=True, db_index=True) 


class CorporateAuthor(P4lModel):
    uri = models.URLField(max_length=2048, unique=True, db_index=True)

class Url(P4lModel):
    record = models.ForeignKey('p4l.Record', related_name="urls", db_index=True)
    address = models.CharField(max_length=2048, blank=False, null=False, db_index=True) #iiep:address
    display = models.CharField(max_length=2048, blank=True, null=True, db_index=True) #iiep:display


class Subject(P4lModel):
    uri = models.URLField(max_length=2048, unique=True, db_index=True)

class Theme(P4lModel):
    uri = models.URLField(max_length=2048, unique=True, db_index=True)

class Country(P4lModel):
    uri = models.URLField(max_length=2048, unique=True, db_index=True)

class Audience(P4lModel):
    uri = models.URLField(max_length=2048, unique=True, db_index=True)


class Isbn(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="isbns", db_index=True)
    isbn = models.CharField(max_length=128) #iiep:isbn


class Issn(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="issns", db_index=True)
    issn = models.CharField(max_length=128) #iiep:issn

class DocumentCode(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="documentCodes", db_index=True)
    documentCode = models.CharField(max_length=128) #iiep:issn

class Language(P4lModel):
    uri = models.URLField(max_length=2048, unique=True, db_index=True)

class BaseTitle(P4lModelLang):
    title = models.CharField(max_length=2048, blank=False, null=False, db_index=True)
    class Meta(P4lModelLang.Meta):
        abstract = True

class Title(BaseTitle):
    record = models.ForeignKey('p4l.Record', related_name="titles", db_index=True)

class AddedTitle(BaseTitle):
    record = models.ForeignKey('p4l.Record', related_name="addedTitles", db_index=True)

class TitleMainDocument(BaseTitle):
    record = models.ForeignKey('p4l.Record', related_name="titlesMainDocument", db_index=True)


class Abstract(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="abstracts", db_index=True)
    abstract = models.TextField(blank=True, null=True)


class Collation(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="collations", db_index=True)
    collation = models.CharField(max_length=1024, blank=False, null=False, db_index=True)


class VolumeIssue(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="volumeIssues", db_index=True)
    volume = models.CharField(max_length=1024, blank=True, null=True, db_index=True) #iiep:volume
    number = models.CharField(max_length=1024, blank=True, null=True, db_index=True) #iiep:number


class P4lPerson(P4lModel):
    name = models.CharField(max_length=2048, blank=False, null=False, db_index=True)
    class Meta(P4lModel.Meta):
        abstract = True


class Author(P4lPerson):
    record = models.ForeignKey('p4l.Record', related_name="authors", db_index=True)
    
class SubjectPerson(P4lPerson):
    record = models.ForeignKey('p4l.Record', related_name="subjectPersons", db_index=True)

class Periodical(P4lModelLang):
    record = models.ForeignKey('p4l.Record', related_name="periodicals", db_index=True)
    label = models.CharField(max_length=2048, blank=False, null=False, db_index=True) #iiep:periodical


class BaseMeeting(P4lModel):
    label = models.CharField(max_length=2048, blank=False, null=False, db_index=True) #rdfs:label
    meetingNumber = models.CharField(max_length=2048, blank=True, null=True, db_index=True) #iiep:meetingNumber
    meetingPlace = models.CharField(max_length=2048, blank=True, null=True, db_index=True) #iiep:meetingPlace
    meetingDate = models.CharField(max_length=2048, blank=True, null=True, db_index=True) #iiep:meetingDate
    meetingYear = models.PositiveSmallIntegerField(blank=True, null=True, db_index=True) #iiep:meetingYear
    class Meta(P4lModel.Meta):
        abstract = True


class Meeting(BaseMeeting):
    lang = models.CharField(max_length=15, blank=True, null=True, db_index=True) #@xml:lang
    record = models.ForeignKey('p4l.Record', related_name="meetings")


class SubjectMeeting(BaseMeeting):
    record = models.ForeignKey('p4l.Record', related_name="subjectMeetings", db_index=True)


class Record(P4lModel):
    uri = models.URLField(max_length=2048, unique=True, db_index=True) #subject
    subjects = models.ManyToManyField('p4l.Subject') #dct:subject                                                       # <Thesaurus> with no country
    themes = models.ManyToManyField('p4l.Theme') #iiep:theme                                                            # <Themes>
    countries = models.ManyToManyField('p4l.Country') #iiep:country                                                     # <Thesaurus> filtered with country only
    identifier = models.CharField(max_length=128, unique=True, db_index=True) #dct:identifier    
    notes = models.TextField(blank=True, null=True) #iiep:notes    
    #issns foreign key from Isbn #iiep:issn
    #isbns foreign key from Isbn #iiep:isbn
    #documentCodes foreign key from Isbn #iiep:documentCode
    language = models.ForeignKey('p4l.Language', blank=True, null=True) #dct:language                                    # <Languages>
    otherLanguages = models.ManyToManyField('p4l.Language', related_name='otherLanguage_record') #iiep:otherLanguage     # <Languages>
    #titles foreign Key from Title #dct:title
    #abstracts foreign Key from Abstract #dct:abstract
    #addedTitles foreign Key from AddedTitle #iiep:addedTitle
    #titlesMainDocument foreign Key from TitleMainDocument #iiep:titleMainDocument
    editionStatement = models.CharField(max_length=1024, blank=True, null=True) #iiep:editionStatement
    #imprints foreign Key from Imprint #iiep:imprint
    #collations = foreign Key from Collation #iiep:collation
    #volumeIssues = foreign Key from VolumeIssue #iiep:volumeIssue
    projectNames = models.ManyToManyField('p4l.ProjectName') #iiep:projectName                                            # <Projects>
    #periodicals = foreign key from 'p4l.Periodical' #iiep:periodical
    #meetings = foreign key from 'p4l.Meeting' #iiep:meeting
    #series = foreign key from 'p4l.Serie'  #iiep:serie
    #authors = foreign key from 'p4l.Author' #iiep:author
    #subjectPersons = foreign key from 'p4l.SubjectPerson' #iiep:subjectPerson
    subjectCorporateBodies = models.ManyToManyField('p4l.CorporateAuthor', related_name='recordsSubjectCorporateBody') #iiep:subjectCorporateBody # <Organizations>
    #subjectMeetings = foreign key from 'p4l.SubjectMeeting' #iiep:subjectMeeting
    corporateAuthors = models.ManyToManyField('p4l.CorporateAuthor', related_name='recordsCorporateAuthor') #iiep:subjectCorporateBody # <Organizations>
    corporateAuthorLabel = models.CharField(max_length=2048, blank=True, null=True, db_index=True) #iiep:corporateAuthorLabel
    #urls foreign Key from Url #iiep:url
    audiences = models.ManyToManyField('p4l.Audience') #dct:audience                                                      # Unknown thesaurus
    recordType = models.URLField(max_length=2048, blank=True, null=True) #dct:type                                        # <DocumentType>
    
    isDocumentPart = models.BooleanField() #iiep:isDocumentPart
    hidden = models.BooleanField(default=False) #iiep:hidden
    restricted = models.BooleanField(default=False) #iiep:restricted
    
    #Record import date and modification date
    creation_date = models.DateTimeField( auto_now_add=True, serialize=False)
    modification_date = models.DateTimeField(auto_now=True, serialize=False)
    modified_by = models.ForeignKey(User, blank=True, null=True)
    
    def get_titles(self):
        return [t.title for t in self.titles.all()]
    
    def get_authors(self):
        return [a.name for a in self.authors.all()]
    
    def get_corporate_authors(self):
        return [c.uri for c in self.corporateAuthors.all()]
    
    def get_imprints_years(self):
        return sorted(set([i.imprintDate for i in self.imprints.all() if i.imprintDate]))

    def __unicode__(self):
        return "Record id %s { identifier: %s, uri: %s, editionStatement: %s,  recordType: %s, isDocumentPart: %s, notes: %s, language : %s}" \
            % (
                self.id,
                self.identifier,
                self.uri,
                self.editionStatement,
                self.recordType,
                self.isDocumentPart,
                self.notes[:100] if self.notes else None,
                self.language.id if self.language else None
            )

#('{http://www.iiep.unesco.org/plan4learning/model.owl#}issn', 3)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}documentCode', 3)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}country', 44)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}imprint', 5)
#('{http://purl.org/dc/terms/}title', 4)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}isDocumentPart', 1)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}notes', 1)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}isbn', 8)
#('{http://purl.org/dc/terms/}identifier', 1)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}meeting', 4)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}projectName', 10)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}addedTitle', 18)
#('{http://purl.org/dc/terms/}subject', 29)
#('{http://purl.org/dc/terms/}language', 1)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}serie', 4)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}volumeIssue', 3)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}url', 20)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}titleMainDocument', 3)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}otherLanguage', 13)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}periodical', 3)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}editionStatement', 1)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}collation', 4)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}subjectMeeting', 6)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}corporateAuthor', 7)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}author', 26)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}subjectPerson', 2)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}subjectCorporateBody', 8)
#('{http://www.iiep.unesco.org/plan4learning/model.owl#}theme', 6)
#('{http://purl.org/dc/terms/}abstract', 3)
#('{http://purl.org/dc/terms/}type', 1)
