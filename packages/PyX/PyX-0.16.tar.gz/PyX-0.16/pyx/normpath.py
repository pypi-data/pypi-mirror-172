# -*- encoding: utf-8 -*-
#
#
# Copyright (C) 2002-2011 Jörg Lehmann <joerg@pyx-project.org>
# Copyright (C) 2003-2013 Michael Schindler <m-schindler@users.sourceforge.net>
# Copyright (C) 2002-2013 André Wobst <wobsta@pyx-project.org>
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

import math, functools
from . import mathutils, trafo, unit
from . import bbox as bboxmodule


class _marker: pass

# specific exception for normpath-related problems
class NormpathException(Exception): pass

# global epsilon (default precision of normsubpaths)
_epsilon = 1e-5

def set(epsilon=None):
    global _epsilon
    if epsilon is not None:
        _epsilon = epsilon


################################################################################
# normsubpathitems
################################################################################

class normsubpathitem:

    """element of a normalized sub path

    Various operations on normsubpathitems might be subject of
    approximitions. Those methods get the finite precision epsilon,
    which is the accuracy needed expressed as a length in pts.

    normsubpathitems should never be modified inplace, since references
    might be shared between several normsubpaths.
    """

    def arclen_pt(self, epsilon, upper=False):
        """return arc length in pts

        When upper is set, the upper bound is calculated, otherwise the lower
        bound is returned."""
        pass

    def _arclentoparam_pt(self, lengths_pt, epsilon):
        """return a tuple of params and the total length arc length in pts"""
        pass

    def arclentoparam_pt(self, lengths_pt, epsilon):
        """return a tuple of params"""
        pass

    def at_pt(self, params):
        """return coordinates at params in pts"""
        pass

    def atbegin_pt(self):
        """return coordinates of first point in pts"""
        pass

    def atend_pt(self):
        """return coordinates of last point in pts"""
        pass

    def bbox(self):
        """return bounding box of normsubpathitem"""
        pass

    def cbox(self):
        """return control box of normsubpathitem

        The control box also fully encloses the normsubpathitem but in the case of a Bezier
        curve it is not the minimal box doing so. On the other hand, it is much faster
        to calculate.
        """
        pass

    def curvature_pt(self, params):
        """return the curvature at params in 1/pts"""
        pass

    def intersect(self, other, epsilon):
        """intersect self with other normsubpathitem"""
        pass

    def modifiedbegin_pt(self, x_pt, y_pt):
        """return a normsubpathitem with a modified beginning point"""
        pass

    def modifiedend_pt(self, x_pt, y_pt):
        """return a normsubpathitem with a modified end point"""
        pass

    def _paramtoarclen_pt(self, param, epsilon):
        """return a tuple of arc lengths and the total arc length in pts"""
        pass

    def pathitem(self):
        """return pathitem corresponding to normsubpathitem"""

    def reversed(self):
        """return reversed normsubpathitem"""
        pass

    def rotation(self, params):
        """return rotation trafos (i.e. trafos without translations) at params"""
        pass

    def segments(self, params):
        """return segments of the normsubpathitem

        The returned list of normsubpathitems for the segments between
        the params. params needs to contain at least two values.
        """
        pass

    def trafo(self, params):
        """return transformations at params"""

    def transformed(self, trafo):
        """return transformed normsubpathitem according to trafo"""
        pass

    def outputPS(self, file, writer):
        """write PS code corresponding to normsubpathitem to file"""
        pass

    def outputPDF(self, file, writer):
        """write PDF code corresponding to normsubpathitem to file"""
        pass

    def returnSVGdata(self, inverse_y):
        """return SVG code corresponding to normsubpathitem"""
        pass


class normline_pt(normsubpathitem):

    """Straight line from (x0_pt, y0_pt) to (x1_pt, y1_pt) (coordinates in pts)"""

    __slots__ = "x0_pt", "y0_pt", "x1_pt", "y1_pt"

    def __init__(self, x0_pt, y0_pt, x1_pt, y1_pt):
        self.x0_pt = x0_pt
        self.y0_pt = y0_pt
        self.x1_pt = x1_pt
        self.y1_pt = y1_pt

    def __str__(self):
        return "normline_pt(%g, %g, %g, %g)" % (self.x0_pt, self.y0_pt, self.x1_pt, self.y1_pt)

    def _arclentoparam_pt(self, lengths_pt, epsilon):
        # do self.arclen_pt inplace for performance reasons
        l_pt = math.hypot(self.x0_pt-self.x1_pt, self.y0_pt-self.y1_pt)
        return [length_pt/l_pt for length_pt in lengths_pt], l_pt

    def arclentoparam_pt(self, lengths_pt, epsilon):
        """return a tuple of params"""
        return self._arclentoparam_pt(lengths_pt, epsilon)[0]

    def arclen_pt(self,  epsilon, upper=False):
        return math.hypot(self.x0_pt-self.x1_pt, self.y0_pt-self.y1_pt)

    def at_pt(self, params):
        return [(self.x0_pt+(self.x1_pt-self.x0_pt)*t, self.y0_pt+(self.y1_pt-self.y0_pt)*t)
                for t in params]

    def atbegin_pt(self):
        return self.x0_pt, self.y0_pt

    def atend_pt(self):
        return self.x1_pt, self.y1_pt

    def bbox(self):
        return bboxmodule.bbox_pt(min(self.x0_pt, self.x1_pt), min(self.y0_pt, self.y1_pt),
                                  max(self.x0_pt, self.x1_pt), max(self.y0_pt, self.y1_pt))

    cbox = bbox

    def curvature_pt(self, params):
        return [0] * len(params)

    def intersect(self, other, epsilon):
        if isinstance(other, normline_pt):
            a_deltax_pt = self.x1_pt - self.x0_pt
            a_deltay_pt = self.y1_pt - self.y0_pt

            b_deltax_pt = other.x1_pt - other.x0_pt
            b_deltay_pt = other.y1_pt - other.y0_pt

            invdet = b_deltax_pt * a_deltay_pt - b_deltay_pt * a_deltax_pt

            if abs(invdet) < epsilon * epsilon:
                # As invdet measures the area spanned by the two lines, least
                # one of the lines is either very short or the lines are almost
                # parallel. In both cases, a proper colinear check is adequate,
                # already. Let's first check for short lines.
                short_self = math.hypot(self.x1_pt - self.x0_pt,
                                        self.y1_pt - self.y0_pt) < epsilon
                short_other = math.hypot(other.x1_pt - other.x0_pt,
                                         other.y1_pt - other.y0_pt) < epsilon

                # For short lines we will only take their middle point into
                # account.
                if short_self:
                    sx_pt = 0.5*(self.x0_pt + self.x1_pt)
                    sy_pt = 0.5*(self.y0_pt + self.x1_pt)
                if short_other:
                    ox_pt = 0.5*(other.x0_pt + other.x1_pt)
                    oy_pt = 0.5*(other.y0_pt + other.y1_pt)

                def closepoint(x_pt, y_pt,
                               x0_pt, y0_pt, x1_pt, y1_pt):
                    """Returns the line parameter p in range [0, 1] for which
                    the point (x_pt, y_pt) is closest to the line defined by
                    ((x0_pt, y0_pt), (x1_pt, y1_pt)). The distance of (x0_pt,
                    y0_pt) and (x1_pt, y1_pt) must be larger than epsilon. If
                    the point has a greater distance than epsilon, None is
                    returned."""
                    p = (((x0_pt - x_pt)*(x0_pt - x1_pt) +
                          (y0_pt - y_pt)*(y0_pt - y1_pt))/
                         ((x1_pt - x0_pt)**2 + (y1_pt - y0_pt)**2))
                    p = min(1, max(0, p))
                    xs_pt = x0_pt + p*(x1_pt - x0_pt)
                    ys_pt = y0_pt + p*(y1_pt - y0_pt)
                    if math.hypot(xs_pt - x_pt, ys_pt - y_pt) < epsilon:
                        return p
                    return None # just be explicit in returning None here

                if short_self and short_other:
                    # If both lines are short, we just measure the distance of
                    # the middle points.
                    if math.hypot(ox_pt - sx_pt, oy_pt - sy_pt) < epsilon:
                        return [(0.5, 0.5)]
                elif short_self:
                    p = closepoint(sx_pt, sy_pt,
                                   other.x0_pt, other.y0_pt, other.x1_pt, other.y1_pt)
                    if p is not None:
                        return [(0.5, p)]
                elif short_other:
                    p = closepoint(ox_pt, oy_pt,
                                   self.x0_pt, self.y0_pt, self.x1_pt, self.y1_pt)
                    if p is not None:
                        return [(p, 0.5)]
                else:
                    # For two long colinear lines, we need to test the
                    # beginning and end point of the two lines with respect to
                    # the other line, in all combinations. We return just one
                    # solution even when the lines intersect for a whole range.
                    p = closepoint(self.x0_pt, self.y0_pt, other.x0_pt, other.y0_pt, other.x1_pt, other.y1_pt)
                    if p is not None:
                        return [(0, p)]
                    p = closepoint(self.x1_pt, self.y1_pt, other.x0_pt, other.y0_pt, other.x1_pt, other.y1_pt)
                    if p is not None:
                        return [(1, p)]
                    p = closepoint(other.x0_pt, other.y0_pt, self.x0_pt, self.y0_pt, self.x1_pt, self.y1_pt)
                    if p is not None:
                        return [(p, 0)]
                    p = closepoint(other.x1_pt, other.y1_pt, self.x0_pt, self.y0_pt, self.x1_pt, self.y1_pt)
                    if p is not None:
                        return [(p, 1)]
                return []

            det = 1.0 / invdet

            ba_deltax0_pt = other.x0_pt - self.x0_pt
            ba_deltay0_pt = other.y0_pt - self.y0_pt

            a_t = (b_deltax_pt * ba_deltay0_pt - b_deltay_pt * ba_deltax0_pt) * det
            b_t = (a_deltax_pt * ba_deltay0_pt - a_deltay_pt * ba_deltax0_pt) * det

            # check for intersections out of bound
            if not (0<=a_t<=1 and 0<=b_t<=1):
                # correct the parameters, if the deviation is smaller than epsilon
                a_t = min(1, max(0, a_t))
                b_t = min(1, max(0, b_t))
                a_x = self.x0_pt + a_deltax_pt*a_t
                a_y = self.y0_pt + a_deltay_pt*a_t
                b_x = other.x0_pt + b_deltax_pt*b_t
                b_y = other.y0_pt + b_deltay_pt*b_t
                if math.hypot(a_x - b_x, a_y - b_y) > epsilon:
                    return []

            # return parameters of intersection
            return [(a_t, b_t)]
        else:
            return [(s_t, o_t) for o_t, s_t in other.intersect(self, epsilon)]

    def modifiedbegin_pt(self, x_pt, y_pt):
        return normline_pt(x_pt, y_pt, self.x1_pt, self.y1_pt)

    def modifiedend_pt(self, x_pt, y_pt):
        return normline_pt(self.x0_pt, self.y0_pt, x_pt, y_pt)

    def _paramtoarclen_pt(self, params, epsilon):
        totalarclen_pt = self.arclen_pt(epsilon)
        arclens_pt = [totalarclen_pt * param for param in params + [1]]
        return arclens_pt[:-1], arclens_pt[-1]

    def pathitem(self):
        from . import path
        return path.lineto_pt(self.x1_pt, self.y1_pt)

    def reversed(self):
        return normline_pt(self.x1_pt, self.y1_pt, self.x0_pt, self.y0_pt)

    def rotation(self, params):
        return [trafo.rotate(math.degrees(math.atan2(self.y1_pt-self.y0_pt, self.x1_pt-self.x0_pt)))]*len(params)

    def segments(self, params):
        if len(params) < 2:
            raise ValueError("at least two parameters needed in segments")
        result = []
        xl_pt = yl_pt = None
        for t in params:
            xr_pt = self.x0_pt + (self.x1_pt-self.x0_pt)*t
            yr_pt = self.y0_pt + (self.y1_pt-self.y0_pt)*t
            if xl_pt is not None:
                result.append(normline_pt(xl_pt, yl_pt, xr_pt, yr_pt))
            xl_pt = xr_pt
            yl_pt = yr_pt
        return result

    def trafo(self, params):
        rotate = trafo.rotate(math.degrees(math.atan2(self.y1_pt-self.y0_pt, self.x1_pt-self.x0_pt)))
        return [trafo.translate_pt(*at_pt) * rotate
                for param, at_pt in zip(params, self.at_pt(params))]

    def transformed(self, trafo):
        return normline_pt(*(trafo.apply_pt(self.x0_pt, self.y0_pt) + trafo.apply_pt(self.x1_pt, self.y1_pt)))

    def outputPS(self, file, writer):
        file.write("%g %g lineto\n" % (self.x1_pt, self.y1_pt))

    def outputPDF(self, file, writer):
        file.write("%f %f l\n" % (self.x1_pt, self.y1_pt))

    def returnSVGdata(self, inverse_y):
        if inverse_y:
            return "L%g %g" % (self.x1_pt, -self.y1_pt)
        return "L%g %g" % (self.x1_pt, self.y1_pt)


