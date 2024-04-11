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

import srx_segmenter
import unittest
import os

srx_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../linguistic-data/segment.srx')
rules = srx_segmenter.parse(srx_filepath)


class TesSrxSegmenter(unittest.TestCase):

    def test_two_sentences(self):
        text =  "This is a sample text. It contains multiple sentences."
        segmenter = srx_segmenter.SrxSegmenter(rules["Catalan2"], text)
        segments, whitespaces = segmenter.extract()
        self.assertEqual(2, len(segments))

    def test_two_sentences_accents(self):
        text =  "Això és una prova. Tot anirà bé"
        segmenter = srx_segmenter.SrxSegmenter(rules["Catalan2"], text)
        segments, whitespaces = segmenter.extract()
        self.assertEqual(2, len(segments))
        self.assertEqual("Això és una prova.", segments[0])
        self.assertEqual("Tot anirà bé", segments[1])        

    def test_two_sentences_commas(self):
        text =  "Això és una prova. va dir. Tot anirà bé"
        segmenter = srx_segmenter.SrxSegmenter(rules["Catalan2"], text)
        segments, whitespaces = segmenter.extract()
        self.assertEqual(2, len(segments))
        self.assertEqual("Això és una prova. va dir.", segments[0])
        self.assertEqual("Tot anirà bé", segments[1])        

    def test_two_sentences_quotes(self):
        text =  "Sense pensar-ho. Tot per tu. Fins demà."
        segmenter = srx_segmenter.SrxSegmenter(rules["Catalan"], text)
        segments, whitespaces = segmenter.extract()
#        self.assertEqual(3, len(segments))
        self.assertEqual("Sense pensar-ho. Tot per tu.", segments[0])
        self.assertEqual("Fins demà.", segments[1])      


if __name__ == '__main__':
    unittest.main()
