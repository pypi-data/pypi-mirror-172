# -*- encoding: utf-8 -*-
#
#
# Copyright (C) 2011 Jörg Lehmann <joerg@pyx-project.org>
# Copyright (C) 2005-2011 André Wobst <wobsta@pyx-project.org>
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

from . import font
__allfont__ = ["T1font", "T1builtinfont", "text_pt", "font"]
for importfromfont in __allfont__:
    locals()[importfromfont] = getattr(font, importfromfont)

__all__ = __allfont__
