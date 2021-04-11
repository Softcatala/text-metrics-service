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

    def _get_stat(self, name, value):
        return {
                "name" : name,
                "value": value
        }

    def _set_stat(self, stats, field, name, value):

        if value == -1:
            stats["message"] = "Les mètriques de llegibilitat només s'ofereixen per a textos prou llargs"
            return

        pair = self._get_stat(name, value)
        stats[field] = pair

    def _get_stats(self):
        stats = {}
        redability = Readability()
        score = redability.get_score(self.document)
        years = redability.get_crawford(self.document)
        read_time = redability.get_read_time(self.document)

        self._set_stat(stats, 'readability', "Llegibilitat", score)
        self._set_stat(stats, 'read_time', "Temps de lectura", read_time)
        self._set_stat(stats, 'paragraphs', "Paràgrafs",len(self.document.get_paragraphs()))
        self._set_stat(stats, 'sentences', "Frases",len(self.document.get_sentences()))
        self._set_stat(stats, 'words', "Paraules",self.document.get_count_words())
        self._set_stat(stats, 'syllabes', "Síl·labes", self.document.get_count_syllabes())
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
