#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
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


from __future__ import print_function
from rules import Rules
from readability import Readability

class Analyzer():

    def __init__(self, document):
        self.document = document

    def _get_stat(self, name, score):
        return {
                "name" : name,
                "score": score
        }

    def _get_stats(self):
        stats = {}
        redability = Readability()
        score = redability.get_score(self.document)
        years = redability.get_crawford(self.document)
        read_time = redability.get_read_time(self.document)

        stats['readability'] = self._get_stat("Llegibilitat", score)
        stats['read_time'] = self._get_stat("Temps de lectura", read_time)
        stats['years'] = self._get_stat("Edat", years)
        stats['paragraphs'] = self._get_stat("Paràgrafs",len(self.document.get_paragraphs()))
        stats['sentences'] = self._get_stat("Frases",len(self.document.get_sentences()))
        stats['words'] = self._get_stat("Paraules",self.document.get_count_words())
        stats['syllabes'] = self._get_stat("Síl·labes", self.document.get_count_syllabes())
        return stats

    def _get_rules(self):
        rules = Rules()
        return rules.check(self.document)

    def get_metrics(self):
        result = {}
        result['metrics'] = self._get_stats()
        return result

    def get_check_rules(self):
        result = {}
        result['matches'] = self._get_rules()
        return result

    def get_all(self):
        result = {}
        result['metrics'] = self._get_stats()
        result['matches'] = self._get_rules()
        return result
