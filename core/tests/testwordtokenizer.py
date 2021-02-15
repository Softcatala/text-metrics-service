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

from wordtokenizer import WordTokenizer
import unittest


class TestWordTokenizer(unittest.TestCase):

    assess = [
            "Hola, benvinguts.",
            "quaranta-cinc",
            "sars-cov-2",
            "l'Alguer",
            "a l'hora d'anar-se'n",
            "Sàsser-l'Alguer",
            "Castella-la Manxa",
            "qui-sap-lo",
            "L'al.lucinació",
            "d'al·lucinar",
            "d’al·lucinar",
            "d’abans-d’ahir",
            "L'any 2009 va passar això.",
            "Són 2 350 123 dòlars",
            "Són 250 350 123 euros",
            "L'any 2005 250 350 123 euros",
            "d’\"'al·lucinar'\""

    ]


    def test_tokenize(self):

        tokenizer = WordTokenizer()

        expected = [
                ['Hola', ',', '', ' ', 'benvinguts', '.', ''],
                ['quaranta-cinc'],
                ["sars-cov-2"],
                ["l'", 'Alguer'],
                ['a', ' ', "l'", 'hora', ' ', "d'", 'anar', '-se', "'n"],
                ['Sàsser', '-', "l'", 'Alguer'],
                ['Castella', '-', 'la', ' ', 'Manxa'],
                ['qui-sap-lo'],
                ["L'", 'al.lucinació'],
                ["d'", 'al·lucinar'],
                ["d’", 'al·lucinar'],
                ['d’', 'abans-d’ahir'],
                ["L'", 'any', ' ', '2009', ' ', 'va', ' ', 'passar', ' ', 'això', '.', ''],
                ['Són', ' ', '2 350 123', ' ', 'dòlars'],
                ['Són', ' ', '250 350 123', ' ', 'euros'],
                ["L'", 'any', ' ', '2005', ' ', '250 350 123', ' ', 'euros'],
                ['d’', '"', '', "'", 'al·lucinar', "'", '"', '']
        ]


        for idx in range(0, len(self.assess)):
            tokenized = tokenizer.tokenize(self.assess[idx])
            self.assertListEqual(expected[idx], tokenized)

    def test_tokenize_without_separators(self):

        tokenizer = WordTokenizer()

        expected = [
                ['Hola', 'benvinguts'],
                ['quaranta-cinc'],
                ["sars-cov-2"],
                ["l'", 'Alguer'],
                ['a', "l'", 'hora', "d'", 'anar', '-se', "'n"],
                ['Sàsser', "l'", 'Alguer'],
                ['Castella', 'la', 'Manxa'],
                ['qui-sap-lo'],
                ["L'", 'al.lucinació'],
                ["d'", 'al·lucinar'],
                ["d’", 'al·lucinar'],
                ['d’', 'abans-d’ahir'],
                ["L'", 'any',  '2009', 'va', 'passar', 'això'],
                ['Són', '2 350 123', 'dòlars'],
                ['Són', '250 350 123', 'euros'],
                ["L'", 'any', '2005', '250 350 123', 'euros'],
                ['d’', 'al·lucinar']
        ]

        for idx in range(0, len(self.assess)):
            tokenized = tokenizer.tokenize_without_separators(self.assess[idx])
            self.assertListEqual(expected[idx], tokenized)

if __name__ == '__main__':
    unittest.main()
