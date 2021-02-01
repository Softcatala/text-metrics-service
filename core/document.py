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
import os
import regex
from syllabes import Syllabes

srx_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'segment.srx')
rules = srx_segmenter.parse(srx_filepath)

class Paragraph():
    def __init__(self, text, offset):
        self.text = text
        self.offset = offset


class Document():

    def __init__(self, text = ''):
        self.text = text

    def get_text(self):
        return self.text

    def read_file(self, filename):
        with open(filename, "r") as source:
            self.text = source.read()

    def get_paragraphs(self):
        PARAGRAPH_SEP = regex.compile("[\r\n]")

        paragraphs = []
        offset = 0
        for text in PARAGRAPH_SEP.split(self.text):
            paragraph = Paragraph(text, offset)
            offset = offset + len(text) + 1
            paragraphs.append(paragraph)

        return paragraphs

    def get_sentences(self):
        segmenter = srx_segmenter.SrxSegmenter(rules["Catalan"], self.text)
        segments, whitespaces = segmenter.extract()
        return segments

    def get_count_syllabes(self):
        syllabes = Syllabes()
        cnt = 0
        for sentence in self.get_sentences():
            words = sentence.split(' ')
            for word in words:
                cnt += syllabes.get_count(word)

        return cnt


    def get_count_words(self):
        words = 0
        for sentence in self.get_sentences():
            words += len(sentence.split(' '))

        return words

if __name__ == "__main__":
    main()