class normcurve_pt(normsubpathitem):

    """Bezier curve with control points x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt (coordinates in pts)"""

    __slots__ = "x0_pt", "y0_pt", "x1_pt", "y1_pt", "x2_pt", "y2_pt", "x3_pt", "y3_pt"

    def __init__(self, x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt):
        self.x0_pt = x0_pt
        self.y0_pt = y0_pt
        self.x1_pt = x1_pt
        self.y1_pt = y1_pt
        self.x2_pt = x2_pt
        self.y2_pt = y2_pt
        self.x3_pt = x3_pt
        self.y3_pt = y3_pt

    def __str__(self):
        return "normcurve_pt(%g, %g, %g, %g, %g, %g, %g, %g)" % (self.x0_pt, self.y0_pt, self.x1_pt, self.y1_pt,
                                                                 self.x2_pt, self.y2_pt, self.x3_pt, self.y3_pt)

    def _split(self, t=0.5, epsilon=None, intersect=False):
        """Split curve into two parts

        The splitting point is defined by the parameter t (in range 0 to 1).
        When epsilon is None, the two resulting curves are returned. However,
        when epsilon is set to a (small) float, the method can be used
        recursively to reduce the complexity of a problem by turning a
        normcurve_pt into several normline_pt segments. The method returns
        normcurve_pt instances only, when they are not yet straight enough to
        be replaceable by normline_pt instances. The criteria for returning a
        line instead of a curve depends on the value of the boolean intersect.
        When not set, the abort cirteria is defined by the error of the arclen
        of the curve vs. the line not being larger than epsilon. When in
        intersect mode, all points of the curve must be closer to the line than
        epsilon.
        """

        s = 1-t

        # first, we have to calculate the  midpoints between adjacent
        # control points
        x01_pt = s*self.x0_pt + t*self.x1_pt
        y01_pt = s*self.y0_pt + t*self.y1_pt
        x12_pt = s*self.x1_pt + t*self.x2_pt
        y12_pt = s*self.y1_pt + t*self.y2_pt
        x23_pt = s*self.x2_pt + t*self.x3_pt
        y23_pt = s*self.y2_pt + t*self.y3_pt

        # In the next iterative step, we need the midpoints between 01 and 12
        # and between 12 and 23
        x01_12_pt = s*x01_pt + t*x12_pt
        y01_12_pt = s*y01_pt + t*y12_pt
        x12_23_pt = s*x12_pt + t*x23_pt
        y12_23_pt = s*y12_pt + t*y23_pt

        # Finally the midpoint is given by
        xmidpoint_pt = s*x01_12_pt + t*x12_23_pt
        ymidpoint_pt = s*y01_12_pt + t*y12_23_pt

        def subcurve(x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt, newline, newcurve):
            if epsilon is None:
                return normcurve_pt(x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt)

            # Before returning the subcurve we check whether we can
            # replace it by a normline within an error of epsilon pts.
            l0_pt = math.hypot(x3_pt-x0_pt, y3_pt-y0_pt)
            l1_pt = math.hypot(x1_pt-x0_pt, y1_pt-y0_pt)
            l2_pt = math.hypot(x2_pt-x1_pt, y2_pt-y1_pt)
            l3_pt = math.hypot(x3_pt-x2_pt, y3_pt-y2_pt)

            # When arclen calculation is performed, the maximal error value is
            # given by the modulus of the difference between the length of the
            # control polygon (i.e. |P1-P0|+|P2-P1|+|P3-P2|), which consitutes
            # an upper bound for the length, and the length of the straight
            # line between start and end point of the normcurve (i.e. |P3-P1|),
            # which represents a lower bound.
            if not intersect and l1_pt+l2_pt+l3_pt-l0_pt < epsilon:
                # We can ignore the sign of l1_pt, l2_pt and l3_pt, as the sum
                # of the absolute values is close to l0_pt anyway.
                return newline(x0_pt, y0_pt, x3_pt, y3_pt, l1_pt, l2_pt, l3_pt)

            if intersect:
                # For intersections we calculate the distance of (x1_pt, y1_pt)
                # and (x2_pt, y2_pt) from the line defined by (x0_pt, y0_pt)
                # and (x3_pt, y3_pt). We skip the division by l0_pt in the
                # result and calculate d1_pt*l0_pt and d2_pt*l0_pt instead.
                d1_pt_times_l0_pt = (x3_pt-x0_pt)*(y0_pt-y1_pt) - (x0_pt-x1_pt)*(y3_pt-y0_pt)
                d2_pt_times_l0_pt = (x0_pt-x3_pt)*(y3_pt-y2_pt) - (x3_pt-x2_pt)*(y0_pt-y3_pt)
                if abs(d1_pt_times_l0_pt) < epsilon*l0_pt and abs(d2_pt_times_l0_pt) < epsilon*l0_pt:
                    # We could return the line now, but for this to be correct,
                    # we would need to take into account the signs of l1_pt,
                    # l2_pt, and l3_pt. In addition, this could result in
                    # multiple parameters matching a position on the line.
                    s1 = (x1_pt-x0_pt)*(x3_pt-x0_pt)+(y1_pt-y0_pt)*(y3_pt-y0_pt)
                    s2 = (x2_pt-x1_pt)*(x3_pt-x0_pt)+(y2_pt-y1_pt)*(y3_pt-y0_pt)
                    s3 = (x2_pt-x3_pt)*(x0_pt-x3_pt)+(y2_pt-y3_pt)*(y0_pt-y3_pt)

                    # If the signs are negative (i.e. we have backwards
                    # directed segments in the control polygon), we can still
                    # continue, if the corresponding segment is smaller than
                    # epsilon.
                    if ((s1 > 0 or l1_pt < epsilon) and
                        (s2 > 0 or l2_pt < epsilon) and
                        (s3 > 0 or l3_pt < epsilon)):
                        # As the sign of the segments is either positive or the
                        # segments are short, we can continue with the unsigned
                        # values for the segment lengths, as for the arclen
                        # calculation.
                        return newline(x0_pt, y0_pt, x3_pt, y3_pt, l1_pt, l2_pt, l3_pt)

            return newcurve(x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt)

        return (subcurve(self.x0_pt, self.y0_pt,
                         x01_pt, y01_pt,
                         x01_12_pt, y01_12_pt,
                         xmidpoint_pt, ymidpoint_pt,
                         _leftnormline_pt, _leftnormcurve_pt),
                subcurve(xmidpoint_pt, ymidpoint_pt,
                         x12_23_pt, y12_23_pt,
                         x23_pt, y23_pt,
                         self.x3_pt, self.y3_pt,
                         _rightnormline_pt, _rightnormcurve_pt))

    def _arclentoparam_pt(self, lengths_pt, epsilon):
        a, b = self._split(epsilon=epsilon)
        params_a, arclen_a_pt = a._arclentoparam_pt(lengths_pt, 0.5*epsilon)
        params_b, arclen_b_pt = b._arclentoparam_pt([length_pt - arclen_a_pt for length_pt in lengths_pt], 0.5*epsilon)
        params = []
        for param_a, param_b, length_pt in zip(params_a, params_b, lengths_pt):
            if length_pt > arclen_a_pt:
                params.append(b.subparamtoparam(param_b))
            else:
                params.append(a.subparamtoparam(param_a))
        return params, arclen_a_pt + arclen_b_pt

    def arclentoparam_pt(self, lengths_pt, epsilon):
        """return a tuple of params"""
        return self._arclentoparam_pt(lengths_pt, epsilon)[0]

    def arclen_pt(self, epsilon, upper=False):
        a, b = self._split(epsilon=epsilon)
        return a.arclen_pt(0.5*epsilon, upper=upper) + b.arclen_pt(0.5*epsilon, upper=upper)

    def at_pt(self, params):
        return [( (-self.x0_pt+3*self.x1_pt-3*self.x2_pt+self.x3_pt)*t*t*t +
                  (3*self.x0_pt-6*self.x1_pt+3*self.x2_pt          )*t*t +
                  (-3*self.x0_pt+3*self.x1_pt                      )*t +
                  self.x0_pt,
                  (-self.y0_pt+3*self.y1_pt-3*self.y2_pt+self.y3_pt)*t*t*t +
                  (3*self.y0_pt-6*self.y1_pt+3*self.y2_pt          )*t*t +
                  (-3*self.y0_pt+3*self.y1_pt                      )*t +
                  self.y0_pt )
                for t in params]

    def atbegin_pt(self):
        return self.x0_pt, self.y0_pt

    def atend_pt(self):
        return self.x3_pt, self.y3_pt

    def bbox(self):
        from . import path
        xmin_pt, xmax_pt = path._bezierpolyrange(self.x0_pt, self.x1_pt, self.x2_pt, self.x3_pt)
        ymin_pt, ymax_pt = path._bezierpolyrange(self.y0_pt, self.y1_pt, self.y2_pt, self.y3_pt)
        return bboxmodule.bbox_pt(xmin_pt, ymin_pt, xmax_pt, ymax_pt)

    def cbox(self):
        return bboxmodule.bbox_pt(min(self.x0_pt, self.x1_pt, self.x2_pt, self.x3_pt),
                                  min(self.y0_pt, self.y1_pt, self.y2_pt, self.y3_pt),
                                  max(self.x0_pt, self.x1_pt, self.x2_pt, self.x3_pt),
                                  max(self.y0_pt, self.y1_pt, self.y2_pt, self.y3_pt))

    def curvature_pt(self, params):
        result = []
        # see notes in rotation
        approxarclen = (math.hypot(self.x1_pt-self.x0_pt, self.y1_pt-self.y0_pt) +
                        math.hypot(self.x2_pt-self.x1_pt, self.y2_pt-self.y1_pt) +
                        math.hypot(self.x3_pt-self.x2_pt, self.y3_pt-self.y2_pt))
        for param in params:
            xdot = ( 3 * (1-param)*(1-param) * (-self.x0_pt + self.x1_pt) +
                     6 * (1-param)*param * (-self.x1_pt + self.x2_pt) +
                     3 * param*param * (-self.x2_pt + self.x3_pt) )
            ydot = ( 3 * (1-param)*(1-param) * (-self.y0_pt + self.y1_pt) +
                     6 * (1-param)*param * (-self.y1_pt + self.y2_pt) +
                     3 * param*param * (-self.y2_pt + self.y3_pt) )
            xddot = ( 6 * (1-param) * (self.x0_pt - 2*self.x1_pt + self.x2_pt) +
                      6 * param * (self.x1_pt - 2*self.x2_pt + self.x3_pt) )
            yddot = ( 6 * (1-param) * (self.y0_pt - 2*self.y1_pt + self.y2_pt) +
                      6 * param * (self.y1_pt - 2*self.y2_pt + self.y3_pt) )

            hypot = math.hypot(xdot, ydot)
            result.append((xdot*yddot - ydot*xddot) / hypot**3)
        return result

    def intersect(self, other, epsilon):
        # There can be no intersection point if the control boxes do not
        # overlap. Note that we use the control box instead of the bounding
        # box here, because the former can be calculated more efficiently for
        # Bezier curves.
        if not self.cbox().enlarged_pt(epsilon).intersects(other.cbox()):
            return []
        a, b = self._split(epsilon=epsilon, intersect=True)
        # To improve the performance in the general case we alternate the
        # splitting process between the two normsubpathitems
        return ( [(a.subparamtoparam(a_t), o_t) for o_t, a_t in other.intersect(a, epsilon)] +
                 [(b.subparamtoparam(b_t), o_t) for o_t, b_t in other.intersect(b, epsilon)] )

    def modifiedbegin_pt(self, x_pt, y_pt):
        return normcurve_pt(x_pt, y_pt,
                            self.x1_pt, self.y1_pt,
                            self.x2_pt, self.y2_pt,
                            self.x3_pt, self.y3_pt)

    def modifiedend_pt(self, x_pt, y_pt):
        return normcurve_pt(self.x0_pt, self.y0_pt,
                            self.x1_pt, self.y1_pt,
                            self.x2_pt, self.y2_pt,
                            x_pt, y_pt)

    def _paramtoarclen_pt(self, params, epsilon):
        arclens_pt = [segment.arclen_pt(epsilon) for segment in self.segments([0] + list(params) + [1])]
        for i in range(1, len(arclens_pt)):
            arclens_pt[i] += arclens_pt[i-1]
        return arclens_pt[:-1], arclens_pt[-1]

    def pathitem(self):
        from . import path
        return path.curveto_pt(self.x1_pt, self.y1_pt, self.x2_pt, self.y2_pt, self.x3_pt, self.y3_pt)

    def reversed(self):
        return normcurve_pt(self.x3_pt, self.y3_pt, self.x2_pt, self.y2_pt, self.x1_pt, self.y1_pt, self.x0_pt, self.y0_pt)

    def rotation(self, params):
        result = []
        for param in params:
            tdx_pt = (3*(  -self.x0_pt+3*self.x1_pt-3*self.x2_pt+self.x3_pt)*param*param +
                      2*( 3*self.x0_pt-6*self.x1_pt+3*self.x2_pt           )*param +
                        (-3*self.x0_pt+3*self.x1_pt                        ))
            tdy_pt = (3*(  -self.y0_pt+3*self.y1_pt-3*self.y2_pt+self.y3_pt)*param*param +
                      2*( 3*self.y0_pt-6*self.y1_pt+3*self.y2_pt           )*param +
                        (-3*self.y0_pt+3*self.y1_pt                        ))
            result.append(trafo.rotate(math.degrees(math.atan2(tdy_pt, tdx_pt))))
        return result

    def segments(self, params):
        if len(params) < 2:
            raise ValueError("at least two parameters needed in segments")

        # first, we calculate the coefficients corresponding to our
        # original bezier curve. These represent a useful starting
        # point for the following change of the polynomial parameter
        a0x_pt = self.x0_pt
        a0y_pt = self.y0_pt
        a1x_pt = 3*(-self.x0_pt+self.x1_pt)
        a1y_pt = 3*(-self.y0_pt+self.y1_pt)
        a2x_pt = 3*(self.x0_pt-2*self.x1_pt+self.x2_pt)
        a2y_pt = 3*(self.y0_pt-2*self.y1_pt+self.y2_pt)
        a3x_pt = -self.x0_pt+3*(self.x1_pt-self.x2_pt)+self.x3_pt
        a3y_pt = -self.y0_pt+3*(self.y1_pt-self.y2_pt)+self.y3_pt

        result = []

        for i in range(len(params)-1):
            t1 = params[i]
            dt = params[i+1]-t1

            # [t1,t2] part
            #
            # the new coefficients of the [t1,t1+dt] part of the bezier curve
            # are then given by expanding
            #  a0 + a1*(t1+dt*u) + a2*(t1+dt*u)**2 +
            #  a3*(t1+dt*u)**3 in u, yielding
            #
            #   a0 + a1*t1 + a2*t1**2 + a3*t1**3        +
            #   ( a1 + 2*a2 + 3*a3*t1**2 )*dt    * u    +
            #   ( a2 + 3*a3*t1 )*dt**2           * u**2 +
            #   a3*dt**3                         * u**3
            #
            # from this values we obtain the new control points by inversion
            #
            # TODO: we could do this more efficiently by reusing for
            # (x0_pt, y0_pt) the control point (x3_pt, y3_pt) from the previous
            # Bezier curve

            x0_pt = a0x_pt + a1x_pt*t1 + a2x_pt*t1*t1 + a3x_pt*t1*t1*t1
            y0_pt = a0y_pt + a1y_pt*t1 + a2y_pt*t1*t1 + a3y_pt*t1*t1*t1
            x1_pt = (a1x_pt+2*a2x_pt*t1+3*a3x_pt*t1*t1)*dt/3.0 + x0_pt
            y1_pt = (a1y_pt+2*a2y_pt*t1+3*a3y_pt*t1*t1)*dt/3.0 + y0_pt
            x2_pt = (a2x_pt+3*a3x_pt*t1)*dt*dt/3.0 - x0_pt + 2*x1_pt
            y2_pt = (a2y_pt+3*a3y_pt*t1)*dt*dt/3.0 - y0_pt + 2*y1_pt
            x3_pt = a3x_pt*dt*dt*dt + x0_pt - 3*x1_pt + 3*x2_pt
            y3_pt = a3y_pt*dt*dt*dt + y0_pt - 3*y1_pt + 3*y2_pt

            result.append(normcurve_pt(x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt))

        return result

    def trafo(self, params):
        result = []
        for rotation, at_pt in zip(self.rotation(params), self.at_pt(params)):
            result.append(trafo.translate_pt(*at_pt) * rotation)
        return result

    def transformed(self, trafo):
        x0_pt, y0_pt = trafo.apply_pt(self.x0_pt, self.y0_pt)
        x1_pt, y1_pt = trafo.apply_pt(self.x1_pt, self.y1_pt)
        x2_pt, y2_pt = trafo.apply_pt(self.x2_pt, self.y2_pt)
        x3_pt, y3_pt = trafo.apply_pt(self.x3_pt, self.y3_pt)
        return normcurve_pt(x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt)

    def outputPS(self, file, writer):
        file.write("%g %g %g %g %g %g curveto\n" % (self.x1_pt, self.y1_pt, self.x2_pt, self.y2_pt, self.x3_pt, self.y3_pt))

    def outputPDF(self, file, writer):
        file.write("%f %f %f %f %f %f c\n" % (self.x1_pt, self.y1_pt, self.x2_pt, self.y2_pt, self.x3_pt, self.y3_pt))

    def returnSVGdata(self, inverse_y):
        if inverse_y:
            return "C%g %g %g %g %g %g" % (self.x1_pt, -self.y1_pt, self.x2_pt, -self.y2_pt, self.x3_pt, -self.y3_pt)
        return "C%g %g %g %g %g %g" % (self.x1_pt, self.y1_pt, self.x2_pt, self.y2_pt, self.x3_pt, self.y3_pt)

    def x_pt(self, t):
        return (((  self.x3_pt-3*self.x2_pt+3*self.x1_pt-self.x0_pt)*t +
                  3*self.x0_pt-6*self.x1_pt+3*self.x2_pt)*t +
                  3*self.x1_pt-3*self.x0_pt)*t + self.x0_pt

    def xdot_pt(self, t):
        return ((3*self.x3_pt-9*self.x2_pt+9*self.x1_pt-3*self.x0_pt)*t +
                 6*self.x0_pt-12*self.x1_pt+6*self.x2_pt)*t + 3*self.x1_pt - 3*self.x0_pt

    def xddot_pt(self, t):
        return (6*self.x3_pt-18*self.x2_pt+18*self.x1_pt-6*self.x0_pt)*t + 6*self.x0_pt - 12*self.x1_pt + 6*self.x2_pt

    def xdddot_pt(self, t):
        return 6*self.x3_pt-18*self.x2_pt+18*self.x1_pt-6*self.x0_pt

    def y_pt(self, t):
        return (((  self.y3_pt-3*self.y2_pt+3*self.y1_pt-self.y0_pt)*t +
                  3*self.y0_pt-6*self.y1_pt+3*self.y2_pt)*t +
                  3*self.y1_pt-3*self.y0_pt)*t + self.y0_pt

    def ydot_pt(self, t):
        return ((3*self.y3_pt-9*self.y2_pt+9*self.y1_pt-3*self.y0_pt)*t +
                 6*self.y0_pt-12*self.y1_pt+6*self.y2_pt)*t + 3*self.y1_pt - 3*self.y0_pt

    def yddot_pt(self, t):
        return (6*self.y3_pt-18*self.y2_pt+18*self.y1_pt-6*self.y0_pt)*t + 6*self.y0_pt - 12*self.y1_pt + 6*self.y2_pt

    def ydddot_pt(self, t):
        return 6*self.y3_pt-18*self.y2_pt+18*self.y1_pt-6*self.y0_pt


