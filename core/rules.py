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
from passiverule import PassiveRule


class Rules():

    def check(self, document):
        matches = []

        repetition_rule = RepetitionRule()
        passive_rule = PassiveRule()
        for paragraph in document.get_paragraphs():
            match = repetition_rule.check(paragraph)
            if match is not None:
                matches.append(match.get_dict())

            match = passive_rule.check(paragraph)
            if match is not None:
                matches.append(match.get_dict())

        return matches

