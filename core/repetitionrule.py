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

from match import Match
import os
import re
import logging

class LoadDictionary():

    def _get_form_lemma_postag_from_line(self, line):
        wordList = line.split()
        form = wordList[0]
        lemma = wordList[1]
        postag = wordList[2]
        return form, lemma, postag


    ''' Excloure auxilars havia girat, vaig anar, '''
    def _should_exclude_verb(self, postag):
        AUXILIAR = 'A'
        vtype = postag[1]
        if vtype == AUXILIAR:
            return True

        return False

    def _should_exclude_noun(self, postag):
        ne = postag[4]
        GEO = 'G'
        ORGANIZATION = 'O'
        PERSON = 'S'
        if ne in [GEO, ORGANIZATION, PERSON]:
            return True

        return False


    def load(self):
        word_lemma = {}

        diccionary_file = os.path.dirname(os.path.realpath(__file__))
        diccionary_file = os.path.join(diccionary_file, "linguistic-data/diccionari.txt")

        num = 0
        excluded = set()
        with open(diccionary_file, "r") as dictionary:
            while True:

                line = dictionary.readline()
#                print(f"line {num}:{line}")
                if not line:
                    break

                num = num + 1
                word, lemma, postag = self._get_form_lemma_postag_from_line(line)
                word = word.lower()

                category = postag[0]

                if category not in ['A', 'V', 'N', 'R']:
                    logging.debug(f"excluded '{category}' - '{word}'")
                    excluded.add(word)
                    continue

                if category == 'V':
                    if self._should_exclude_verb(postag):
                        logging.debug(f"Excluded verb {postag[1]} {postag} - '{word}'")
                        excluded.add(word)
                        continue

                if category == 'N':
                    if self._should_exclude_noun(postag):
                        excluded.add(word)
                        logging.debug(f"Excluded noun class {postag[4]} {postag} - '{word}'")
                        continue

                if len(word) < 3: ## 8a, 7è, 6è
                    continue

                word_lemma[word] = lemma

        for word in excluded:
            if word in word_lemma:
                logging.debug(f"removing '{word}'")
                del word_lemma[word]

        print(f"Repetition rule loaded. Words: {len(word_lemma)}")
        return word_lemma

d = LoadDictionary()
g_word_lemma = d.load()


class RepetitionRule():

    def __init__(self):
        self.word_lemma = g_word_lemma

    def check(self, paragraph):
#        print(f"{paragraph.offset} - {paragraph.text}")
        matches = []

        sentence = paragraph.text
        words = sentence.split(' ')

        lemma_frequency = {}
        lemma_occurrences = {}

        for word in words:
            if word not in self.word_lemma:
                #print(f"{word} not found")
                continue

            lemma = self.word_lemma[word]

            if lemma in lemma_occurrences:
                ocurrences = lemma_occurrences[lemma]
            else:
                ocurrences = set()

            ocurrences.add(word)
            lemma_occurrences[lemma] = ocurrences

            if lemma in lemma_frequency:
                frequency = lemma_frequency[lemma]
            else:
                frequency = 0 

            frequency = frequency + 1
            lemma_frequency[lemma] = frequency

        for lemma in lemma_frequency:
            frequency = lemma_frequency[lemma]

            if frequency > 2:
                match = Match()
                match.line = paragraph.line
                match.offset = paragraph.offset
                ocurrences = ', '.join(lemma_occurrences[lemma])

                match.message = f"Repetició {frequency} cops del lema «{lemma}» ({ocurrences})"
                matches.append(match)

        return matches
