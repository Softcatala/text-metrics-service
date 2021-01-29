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

    def _get_document(self, filename):
        full_path = self._get_path_to_file(filename)
        print(full_path)
        doc = Document()
        doc.read_file(full_path)
        return doc

    def test_get_score(self):
        doc = self._get_document('codi-de-conducta.txt')
        readability = Readability()
        score = readability.get_score(doc)
        self.assertEquals(54.38657922558478, score)

    def test_get_crawford(self):
        doc = self._get_document('codi-de-conducta.txt')
        readability = Readability()
        crawford = readability.get_crawford(doc)
        print(crawford)
        self.assertEquals(5.9, crawford)

if __name__ == '__main__':
    unittest.main()
