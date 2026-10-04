"""
GENERATION OF DISCRETE-TIME SIGNALS  --  zero-dependency version
==================================================================

Produces the same five signals as signal_generation.py, but with no
third-party packages: the plots are written as SVG using only the Python
standard library. Useful where numpy/matplotlib cannot be installed.

Run with:  python signal_generation_pure.py

Signals (continuous-time | discrete-time):
    i.   Step       u(t)   |  u[n]
    ii.  Impulse    d(t)   |  d[n]
    iii. Exponential e^(at) |  a^n
    iv.  Ramp       r(t)   |  r[n]
    v.   Sine       sin(wt)|  sin(wn)
"""

import math
import os

OUTDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures_pure")
os.makedirs(OUTDIR, exist_ok=True)

A_EXP = 0.5
W_SIN = math.pi / 4

# --------------------------------------------------------------------------
# Minimal SVG plotting engine
# --------------------------------------------------------------------------
FONT = "font-family='DejaVu Sans,Helvetica,Arial,sans-serif'"


def nice_ticks(lo, hi, target=6):
    """Return a list of 'nice' tick values spanning [lo, hi]."""
    if hi <= lo:
        return [lo]
    raw = (hi - lo) / target
    mag = 10 ** math.floor(math.log10(raw))
    for mult in (1, 2, 2.5, 5, 10):
        step = mult * mag
        if raw <= step:
            break
    start = math.ceil(lo / step) * step
    ticks, v = [], start
    while v <= hi + step * 1e-9:
        ticks.append(round(v, 10))
        v += step
    return ticks


def fmt(v):
    """Compact number formatting for tick labels."""
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return ("%g" % v)


class Panel:
    """A single 2-D axes that emits SVG fragments."""

    def __init__(self, x0, y0, x1, y1, xlim, ylim):
        # Pixel rectangle of the plotting area.
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.xlim, self.ylim = xlim, ylim
        self.out = []

    # -- coordinate mapping ------------------------------------------------
    def px(self, x):
        xmin, xmax = self.xlim
        return self.x0 + (x - xmin) / (xmax - xmin) * (self.x1 - self.x0)

    def py(self, y):
        ymin, ymax = self.ylim
        return self.y1 - (y - ymin) / (ymax - ymin) * (self.y1 - self.y0)

    # -- primitives --------------------------------------------------------
    def rect(self, x, y, w, h, fill="none", stroke=None, sw=1):
        """Rectangle. `sw` is stroke width -- `width` is already a rect attribute."""
        border = "" if stroke is None else " stroke='%s' stroke-width='%.2f'" % (
            stroke, sw
        )
        self.out.append(
            "<rect x='%.2f' y='%.2f' width='%.2f' height='%.2f' fill='%s'%s/>"
            % (x, y, w, h, fill, border)
        )

    def line(self, x1, y1, x2, y2, color="#000", width=1, dash=None):
        d = " stroke-dasharray='%s'" % dash if dash else ""
        self.out.append(
            "<line x1='%.2f' y1='%.2f' x2='%.2f' y2='%.2f' stroke='%s' "
            "stroke-width='%.2f'%s/>" % (x1, y1, x2, y2, color, width, d)
        )

    def circle(self, x, y, r, fill="none", stroke="#000", width=1.4):
        self.out.append(
            "<circle cx='%.2f' cy='%.2f' r='%.2f' fill='%s' stroke='%s' "
            "stroke-width='%.2f'/>" % (x, y, r, fill, stroke, width)
        )

    def polyline(self, pts, color="#1f77b4", width=2.2):
        if len(pts) < 2:
            return
        d = " ".join("%.2f,%.2f" % p for p in pts)
        self.out.append(
            "<polyline points='%s' fill='none' stroke='%s' stroke-width='%.2f' "
            "stroke-linejoin='round'/>" % (d, color, width)
        )

    def text(self, x, y, s, size=12, anchor="middle", color="#000", weight=None):
        w = " font-weight='%s'" % weight if weight else ""
        self.out.append(
            "<text x='%.2f' y='%.2f' %s font-size='%d' text-anchor='%s' "
            "fill='%s'%s>%s</text>"
            % (x, y, FONT, size, anchor, color, w, s)
        )

    def arrow(self, x, ybase, ytip, color="#1f77b4", width=2.4):
        """Vertical arrow from (x, ybase) to (x, ytip) with a solid head."""
        bx, by, tx, ty = self.px(x), self.py(ybase), self.px(x), self.py(ytip)
        ang = math.atan2(ty - by, tx - bx)
        size, spread = 9.0, math.radians(24)
        p1 = (tx - size * math.cos(ang - spread), ty - size * math.sin(ang - spread))
        p2 = (tx - size * math.cos(ang + spread), ty - size * math.sin(ang + spread))
        self.out.append(
            "<line x1='%.2f' y1='%.2f' x2='%.2f' y2='%.2f' stroke='%s' "
            "stroke-width='%.2f'/>" % (bx, by, tx, ty, color, width)
        )
        self.out.append(
            "<polygon points='%.2f,%.2f %.2f,%.2f %.2f,%.2f' fill='%s'/>"
            % (tx, ty, p1[0], p1[1], p2[0], p2[1], color)
        )

    # -- composite drawings ------------------------------------------------
    def grid_and_axes(self):
        xmin, xmax = self.xlim
        ymin, ymax = self.ylim
        # Tick marks + gridlines, keeping only those inside the data range.
        for tx in nice_ticks(xmin, xmax):
            if not (xmin <= tx <= xmax):
                continue
            X = self.px(tx)
            self.line(X, self.y0, X, self.y1, color="#e3e3e3", width=1)
            self.text(X, self.y1 + 15, fmt(tx), size=11, color="#444")
        for ty in nice_ticks(ymin, ymax):
            if not (ymin <= ty <= ymax):
                continue
            Y = self.py(ty)
            self.line(self.x0, Y, self.x1, Y, color="#e3e3e3", width=1)
            self.text(self.x0 - 8, Y + 4, fmt(ty), size=11, anchor="end", color="#444")
        # Axes through the origin, drawn heavier than the grid.
        if ymin <= 0 <= ymax:
            self.line(self.x0, self.py(0), self.x1, self.py(0), color="#000", width=1.3)
        if xmin <= 0 <= xmax:
            self.line(self.px(0), self.y0, self.px(0), self.y1, color="#000", width=1.3)
            # Hollow marker at the origin to make the jump point unambiguous.
            self.circle(self.px(0), self.py(0), 3.2, fill="#fff", stroke="#000", width=1.4)
        self.rect(
            self.x0, self.y0, self.x1 - self.x0, self.y1 - self.y0,
            fill="none", stroke="#999", sw=1,
        )

    def axis_labels(self, xlab, ylab, title):
        cx = (self.x0 + self.x1) / 2
        self.text(cx, self.y1 + 36, xlab, size=13)
        self.text(
            self.x0 - 46, (self.y0 + self.y1) / 2, ylab, size=13, anchor="middle",
        )
        self.text(
            cx, self.y0 - 14, title, size=12.5, weight="bold", color="#123f6b"
        )

    def draw_line(self, xs, ys, **kw):
        pts = [(self.px(x), self.py(y)) for x, y in zip(xs, ys)]
        self.polyline(pts, **kw)

    def draw_step_ct(self, t, level_after, ymin, ymax):
        """Continuous-time step: trace the 0-level run then jump at t = 0."""
        X0, X1 = self.px(t[0]), self.px(t[-1])
        Yb = self.py(0.0)
        Ya = self.py(level_after)
        self.out.append(
            "<polyline points='%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f' "
            "fill='none' stroke='#1f77b4' stroke-width='%.2f' "
            "stroke-linejoin='round'/>" % (X0, Yb, self.px(0), Yb,
                                           self.px(0), Ya, X1, Ya, 2.2)
        )

    def draw_stem(self, ns, ys, **kw):
        """Discrete-time stem plot: vertical line plus a filled marker."""
        color = kw.get("color", "#1f77b4")
        Yb = self.py(0.0)
        for n, y in zip(ns, ys):
            X = self.px(n)
            self.line(X, Yb, X, self.py(y), color=color, width=1.8)
            self.circle(X, self.py(y), 3.6, fill=color, stroke=color, width=1)


