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


#. Podries comptar síl·labes fàcilment comptant vocals,
# amb l'excepció de vocal forta + feble (ai, au, ei, eu, etc.) i les combinacions qua, qüe, gua, etc.

class Syllabes():

    def _remove_accents(self, text):
        text = text.replace('à', 'a')
        text = text.replace('é', 'e')
        text = text.replace('í', 'i')
        text = text.replace('ó', 'o')
        text = text.replace('ò', 'o')
        text = text.replace('ú', 'u')
        text = text.replace('ü', 'u')
        return text

    def get_count(self, text):
        text = self._remove_accents(text)

        # forta + feable
        text = text.replace('ae', 'a')
        text = text.replace('ai', 'a')
        text = text.replace('ao', 'a')
        text = text.replace('au', 'a')

        text = text.replace('ea', 'e')
        text = text.replace('ei', 'e')
        text = text.replace('eo', 'e')
        text = text.replace('eu', 'e')

        text = text.replace('ea', 'e')
        text = text.replace('ei', 'e')
        text = text.replace('eo', 'e')
        text = text.replace('eu', 'e')

        #combinacions qua, qüe, gua
        text = text.replace('qua', 'a')
        text = text.replace('que', 'u')
        text = text.replace('gua', 'u')

        vocals = 0
        for c in text:
            if c in ['a', 'e', 'i', 'o', 'u']:
                vocals = vocals + 1

        return vocals

