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

import datetime as dt
import humanize


class Readability():

    MIN_WORDS_REQUIRED = 100
    init_locale = False
    
    def get_crawford(self, document):

        word_cnt = document.get_count_words()

        if word_cnt < self.MIN_WORDS_REQUIRED:
            return -1

        syllabes_cnt = document.get_count_syllabes()
        sentences_cnt = document.get_count_sentences()
        
        SeW = 100 * sentences_cnt / word_cnt
        SiW = 100 * syllabes_cnt / word_cnt
        years = -0.205 * SeW + 0.049 * SiW - 3.407
        years = round(years,1)
        return years

    # https://legible.es/blog/perspicuidad-szigriszt-pazos/
    # Adapted for Catalan language
    def get_score(self, document):

        word_cnt = document.get_count_words()

        if word_cnt < self.MIN_WORDS_REQUIRED:
            return -1

        syllabes_cnt = document.get_count_syllabes()
        sentences_cnt = document.get_count_sentences()
        
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
        text = humanize.precisedelta(delta, minimum_unit="seconds", format="%0.0f")

        text = text.replace("hores", "h")
        text = text.replace("minuts", "min")
        text = text.replace("segons", "s")
        text = text.replace("hora", "h")
        text = text.replace("minut", "min")
        text = text.replace("segon", "s")
        text = text.replace(" i ", " ")
        return text

    def get_read_time(self, document):
        words = document.get_count_words()
        seconds = (int) (words / 311 * 60)

        if words > 0 and seconds == 0:
            seconds = 1

        return self._get_humanized_time(seconds)

    def get_speak_time(self, document):
        words = document.get_count_words()
        seconds = (int) (words / 180 * 60)

        if words > 0 and seconds == 0:
            seconds = 1

        return self._get_humanized_time(seconds)
