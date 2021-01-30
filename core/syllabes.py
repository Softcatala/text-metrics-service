
""" Hyphenation, using Frank Liang's algorithm.

    This module provides a single function to hyphenate words.  hyphenate_word takes
    a string (the word), and returns a list of parts that can be separated by hyphens.

    >>> hyphenate_word("hyphenation")
    ['hy', 'phen', 'ation']
    >>> hyphenate_word("supercalifragilisticexpialidocious")
    ['su', 'per', 'cal', 'ifrag', 'ilis', 'tic', 'ex', 'pi', 'ali', 'do', 'cious']
    >>> hyphenate_word("project")
    ['project']
    
    Ned Batchelder, July 2007.
    This Python code is in the public domain.
"""

import re

__version__ = '1.0.20070709'

class Hyphenator:
    def __init__(self, patterns, exceptions=''):
        self.tree = {}
        for pattern in patterns.split():
            self._insert_pattern(pattern)

        self.exceptions = {}
        #for ex in exceptions.split():
        #    # Convert the hyphenated pattern into a point array for use later.
        #    self.exceptions[ex.replace('-', '')] = [0] + [ int(h == '-') for h in re.split(r"[^0-9 \r\n\t]", ex) ]

    def _insert_pattern(self, pattern):
        # Convert the a pattern like 'a1bc3d4' into a string of chars 'abcd'
        # and a list of points [ 0, 1, 0, 3, 4 ].
        chars = re.sub('[0-9]', '', pattern)
        points = [ int(d or 0) for d in re.split("[.a-z’'·ŀàáèéíòóúçüï-ö-î]", pattern) ]

        # Insert the pattern into the tree.  Each character finds a dict
        # another level down in the tree, and leaf nodes have the list of
        # points.
        t = self.tree
        for c in chars:
            if c not in t:
                t[c] = {}
            t = t[c]
        t[None] = points

    def hyphenate_word(self, word):
        """ Given a word, returns a list of pieces, broken at the possible
            hyphenation points.
        """
        # Short words aren't hyphenated.
        #if len(word) <= 4:
        #    return [word]
        # If the word is an exception, get the stored points.
        if word.lower() in self.exceptions:
            points = self.exceptions[word.lower()]
        else:
            work = '.' + word.lower() + '.'
            points = [0] * (len(work)+1)
            for i in range(len(work)):
                t = self.tree
                for c in work[i:]:
                    if c in t:
                        t = t[c]
                        if None in t:
                            p = t[None]
                            for j in range(len(p)):
                                points[i+j] = max(points[i+j], p[j])
                    else:
                        break
            # No hyphens in the first two chars or the last two.
            # points[1] = points[2] = points[-2] = points[-3] = 0

        # Examine the points to build the pieces list.
        pieces = ['']
        for c, p in zip(word, points[2:]):
            pieces[-1] += c
            if p % 2:
                pieces.append('')
        return pieces


