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


class TestDocument(unittest.TestCase):

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

    def test_get_paragraphs(self):
        doc = self._get_document()
        paragraphs = len(doc.get_paragraphs())
        self.assertEquals(18, paragraphs)

    def test_get_sentences(self):
        doc = self._get_document()
        sentences = len(doc.get_sentences())
        self.assertEquals(31, sentences)

    def test_get_sentences_lines(self):
        text  = 'Hola amics.\r\nNo hi anirem tots. Pero jo anire i sera molt divertit.\n\nQuin dia es?\n\rDilluns'
        doc = Document(text)
        sentences = doc.get_sentences()

        expected_results = [
                [1, 0, "Hola amics."],
                [2, 13, "No hi anirem tots."],
                [2, 32, "Pero jo anire i sera molt divertit."],
                [4, 69, "Quin dia es?"],
                [5, 83, "Dilluns"]
            ]

        self.assertEquals(len(expected_results), len(sentences))

        idx = 0
        for expected in expected_results:
            self.assertEquals(expected[0], sentences[idx].line)
            self.assertEquals(expected[1], sentences[idx].offset)
            self.assertEquals(expected[2], sentences[idx].text)
            idx = idx + 1

    def test_get_sentences_lines(self):
        text  = 'Hola amics.\r\nNo hi anirem tots. Pero jo anire i sera molt divertit.\n\nQuin dia es?\n\rDilluns'
        doc = Document(text)
        paragraphs = doc.get_paragraphs()

        expected_results = [
                [1, 0, "Hola amics."],
                [2, 13, "No hi anirem tots. Pero jo anire i sera molt divertit."],
                [4, 69, "Quin dia es?"],
                [5, 83, "Dilluns"]
            ]

        self.assertEquals(len(expected_results), len(paragraphs))

        idx = 0
        for expected in expected_results:
            self.assertEquals(expected[0], paragraphs[idx].line)
            self.assertEquals(expected[1], paragraphs[idx].offset)
            self.assertEquals(expected[2], paragraphs[idx].text)
            idx = idx + 1

    def test_get_words(self):
        doc = self._get_document()
        words = doc.get_count_words()
        self.assertEquals(342, words)

    def test_get_count_syllabes(self):
        doc = self._get_document()
        syllabes = doc.get_count_syllabes()
        self.assertEquals(730, syllabes)


if __name__ == '__main__':
    unittest.main()
