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
import re
import datetime as dt
import humanize


class Readability():

    MIN_WORDS_REQUIRED = 100
    init_locale = False

    def _count_sentences(self, text):
        text = text.replace("\n","")
        sentence_end = re.compile('[.:;!?\)\()]')
        sencences=sentence_end.split(text)
        sencences = list(filter(None, sencences))
        if len(sencences) == 0:
            return 1
        else:
            return len(sencences)

    
    def get_crawford(self, document):

        if document.get_count_words() < self.MIN_WORDS_REQUIRED:
            return -1

        syllabes = Syllabes()
        sentences = document.get_sentences()

        word_cnt = 0
        syllabes_cnt = 0
        sentences_cnt = self._count_sentences(document.get_text())
        
        for word in document.get_words():
            word_cnt = word_cnt + 1
            syllabes_cnt = syllabes_cnt + syllabes.get_count(word)

        SeW = 100 * sentences_cnt / word_cnt
        SiW = 100 * syllabes_cnt / word_cnt
        years = -0.205 * SeW + 0.049 * SiW - 3.407
        years = round(years,1)
        return years

    # https://legible.es/blog/perspicuidad-szigriszt-pazos/
    # Adapted for Catalan language
    def get_score(self, document):

        if document.get_count_words() < self.MIN_WORDS_REQUIRED:
            return -1

        syllabes = Syllabes()
        sentences = document.get_sentences()

        word_cnt = 0
        syllabes_cnt = 0
        sentences_cnt = self._count_sentences(document.get_text())
        
        for word in document.get_words():
            word_cnt = word_cnt + 1
            syllabes_cnt = syllabes_cnt + syllabes.get_count(word)

        p = 206.835 - (67.409 * syllabes_cnt / word_cnt) - (0.994 * word_cnt / sentences_cnt)
#        print(f"p = {p} - {sentences_cnt} - {word_cnt} - {syllabes_cnt}")
        if p < 0: p = 0
        if p > 100: p = 100

        return round(p)

    def _get_humanized_time(self, seconds):
        if self.init_locale is False:
            try:
                humanize.i18n.activate("ca_ES")
            except:
                pass

            self.init_locale = True

        delta = dt.timedelta(seconds=seconds)
        return humanize.precisedelta(delta, minimum_unit="seconds", format="%0.0f")

    def get_read_time(self, document):
        words = document.get_count_words()
        seconds = (int) (words / 265 * 60)
        return self._get_humanized_time(seconds)