# curve replacements used by midpointsplit:
# The replacements are normline_pt and normcurve_pt instances with an
# additional subparamtoparam function for proper conversion of the
# parametrization. Note that we only one direction (when a parameter
# gets calculated), since the other way around direction midpointsplit
# is not needed at all

class _leftnormline_pt(normline_pt):

    __slots__ = "x0_pt", "y0_pt", "x1_pt", "y1_pt", "l1_pt", "l2_pt", "l3_pt"

    def __init__(self, x0_pt, y0_pt, x1_pt, y1_pt, l1_pt, l2_pt, l3_pt):
        normline_pt.__init__(self, x0_pt, y0_pt, x1_pt, y1_pt)
        self.l1_pt = l1_pt
        self.l2_pt = l2_pt
        self.l3_pt = l3_pt

    def arclen_pt(self,  epsilon, upper=False):
        if upper:
            return self.l1_pt + self.l2_pt + self.l3_pt
        else:
            return math.hypot(self.x0_pt-self.x1_pt, self.y0_pt-self.y1_pt)

    def subparamtoparam(self, param):
        if 0 <= param <= 1:
            params = mathutils.realpolyroots(self.l1_pt-2*self.l2_pt+self.l3_pt,
                                             -3*self.l1_pt+3*self.l2_pt,
                                             3*self.l1_pt,
                                             -param*(self.l1_pt+self.l2_pt+self.l3_pt))
            # we might get several solutions and choose the one closest to 0.5
            # (we want the solution to be in the range 0 <= param <= 1; in case
            # we get several solutions in this range, they all will be close to
            # each other since l1_pt+l2_pt+l3_pt-l0_pt < epsilon)
            params.sort(key=lambda t: abs(t-0.5))
            return 0.5*params[0]
        else:
            # when we are outside the proper parameter range, we skip the non-linear
            # transformation, since it becomes slow and it might even start to be
            # numerically instable
            return 0.5*param


