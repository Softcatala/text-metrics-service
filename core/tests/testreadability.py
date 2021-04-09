# -*- coding: utf-8 -*-
#
# Copyright (c) 2021 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from readability import Readability
from document import Document
import unittest
import os


class TestReadability(unittest.TestCase):

    def _get_path_to_file(self, filename):
        directory = os.path.dirname(os.path.realpath(__file__))
        directory += '/data/'
        return os.path.join(directory, filename)

    def _get_document(self):
        filename = 'codi-de-conducta.txt'
        full_path = self._get_path_to_file(filename)
        doc = Document()
        doc.read_file(full_path)
        return doc

    def test_get_score(self):
        doc = self._get_document()
        readability = Readability()
        score = readability.get_score(doc)
        self.assertEquals(57, score)

    def test_get_score_too_short(self):
        doc = Document("Hola")
        readability = Readability()
        score = readability.get_score(doc)
        self.assertEquals(-1, score)

    def test_get_crawford(self):
        doc = self._get_document()
        readability = Readability()
        crawford = readability.get_crawford(doc)
        self.assertEquals(5.7, crawford)

    def test_get_crawford_too_short(self):
        doc = Document("Hola")
        readability = Readability()
        crawford = readability.get_crawford(doc)
        self.assertEquals(-1, crawford)


    def test_get_read_time(self):
        doc = self._get_document()
        readability = Readability()
        time = readability.get_read_time(doc)
        self.assertEquals("1 minut i 17 segons", time)

if __name__ == '__main__':
    unittest.main()