patterns = (
"""
8'8
8’8
l·9l
ŀ9l
1ba 1be 1bi 1bo 1bu
1ca 1ce 1ci 1co 1cu
1da 1de 1di 1do 3du
1fa 1fe 1fi 1fo 1fu
1ga 1ge 1gi 1go 1gu
1ha 1he 1hi 1ho 1hu
1ja 1je 1ji 1jo 1ju
1ka 1ke 1ki 1ko 1ku
1la 1le 1li 1lo 1lu
1ma 1me 1mi 1mo 1mu
1na 1ne 3ni 1no 1nu
1pa 3pe 3pi 3po 1pu
1qu
1ra 1re 1ri 1ro 1ru
1sa 1se 1si 1so 1su
1ta 1te 1ti 1to 1tu
1va 1ve 1vi 1vo 1vu
1xa 1xe 1xi 1xo 1xu
1za 1ze 1zi 1zo 1zu
1bé 1bí 1bó 1bú 1bà 1bè 1bò
1cé 1cí 1có 1cú 1cà 1cè 1cò
1ço 1ça 1çu
1çó 1çú 1çà 1çò
1dé 1dí 1dó 1dú 1dà 1dè 1dò
1fé 1fí 1fó 1fú 1fà 1fè 1fò
1gé 1gí 1gó 1gú 1gà 1gè
1gò 1gü
1hé 1hí 1hó 1hú 1hà 1hè 1hò
1jé 1jí 1jó 1jú 1jà 1jè 1jò
1ké 1kí 1kó 1kú 1kà 1kè 1kò
1lé 1lí 1ló 1lú 1là 1lè 1lò
1mé 1mí 1mó 1mú 1mà 1mè 1mò
1né 1ní 1nó 1nú 1nà 1nè 1nò
1pé 1pí 1pó 1pú 1pà 1pè 1pò
1qü
1ré 1rí 1ró 1rú 1rà 1rè 1rò
1sé 1sí 1só 1sú 1sà 1sè 1sò
1té 1tí 1tó 1tú 1tà 1tè 1tò
1vé 1ví 1vó 1vú 1và 1vè 1vò
1xé 1xí 1xó 1xú 1xà 1xè 1xò
1zé 1zí 1zó 1zú 1zà 1zè 1zò
1wa 1we 1wi 1wo 1wu
1ka 1ke 1ki 1ko 1ku
3l2la 1l2le 1l2li 3l2lo 1l2lu
1b2la 1b2le 1b2li 1b2lo 1b2lu
1b2ra 1b2re 1b2ri 1b2ro 1b2ru
1c2la 1c2le 1c2li 1c2lo 1c2lu
1c2ra 1c2re 1c2ri 1c2ro 1c2ru
1d2ra 1d2re 1d2ri 1d2ro 1d2ru
1f2la 1f2le 1f2li 1f2lo 1f2lu
1f2ra 1f2re 1f2ri 1f2ro 1f2ru
1g2la 1g2le 1g2li 1g2lo 1g2lu
1g2ra 1g2re 1g2ri 1g2ro 1g2ru
1p2la 1p2le 1p2li 1p2lo 1p2lu
1p2ra 1p2re 1p2ri 1p2ro 1p2ru
1t2ra 1t2re 1t2ri 1t2ro 1t2ru
1n2ya 1n2ye 1n2yi 1n2yo 1n2yu
1l2lé 1l2lí 1l2ló 1l2lú 1l2là
1l2lè 1l2lò
1b2lé 1b2lí 1b2ló 1b2lú 1b2là
1b2lè 1b2lò
1b2ré 1b2rí 1b2ró 1b2rú 1b2rà
1b2rè 1b2rò
1c2lé 1c2lí 1c2ló 1c2lú 1c2là
1c2lè 1c2lò
1c2ré 1c2rí 1c2ró 1c2rú 1c2rà
1c2rè 1c2rò
1d2ré 1d2rí 1d2ró 1d2rú 1d2rà
1d2rè 1d2rò
1f2lé 1f2lí 1f2ló 1f2lú 1f2là
1f2lè 1f2lò
1f2ré 1f2rí 1f2ró 1f2rú 1f2rà
1f2rè 1f2rò
1g2lé 1g2lí 1g2ló 1g2lú 1g2là
1g2lè 1g2lò
1g2ré 1g2rí 1g2ró 1g2rú 1g2rà
1g2rè 1g2rò
1p2lé 1p2lí 1p2ló 1p2lú 1p2là
1p2lè 1p2lò
1p2ré 1p2rí 1p2ró 1p2rú 1p2rà
1p2rè 1p2rò
1t2ré 1t2rí 1t2ró 1t2rú 1t2rà
1t2rè 1t2rò
1n2yé 1n2yí 1n2yó 1n2yú 1n2yà
1n2yè 1n2yò 1n2yá
a1a a1e a1o
e1a e1e e1o
i1a i1e i1o
o1a o1e o1o
u1a u1e u1o
a1é a1í a1ó a1ú a1à a1è
a1ò a1ï a1ü
e1é e1í e1ó e1ú e1à e1è
e1ò e1ï e1ü
i1é i1í i1ó i1ú i1à i1è
i1ò i1ï i1ü
o1é o1í o1ó o1ú o1à o1è o1á
o1ò o1ï o1ü
u1é u1í u1ó u1ú u1à u1è
u1ò u1ï u1ü
é1a é1e é1o
é1ï é1ü
í1a í1e í1o í1i
í1ï í1ü
ó1a ó1e ó1o
ó1ï ó1ü
ú1a ú1e ú1o
ú1ï ú1ü
à1a à1e à1o
à1ï à1ü
è1a è1e è1o
è1ï è1ü
ò1a ò1e ò1o
ò1ï ò1ü
ï1a ï1e ï1o ï1é ï1í
ï1ó ï1ú ï1à
ï1è ï1ò ï1i
ü1a ü1e ü1o ü1é ü1í
ü1ó ü1ú ü1à
ü1è ü1ò
a1i2a a1i2e a1i2o a1i2u
a1u2a a1u2e a1u2i a1u2o a1u2u
e1i2a e1i2e e1i2o e1i2u
e1u2a e1u2e e1u2i e1u2o e1u2u
i1i2a i1i2e i1i2o i1i2u
i1u2a i1u2e i1u2i i1u2o i1u2u
o1i2a o1i2e o1i2o o1i2u
o1u2a o1u2e o1u2o o1u2i o1u2u
u1i2a u1i2e u1i2o u1i2u
u1u2a u1u2e u1u2i u1u2o u1u2u
a1i2é a1i2í a1i2ó a1i2ú a1i2à
a1i2è a1i2ò
a1u2é a1u2í a1u2ó a1u2ú a1u2à
a1u2è a1u2ò
e1i2é e1i2í e1i2ó e1i2ú e1i2à
e1i2è e1i2ò
e1u2é e1u2í e1u2ó e1u2ú e1u2à
e1u2è e1u2ò
i1i2é i1i2í i1i2ó i1i2ú i1i2à
i1i2è i1i2ò
i1u2é i1u2í i1u2ó i1u2ú i1u2à
i1u2è i1u2ò
o1i2é o1i2í o1i2ó o1i2ú o1i2à
o1i2è o1i2ò
o1u2é o1u2í o1u2ó o1u2ú o1u2à
o1u2è o1u2ò
u1i2é u1i2í u1i2ó u1i2ú u1i2à
u1i2è u1i2ò
u1u2é u1u2í u1u2ó u1u2ú u1u2à
u1u2è u1u2ò
é1i2a é1i2e é1i2o é1i2u
é1u2a é1u2e é1u2o é1u2i é1u2u
í1i2a í1i2e í1i2o í1i2u
í1u2a í1u2e í1u2o í1u2i í1u2u
ó1i2a ó1i2e ó1i2o ó1i2u
ó1u2a ó1u2e ó1u2o ó1u2i ó1u2u
ú1i2a ú1i2e ú1i2o ú1i2u
ú1u2a ú1u2e ú1u2o ú1u2i ú1u2u
à1i2a à1i2e à1i2o à1i2u
à1u2a à1u2e à1u2o à1u2i à1u2u
è1i2a è1i2e è1i2o è1i2u
è1u2a è1u2e è1u2o è1u2i è1u2u
ò1i2a ò1i2e ò1i2o ò1i2u
ò1u2a ò1u2e ò1u2o ò1u2i ò1u2u
ï1i2a ï1i2e ï1i2o ï1i2é ï1i2í
ï1i2ó
ï1i2ú ï1i2à
ï1i2è ï1i2ò ï1i2u
ï1u2a ï1u2e ï1u2o ï1u2é ï1u2í
ï1u2ó
ï1u2ú ï1u2à
ï1u2è ï1u2ò ï1u2i ï1u2u
ü1i2a ü1i2e ü1i2o ü1i2é ü1i2í
ü1i2ó
ü1i2ú ü1i2à
ü1i2è ü1i2ò ü1i2u
ü1u2a ü1u2e ü1u2o ü1u2é ü1u2í
ü1u2ó
ü1u2ú ü1u2à
ü1u2è ü1u2ò ü1u2i ü1u2u
qui3a qui3à qui3e qui3è qui3é qui3o qui3ó qui3ò qui3ú
gui3a gui3à gui3e gui3è gui3é gui3o gui3ó gui3ò
.i2a .i2e .i2o .i2u .u2a .u2e .u2i .u2o
.hi2a .hi2e .hi2o .hi2u .hu2a .hu2e .hu2i .hu2o
.i2é .i2í .i2ó .i2ú .i2à
.i2è .i2ò
.u2é .u2í .u2ó .u2ú .u2à
.u2è .u2ò
.hi2é .hi2ó .hi2ú .hi2à .hi2è
.hi2ò
.hu2é .hu2í .hu2ó .hu2à .hu2è
.hu2ò
-i2o
gu2a gu2e gu2i gu2o
gu2à gu2é gu2è gu2í gu2ó gu2ò
qu2a qu2e qu2i qu2o
qu2à qu2è qu2é qu2í qu2ó qu2ò
gü2e gü2é gü2í gü2è gü2i
qü2e qü2é qü2í qü2è qü2i
a1isme. e1isme. i1isme. o1isme. u1isme.
a1ista. e1ista. i1ista. o1ista. u1ista.
a1iste. e1iste. i1iste. o1iste. u1iste.
a1ismes. e1ismes. i1ismes. o1ismes. u1ismes.
a1istes. e1istes. i1istes. o1istes. u1istes.
a1istament. e1istament. i1istament. o1istament. u1istament.
a1um. e1um. i1um. o1um. u1um.
a1ums. e1ums. i1ums. o1ums. u1ums.
.b4 .c4 .d4 .f4 .g4 .h4 .j4 .k4 .l4 .m4 .n4 .q4 .r4 .s4 .t4 .v4 .w4 .x4 .z4
.p4s4 .p4t4 .p4n4 .m4n4 .t4s4 .g4n4 .c4n4 .f4t4 .k4h4 .k4r4 .k4l4
.s4c4 .s4t4 .r4h4 .t4x4 .s4h4 .s4n4 .g4h4 .s4p4 .c4t4
.sch4 .s4w .t4w .s4t4o
3f4t4alat
3f4t4àli
na4f5tàli
3p4n4eumàti
3f4taleïn
à1id.
è1id.
é1id.
ò1id.
ó1id.
ú1id.
à1ids.
è1ids.
ó1ids.
ò1ids.
ó1ids.
ú1ids.
u1ir. qu4ir. gu4ir. u1int. qu4int. gu4int.
e1ir. e1int. a1ir. a1int. o1ir. o1int.
u1ir- qu4ir- gu4ir- u1int- qu4int- gu4int-
e1ir- e1int- a1ir- a1int- o1ir- o1int-
.cu4ir. .va4ir.
a1iré. a1iràs. a1irà. a1irem. a1ireu. a1iran.
e1iré. e1iràs. e1irà. e1irem. e1ireu. e1iran.
o1iré. o1iràs. o1irà. o1irem. o1ireu. o1iran.
u1iré. u1iràs. u1irà. u1irem. u1ireu. u1iran.
qu4iré. qu4iràs. qu4irà. qu4irem. qu4ireu. qu4iran.
gu4iré. gu4iràs. gu4irà. gu4irem. gu4ireu. gu4iran.
.ca4ir .desa4ir .enla4ir .esca4ir .fla4ir .repa4ir
a1iria. a1iries. a1iríem. a1iríeu. a1irien.
e1iria. e1iries. e1iríem. e1iríeu. e1irien.
o1iria. o1iries. o1iríem. o1iríeu. o1irien.
u1iria. u1iries. u1iríem. u1iríeu. u1irien.
qu4iria. qu4iries. qu4iríem. qu4iríeu. qu4irien.
gu4iria. gu4iries. gu4iríem. gu4iríeu. gu4irien.
.para4iria. .para4iries. .pera4iria. .pera4iries. .le4iria.
.c2h2 .t2h2 .w2h2
.b4d .b4h .w4r4 .z4w4
hi4àt
3p4sico 3p4siqu 3p4síqu
co3incid
i3onitz
l3f4t
o3p4neum
tio3ure
tio3uri
.a2b3alien
.a2b3ampere
.a2b3axial
.a2b3intesta
.a2d3axial
.a2b3reacc
a4b3rog
.a4n3abio
.a4n3abiò
.a4n3acústic
.a4n3aero
.a4n3aerò
.a4n3afrod
.a4n3alcoh
.a4n3alfabet
.a4n3algèsi
.a4n3algesina
.a4n3àlgia
.a4n3al·
.a4n3amniota
.a4n3anabàsia
.a4n3anastàsia
.a4n3apodíctic
.a4n3àrtria
.a4n3àspid
.a4n3astigm
.a4n3ecoic
.a4n3elast
.a4n3elèctric
.a4n3energètic
.a4n3epígraf
.a4n3epigràfic
.a4n3erotisme
.a4n3estesi
.a4n3estèsi
.a4n3euplo
.a4n3ictèric
.a4n3ideació
.a4n3ió
.a4n3iònic
.a4n3iotropia
.a4n3irídia
.a4n3iso
.a4n3isò
.a4n3odòncia
.a4n3opistògraf
.a4n3orc
.a4n3orè
.a4n3orgà
.a4n3òrtic
.a4n3ort
.a4n3ostracis
.a4n3ovul
.a4n3oxèmia
.a4n3òxi
.a4n3oxi
.a4n3ur
.a4n3úria
.a2n3axial
.a2n3abiòti
.a2n3adèni
.a2n3nabàsi
.a2n3artròpode
.a2n3aspidaci
.a2n3estable
.a2n3eusomi
.a2n3oftàlmi
.a2n3èdri
.anti3i .anti3u
.auto3i
argü5i
argü5í
argü5ï
argü5e
.arque1us.
.adamaua3ubangui
.a4ll3ioli
.a4ll3ipebre
o3immun
.al4t3alemany
.al4t3imperial
.a4n3andre
.anglo3i
.a4n3iono
.aniso3ic
.a4n3òsmi
.a3p4neumàtic
.a3p4nèumia
.a3p4tialisme
.atropo3isomeria
.auto4ic
be4s3avi
be4s3àvi
be4s3oncle
.bio3i
.bi3un
.be4n3afect
.be4n3am
.be4n3an
.be4n3astru
.be4n3aura
.be4n3aven
.be4n3avin
.be4n3entès
.be4n3esta
.be4n3inten
.bai4x3alemany
.bai4x3imperial
.ba3t4honi
.bi4s3anual
.bi1uret
.brew3s4ter
.bronco3p4neu
í3um.
í3ums.
.ca4p3alç
.ca4p3alc
.ca4p3alt
.ca4p3ialt
.ca4p3esflora
.ca4p3ialça
.ca4p3ipot
.cen4t3enram
.cibe4r3espai
.ci4s3alpí
.ci4s3alpin
.ca4p3iampl
.ca4p3icaus
.ca4p3icu
.ca4p3imo
.carbodi3imid
.ce4l3obert
.cen4t3engran
.ce4s3alp
cla4r3obscur
àusi3us.
.cofi4s3imofis
.co4l3iflor
.co4l3inap
.co4ll3estret
.co4ll3ibè
.co4n3establ
.co4n3oncle
.contra3i
.co4n3urba
.co4r3agr
.co4r3esforç
.co4r3esforc
.curaça4o
.curi4e
de1bye
.de2s
.des3a
.de3s4ament
.de3s4ar.
.de3s4ant.
.de3s4at.
.de3s4ada.
.de3s4ats.
.de3s4ades.
.de3s4o.
.de3s4e.
.de3s4es.
.de3s4a.
.de3s4em.
.de3s4eu.
.de3s4en.
.de3s4ava.
.de3s4aves.
.de3s4ava.
.de3s4àvem.
.de3s4àveu.
.de3s4aven.
.de3s4í.
.de3s4ares.
.de3s4à.
.de3s4àrem.
.de3s4àreu.
.de3s4aren.
.de3s4aré.
.de3s4aràs.
.de3s4arà.
.de3s4arem.
.de3s4areu.
.de3s4aran.
.de3s4aria.
.de3s4aries.
.de3s4aria.
.de3s4aríem.
.de3s4aríeu.
.de3s4arien.
.de3s4i.
.de3s4is.
.de3s4i.
.de3s4em.
.de3s4eu.
.de3s4in.
.de3s4és.
.de3s4ara.
.de3s4essis.
.de3s4és.
.de3s4éssim.
.de3s4éssiu.
.de3s4essin.
.de3s4a.
.de3s4i.
.de3s4em.
.de3s4eu.
.de3s4in.
.de3s4è.
.des3em
.de3s4em3bre
.de3s4em3bral
.de3s4em3brist
.des3en
.dese4n3aig
.dese4n3amor
.dese4n3aspr
.dese4n3ast
.de3s4e3na.
.de3s4e3nes.
.de3s4e3nal
.de3s4e3nà3ri
.de3s4e3na3ri
.de3s4e3ner
de2s3envol
.des3e3qui
.de3s4ert
.de3s4èrt
.des3es
.des3i3gual
.des3il
.des3i3mant
.des3im
.des3in
.de3s4i3nèn3ci
.de3s4i3nen3ci
.des3i3o3ni
.de3siderata
.de3sideràtum
.de3sig.
.de3sigs.
.de3sign
.de3sist
.de3sitj
.de3sitg
.de3sídi
.de3sidi
.de4s3edifi
.de4s3eix
.de4s3isc
.de4s3isq
.de4s3electr
.de3s4erci
.de4s3erm
.de3sideratiu
.des3ànim
.de4s3ús
.des3ésser
.des3o
.de3s4o3l
.de3s4or3ci
.de3s4o3ri.
.de3s4o3ris.
.des3u
.de3s4u3e3tud
.de3s4u3et.
.de3s4u3ets.
.diastereo3is
.di4s3azoic
.di4s3economi
.di4s3endocríni
.di4s3estèsi
.di4s3àgio
.dis3m4nèsi
.di4s3àrtri
.due4s3aigüe
.du1umvir
.ein3s4tein
.electro3i
.e4n3a
.e9n8agües.
.e5n4anti
.e5n4a.
.e5n4es.
.e5n4agist
.e5n4agos.
.e5n4ans.
.e5n4ant
.e5n4argit
.e4n3oft
.e4n3org
.equi3uroïdeus
.escura3u
.estereo3is
.e8u9èdri
.e4x3estipul
.e4x3ànime
.e2x3a
.e3x4am
.e3x4ag
.ex3a3br
e4x3a4c3t
.he5x4act
.e4x3oft
.e4x3oner
.e4x3orable
.e4x3orbi
.e4x3orna
.e4x3osmosi
.e4x3ulce
fue4l5oil
.farmaco3röntgen
de4s3integr
.fron4t3ampl
.fran3k4lin
.ga4s3oil
.g4j4eli
grei4x3oli
.gastro3intest
.genito3urin
.go4e3t4hi
.guarda3infant
.gup3py
.hep3t4hemímer
.hete4r3oft
he3ixvan
.hi3òlit
.hi3al
.hi3ogl
.hi3osc
.hipe4r3
.hipe5r4icàci
.hiperm4n4
.hiperp4n4
.hipe5r4ó.
.hipe5r4ons.
.hipe5r4èmi
.hiper4sten
.hu3axt
.hu3astec
.hu3asteq
ho1llywo4od
.iu5an.
.iu5ans.
.i3ó.
.i3ons.
.ibero3i
.i4àmbic
.i4n3a
.i5n4anitat
.i5n4anici
.i4n3e
.i5n4ebri
.i5n4ercial
.i5n4erme
.i5n4ert
.i5n4ept
.i5n4eluc
.i5n4efab
.i4n5in
.i4n5im
.i4n5ig
.i4n3o
.i5n4osi
.i5n4otr
.i4n3òpi
.i5n4osínic
.i5n4o-
.i4n3èdit
.indo3i
.i4n3e4x3or
.i3ònic
.inte4r3
.inte5r4ior
.inter4stici
.inte5r4ocep
.inte5r4opercl
.inte5r4í.
.inte5r4ina.
.inte5r4ins.
.inte5r4ines.
.inte5r4inament.
.inte5r4initat
.inter4n.
.inte5r4ès.
.inte5r4ess
.i4n3útil
.intra3u
.i4n3urb
.i4n3us
.i4n3ut
.i3on
.irre3ivind
.iso3immun
.i4àtric
.i4oni.
.i4onis.
.i4onona.
.i4onones.
1injecci
1inject
.jans3ky.
.je4ep
.jou4le
kle4b3s4hormi
íle3us.
.lo4el·lingit
.maastri4chtià
.macro3instr
.ma2l3absor
.ma2l3acons
.ma2l3acostum
.ma2l3agr
.ma2l3air
.ma2l3amor
.ma2l3ana
.ma2l3àn
.ma2l3ap
.ma2l3arm
.ma2l3as
.ma2l3au
.ma2l3avent
.ma2l3aves
.ma2l3avin
.ma2l3enca
.ma2l3encert
.ma2l3endr
.ma2l3espàrrec
.ma2l3ent
.ma2l3est
.ma2l3int
.ma2l3ord
.ma2l3obedient
.ma2l3oclusi
àri3us.
.marihu4an
.medi3umitz
mesclan4t3aigües
.micro3inform
.micro3instr
.mi4l3engran
.mi4l3eurist
mon4t3agut
mon4t3esquiuen
qui3ue
mon4t3oliuen
mon4t3oriol
mon4t3roi
na3hu4a
.n4g4ai
.na4p3icol
.neo3impr
.nàhu4atl
9ni4etz3s4che9
9ni4etz3s4chi9
òni3us.
.nor4d3est
.nor4d3oest
.no4s3altres.
.o4i3oi.
.osco3umbr
.o4b3liter
.o4b3rep
.orto3g4neis
.o4t3àlg
.oxi3uroïdeus
.palim3p4sest
.pa4n3afric
.pa4n3americ
.pa4n3arab
.pa4n3àrab
.pa4n3arteritis
.pa4n3aten
.pa4n3esla
.pa4n3icogr
.pa4n3isl
.pa4n3oft
.pa4n3òptic
.para3g4neis
.para3p4neum
.para3p4sori
.pe4chblend
.pe4ll3obr
.pe4r3alt
.pe4r3equaci
.pe4r3or
.pe4r3oxi
.pe4r3oxo
.pe4r3òxid
.pesa3infant
.pirido3indole
.poise4uille
.poli3i
.poli3u
.pos4t3abd
.pos4t3accel
.pos4t3alveo
.pos4t3apocal
.pos4t3enc
.pos4t3impr
.pos4t3oper
.pos4t3esquí
.primo3infec
.pro3indiv
.pro3insul
.proto3u
.quasi3usdefruit
pseudo3t4sug
.rada4r3astr
.radio3i
.radi3um
.raja3s4t4hani
.re3i
.re4inesenc
.re4inesenq
.re4i.
.re4is.
.re4ina.
.re4ines.
.re4ineta.
.re4inetes.
.re4ids.
.re4ig.
.re4igs.
.re4iter.
.re4iters.
.re4ix
.retro3inhi
.reu4chlini
.re3un
re3unió.
re3unions.
.ri3c4ket3t4si
.ri3c4kèt3t4si
.ri3s4h
.ru3t4her
.ru4r1urb
.r4wand
.sacro3i
.s4che4elit
.s4ch4watzit
.semi3u
òle3us.
.sobre3i
.sot4s3
.sot5s4obr
ísqui3um.
àqui3um.
.su4ahili
.su2b3
.su3b4irac
.su3b4lev
.su3b4lim
.su4b5liminar
.su3b4ordina
.su3b4orn
.su4b4s3t
.su4b4s3c
.sú3b4er
.su3b4er
.su3b4èric
.su3b4eritza
.su3b4ula
.supe5r4.
.supe5r4a.
.supe5r4ada.
.supe5r4ades.
.supe5r4am.
.supe5r4ant.
.supe5r4ar.
.supe5r4ara.
.supe5r4aran.
.supe5r4arem.
.supe5r4aren.
.supe5r4ares.
.supe5r4areu.
.supe5r4aria.
.supe5r4arien.
.supe5r4aries.
.supe5r4arà.
.supe5r4aràs.
.supe5r4aré.
.supe5r4aríem.
.supe5r4aríeu.
.supe5r4assen.
.supe5r4asses.
.supe5r4assin.
.supe5r4assis.
.supe5r4at.
.supe5r4ats.
.supe5r4au.
.supe5r4ava.
.supe5r4aven.
.supe5r4aves.
.supe5r4e.
.supe5r4em.
.supe5r4en.
.supe5r4es.
.supe5r4essen.
.supe5r4esses.
.supe5r4essin.
.supe5r4essis.
.supe5r4eu.
.supe5r4i.
.supe5r4in.
.supe5r4is.
.supe5r4o.
.supe5r4à.
.supe5r4àrem.
.supe5r4àreu.
.supe5r4às.
.supe5r4àssem.
.supe5r4àsseu.
.supe5r4àssim.
.supe5r4àssiu.
.supe5r4àvem.
.supe5r4àveu.
.supe5r4és.
.supe5r4éssem.
.supe5r4ésseu.
.supe5r4éssim.
.supe5r4éssiu.
.supe5r4í.
supe5r4ació
supe5r4acions
supe5r4ior
supe5r4able
supe5r4abilitat
supe5r4àvit
supe6r6stici
supe6r6b.
supe6r6bs.
supe6r6strat
.supe5r4oexterior
.supe5r4olateral
.supe5r4oanterior
.supe5r4oinferior
.supe5r4oposterior
.supe5r4omedi
.supe5r4o-
.supe4r3
.talla3ungl
.pinta3ungl
.taqui3úri
è3um.
è3ums.
.te3k4rur
.tele3i
.termohipe4r3alg
.termohipe4r3est
.termoi3ònic
.tio3indi
.to4t3estiu
.tran4s3a
.tran4s3e
.tran4s3il·
.tran4s3o
.tran4s3u
.trieti4l3alumini
.triqui3uroïdeus
.tri3umvir
.txib3t4x
-t4se
.u3ís.
uki1yo
.vol4t3amper
.vo4s3altres
vete4s3ifils
vis4t3iplau
vo1yeur
.wa3s4hing
.wit4h3erit
wel1wítsqui
xi1itake
.za1in.
1b4w
1impressor
1impressi
1imprim
1incompatib
1industrial
1indústri
1informa
1informe
1informi
1informà
1informé
1inscripci
1inscriu
1interpret
1itàli
1urbà.
1urbans.
1urbanes.
1urbana.
1urbanitz
1usuari
1usuàri
1uterin
1uterí
1utilitz
.ta4ll3oil
kinde4r3s4cout
o4uija
o4uijes
tai3t4xi3t4xu4an
tai3t4xí
.a4equo.
.ca3t4hedra.
mal3t4hus
wa4re.
wa4res.
.fo4ie.
.ga4me.
.ga4mes.
.ha4s4h3ing
.ket4ch.
.ket4chs.
kirs4ch
afrika4ans
.a4l3legro
.baudelai4re.
.bob3s4leigh
.bo4om
.boî4te
brid4ge
by4te
char4les
co4l3la4ge
contai4n3er
conver4t3er
cra4c4k3ing
.fondu4e
.lu4ge.
.lu4ges.
.ma4n3a4gement
.minet4te
mozzare4l3l
.rati4o.
.rati4os.
mena4ge
sur4f3ing.
-se4ller.
-se4llers.
su3s4hi
.b4ro4adway.
.dic8k9ens
.wi4l3li4am
.feng9s8hui
ho8oligan
rockabi8l9ly
rockabi8l9li8es
thri8l9ler
vinta8ge
.bre8cht
.hit8chcock
we8alth
bo8ok
fa8cebook
fu8erteventura
go8ogle
lou9v8re
monte9r8rey
o8h8i8o
ovi8edo
ra9s8hid
rey9k8javík
ro8osevelt
1t8wi8t9ter
1t8w8e8et
unico8de
.v8la
.v8ra
yaho8o
.a8l9len.
debus9sy
gan9d8hi
rousse8au
9s8ha8ke9s8pe8a8r8e.
9s8ha8ke9s8pe8a8r9i
fi8eld
.o9k8lahoma
orwe8l9li
1ña 1ñe 3ñi 1ño 1ñu
1ñá 1ñé 3ñí 1ñó 1ñú
1ñà 1ñè 1ñò
1ya 1ye 1yi 1yo 1yu
1yá 1yé 1yí 1yó 1yú
1yà 1yè 1yò
l2yita.
1b2ya 1b2ye 1b2yi 1b2yo 1b2yu
1v2la 1v2le 1v2li 1v2lo 1v2lu
1v2ra 1v2re 1v2ri 1v2ro 1v2ru
1c2ha 1c2he 1c2hi 1c2ho 1c2hu
1k2ha 1k2he 1k2hi 1k2ho 1k2hu
1k2hé
1l2ha 1l2he 1l2hi 1l2ho 1l2hu
1n2ha 1n2he 1n2hi 1n2ho 1n2hu
1p2ha 1p2he 1p2hi 1p2ho 1p2hu
1t2ha 1t2he 1t2hi 1t2ho 1t2hu
1t2hò
1s2ha 1s2he 1s2hi 1s2ho 1s2hu
1z2ha 1z2he 1z2hi 1z2ho 1z2hu
.ale2s3hor
.a2l3hora
a2n3hedon
a2n3hel
2n3hidr
2s3hidr
2l3hidr
2z3hidr
2n3habil
2n3hàbil
2s3habil
2s3hàbil
2n3habit
2s3habit
2s3harmon
2s3harmòn
2n3harmon
2n3harmòn
2l3harmon
2l3harmòn
2n3hist
2s3hipo
2n3hipo
2l3hipo
.a2n3hipn
.a2n3hist
.be2n3haja
.ma2l3haja
.be2n3hage
.ma2l3hage
.bo2n3homi
.bi2l3harz
.brei2t3haupt
de2s3herb
de2s3heret
de2s3hipotec
de2s3honest
de2s3honor
de2s3honr
de2s3humanitz
.de2s3hor
.dre2t3havent
e2n3herb
.e2n3horabon
fi2l3hel
.genti2l3home
.genti2l3hòmen
i2n3heren
i2n3herèn
i2n3hibi
i2n3honest
i2n3hospital
i2n3hal
i2n3hum
co2n3hort
ma2l3humor
male2s3herb
ma2l3herb
be2n3humor
.me2n3hir
.mi2l3home
.mi2l3hòme
.tran2s3humà
.tran2s3huma
.to2t3hom
.to2t3hor
.para2t3hormon
.wi2th1erit
.ca2p3huit
.ste2p3hanià.
.ste2p3hanian
l·1l2y3i
2yita.
a3yita.
e3yita.
i3yita.
o3yita.
u3yita.
y1ïta.
ü3ï
ch2r
.agú3a
.agú3o
.agú3u
.agú3e
.agu3a
.agü3e
.agü3i
.agu3o
.agu3à
.agü3í
.agu3ï
.agü3é
-agú3a
-agú3o
-agú3u
-agú3e
-agu3a
-agü3e
-agü3i
-agu3o
-agu3à
-agü3í
-agü3é
.agu4ant
-agu4ant
.agu4ait
-agu4ait
""")

exceptions = ""

hyphenator = Hyphenator(patterns, exceptions)
hyphenate_word = hyphenator.hyphenate_word

del patterns
del exceptions



class Syllabes():

    def get_count(self, text):
        words = hyphenate_word(text)
        return len(words)
