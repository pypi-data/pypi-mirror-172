# -*- encoding: utf-8 -*-
#
#
# Copyright (C) 2002-2012, 2021 Jörg Lehmann <joerg@pyx-project.org>
# Copyright (C) 2003-2006 Michael Schindler <m-schindler@users.sourceforge.net>
# Copyright (C) 2002-2012 André Wobst <wobsta@pyx-project.org>
#
# This file is part of PyX (https://pyx-project.org/).
#
# PyX is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PyX is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PyX; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import math
from . import attr, unit

#
# base classes for stroke and fill styles
#

class style:
    pass

class strokestyle(style):
    pass

class fillstyle(style):
    pass

#
# common stroke styles
#


class linecap(attr.exclusiveattr, strokestyle):

    """linecap of paths"""

    def __init__(self, value=0):
        attr.exclusiveattr.__init__(self, linecap)
        self.value = value

    def __eq__(self, other):
        return self.value == other.value if isinstance(other, self.__class__) else NotImplemented

    def processPS(self, file, writer, context, registry):
        file.write("%d setlinecap\n" % self.value)

    def processPDF(self, file, writer, context, registry):
        file.write("%d J\n" % self.value)

    def processSVGattrs(self, attrs, writer, context, registry):
        attrs["stroke-linecap"] = {0: "butt", 1: "round", 2: "square"}[self.value]


linecap.butt = linecap(0)
linecap.round = linecap(1)
linecap.square = linecap(2)
linecap.clear = attr.clearclass(linecap)


class linejoin(attr.exclusiveattr, strokestyle):

    """linejoin of paths"""

    def __init__(self, value=0):
        attr.exclusiveattr.__init__(self, linejoin)
        self.value = value

    def __eq__(self, other):
        return self.value == other.value if isinstance(other, self.__class__) else NotImplemented

    def processPS(self, file, writer, context, registry):
        file.write("%d setlinejoin\n" % self.value)

    def processPDF(self, file, writer, context, registry):
        file.write("%d j\n" % self.value)

    def processSVGattrs(self, attrs, writer, context, registry):
        attrs["stroke-linejoin"] = {0: "miter", 1: "round", 2: "bevel"}[self.value]

linejoin.miter = linejoin(0)
linejoin.round = linejoin(1)
linejoin.bevel = linejoin(2)
linejoin.clear = attr.clearclass(linejoin)


class miterlimit(attr.exclusiveattr, strokestyle):

    """miterlimit of paths"""

    def __init__(self, value=10.0):
        attr.exclusiveattr.__init__(self, miterlimit)
        self.value = value

    def __eq__(self, other):
        return self.value == other.value if isinstance(other, self.__class__) else NotImplemented

    def processPS(self, file, writer, context, registry):
        file.write("%f setmiterlimit\n" % self.value)

    def processPDF(self, file, writer, context, registry):
        file.write("%f M\n" % self.value)

    def processSVGattrs(self, attrs, writer, context, registry):
        attrs["stroke-miterlimit"] = "%f" % self.value

miterlimit.lessthan180deg = miterlimit(1/math.sin(math.pi*180/360))
miterlimit.lessthan90deg = miterlimit(1/math.sin(math.pi*90/360))
miterlimit.lessthan60deg = miterlimit(1/math.sin(math.pi*60/360))
miterlimit.lessthan45deg = miterlimit(1/math.sin(math.pi*45/360))
miterlimit.lessthan11deg = miterlimit(10) # the default, approximately 11.4783 degress
miterlimit.clear = attr.clearclass(miterlimit)


_defaultlinewidth = 0.02 * unit.w_cm
_defaultlinewidth_pt = unit.topt(_defaultlinewidth)

class dash(attr.exclusiveattr, strokestyle):

    """dash of paths"""

    def __init__(self, pattern=[], offset=0, rellengths=1):
        """set pattern with offset.

        If rellengths is True, interpret all dash lengths relative to current linewidth.
        """
        attr.exclusiveattr.__init__(self, dash)
        self.pattern = pattern
        self.offset = offset
        self.rellengths = rellengths

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pattern == other.pattern and self.offset == other.offset and self.rellengths == other.rellengths
        return NotImplemented

    def processPS(self, file, writer, context, registry):
        if self.rellengths:
            patternstring = " ".join(["%f" % (element * context.linewidth_pt/_defaultlinewidth_pt) for element in self.pattern])
        else:
            patternstring = " ".join(["%f" % element for element in self.pattern])
        file.write("[%s] %f setdash\n" % (patternstring, self.offset))

    def processPDF(self, file, writer, context, registry):
        if self.rellengths:
            patternstring = " ".join(["%f" % (element * context.linewidth_pt/_defaultlinewidth_pt) for element in self.pattern])
        else:
            patternstring = " ".join(["%f" % element for element in self.pattern])
        file.write("[%s] %f d\n" % (patternstring, self.offset))

    def processSVGattrs(self, attrs, writer, context, registry):
        if self.rellengths:
            patternstring = " ".join(["%f" % (element * context.linewidth_pt/_defaultlinewidth_pt) for element in self.pattern])
        else:
            patternstring = " ".join(["%f" % element for element in self.pattern])
        if patternstring:
            attrs["stroke-dasharray"] = patternstring
            attrs["stroke-dashoffset"] = "%f" % self.offset
        else:
            attrs["stroke-dasharray"] = "none"

