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


class RepetitionRule():


    def load(self):
        self.word_lemma = {}

        with open("diccionari.txt", "r") as dictionary:
            while True:

                line = dictionary.readline().lower()
                if not line:
                    break

                components = line.split(' ')
                word = components[0]
                lemma = components[1]

                if len(word) < 5: ## skip stop words: la, una, etc
                    continue

                self.word_lemma[word] = lemma

#        for word in self.word_lemma:
#            print(f"{word} -> {self.word_lemma[word]}")

    def check(self, sentence):
        words = sentence.split(' ')

        lemma_frequency = {}

        for word in words:
            if word not in self.word_lemma:
                #print(f"{word} not found")
                continue

            lemma = self.word_lemma[word]

            if lemma in lemma_frequency:
                frequency = lemma_frequency[lemma]
            else:
                frequency = 0 

            frequency = frequency + 1
            lemma_frequency[lemma] = frequency

        for lemma in lemma_frequency:
            frequency = lemma_frequency[lemma]

            if frequency > 3:
                print(f"{lemma} -> {sentence}")  


class Document():


    def do(self, filename):
        repetitionRule = RepetitionRule()
        repetitionRule.load()
    
        with open(filename, "r") as source:
            while True:

                line = source.readline()
                if not line:
                    break

                repetitionRule.check(line)
        

def main():
    doc = Document()
    doc.do("tgt-train.txt")



if __name__ == "__main__":
    main()