class _rightnormline_pt(_leftnormline_pt):

    __slots__ = "x0_pt", "y0_pt", "x1_pt", "y1_pt", "l1_pt", "l2_pt", "l3_pt"

    def subparamtoparam(self, param):
        return 0.5+_leftnormline_pt.subparamtoparam(self, param)


class _leftnormcurve_pt(normcurve_pt):

    __slots__ = "x0_pt", "y0_pt", "x1_pt", "y1_pt", "x2_pt", "y2_pt", "x3_pt", "y3_pt"

    def subparamtoparam(self, param):
        return 0.5*param


class _rightnormcurve_pt(normcurve_pt):

    __slots__ = "x0_pt", "y0_pt", "x1_pt", "y1_pt", "x2_pt", "y2_pt", "x3_pt", "y3_pt"

    def subparamtoparam(self, param):
        return 0.5+0.5*param


################################################################################
# normsubpath
################################################################################

class normsubpath:

    """sub path of a normalized path

    A subpath consists of a list of normsubpathitems, i.e., normlines_pt and
    normcurves_pt and can either be closed or not.

    Some invariants, which have to be obeyed:
    - All normsubpathitems have to be longer than epsilon pts.
    - At the end there may be a normline (stored in self.skippedline) whose
      length is shorter than epsilon -- it has to be taken into account
      when adding further normsubpathitems
    - The last point of a normsubpathitem and the first point of the next
      element have to be equal.
    - When the path is closed, the last point of last normsubpathitem has
      to be equal to the first point of the first normsubpathitem.
    - epsilon might be none, disallowing any numerics, but allowing for
      arbitrary short paths. This is used in pdf output, where all paths need
      to be transformed to normpaths.
    """

    __slots__ = "normsubpathitems", "closed", "epsilon", "skippedline"

    def __init__(self, normsubpathitems=[], closed=0, epsilon=_marker):
        """construct a normsubpath"""
        if epsilon is _marker:
            epsilon = _epsilon
        self.epsilon = epsilon
        # If one or more items appended to the normsubpath have been
        # skipped (because their total length was shorter than epsilon),
        # we remember this fact by a line because we have to take it
        # properly into account when appending further normsubpathitems
        self.skippedline = None

        self.normsubpathitems = []
        self.closed = 0

        # a test (might be temporary)
        for anormsubpathitem in normsubpathitems:
            assert isinstance(anormsubpathitem, normsubpathitem), "only list of normsubpathitem instances allowed"

        self.extend(normsubpathitems)

        if closed:
            self.close()

    def __getitem__(self, i):
        """return normsubpathitem i"""
        return self.normsubpathitems[i]

    def __len__(self):
        """return number of normsubpathitems"""
        return len(self.normsubpathitems)

    def __str__(self):
        l = ", ".join(map(str, self.normsubpathitems))
        if self.closed:
            return "normsubpath([%s], closed=1)" % l
        else:
            return "normsubpath([%s])" % l

    def _distributeparams(self, params):
        """return a dictionary mapping normsubpathitemindices to a tuple
        of a paramindices and normsubpathitemparams.

        normsubpathitemindex specifies a normsubpathitem containing
        one or several positions.  paramindex specify the index of the
        param in the original list and normsubpathitemparam is the
        parameter value in the normsubpathitem.
        """

        result = {}
        for i, param in enumerate(params):
            if param > 0:
                index = int(param)
                if index > len(self.normsubpathitems) - 1:
                    index = len(self.normsubpathitems) - 1
            else:
                index = 0
            result.setdefault(index, ([], []))
            result[index][0].append(i)
            result[index][1].append(param - index)
        return result

    def append(self, anormsubpathitem):
        """append normsubpathitem

        Fails on closed normsubpath.
        """
        if self.epsilon is None:
            self.normsubpathitems.append(anormsubpathitem)
        else:
            # consitency tests (might be temporary)
            assert isinstance(anormsubpathitem, normsubpathitem), "only normsubpathitem instances allowed"
            if self.skippedline:
                assert math.hypot(*[x-y for x, y in zip(self.skippedline.atend_pt(), anormsubpathitem.atbegin_pt())]) < self.epsilon, "normsubpathitems do not match"
            elif self.normsubpathitems:
                assert math.hypot(*[x-y for x, y in zip(self.normsubpathitems[-1].atend_pt(), anormsubpathitem.atbegin_pt())]) < self.epsilon, "normsubpathitems do not match"

            if self.closed:
                raise NormpathException("Cannot append to closed normsubpath")

            if self.skippedline:
                anormsubpathitem = anormsubpathitem.modifiedbegin_pt(*self.skippedline.atbegin_pt())
                self.skippedline = None

            if isinstance(anormsubpathitem, normline_pt):
                if math.hypot(anormsubpathitem.x1_pt-anormsubpathitem.x0_pt, anormsubpathitem.y1_pt-anormsubpathitem.y0_pt) >= self.epsilon:
                    self.normsubpathitems.append(anormsubpathitem)
                else:
                    self.skippedline = anormsubpathitem
            else:
                # it is a normcurve_pt
                x0_pt = anormsubpathitem.x0_pt
                y0_pt = anormsubpathitem.y0_pt
                x1_pt = anormsubpathitem.x1_pt
                y1_pt = anormsubpathitem.y1_pt
                x2_pt = anormsubpathitem.x2_pt
                y2_pt = anormsubpathitem.y2_pt
                x3_pt = anormsubpathitem.x3_pt
                y3_pt = anormsubpathitem.y3_pt

                l03_pt = math.hypot(x3_pt-x0_pt, y3_pt-y0_pt)
                l01_pt = math.hypot(x1_pt-x0_pt, y1_pt-y0_pt)
                l02_pt = math.hypot(x2_pt-x0_pt, y2_pt-y0_pt)
                l23_pt = math.hypot(x2_pt-x3_pt, y2_pt-y3_pt)
                l13_pt = math.hypot(x1_pt-x3_pt, y1_pt-y3_pt)

                if l03_pt >= self.epsilon or ( (l01_pt*3 >= self.epsilon or l02_pt*3 >= self.epsilon) and
                                               (l23_pt*3 >= self.epsilon or l13_pt*3 >= self.epsilon) ):
                    # We first may shift (x1_pt, y1_pt) and (x2_pt, y2_pt) to
                    # have minimal derivates at the beginning and end point.

                    # keep a copy of (x1_pt, y1_pt) for shifting (x2_pt, y2_pt)
                    x1o_pt = x1_pt
                    y1o_pt = y1_pt

                    # When repositioning the control points, use a factor 2.9
                    # instead of 3 to get a derivative above the threshold as
                    # otherwise deep recursions can occur.
                    if l01_pt*3 < self.epsilon:
                        if l02_pt*3 >= self.epsilon:
                            x1_pt = x0_pt + (x2_pt-x0_pt)*self.epsilon/l02_pt/2.9
                            y1_pt = y0_pt + (y2_pt-y0_pt)*self.epsilon/l02_pt/2.9
                        else:
                            x1_pt = x0_pt + (x3_pt-x0_pt)*self.epsilon/l03_pt/2.9
                            y1_pt = y0_pt + (y3_pt-y0_pt)*self.epsilon/l03_pt/2.9

                    if l23_pt*3 < self.epsilon:
                        if l13_pt*3 >= self.epsilon:
                            x2_pt = x3_pt + (x1o_pt-x3_pt)*self.epsilon/l13_pt/2.9
                            y2_pt = y3_pt + (y1o_pt-y3_pt)*self.epsilon/l13_pt/2.9
                        else:
                            x2_pt = x3_pt + (x0_pt-x3_pt)*self.epsilon/l03_pt/2.9
                            y2_pt = y3_pt + (y0_pt-y3_pt)*self.epsilon/l03_pt/2.9

                    newitems = [normcurve_pt(x0_pt, y0_pt, x1_pt, y1_pt, x2_pt, y2_pt, x3_pt, y3_pt)]

                    # find extrema of the derivative
                    ax = x3_pt - 3*x2_pt + 3*x1_pt - x0_pt
                    bx = 2*x0_pt - 4*x1_pt + 2*x2_pt
                    cx = x1_pt - x0_pt
                    ay = y3_pt - 3*y2_pt + 3*y1_pt - y0_pt
                    by = 2*y0_pt - 4*y1_pt + 2*y2_pt
                    cy = y1_pt - y0_pt
                    roots = mathutils.realpolyroots(4*ax*ax + 4*ay*ay, 6*ax*bx + 6*ay*by, 4*ax*cx + 4*ay*cy + 2*bx*bx + 2*by*by, 2*bx*cx + 2*by*cy)

                    # split at points of too small derivative
                    splitpoints = [t for t in roots if 0 < t < 1 and 9*((ax*t*t+bx*t+cx)**2+(ay*t*t+by*t+cy)**2) < self.epsilon*self.epsilon]
                    if not splitpoints:
                        self.normsubpathitems.extend(newitems)
                    else:
                        splitpoints.sort()
                        for i, splitpoint in enumerate(splitpoints):
                            if i:
                                # take splitpoint relative to the subcurve
                                splitpoint = (splitpoint-splitpoints[i-1])/(1-splitpoints[i-1])
                            newitems.extend(newitems.pop()._split(splitpoint))

                        # Replace short curves by lines. Otherwise skippedline
                        # could shake up the short curve completely.
                        for i in range(len(newitems)):
                            l01_pt = math.hypot(newitems[i].x1_pt-newitems[i].x0_pt, newitems[i].y1_pt-newitems[i].y0_pt)
                            l12_pt = math.hypot(newitems[i].x2_pt-newitems[i].x1_pt, newitems[i].y2_pt-newitems[i].y1_pt)
                            l23_pt = math.hypot(newitems[i].x3_pt-newitems[i].x2_pt, newitems[i].y3_pt-newitems[i].y2_pt)
                            if l01_pt+l12_pt+l23_pt < self.epsilon:
                                newitems[i] = normline_pt(newitems[i].x0_pt, newitems[i].y0_pt, newitems[i].x3_pt, newitems[i].y3_pt)

                        self.extend(newitems)
                else:
                    self.skippedline = normline_pt(anormsubpathitem.x0_pt, anormsubpathitem.y0_pt, anormsubpathitem.x3_pt, anormsubpathitem.y3_pt)

    def arclen_pt(self, upper=False):
        """return arc length in pts

        When upper is set, the upper bound is calculated, otherwise the lower
        bound is returned."""
        return sum([npitem.arclen_pt(self.epsilon, upper=upper) for npitem in self.normsubpathitems])

    def _arclentoparam_pt(self, lengths_pt):
        """return a tuple of params and the total length arc length in pts"""
        # work on a copy which is counted down to negative values
        lengths_pt = lengths_pt[:]
        results = [None] * len(lengths_pt)

        totalarclen = 0
        for normsubpathindex, normsubpathitem in enumerate(self.normsubpathitems):
            params, arclen = normsubpathitem._arclentoparam_pt(lengths_pt, self.epsilon)
            for i in range(len(results)):
                if results[i] is None:
                    lengths_pt[i] -= arclen
                    if lengths_pt[i] < 0 or normsubpathindex == len(self.normsubpathitems) - 1:
                        # overwrite the results until the length has become negative
                        results[i] = normsubpathindex + params[i]
            totalarclen += arclen

        return results, totalarclen

    def arclentoparam_pt(self, lengths_pt):
        """return a tuple of params"""
        return self._arclentoparam_pt(lengths_pt)[0]

    def at_pt(self, params):
        """return coordinates at params in pts"""
        if not self.normsubpathitems and self.skippedline:
            return [self.skippedline.atbegin_pt()]*len(params)
        result = [None] * len(params)
        for normsubpathitemindex, (indices, params) in list(self._distributeparams(params).items()):
            for index, point_pt in zip(indices, self.normsubpathitems[normsubpathitemindex].at_pt(params)):
                result[index] = point_pt
        return result

    def atbegin_pt(self):
        """return coordinates of first point in pts"""
        if not self.normsubpathitems and self.skippedline:
            return self.skippedline.atbegin_pt()
        return self.normsubpathitems[0].atbegin_pt()

    def atend_pt(self):
        """return coordinates of last point in pts"""
        if self.skippedline:
            return self.skippedline.atend_pt()
        return self.normsubpathitems[-1].atend_pt()

    def bbox(self):
        """return bounding box of normsubpath"""
        if self.normsubpathitems:
            abbox = self.normsubpathitems[0].bbox()
            for anormpathitem in self.normsubpathitems[1:]:
                abbox += anormpathitem.bbox()
            return abbox
        else:
            return bboxmodule.empty()

    def close(self):
        """close subnormpath

        Fails on closed normsubpath.
        """
        if self.closed:
            raise NormpathException("Cannot close already closed normsubpath")
        if not self.normsubpathitems:
            if self.skippedline is None:
                raise NormpathException("Cannot close empty normsubpath")
            else:
                raise NormpathException("Normsubpath too short, cannot be closed")

        xs_pt, ys_pt = self.normsubpathitems[-1].atend_pt()
        xe_pt, ye_pt = self.normsubpathitems[0].atbegin_pt()
        self.append(normline_pt(xs_pt, ys_pt, xe_pt, ye_pt))
        self.flushskippedline()
        self.closed = 1

    def copy(self):
        """return copy of normsubpath"""
        # Since normsubpathitems are never modified inplace, we just
        # need to copy the normsubpathitems list. We do not pass the
        # normsubpathitems to the constructor to not repeat the checks
        # for minimal length of each normsubpathitem.
        result = normsubpath(epsilon=self.epsilon)
        result.normsubpathitems = self.normsubpathitems[:]
        result.closed = self.closed

        # We can share the reference to skippedline, since it is a
        # normsubpathitem as well and thus not modified in place either.
        result.skippedline = self.skippedline

        return result

    def curvature_pt(self, params):
        """return the curvature at params in 1/pts"""
        result = [None] * len(params)
        for normsubpathitemindex, (indices, params) in list(self._distributeparams(params).items()):
            for index, curvature_pt in zip(indices, self.normsubpathitems[normsubpathitemindex].curvature_pt(params)):
                result[index] = curvature_pt
        return result

    def extend(self, normsubpathitems):
        """extend path by normsubpathitems

        Fails on closed normsubpath.
        """
        for normsubpathitem in normsubpathitems:
            self.append(normsubpathitem)

    def flushskippedline(self):
        """flush the skippedline, i.e. apply it to the normsubpath

        remove the skippedline by modifying the end point of the existing normsubpath
        """
        while self.skippedline:
            try:
                lastnormsubpathitem = self.normsubpathitems.pop()
            except IndexError:
                raise ValueError("normsubpath too short to flush the skippedline")
            lastnormsubpathitem = lastnormsubpathitem.modifiedend_pt(*self.skippedline.atend_pt())
            self.skippedline = None
            self.append(lastnormsubpathitem)

    def intersect(self, other):
        """intersect self with other normsubpath

        Returns a tuple of lists consisting of the parameter values
        of the intersection points of the corresponding normsubpath.
        """
        intersections_a = []
        intersections_b = []
        epsilon = min(self.epsilon, other.epsilon)
        # Intersect all subpaths of self with the subpaths of other, possibly including
        # one intersection point several times
        for t_a, pitem_a  in enumerate(self.normsubpathitems):
            for t_b, pitem_b in enumerate(other.normsubpathitems):
                for intersection_a, intersection_b in pitem_a.intersect(pitem_b, epsilon):
                    intersections_a.append(intersection_a + t_a)
                    intersections_b.append(intersection_b + t_b)

        # although intersectipns_a are sorted for the different normsubpathitems,
        # within a normsubpathitem, the ordering has to be ensured separately:
        intersections = list(zip(intersections_a, intersections_b))
        intersections.sort()
        intersections_a = [a for a, b in intersections]
        intersections_b = [b for a, b in intersections]

        # for symmetry reasons we enumerate intersections_a as well, although
        # they are already sorted (note we do not need to sort intersections_a)
        intersections_a = list(zip(intersections_a, list(range(len(intersections_a)))))
        intersections_b = list(zip(intersections_b, list(range(len(intersections_b)))))
        intersections_b.sort()

        # now we search for intersections points which are closer together than epsilon
        # This task is handled by the following function
        def closepoints(normsubpath, intersections):
            split = normsubpath.segments([0] + [intersection for intersection, index in intersections] + [len(normsubpath)])
            result = []
            if normsubpath.closed:
                # note that the number of segments of a closed path is off by one
                # compared to an open path
                i = 0
                while i < len(split):
                    splitnormsubpath = split[i]
                    j = i
                    while not splitnormsubpath.normsubpathitems: # i.e. while "is short"
                        ip1, ip2 = intersections[i-1][1], intersections[j][1]
                        if ip1<ip2:
                            result.append((ip1, ip2))
                        else:
                            result.append((ip2, ip1))
                        j += 1
                        if j == len(split):
                            j = 0
                        if j < len(split):
                            splitnormsubpath = splitnormsubpath.joined(split[j])
                        else:
                            break
                    i += 1
            else:
                i = 1
                while i < len(split)-1:
                    splitnormsubpath = split[i]
                    j = i
                    while not splitnormsubpath.normsubpathitems: # i.e. while "is short"
                        ip1, ip2 = intersections[i-1][1], intersections[j][1]
                        if ip1<ip2:
                            result.append((ip1, ip2))
                        else:
                            result.append((ip2, ip1))
                        j += 1
                        if j < len(split)-1:
                            splitnormsubpath = splitnormsubpath.joined(split[j])
                        else:
                            break
                    i += 1
            return result

        closepoints_a = closepoints(self, intersections_a)
        closepoints_b = closepoints(other, intersections_b)

        # map intersection point to lowest point which is equivalent to the
        # point
        equivalentpoints = list(range(len(intersections_a)))

        for closepoint_a in closepoints_a:
            for closepoint_b in closepoints_b:
                if closepoint_a == closepoint_b:
                    for i in range(closepoint_a[1], len(equivalentpoints)):
                        if equivalentpoints[i] == closepoint_a[1]:
                            equivalentpoints[i] = closepoint_a[0]

        # determine the remaining intersection points
        intersectionpoints = {}
        for point in equivalentpoints:
            intersectionpoints[point] = 1

        # build result
        result = []
        intersectionpointskeys = list(intersectionpoints.keys())
        intersectionpointskeys.sort()
        for point in intersectionpointskeys:
            for intersection_a, index_a in intersections_a:
                if index_a == point:
                    result_a = intersection_a
            for intersection_b, index_b in intersections_b:
                if index_b == point:
                    result_b = intersection_b
            result.append((result_a, result_b))
        # note that the result is sorted in a, since we sorted
        # intersections_a in the very beginning

        return [x for x, y in result], [y for x, y in result]

    def join(self, other):
        """join other normsubpath inplace

        Fails on closed normsubpath. Fails to join closed normsubpath.
        """
        if other.closed:
            raise NormpathException("Cannot join closed normsubpath")

        if self.normsubpathitems:
            # insert connection line
            x0_pt, y0_pt = self.atend_pt()
            x1_pt, y1_pt = other.atbegin_pt()
            self.append(normline_pt(x0_pt, y0_pt, x1_pt, y1_pt))

        # append other normsubpathitems
        self.extend(other.normsubpathitems)
        if other.skippedline:
            self.append(other.skippedline)

    def joined(self, other):
        """return joined self and other

        Fails on closed normsubpath. Fails to join closed normsubpath.
        """
        result = self.copy()
        result.join(other)
        return result

    def _paramtoarclen_pt(self, params):
        """return a tuple of arc lengths and the total arc length in pts"""
        if not self.normsubpathitems:
            return [0] * len(params), 0
        result = [None] * len(params)
        totalarclen_pt = 0
        distributeparams = self._distributeparams(params)
        for normsubpathitemindex in range(len(self.normsubpathitems)):
            if normsubpathitemindex in distributeparams:
                indices, params = distributeparams[normsubpathitemindex]
                arclens_pt, normsubpathitemarclen_pt = self.normsubpathitems[normsubpathitemindex]._paramtoarclen_pt(params, self.epsilon)
                for index, arclen_pt in zip(indices, arclens_pt):
                    result[index] = totalarclen_pt + arclen_pt
                totalarclen_pt += normsubpathitemarclen_pt
            else:
                totalarclen_pt += self.normsubpathitems[normsubpathitemindex].arclen_pt(self.epsilon)
        return result, totalarclen_pt

    def pathitems(self):
        """return list of pathitems"""

        from . import path

        if not self.normsubpathitems:
            return []

        # remove trailing normline_pt of closed subpaths
        if self.closed and isinstance(self.normsubpathitems[-1], normline_pt):
            normsubpathitems = self.normsubpathitems[:-1]
        else:
            normsubpathitems = self.normsubpathitems

        result = [path.moveto_pt(*self.atbegin_pt())]
        for normsubpathitem in normsubpathitems:
            result.append(normsubpathitem.pathitem())
        if self.closed:
            result.append(path.closepath())
        return result

    def reversed(self):
        """return reversed normsubpath"""
        nnormpathitems = []
        for i in range(len(self.normsubpathitems)):
            nnormpathitems.append(self.normsubpathitems[-(i+1)].reversed())
        return normsubpath(nnormpathitems, self.closed, self.epsilon)

    def rotation(self, params):
        """return rotations at params"""
        result = [None] * len(params)
        for normsubpathitemindex, (indices, params) in list(self._distributeparams(params).items()):
            for index, rotation in zip(indices, self.normsubpathitems[normsubpathitemindex].rotation(params)):
                result[index] = rotation
        return result

    def segments(self, params):
        """return segments of the normsubpath

        The returned list of normsubpaths for the segments between
        the params. params need to contain at least two values.

        For a closed normsubpath the last segment result is joined to
        the first one when params starts with 0 and ends with len(self).
        or params starts with len(self) and ends with 0. Thus a segments
        operation on a closed normsubpath might properly join those the
        first and the last part to take into account the closed nature of
        the normsubpath. However, for intermediate parameters, closepath
        is not taken into account, i.e. when walking backwards you do not
        loop over the closepath forwardly. The special values 0 and
        len(self) for the first and the last parameter should be given as
        integers, i.e. no finite precision is used when checking for
        equality."""

        if len(params) < 2:
            raise ValueError("at least two parameters needed in segments")
        if not self.normsubpathitems:
            assert not self.closed # "empty" normsubpath cannot be closed
            return [self]*(len(params)-1)

        result = [normsubpath(epsilon=self.epsilon)]

        # instead of distribute the parameters, we need to keep their
        # order and collect parameters for the needed segments of
        # normsubpathitem with index collectindex
        collectparams = []
        collectindex = None
        for param in params:
            # calculate index and parameter for corresponding normsubpathitem
            if param > 0:
                index = int(param)
                if index > len(self.normsubpathitems) - 1:
                    index = len(self.normsubpathitems) - 1
                param -= index
            else:
                index = 0
            if index != collectindex:
                if collectindex is not None:
                    # append end point depening on the forthcoming index
                    if index > collectindex:
                        collectparams.append(1)
                    else:
                        collectparams.append(0)
                    # get segments of the normsubpathitem and add them to the result
                    segments = self.normsubpathitems[collectindex].segments(collectparams)
                    result[-1].append(segments[0])
                    result.extend([normsubpath([segment], epsilon=self.epsilon) for segment in segments[1:]])
                    # add normsubpathitems and first segment parameter to close the
                    # gap to the forthcoming index
                    if index > collectindex:
                        for i in range(collectindex+1, index):
                            result[-1].append(self.normsubpathitems[i])
                        collectparams = [0]
                    else:
                        for i in range(collectindex-1, index, -1):
                            result[-1].append(self.normsubpathitems[i].reversed())
                        collectparams = [1]
                collectindex = index
            collectparams.append(param)
        # add remaining collectparams to the result
        segments = self.normsubpathitems[collectindex].segments(collectparams)
        result[-1].append(segments[0])
        result.extend([normsubpath([segment], epsilon=self.epsilon) for segment in segments[1:]])

        if self.closed:
            # join last and first segment together if the normsubpath was
            # originally closed and first and the last parameters are the
            # beginning and end points of the normsubpath
            if ( ( params[0] == 0 and params[-1] == len(self.normsubpathitems) ) or
                 ( params[-1] == 0 and params[0] == len(self.normsubpathitems) ) ):
                result[-1].normsubpathitems.extend(result[0].normsubpathitems)
                result = result[-1:] + result[1:-1]

        return result

    def trafo(self, params):
        """return transformations at params"""
        result = [None] * len(params)
        for normsubpathitemindex, (indices, params) in list(self._distributeparams(params).items()):
            for index, trafo in zip(indices, self.normsubpathitems[normsubpathitemindex].trafo(params)):
                result[index] = trafo
        return result

    def transformed(self, trafo):
        """return transformed path"""
        nnormsubpath = normsubpath(epsilon=self.epsilon)
        for pitem in self.normsubpathitems:
            nnormsubpath.append(pitem.transformed(trafo))
        if self.closed:
            nnormsubpath.close()
        elif self.skippedline is not None:
            nnormsubpath.append(self.skippedline.transformed(trafo))
        return nnormsubpath

    def outputPS(self, file, writer):
        # if the normsubpath is closed, we must not output a normline at
        # the end
        if not self.normsubpathitems:
            return
        if self.closed and isinstance(self.normsubpathitems[-1], normline_pt):
            assert len(self.normsubpathitems) > 1, "a closed normsubpath should contain more than a single normline_pt"
            normsubpathitems = self.normsubpathitems[:-1]
        else:
            normsubpathitems = self.normsubpathitems
        file.write("%g %g moveto\n" % self.atbegin_pt())
        for anormsubpathitem in normsubpathitems:
            anormsubpathitem.outputPS(file, writer)
        if self.closed:
            file.write("closepath\n")

    def outputPDF(self, file, writer):
        # if the normsubpath is closed, we must not output a normline at
        # the end
        if not self.normsubpathitems:
            return
        if self.closed and isinstance(self.normsubpathitems[-1], normline_pt):
            assert len(self.normsubpathitems) > 1, "a closed normsubpath should contain more than a single normline_pt"
            normsubpathitems = self.normsubpathitems[:-1]
        else:
            normsubpathitems = self.normsubpathitems
        file.write("%f %f m\n" % self.atbegin_pt())
        for anormsubpathitem in normsubpathitems:
            anormsubpathitem.outputPDF(file, writer)
        if self.closed:
            file.write("h\n")

    def returnSVGdata(self, inverse_y):
        # if the normsubpath is closed, we must not output a normline at
        # the end
        if not self.normsubpathitems:
            return ""
        if self.closed and isinstance(self.normsubpathitems[-1], normline_pt):
            assert len(self.normsubpathitems) > 1, "a closed normsubpath should contain more than a single normline_pt"
            normsubpathitems = self.normsubpathitems[:-1]
        else:
            normsubpathitems = self.normsubpathitems
        x_pt, y_pt = self.atbegin_pt()
        if inverse_y:
            y_pt = -y_pt
        data = ["M%g %g" % (x_pt, y_pt)]
        for anormsubpathitem in normsubpathitems:
            data.append(anormsubpathitem.returnSVGdata(inverse_y))
        if self.closed:
            data.append("Z")
        return "".join(data)



