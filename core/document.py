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
import re
from syllabes import Syllabes
from wordtokenizer import WordTokenizer

srx_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'linguistic-data/segment.srx')
rules = srx_segmenter.parse(srx_filepath)

class Paragraph():
    def __init__(self, text, offset, line):
        self.text = text
        self.offset = offset
        self.line = line

class Sentence():
    def __init__(self, text, offset, line):
        self.text = text
        self.offset = offset
        self.line = line


class Document():

    def __init__(self, text = ''):
        self.text = text
        self.words = []

    def get_text(self):
        return self.text

    def read_file(self, filename):
        with open(filename, "r") as source:
            self.text = source.read()

    def get_paragraphs(self):
        PARAGRAPH_SEP = re.compile("([\r\n])")
        PARAGRAPH_LINES_CNT = re.compile("\r?\n")
        line = 1
        offset = 0
        paragraphs = []

        for text in PARAGRAPH_SEP.split(self.text):
            if len(text.strip()) > 0:
                paragraph = Paragraph(text, offset, line)
                paragraphs.append(paragraph)

            offset = offset + len(text)
            line = line + len(re.findall(PARAGRAPH_LINES_CNT, text))

        return paragraphs

    def get_sentences(self):
        PARAGRAPH_LINES_CNT = re.compile("\r?\n")
        segmenter = srx_segmenter.SrxSegmenter(rules["Catalan"], self.text)
        segments, whitespaces = segmenter.extract()

        line = 1
        offset = 0
        sentences = []

        for i in range(0, len(segments)):
            line = line + len(re.findall(PARAGRAPH_LINES_CNT, whitespaces[i]))

            offset = offset + len(whitespaces[i])
            sentence = Sentence(segments[i], offset, line)
            offset = offset + len(segments[i])
            sentences.append(sentence)

        return sentences

    def get_words(self):

        if len(self.words) == 0:
            tokenizer = WordTokenizer()
            self.words = tokenizer.tokenize_without_separators(self.text)

        return self.words

    def get_count_syllabes(self):
        syllabes = Syllabes()
        cnt = 0
        for word in self.get_words():
            cnt += syllabes.get_count(word)

        return cnt

    def get_count_words(self):
        return len(self.get_words())
