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
import grapheme

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
        self.syllabes = 0
        self.sentences = []

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

        if len(self.sentences) > 0:
            return self.sentences

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

        self.sentences = sentences
        return self.sentences

    def get_words(self):

        if len(self.words) == 0:
            tokenizer = WordTokenizer()
            words = []
            # We count words at setence level to allow the tokenizer to cache at sentence level since users
            # in production review modified versions of the text instead (once modifications are applied)
            for sentence in self.get_sentences():
                sentence_words = tokenizer.tokenize_without_separators(sentence.text)
                words += sentence_words

            self.words = words

        return self.words

    def get_count_syllabes(self):

        if self.syllabes == 0:
            syllabes = Syllabes()
            cnt = 0
            for word in self.get_words():
                # Count syllabes for words with vowels only
                if re.search('[aeiouàèéíïòóúüáùìäöëî]', word, re.I): cnt += syllabes.get_count(word)

            self.syllabes = cnt

        return self.syllabes

    def get_count_words(self):
        return len(self.get_words())

    def get_count_sentences(self):
        return len(self.get_sentences())

    def get_count_graphemes(self):
        return grapheme.length(self.text)