# --------------------------------------------------------------------------
# Figure assembly
# --------------------------------------------------------------------------
PW, PH = 520, 380          # panel plotting-area size
PADX, PADTOP, PADBOT = 78, 46, 74
FIGW = PADX + PW + PADX + PW + PADX
FIGH = PADTOP + PH + PADBOT


def figure(title, panels_spec):
    """panels_spec: list of (Panel, drawer) where drawer(p) renders the data."""
    parts = [
        "<?xml version='1.0' encoding='UTF-8'?>",
        "<svg xmlns='http://www.w3.org/2000/svg' width='%d' height='%d' "
        "viewBox='0 0 %d %d'>" % (FIGW, FIGH, FIGW, FIGH),
        "<rect width='%d' height='%d' fill='#ffffff'/>" % (FIGW, FIGH),
        "<text x='%d' y='30' %s font-size='17' font-weight='bold' "
        "text-anchor='middle' fill='#111'>%s</text>" % (FIGW // 2, FONT, title),
    ]
    for idx, (panel, drawer) in enumerate(panels_spec):
        ox = PADX + idx * (PW + PADX)
        oy = PADTOP
        # Shift the panel into position by translating its emitted geometry.
        inner = panel.__class__.__new__(panel.__class__)
        inner.__dict__ = dict(panel.__dict__)
        inner.x0, inner.y1 = panel.x0 + ox, panel.y1 + oy
        inner.y0, inner.x1 = panel.y0 + oy, panel.x1 + ox
        inner.out = []
        inner.grid_and_axes()
        drawer(inner)
        parts.extend(inner.out)
    parts.append("</svg>")
    return "\n".join(parts)


def make_pair(xlim_ct, ylim_ct, xlim_dt, ylim_dt):
    """Build the two panels (CT left, DT right) for one signal."""
    left = Panel(0, 0, PW, PH, xlim_ct, ylim_ct)
    right = Panel(0, 0, PW, PH, xlim_dt, ylim_dt)
    return left, right


def save(svg, name):
    path = os.path.join(OUTDIR, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print("  wrote", path)


# --------------------------------------------------------------------------
# i. Step function
# --------------------------------------------------------------------------
def fig_step():
    t = [-5 + 10 * i / 400 for i in range(401)]
    ns = list(range(-10, 11))
    lc, rc = make_pair((-5, 5), (-0.35, 1.45), (-10.5, 10.5), (-0.35, 1.45))
    svg = figure(
        "Step Function",
        [
            (lc, lambda p: (p.draw_step_ct(t, 1.0, None, None),
                            p.axis_labels("t", "u(t)", "Continuous-Time  u(t)"))),
            (rc, lambda p: (p.draw_stem(ns, [1.0 if n >= 0 else 0.0 for n in ns]),
                            p.axis_labels("n", "u[n]", "Discrete-Time  u[n]"))),
        ],
    )
    save(svg, "1_step_function.svg")


# --------------------------------------------------------------------------
# ii. Impulse function
# --------------------------------------------------------------------------
def fig_impulse():
    ns = list(range(-10, 11))
    lc, rc = make_pair((-5, 5), (-0.35, 1.45), (-10.5, 10.5), (-0.35, 1.45))
    svg = figure(
        "Impulse Function",
        [
            (lc, lambda p: (p.arrow(0, 0.0, 1.0),
                            p.axis_labels("t", "d(t)",
                                          "Continuous-Time  d(t)  (Dirac delta)"))),
            (rc, lambda p: (p.draw_stem(ns, [1.0 if n == 0 else 0.0 for n in ns]),
                            p.axis_labels("n", "d[n]",
                                          "Discrete-Time  d[n]  (Kronecker delta)"))),
        ],
    )
    save(svg, "2_impulse_function.svg")


# --------------------------------------------------------------------------
# iii. Exponential function
# --------------------------------------------------------------------------
def fig_exponential():
    t = [-5 + 10 * i / 400 for i in range(401)]
    ns = list(range(-10, 11))
    ymax = math.exp(A_EXP * 5)
    lc, rc = make_pair(
        (-5, 5), (0, ymax * 1.15), (-10.5, 10.5), (0, ymax * 1.15)
    )
    svg = figure(
        "Exponential Function",
        [
            (lc, lambda p: (
                p.draw_line(t, [math.exp(A_EXP * x) for x in t]),
                p.axis_labels("t", "e^(at)",
                              "Continuous-Time  e^(%.1f t)" % A_EXP))),
            (rc, lambda p: (
                p.draw_stem(ns, [A_EXP ** n for n in ns]),
                p.axis_labels("n", "a^n",
                              "Discrete-Time  %.1f^n" % A_EXP))),
        ],
    )
    save(svg, "3_exponential_function.svg")


# --------------------------------------------------------------------------
# iv. Ramp function
# --------------------------------------------------------------------------
def fig_ramp():
    t = [-5 + 10 * i / 400 for i in range(401)]
    ns = list(range(-10, 11))
    lc, rc = make_pair((-5, 5), (-0.4, 5.5), (-10.5, 10.5), (-0.4, 11))
    svg = figure(
        "Ramp Function",
        [
            (lc, lambda p: (
                p.draw_line(t, [x if x >= 0 else 0.0 for x in t]),
                p.axis_labels("t", "r(t)", "Continuous-Time  r(t)"))),
            (rc, lambda p: (
                p.draw_stem(ns, [n if n >= 0 else 0.0 for n in ns]),
                p.axis_labels("n", "r[n]", "Discrete-Time  r[n]"))),
        ],
    )
    save(svg, "4_ramp_function.svg")


# --------------------------------------------------------------------------
# v. Sine function
# --------------------------------------------------------------------------
def fig_sine():
    t = [-5 + 10 * i / 600 for i in range(601)]
    ns = list(range(-10, 11))
    lc, rc = make_pair((-5, 5), (-1.45, 1.45), (-10.5, 10.5), (-1.45, 1.45))
    svg = figure(
        "Sine Function",
        [
            (lc, lambda p: (
                p.draw_line(t, [math.sin(W_SIN * x) for x in t]),
                p.axis_labels("t", "sin(wt)",
                              "Continuous-Time  sin(%.4f t)" % W_SIN))),
            (rc, lambda p: (
                p.draw_stem(ns, [math.sin(W_SIN * n) for n in ns]),
                p.axis_labels("n", "sin(wn)",
                              "Discrete-Time  sin(%.4f n)" % W_SIN))),
        ],
    )
    save(svg, "5_sine_function.svg")


def main():
    print("Generating SVG signal plots ->", OUTDIR)
    fig_step()
    fig_impulse()
    fig_exponential()
    fig_ramp()
    fig_sine()
    print("Done.")


if __name__ == "__main__":
    main()