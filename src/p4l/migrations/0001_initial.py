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

import datetime

from django.db import models
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'p4l_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=2)),
        ))
        db.send_create_signal('p4l', ['User'])

        # Adding M2M table for field groups on 'User'
        db.create_table(u'p4l_user_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['p4l.user'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'p4l_user_groups', ['user_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'User'
        db.create_table(u'p4l_user_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(orm['p4l.user'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'p4l_user_user_permissions', ['user_id', 'permission_id'])

        # Adding model 'Imprint'
        db.create_table(u'p4l_imprint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imprints', to=orm['p4l.Record'])),
            ('imprintCity', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=512, null=True, blank=True)),
            ('publisher', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=512, null=True, blank=True)),
            ('imprintDate', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal('p4l', ['Imprint'])

        # Adding model 'Serie'
        db.create_table(u'p4l_serie', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='series', to=orm['p4l.Record'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
        ))
        db.send_create_signal('p4l', ['Serie'])

        # Adding model 'ProjectName'
        db.create_table(u'p4l_projectname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, db_index=True)),
        ))
        db.send_create_signal('p4l', ['ProjectName'])

        # Adding model 'CorporateAuthor'
        db.create_table(u'p4l_corporateauthor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, db_index=True)),
        ))
        db.send_create_signal('p4l', ['CorporateAuthor'])

        # Adding model 'Url'
        db.create_table(u'p4l_url', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='urls', to=orm['p4l.Record'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('display', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
        ))
        db.send_create_signal('p4l', ['Url'])

        # Adding model 'Subject'
        db.create_table(u'p4l_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, db_index=True)),
        ))
        db.send_create_signal('p4l', ['Subject'])

        # Adding model 'Theme'
        db.create_table(u'p4l_theme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, db_index=True)),
        ))
        db.send_create_signal('p4l', ['Theme'])

        # Adding model 'Country'
        db.create_table(u'p4l_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, db_index=True)),
        ))
        db.send_create_signal('p4l', ['Country'])

        # Adding model 'Audience'
        db.create_table(u'p4l_audience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, db_index=True)),
        ))
        db.send_create_signal('p4l', ['Audience'])

        # Adding model 'Isbn'
        db.create_table(u'p4l_isbn', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='isbns', to=orm['p4l.Record'])),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('p4l', ['Isbn'])

        # Adding model 'Issn'
        db.create_table(u'p4l_issn', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issns', to=orm['p4l.Record'])),
            ('issn', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('p4l', ['Issn'])

        # Adding model 'DocumentCode'
        db.create_table(u'p4l_documentcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='documentCodes', to=orm['p4l.Record'])),
            ('documentCode', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('p4l', ['DocumentCode'])

        # Adding model 'Language'
        db.create_table(u'p4l_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, db_index=True)),
        ))
        db.send_create_signal('p4l', ['Language'])

        # Adding model 'Title'
        db.create_table(u'p4l_title', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titles', to=orm['p4l.Record'])),
        ))
        db.send_create_signal('p4l', ['Title'])

        # Adding model 'AddedTitle'
        db.create_table(u'p4l_addedtitle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='addedTitles', to=orm['p4l.Record'])),
        ))
        db.send_create_signal('p4l', ['AddedTitle'])

        # Adding model 'TitleMainDocument'
        db.create_table(u'p4l_titlemaindocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titlesMainDocument', to=orm['p4l.Record'])),
        ))
        db.send_create_signal('p4l', ['TitleMainDocument'])

        # Adding model 'Abstract'
        db.create_table(u'p4l_abstract', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='abstracts', to=orm['p4l.Record'])),
            ('abstract', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('p4l', ['Abstract'])

        # Adding model 'Collation'
        db.create_table(u'p4l_collation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collations', to=orm['p4l.Record'])),
            ('collation', self.gf('django.db.models.fields.CharField')(max_length=1024, db_index=True)),
        ))
        db.send_create_signal('p4l', ['Collation'])

        # Adding model 'VolumeIssue'
        db.create_table(u'p4l_volumeissue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='volumeIssues', to=orm['p4l.Record'])),
            ('volume', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=1024, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal('p4l', ['VolumeIssue'])

        # Adding model 'Author'
        db.create_table(u'p4l_author', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='authors', to=orm['p4l.Record'])),
        ))
        db.send_create_signal('p4l', ['Author'])

        # Adding model 'SubjectPerson'
        db.create_table(u'p4l_subjectperson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subjectPersons', to=orm['p4l.Record'])),
        ))
        db.send_create_signal('p4l', ['SubjectPerson'])

        # Adding model 'Periodical'
        db.create_table(u'p4l_periodical', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='periodicals', to=orm['p4l.Record'])),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
        ))
        db.send_create_signal('p4l', ['Periodical'])

        # Adding model 'Meeting'
        db.create_table(u'p4l_meeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('meetingNumber', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
            ('meetingPlace', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
            ('meetingDate', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
            ('meetingYear', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
            ('lang', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=15, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='meetings', to=orm['p4l.Record'])),
        ))
        db.send_create_signal('p4l', ['Meeting'])

        # Adding model 'SubjectMeeting'
        db.create_table(u'p4l_subjectmeeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=2048, db_index=True)),
            ('meetingNumber', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
            ('meetingPlace', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
            ('meetingDate', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
            ('meetingYear', self.gf('django.db.models.fields.PositiveSmallIntegerField')(db_index=True, null=True, blank=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subjectMeetings', to=orm['p4l.Record'])),
        ))
        db.send_create_signal('p4l', ['SubjectMeeting'])

        # Adding model 'Record'
        db.create_table(u'p4l_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uri', self.gf('django.db.models.fields.URLField')(unique=True, max_length=2048, db_index=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, db_index=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['p4l.Language'], null=True, blank=True)),
            ('editionStatement', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('corporateAuthorLabel', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=2048, null=True, blank=True)),
            ('recordType', self.gf('django.db.models.fields.URLField')(max_length=2048, null=True, blank=True)),
            ('isDocumentPart', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hidden', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('restricted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modification_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['p4l.User'], null=True, blank=True)),
        ))
        db.send_create_signal('p4l', ['Record'])

        # Adding M2M table for field subjects on 'Record'
        db.create_table(u'p4l_record_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm['p4l.record'], null=False)),
            ('subject', models.ForeignKey(orm['p4l.subject'], null=False))
        ))
        db.create_unique(u'p4l_record_subjects', ['record_id', 'subject_id'])

        # Adding M2M table for field themes on 'Record'
        db.create_table(u'p4l_record_themes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm['p4l.record'], null=False)),
            ('theme', models.ForeignKey(orm['p4l.theme'], null=False))
        ))
        db.create_unique(u'p4l_record_themes', ['record_id', 'theme_id'])

        # Adding M2M table for field countries on 'Record'
        db.create_table(u'p4l_record_countries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm['p4l.record'], null=False)),
            ('country', models.ForeignKey(orm['p4l.country'], null=False))
        ))
        db.create_unique(u'p4l_record_countries', ['record_id', 'country_id'])

        # Adding M2M table for field otherLanguages on 'Record'
        db.create_table(u'p4l_record_otherLanguages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm['p4l.record'], null=False)),
            ('language', models.ForeignKey(orm['p4l.language'], null=False))
        ))
        db.create_unique(u'p4l_record_otherLanguages', ['record_id', 'language_id'])

        # Adding M2M table for field projectNames on 'Record'
        db.create_table(u'p4l_record_projectNames', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm['p4l.record'], null=False)),
            ('projectname', models.ForeignKey(orm['p4l.projectname'], null=False))
        ))
        db.create_unique(u'p4l_record_projectNames', ['record_id', 'projectname_id'])

        # Adding M2M table for field subjectCorporateBodies on 'Record'
        db.create_table(u'p4l_record_subjectCorporateBodies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm['p4l.record'], null=False)),
            ('corporateauthor', models.ForeignKey(orm['p4l.corporateauthor'], null=False))
        ))
        db.create_unique(u'p4l_record_subjectCorporateBodies', ['record_id', 'corporateauthor_id'])

        # Adding M2M table for field corporateAuthors on 'Record'
        db.create_table(u'p4l_record_corporateAuthors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm['p4l.record'], null=False)),
            ('corporateauthor', models.ForeignKey(orm['p4l.corporateauthor'], null=False))
        ))
        db.create_unique(u'p4l_record_corporateAuthors', ['record_id', 'corporateauthor_id'])

        # Adding M2M table for field audiences on 'Record'
        db.create_table(u'p4l_record_audiences', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('record', models.ForeignKey(orm['p4l.record'], null=False)),
            ('audience', models.ForeignKey(orm['p4l.audience'], null=False))
        ))
        db.create_unique(u'p4l_record_audiences', ['record_id', 'audience_id'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table(u'p4l_user')

        # Removing M2M table for field groups on 'User'
        db.delete_table('p4l_user_groups')

        # Removing M2M table for field user_permissions on 'User'
        db.delete_table('p4l_user_user_permissions')

        # Deleting model 'Imprint'
        db.delete_table(u'p4l_imprint')

        # Deleting model 'Serie'
        db.delete_table(u'p4l_serie')

        # Deleting model 'ProjectName'
        db.delete_table(u'p4l_projectname')

        # Deleting model 'CorporateAuthor'
        db.delete_table(u'p4l_corporateauthor')

        # Deleting model 'Url'
        db.delete_table(u'p4l_url')

        # Deleting model 'Subject'
        db.delete_table(u'p4l_subject')

        # Deleting model 'Theme'
        db.delete_table(u'p4l_theme')

        # Deleting model 'Country'
        db.delete_table(u'p4l_country')

        # Deleting model 'Audience'
        db.delete_table(u'p4l_audience')

        # Deleting model 'Isbn'
        db.delete_table(u'p4l_isbn')

        # Deleting model 'Issn'
        db.delete_table(u'p4l_issn')

        # Deleting model 'DocumentCode'
        db.delete_table(u'p4l_documentcode')

        # Deleting model 'Language'
        db.delete_table(u'p4l_language')

        # Deleting model 'Title'
        db.delete_table(u'p4l_title')

        # Deleting model 'AddedTitle'
        db.delete_table(u'p4l_addedtitle')

        # Deleting model 'TitleMainDocument'
        db.delete_table(u'p4l_titlemaindocument')

        # Deleting model 'Abstract'
        db.delete_table(u'p4l_abstract')

        # Deleting model 'Collation'
        db.delete_table(u'p4l_collation')

        # Deleting model 'VolumeIssue'
        db.delete_table(u'p4l_volumeissue')

        # Deleting model 'Author'
        db.delete_table(u'p4l_author')

        # Deleting model 'SubjectPerson'
        db.delete_table(u'p4l_subjectperson')

        # Deleting model 'Periodical'
        db.delete_table(u'p4l_periodical')

        # Deleting model 'Meeting'
        db.delete_table(u'p4l_meeting')

        # Deleting model 'SubjectMeeting'
        db.delete_table(u'p4l_subjectmeeting')

        # Deleting model 'Record'
        db.delete_table(u'p4l_record')

        # Removing M2M table for field subjects on 'Record'
        db.delete_table('p4l_record_subjects')

        # Removing M2M table for field themes on 'Record'
        db.delete_table('p4l_record_themes')

        # Removing M2M table for field countries on 'Record'
        db.delete_table('p4l_record_countries')

        # Removing M2M table for field otherLanguages on 'Record'
        db.delete_table('p4l_record_otherLanguages')

        # Removing M2M table for field projectNames on 'Record'
        db.delete_table('p4l_record_projectNames')

        # Removing M2M table for field subjectCorporateBodies on 'Record'
        db.delete_table('p4l_record_subjectCorporateBodies')

        # Removing M2M table for field corporateAuthors on 'Record'
        db.delete_table('p4l_record_corporateAuthors')

        # Removing M2M table for field audiences on 'Record'
        db.delete_table('p4l_record_audiences')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'p4l.abstract': {
            'Meta': {'object_name': 'Abstract'},
            'abstract': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'abstracts'", 'to': "orm['p4l.Record']"})
        },
        'p4l.addedtitle': {
            'Meta': {'object_name': 'AddedTitle'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'addedTitles'", 'to': "orm['p4l.Record']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.audience': {
            'Meta': {'object_name': 'Audience'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.author': {
            'Meta': {'object_name': 'Author'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'authors'", 'to': "orm['p4l.Record']"})
        },
        'p4l.collation': {
            'Meta': {'object_name': 'Collation'},
            'collation': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collations'", 'to': "orm['p4l.Record']"})
        },
        'p4l.corporateauthor': {
            'Meta': {'object_name': 'CorporateAuthor'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.documentcode': {
            'Meta': {'object_name': 'DocumentCode'},
            'documentCode': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documentCodes'", 'to': "orm['p4l.Record']"})
        },
        'p4l.imprint': {
            'Meta': {'object_name': 'Imprint'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imprintCity': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'imprintDate': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imprints'", 'to': "orm['p4l.Record']"})
        },
        'p4l.isbn': {
            'Meta': {'object_name': 'Isbn'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'isbns'", 'to': "orm['p4l.Record']"})
        },
        'p4l.issn': {
            'Meta': {'object_name': 'Issn'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issn': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issns'", 'to': "orm['p4l.Record']"})
        },
        'p4l.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.meeting': {
            'Meta': {'object_name': 'Meeting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'meetingDate': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'meetingNumber': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'meetingPlace': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'meetingYear': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'meetings'", 'to': "orm['p4l.Record']"})
        },
        'p4l.periodical': {
            'Meta': {'object_name': 'Periodical'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'periodicals'", 'to': "orm['p4l.Record']"})
        },
        'p4l.projectname': {
            'Meta': {'object_name': 'ProjectName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.record': {
            'Meta': {'object_name': 'Record'},
            'audiences': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['p4l.Audience']", 'symmetrical': 'False'}),
            'corporateAuthorLabel': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'corporateAuthors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recordsCorporateAuthor'", 'symmetrical': 'False', 'to': "orm['p4l.CorporateAuthor']"}),
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['p4l.Country']", 'symmetrical': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editionStatement': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'db_index': 'True'}),
            'isDocumentPart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['p4l.Language']", 'null': 'True', 'blank': 'True'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['p4l.User']", 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'otherLanguages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'otherLanguage_record'", 'symmetrical': 'False', 'to': "orm['p4l.Language']"}),
            'projectNames': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['p4l.ProjectName']", 'symmetrical': 'False'}),
            'recordType': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'restricted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subjectCorporateBodies': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'recordsSubjectCorporateBody'", 'symmetrical': 'False', 'to': "orm['p4l.CorporateAuthor']"}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['p4l.Subject']", 'symmetrical': 'False'}),
            'themes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['p4l.Theme']", 'symmetrical': 'False'}),
            'uri': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.serie': {
            'Meta': {'object_name': 'Serie'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'series'", 'to': "orm['p4l.Record']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'})
        },
        'p4l.subject': {
            'Meta': {'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.subjectmeeting': {
            'Meta': {'object_name': 'SubjectMeeting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'}),
            'meetingDate': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'meetingNumber': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'meetingPlace': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'meetingYear': ('django.db.models.fields.PositiveSmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjectMeetings'", 'to': "orm['p4l.Record']"})
        },
        'p4l.subjectperson': {
            'Meta': {'object_name': 'SubjectPerson'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjectPersons'", 'to': "orm['p4l.Record']"})
        },
        'p4l.theme': {
            'Meta': {'object_name': 'Theme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uri': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.title': {
            'Meta': {'object_name': 'Title'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'to': "orm['p4l.Record']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.titlemaindocument': {
            'Meta': {'object_name': 'TitleMainDocument'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titlesMainDocument'", 'to': "orm['p4l.Record']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'})
        },
        'p4l.url': {
            'Meta': {'object_name': 'Url'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'db_index': 'True'}),
            'display': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'urls'", 'to': "orm['p4l.Record']"})
        },
        'p4l.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'p4l.volumeissue': {
            'Meta': {'object_name': 'VolumeIssue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'volumeIssues'", 'to': "orm['p4l.Record']"}),
            'volume': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '1024', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['p4l']