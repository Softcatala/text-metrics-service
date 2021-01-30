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

from syllabes import Syllabes
import unittest


class TestSyllabes(unittest.TestCase):

    WORDS = [   
                "camió",  3,
                "mariner", 3,
                "aigua", 2,
                "sensesostre", 4,
                "ajudeu", 3,
                "il·luminació", 6,
                "aplicacions", 5,
                "malpensat", 3,
                "capsigrany", 3
            ]

    def test_words(self):
        length = int(len(self.WORDS) / 2)
        i = 0

        while i < len(self.WORDS):

            word = self.WORDS[i]
            cnt_good = self.WORDS[i+1]

            syllabes = Syllabes()
            cnt = syllabes.get_count(word)
            self.assertEquals(cnt_good, cnt)
            i = i + 2


if __name__ == '__main__':
    unittest.main()
