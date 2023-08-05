from pyx import *

text.preamble(r"\parindent0pt")

c = canvas.canvas()
t = c.text(0, 0, r"spam \& eggs", [trafo.scale(6), text.parbox(1.2, baseline=text.parbox.top)])
t2 = text.text(0, 0, "eggs", [trafo.scale(6)])
b, b2 = t.bbox(), t2.bbox()
c.stroke(t.path(), [style.linewidth.THin])
c.stroke(path.line(-0.3, b.top(), -0.1, b.top()), [deco.earrow.Small])
c.text(-0.5, b.top(), "valign.top", [text.vshift.mathaxis, text.halign.right])
c.stroke(path.line(-0.3, 0.5*(b.top()+b.bottom()), -0.1, 0.5*(b.top()+b.bottom())), [deco.earrow.Small])
c.text(-0.5, 0.5*(b.top()+b.bottom()), "valign.middle", [text.vshift.mathaxis, text.halign.right])
c.stroke(path.line(-0.3, b.bottom(), -0.1, b.bottom()), [deco.earrow.Small])
c.text(-0.5, b.bottom(), "valign.bottom", [text.vshift.mathaxis, text.halign.right])
c.stroke(path.line(0, 0, 7.2, 0))
c.stroke(path.line(7.3, 0, 7.5, 0), [deco.barrow.Small])
c.text(7.7, 0, "parbox.top", [text.vshift.mathaxis])
c.stroke(path.line(7.3, 0.5*(b.bottom()-b2.bottom()), 7.5, 0.5*(b.bottom()-b2.bottom())), [deco.barrow.Small])
c.text(7.7, 0.5*(b.bottom()-b2.bottom()), "parbox.middle", [text.vshift.mathaxis])
c.stroke(path.line(0, b.bottom()-b2.bottom(), 7.2, b.bottom()-b2.bottom()))
c.stroke(path.line(7.3, b.bottom()-b2.bottom(), 7.5, b.bottom()-b2.bottom()), [deco.barrow.Small])
c.text(7.7, b.bottom()-b2.bottom(), "parbox.bottom", [text.vshift.mathaxis])
c.writePDFfile()
