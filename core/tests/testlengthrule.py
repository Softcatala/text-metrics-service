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

import unittest
from lengthrule import LengthRule
from document import Document

class TestLengthRule(unittest.TestCase):


    def test_check_longsentence(self):
        doc = Document('El GIMP es pot utilitzar com a un simple programa de dibuix, com a un programa de retoc fotogràfic professional, com a un sistema de processament massiu en línia, com a un sistema de processament massiu en línia, com a un sistema de processament.')
        rule = LengthRule()
        matches = rule.check(doc.get_sentences()[0])
        self.assertEquals(1, len(matches))
        match = matches[0]
        self.assertEquals(0, match.offset)
        self.assertEquals(1, match.line)
        self.assertEquals(246, match.length)

    def test_check_shortsentence(self):
        doc = Document('El GIMP es pot utilitzar com a un simple programa de dibuix, com a un programa de retoc fotogràfic professional.')
        rule = LengthRule()
        matches = rule.check(doc.get_sentences()[0])
        self.assertEquals(0, len(matches))


if __name__ == '__main__':
    unittest.main()
