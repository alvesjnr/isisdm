#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# ISIS-DM: the ISIS Data Model API
#
# Copyright (C) 2010 BIREME/PAHO/WHO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from ..utils import base28
from .mapper import Document, TextProperty
import uuid
import couchdbkit
import time

class CouchdbDocument(Document):

    def __clean_before_save(self, doc):
        '''
        removes attributes with None values
        '''
        doc = dict((str(k), v) for k, v in doc.items() if v is not None)

        return doc

    def save(self, db):
        doc = self.to_python()
        if not doc.has_key('_id'):
            doc['_id'] = base28.reprbase(int(uuid.uuid4()))

        doc = self.__clean_before_save(doc)

        while True:
            try:
                db.save_doc(doc)
                break
            except couchdbkit.ResourceConflict:
                time.sleep(0.5)
                doc['_id'] = base28.reprbase(int(uuid.uuid4()))

        return doc['_id']

    @classmethod
    def get(cls, db, doc_id):
        doc = db.get(doc_id)
        return cls.from_python(doc)