################################################################################
# normpath
################################################################################

@functools.total_ordering
class normpathparam:

    """parameter of a certain point along a normpath"""

    __slots__ = "normpath", "normsubpathindex", "normsubpathparam"

    def __init__(self, normpath, normsubpathindex, normsubpathparam):
        self.normpath = normpath
        self.normsubpathindex = normsubpathindex
        self.normsubpathparam = normsubpathparam

    def __str__(self):
        return "normpathparam(%s, %s, %s)" % (self.normpath, self.normsubpathindex, self.normsubpathparam)

    def __add__(self, other):
        if isinstance(other, normpathparam):
            assert self.normpath is other.normpath, "normpathparams have to belong to the same normpath"
            return self.normpath.arclentoparam_pt(self.normpath.paramtoarclen_pt(self) +
                                                  other.normpath.paramtoarclen_pt(other))
        else:
            return self.normpath.arclentoparam_pt(self.normpath.paramtoarclen_pt(self) + unit.topt(other))

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, normpathparam):
            assert self.normpath is other.normpath, "normpathparams have to belong to the same normpath"
            return self.normpath.arclentoparam_pt(self.normpath.paramtoarclen_pt(self) -
                                                  other.normpath.paramtoarclen_pt(other))
        else:
            return self.normpath.arclentoparam_pt(self.normpath.paramtoarclen_pt(self) - unit.topt(other))

    def __rsub__(self, other):
        # other has to be a length in this case
        return self.normpath.arclentoparam_pt(-self.normpath.paramtoarclen_pt(self) + unit.topt(other))

    def __mul__(self, factor):
        return self.normpath.arclentoparam_pt(self.normpath.paramtoarclen_pt(self) * factor)

    __rmul__ = __mul__

    def __div__(self, divisor):
        return self.normpath.arclentoparam_pt(self.normpath.paramtoarclen_pt(self) / divisor)

    def __neg__(self):
        return self.normpath.arclentoparam_pt(-self.normpath.paramtoarclen_pt(self))

    def __eq__(self, other):
        if isinstance(other, normpathparam):
            assert self.normpath is other.normpath, "normpathparams have to belong to the same normpath"
            return (self.normsubpathindex, self.normsubpathparam) == (other.normsubpathindex, other.normsubpathparam)
        else:
            return self.normpath.paramtoarclen_pt(self) == unit.topt(other)

    def __lt__(self, other):
        if isinstance(other, normpathparam):
            assert self.normpath is other.normpath, "normpathparams have to belong to the same normpath"
            return (self.normsubpathindex, self.normsubpathparam) < (other.normsubpathindex, other.normsubpathparam)
        else:
            return self.normpath.paramtoarclen_pt(self) < unit.topt(other)

    def arclen_pt(self):
        """return arc length in pts corresponding to the normpathparam """
        return self.normpath.paramtoarclen_pt(self)

    def arclen(self):
        """return arc length corresponding to the normpathparam """
        return self.normpath.paramtoarclen(self)


