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

class PassiveRule():

    S = "S"
    P = "P"

    def _get_form_lemma_postag_from_line(self, line):
        wordList = re.sub("[^(\w|·)]", " ",  line).split()
        form = wordList[0]
        lemma = wordList[1]
        postag = wordList[2]
        return form, lemma, postag


    def _add_passat_perifrastic_indicatiu(self, sers, ser):
        sers[f'vaig {ser}'] = self.S
        sers[f'vas {ser}'] = self.S
        sers[f'va {ser}'] = self.S
        sers[f'vares {ser}'] = self.S

        sers[f'vam {ser}'] = self.P
        sers[f'vàrem {ser}'] = self.P
        sers[f'vau {ser}'] = self.P
        sers[f'vàreu {ser}'] = self.P
        sers[f'van {ser}'] = self.P
        sers[f'varen {ser}'] = self.P

    def _add_participis(self, participis, participi, postag):

        if postag == 'SF0' or postag == 'SM0':
            if self.S not in participis:
                participis[self.S] = set()

            verbs = participis[self.S]
            verbs.add(participi)
            participis[self.S] = verbs

        if postag == 'PF0' or postag == 'PM0':
            if self.P not in participis:
                participis[self.P] = set()

            verbs = participis[self.P]
            verbs.add(participi)
            participis[self.P] = verbs


    # Part of speech tags documentation:
    # https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-ca/#part-of-speech-verb
    def load(self):
        SER_POSTAG = 'VSN0'
        PARTICIPI_POSTAG = 'VMP00'
        self.sers = {}
        self.participis = {}

        diccionary_file = os.path.dirname(os.path.realpath(__file__))
        diccionary_file = os.path.join(diccionary_file, "diccionari.txt")

        with open(diccionary_file, "r") as dictionary:
            while True:

                line = dictionary.readline()
                if not line:
                    break

                form, lemma, postag = self._get_form_lemma_postag_from_line(line)

                if postag[0:4] == SER_POSTAG:
                    self._add_passat_perifrastic_indicatiu(self.sers, form)

                if postag[0:5] == PARTICIPI_POSTAG:
                    self._add_participis(self.participis, form, postag[5:])

        for ser in self.sers:
            logging.debug(f"ser: {ser} -> {self.sers[ser]}")

        for num in self.participis.keys():
            for participi in self.participis[num]:
                logging.info(f"participi: {num} -> {participi}")

    # https://geiec.iec.cat/capitol_veure.asp?id_gelc=321&capitol=19
    '''

    Passiva perifràstica

    Passiva que es construeix amb l’auxiliar ser acompanyat d’un verb transitiu en participi passat 
    i que pot incloure un complement agent que equival al subjecte agent de la construcció activa corresponent.

    El quadre va ser robat per una banda organitzada

    Passat perifràstic (ser) + Participi
    '''


    # See: https://geiec.iec.cat/capitol_veure.asp?id_gelc=320&capitol=19
    def check(self, paragraph):
        print(f"{paragraph.offset} - {paragraph.text}")
        match = None

        sentence = paragraph.text.lower()
        words = sentence.split(' ')
        len_words = len(words)

        if len_words < 5:
            return match

        for idx in range(0, len_words - 3):
            for ser in self.sers.keys():
                words_ser = ser.split(' ')
                # Looking for example for 'va ser participi'
                if words_ser[0] == words[idx] and words_ser[1] == words[idx + 1]:
                    participi = words[idx + 2]
                    tag = self.sers[ser]
                    if participi in self.participis[tag]:
                        match = Match()
                        match.offset = paragraph.offset
                        match.message = f"La frase {words[idx]} {words[idx+1]} {words[idx+2]} és passiva"

        return match
