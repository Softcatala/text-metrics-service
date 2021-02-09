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


class LengthRule():


    def check(self, sentence):
        MAX_WORDS = 35
        matches = []

        words = sentence.text.split(' ')

        if len(words) > MAX_WORDS:
            match = Match()
            match.line = sentence.line
            match.offset = sentence.offset

            text = sentence.text[:20]
            match.message = f"La frase «{text}...» que és massa larga"
            matches.append(match)

        return matches