def _valueorlistmethod(method):
    """Creates a method which takes a single argument or a list and
    returns a single value or a list out of method, which always
    works on lists."""

    @functools.wraps(method)
    def wrappedmethod(self, valueorlist, *args, **kwargs):
        try:
            for item in valueorlist:
                break
        except Exception:
            return method(self, [valueorlist], *args, **kwargs)[0]
        return method(self, valueorlist, *args, **kwargs)
    return wrappedmethod


class normpath:

    """normalized path

    A normalized path consists of a list of normsubpaths.
    """

    def __init__(self, normsubpaths=None):
        """construct a normpath from a list of normsubpaths"""

        if normsubpaths is None:
            self.normsubpaths = [] # make a fresh list
        else:
            self.normsubpaths = normsubpaths
            for subpath in normsubpaths:
                assert isinstance(subpath, normsubpath), "only list of normsubpath instances allowed"

    def __add__(self, other):
        """create new normpath out of self and other"""
        result = self.copy()
        result += other
        return result

    def __iadd__(self, other):
        """add other inplace"""
        for normsubpath in other.normpath().normsubpaths:
            self.normsubpaths.append(normsubpath.copy())
        return self

    def __getitem__(self, i):
        """return normsubpath i"""
        return self.normsubpaths[i]

    def __len__(self):
        """return the number of normsubpaths"""
        return len(self.normsubpaths)

    def __str__(self):
        return "normpath([%s])" % ", ".join(map(str, self.normsubpaths))

    def _convertparams(self, params, convertmethod):
        """return params with all non-normpathparam arguments converted by convertmethod

        usecases:
        - self._convertparams(params, self.arclentoparam_pt)
        - self._convertparams(params, self.arclentoparam)
        """

        converttoparams = []
        convertparamindices = []
        for i, param in enumerate(params):
            if not isinstance(param, normpathparam):
                converttoparams.append(param)
                convertparamindices.append(i)
        if converttoparams:
            params = params[:]
            for i, param in zip(convertparamindices, convertmethod(converttoparams)):
                params[i] = param
        return params

    def _distributeparams(self, params):
        """return a dictionary mapping subpathindices to a tuple of a paramindices and subpathparams

        subpathindex specifies a subpath containing one or several positions.
        paramindex specify the index of the normpathparam in the original list and
        subpathparam is the parameter value in the subpath.
        """

        result = {}
        for i, param in enumerate(params):
            assert param.normpath is self, "normpathparam has to belong to this path"
            result.setdefault(param.normsubpathindex, ([], []))
            result[param.normsubpathindex][0].append(i)
            result[param.normsubpathindex][1].append(param.normsubpathparam)
        return result

    def append(self, item):
        """append a normpath by a normsubpath or a pathitem"""
        from . import path
        if isinstance(item, normsubpath):
            # the normsubpaths list can be appended by a normsubpath only
            self.normsubpaths.append(item)
        elif isinstance(item, path.pathitem):
            # ... but we are kind and allow for regular path items as well
            # in order to make a normpath to behave more like a regular path
            if self.normsubpaths:
                context = path.context(*(self.normsubpaths[-1].atend_pt() +
                                         self.normsubpaths[-1].atbegin_pt()))
                item.updatenormpath(self, context)
            else:
                self.normsubpaths = item.createnormpath(self).normsubpaths

    def arclen_pt(self, upper=False):
        """return arc length in pts

        When upper is set, the upper bound is calculated, otherwise the lower
        bound is returned."""
        return sum([normsubpath.arclen_pt(upper=upper) for normsubpath in self.normsubpaths])

    def arclen(self, upper=False):
        """return arc length

        When upper is set, the upper bound is calculated, otherwise the lower
        bound is returned."""
        return self.arclen_pt(upper=upper) * unit.t_pt

    def _arclentoparam_pt(self, lengths_pt):
        """return the params matching the given lengths_pt"""
        # work on a copy which is counted down to negative values
        lengths_pt = lengths_pt[:]
        results = [None] * len(lengths_pt)

        for normsubpathindex, normsubpath in enumerate(self.normsubpaths):
            params, arclen = normsubpath._arclentoparam_pt(lengths_pt)
            done = 1
            for i, result in enumerate(results):
                if results[i] is None:
                    lengths_pt[i] -= arclen
                    if lengths_pt[i] < 0 or normsubpathindex == len(self.normsubpaths) - 1:
                        # overwrite the results until the length has become negative
                        results[i] = normpathparam(self, normsubpathindex, params[i])
                    done = 0
            if done:
                break

        return results

    arclentoparam_pt = _valueorlistmethod(_arclentoparam_pt)

    @_valueorlistmethod
    def arclentoparam(self, lengths):
        """return the param(s) matching the given length(s)"""
        return self._arclentoparam_pt([unit.topt(l) for l in lengths])

    def _at_pt(self, params):
        """return coordinates of normpath in pts at params"""
        result = [None] * len(params)
        for normsubpathindex, (indices, params) in list(self._distributeparams(params).items()):
            for index, point_pt in zip(indices, self.normsubpaths[normsubpathindex].at_pt(params)):
                result[index] = point_pt
        return result

    @_valueorlistmethod
    def at_pt(self, params):
        """return coordinates of normpath in pts at param(s) or lengths in pts"""
        return self._at_pt(self._convertparams(params, self.arclentoparam_pt))

    @_valueorlistmethod
    def at(self, params):
        """return coordinates of normpath at param(s) or arc lengths"""
        return [(x_pt * unit.t_pt, y_pt * unit.t_pt)
                for x_pt, y_pt in self._at_pt(self._convertparams(params, self.arclentoparam))]

    def atbegin_pt(self):
        """return coordinates of the beginning of first subpath in normpath in pts"""
        if self.normsubpaths:
            return self.normsubpaths[0].atbegin_pt()
        else:
            raise NormpathException("cannot return first point of empty path")

    def atbegin(self):
        """return coordinates of the beginning of first subpath in normpath"""
        x, y = self.atbegin_pt()
        return x * unit.t_pt, y * unit.t_pt

    def atend_pt(self):
        """return coordinates of the end of last subpath in normpath in pts"""
        if self.normsubpaths:
            return self.normsubpaths[-1].atend_pt()
        else:
            raise NormpathException("cannot return last point of empty path")

    def atend(self):
        """return coordinates of the end of last subpath in normpath"""
        x, y = self.atend_pt()
        return x * unit.t_pt, y * unit.t_pt

    def bbox(self):
        """return bbox of normpath"""
        abbox = bboxmodule.empty()
        for normsubpath in self.normsubpaths:
            abbox += normsubpath.bbox()
        return abbox

    def begin(self):
        """return param corresponding of the beginning of the normpath"""
        if self.normsubpaths:
            return normpathparam(self, 0, 0)
        else:
            raise NormpathException("empty path")

    def copy(self):
        """return copy of normpath"""
        result = normpath()
        for normsubpath in self.normsubpaths:
            result.append(normsubpath.copy())
        return result

    @_valueorlistmethod
    def curvature_pt(self, params):
        """return the curvature in 1/pt at params or arc length(s) in pts"""

        result = [None] * len(params)
        for normsubpathindex, (indices, params) in list(self._distributeparams(self._convertparams(params, self.arclentoparam_pt)).items()):
            for index, curvature_pt in zip(indices, self.normsubpaths[normsubpathindex].curvature_pt(params)):
                result[index] = curvature_pt
        return result

    def end(self):
        """return param corresponding of the end of the path"""
        if self.normsubpaths:
            return normpathparam(self, len(self)-1, len(self.normsubpaths[-1]))
        else:
            raise NormpathException("empty path")

    def extend(self, normsubpaths):
        """extend path by normsubpaths or pathitems"""
        for anormsubpath in normsubpaths:
            # use append to properly handle regular path items as well as normsubpaths
            self.append(anormsubpath)

    def intersect(self, other):
        """intersect self with other path

        Returns a tuple of lists consisting of the parameter values
        of the intersection points of the corresponding normpath.
        """
        other = other.normpath()

        # here we build up the result
        intersections = ([], [])

        # Intersect all normsubpaths of self with the normsubpaths of
        # other.
        for ia, normsubpath_a in enumerate(self.normsubpaths):
            for ib, normsubpath_b in enumerate(other.normsubpaths):
                for intersection in zip(*normsubpath_a.intersect(normsubpath_b)):
                    intersections[0].append(normpathparam(self, ia, intersection[0]))
                    intersections[1].append(normpathparam(other, ib, intersection[1]))
        return intersections

    def join(self, other):
        """join other normsubpath inplace

        Both normpaths must contain at least one normsubpath.
        The last normsubpath of self will be joined to the first
        normsubpath of other.
        """
        other = other.normpath()

        if not self.normsubpaths:
            raise NormpathException("cannot join to empty path")
        if not other.normsubpaths:
            raise NormpathException("cannot join empty path")
        self.normsubpaths[-1].join(other.normsubpaths[0])
        self.normsubpaths.extend(other.normsubpaths[1:])

    def joined(self, other):
        """return joined self and other

        Both normpaths must contain at least one normsubpath.
        The last normsubpath of self will be joined to the first
        normsubpath of other.
        """
        result = self.copy()
        result.join(other.normpath())
        return result

    # << operator also designates joining
    __lshift__ = joined

    def normpath(self):
        """return a normpath, i.e. self"""
        return self

    def _paramtoarclen_pt(self, params):
        """return arc lengths in pts matching the given params"""
        result = [None] * len(params)
        totalarclen_pt = 0
        distributeparams = self._distributeparams(params)
        for normsubpathindex in range(max(distributeparams.keys()) + 1):
            if normsubpathindex in distributeparams:
                indices, params = distributeparams[normsubpathindex]
                arclens_pt, normsubpatharclen_pt = self.normsubpaths[normsubpathindex]._paramtoarclen_pt(params)
                for index, arclen_pt in zip(indices, arclens_pt):
                    result[index] = totalarclen_pt + arclen_pt
                totalarclen_pt += normsubpatharclen_pt
            else:
                totalarclen_pt += self.normsubpaths[normsubpathindex].arclen_pt()
        return result

    paramtoarclen_pt = _valueorlistmethod(_paramtoarclen_pt)

    @_valueorlistmethod
    def paramtoarclen(self, params):
        """return arc length(s) matching the given param(s)"""
        return [arclen_pt * unit.t_pt for arclen_pt in self._paramtoarclen_pt(params)]

    def path(self):
        """return path corresponding to normpath"""
        from . import path
        pathitems = []
        for normsubpath in self.normsubpaths:
            pathitems.extend(normsubpath.pathitems())
        return path.path(*pathitems)

    def reversed(self):
        """return reversed path"""
        nnormpath = normpath()
        for i in range(len(self.normsubpaths)):
            nnormpath.normsubpaths.append(self.normsubpaths[-(i+1)].reversed())
        return nnormpath

    def _rotation(self, params):
        """return rotation at params"""
        result = [None] * len(params)
        for normsubpathindex, (indices, params) in list(self._distributeparams(params).items()):
            for index, rotation in zip(indices, self.normsubpaths[normsubpathindex].rotation(params)):
                result[index] = rotation
        return result

    @_valueorlistmethod
    def rotation_pt(self, params):
        """return rotation at param(s) or arc length(s) in pts"""
        return self._rotation(self._convertparams(params, self.arclentoparam_pt))

    @_valueorlistmethod
    def rotation(self, params):
        """return rotation at param(s) or arc length(s)"""
        return self._rotation(self._convertparams(params, self.arclentoparam))

    def _split_pt(self, params):
        """split path at params and return list of normpaths"""
        if not params:
            return [self.copy()]

        # instead of distributing the parameters, we need to keep their
        # order and collect parameters for splitting of normsubpathitem
        # with index collectindex
        collectindex = None
        for param in params:
            if param.normsubpathindex != collectindex:
                if collectindex is not None:
                    # append end point depening on the forthcoming index
                    if param.normsubpathindex > collectindex:
                        collectparams.append(len(self.normsubpaths[collectindex]))
                    else:
                        collectparams.append(0)
                    # get segments of the normsubpath and add them to the result
                    segments = self.normsubpaths[collectindex].segments(collectparams)
                    result[-1].append(segments[0])
                    result.extend([normpath([segment]) for segment in segments[1:]])
                    # add normsubpathitems and first segment parameter to close the
                    # gap to the forthcoming index
                    if param.normsubpathindex > collectindex:
                        for i in range(collectindex+1, param.normsubpathindex):
                            result[-1].append(self.normsubpaths[i])
                        collectparams = [0]
                    else:
                        for i in range(collectindex-1, param.normsubpathindex, -1):
                            result[-1].append(self.normsubpaths[i].reversed())
                        collectparams = [len(self.normsubpaths[param.normsubpathindex])]
                else:
                    result = [normpath(self.normsubpaths[:param.normsubpathindex])]
                    collectparams = [0]
                collectindex = param.normsubpathindex
            collectparams.append(param.normsubpathparam)
        # add remaining collectparams to the result
        collectparams.append(len(self.normsubpaths[collectindex]))
        segments = self.normsubpaths[collectindex].segments(collectparams)
        result[-1].append(segments[0])
        result.extend([normpath([segment]) for segment in segments[1:]])
        result[-1].extend(self.normsubpaths[collectindex+1:])
        return result

    def split_pt(self, params):
        """split path at param(s) or arc length(s) in pts and return list of normpaths"""
        try:
            for param in params:
                break
        except Exception:
            params = [params]
        return self._split_pt(self._convertparams(params, self.arclentoparam_pt))

    def split(self, params):
        """split path at param(s) or arc length(s) and return list of normpaths"""
        try:
            for param in params:
                break
        except Exception:
            params = [params]
        return self._split_pt(self._convertparams(params, self.arclentoparam))

    def _tangent(self, params, length_pt):
        """return tangent vector of path at params

        If length_pt in pts is not None, the tangent vector will be scaled to
        the desired length.
        """
        from . import path
        result = [None] * len(params)
        tangenttemplate = path.line_pt(0, 0, length_pt, 0).normpath()
        for normsubpathindex, (indices, params) in list(self._distributeparams(params).items()):
            for index, atrafo in zip(indices, self.normsubpaths[normsubpathindex].trafo(params)):
                result[index] = tangenttemplate.transformed(atrafo)
        return result

    @_valueorlistmethod
    def tangent_pt(self, params, length_pt):
        """return tangent vector of path at param(s) or arc length(s) in pts

        If length in pts is not None, the tangent vector will be scaled to
        the desired length.
        """
        return self._tangent(self._convertparams(params, self.arclentoparam_pt), length_pt)

    @_valueorlistmethod
    def tangent(self, params, length=1):
        """return tangent vector of path at param(s) or arc length(s)

        If length is not None, the tangent vector will be scaled to
        the desired length.
        """
        return self._tangent(self._convertparams(params, self.arclentoparam), unit.topt(length))

    def _trafo(self, params):
        """return transformation at params"""
        result = [None] * len(params)
        for normsubpathindex, (indices, params) in list(self._distributeparams(params).items()):
            for index, trafo in zip(indices, self.normsubpaths[normsubpathindex].trafo(params)):
                result[index] = trafo
        return result

    @_valueorlistmethod
    def trafo_pt(self, params):
        """return transformation at param(s) or arc length(s) in pts"""
        return self._trafo(self._convertparams(params, self.arclentoparam_pt))

    @_valueorlistmethod
    def trafo(self, params):
        """return transformation at param(s) or arc length(s)"""
        return self._trafo(self._convertparams(params, self.arclentoparam))

    def transformed(self, trafo):
        """return transformed normpath"""
        return normpath([normsubpath.transformed(trafo) for normsubpath in self.normsubpaths])

    def outputPS(self, file, writer):
        for normsubpath in self.normsubpaths:
            normsubpath.outputPS(file, writer)

    def outputPDF(self, file, writer):
        for normsubpath in self.normsubpaths:
            normsubpath.outputPDF(file, writer)

    def returnSVGdata(self, inverse_y=True):
        return "".join(normsubpath.returnSVGdata(inverse_y) for normsubpath in self.normsubpaths)