dash.clear = attr.clearclass(dash)


class linestyle(attr.exclusiveattr, strokestyle):

    """linestyle (linecap together with dash) of paths"""

    def __init__(self, c=linecap.butt, d=dash([])):
        # XXX better, but at the moment not supported by attr.exlusiveattr would be:
        # XXX   attr.exclusiveattr.__init__(self, [linestyle, linecap, dash])
        attr.exclusiveattr.__init__(self, linestyle)
        self.c = c
        self.d = d

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.c == other.c and self.d == other.d
        return NotImplemented

    def processPS(self, file, writer, context, registry):
        self.c.processPS(file, writer, context, registry)
        self.d.processPS(file, writer, context, registry)

    def processPDF(self, file, writer, context, registry):
        self.c.processPDF(file, writer, context, registry)
        self.d.processPDF(file, writer, context, registry)

    def processSVGattrs(self, attrs, writer, context, registry):
        self.c.processSVGattrs(attrs, writer, context, registry)
        self.d.processSVGattrs(attrs, writer, context, registry)

linestyle.solid = linestyle(linecap.butt, dash([]))
linestyle.dashed = linestyle(linecap.butt, dash([2]))
linestyle.dotted = linestyle(linecap.round, dash([0, 2]))
linestyle.dashdotted = linestyle(linecap.round, dash([0, 2, 2, 2]))
linestyle.clear = attr.clearclass(linestyle)


class linewidth(attr.sortbeforeexclusiveattr, strokestyle):

    """linewidth of paths"""

    def __init__(self, width):
        attr.sortbeforeexclusiveattr.__init__(self, linewidth, [dash, linestyle])
        self.width = width

    def __eq__(self, other):
        return self.width == other.width if isinstance(other, self.__class__) else NotImplemented

    def processPS(self, file, writer, context, registry):
        context.linewidth_pt = unit.topt(self.width)
        file.write("%f setlinewidth\n" % context.linewidth_pt)

    def processPDF(self, file, writer, context, registry):
        context.linewidth_pt = unit.topt(self.width)
        file.write("%f w\n" % context.linewidth_pt)

    def processSVGattrs(self, attrs, writer, context, registry):
        context.linewidth_pt = unit.topt(self.width)
        attrs["stroke-width"] = "%f" % context.linewidth_pt

linewidth.THIN = linewidth(_defaultlinewidth/math.sqrt(32))
linewidth.THIn = linewidth(_defaultlinewidth/math.sqrt(16))
linewidth.THin = linewidth(_defaultlinewidth/math.sqrt(8))
linewidth.Thin = linewidth(_defaultlinewidth/math.sqrt(4))
linewidth.thin = linewidth(_defaultlinewidth/math.sqrt(2))
linewidth.normal = linewidth(_defaultlinewidth)
linewidth.thick = linewidth(_defaultlinewidth*math.sqrt(2))
linewidth.Thick = linewidth(_defaultlinewidth*math.sqrt(4))
linewidth.THick = linewidth(_defaultlinewidth*math.sqrt(8))
linewidth.THIck = linewidth(_defaultlinewidth*math.sqrt(16))
linewidth.THICk = linewidth(_defaultlinewidth*math.sqrt(32))
linewidth.THICK = linewidth(_defaultlinewidth*math.sqrt(64))
linewidth.clear = attr.clearclass(linewidth)


class fillrule(attr.exclusiveattr, fillstyle):

    """defines the fill rule to be used"""

    def __init__(self, even_odd):
        attr.exclusiveattr.__init__(self, fillrule)
        self.even_odd = even_odd

    def __eq__(self, other):
        return self.even_odd == other.even_odd if isinstance(other, self.__class__) else NotImplemented

    def processPS(self, file, writer, context, registry):
        context.fillrule = self.even_odd

    def processPDF(self, file, writer, context, registry):
        context.fillrule = self.even_odd

    def processSVGattrs(self, attrs, writer, context, registry):
        attrs["fill-rule"] = {0: "nonzero", 1: "evenodd"}[self.even_odd]

fillrule.nonzero_winding = fillrule(0)
fillrule.even_odd = fillrule(1)
fillrule.clear = attr.clearclass(fillrule)
