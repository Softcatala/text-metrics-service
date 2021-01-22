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

from repetitionrule import RepetitionRule
from readability import Readability

import srx_segmenter
import os

srx_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'segment.srx')
rules = srx_segmenter.parse(srx_filepath)


class Document():

    def get_text(self):
        return self.text

    def read_file(self, filename):
        with open(filename, "r") as source:
            self.text = source.read()


    def __do__old(self, text):
        repetitionRule = RepetitionRule()
        repetitionRule.load()
    
        with open(filename, "r") as source:
            while True:

                line = source.readline()
                if not line:
                    break

                repetitionRule.check(line)

    def get_paragraphs(self):
        PARAGRAPH_SEP = regex.compile("[\r\n]")
        return PARAGRAPH_SEP.split(self.text)

    def get_sentences(self):
        segmenter = srx_segmenter.SrxSegmenter(rules["Catalan"], self.text)
        segments, whitespaces = segmenter.extract()
        return segments

def main():
    doc = Document()
    doc.read_file("1000.txt")
    redability = Readability()
    score = redability.get_score(doc)
    years = redability.get_crawford(doc)
    print(f"Readibility Szigriszt-pazos: {score}, years: {years}")

if __name__ == "__main__":
    main()
