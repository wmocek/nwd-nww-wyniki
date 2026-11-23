from manim import *

BG = "#1b1f2a"
GREEN = "#8bc34a"
RED_ = "#ef6c57"
ORANGE_ = "#f39c32"
YEL = "#ffd54f"
BLUE_ = "#4fc3f7"
config.background_color = BG

def T(s, size=36, color=WHITE, weight=NORMAL):
    return Text(s, font="DejaVu Sans", font_size=size, color=color, weight=weight)


class NWWPaski(Scene):
    def construct(self):
        title = T("Zielone paski po 12 cm, czerwone po 14 cm", 30, ORANGE_, BOLD).to_edge(UP)
        self.play(Write(title))
        u = 0.13
        x0 = -4.9
        yg, yr = 1.0, -0.9
        g, r = 0, 0
        lbl_g = T("Ola", 26, GREEN).move_to([x0 - 0.5, yg, 0]).shift(LEFT * 0.1)
        lbl_r = T("Wojtek", 26, RED_).move_to([x0 - 0.7, yr, 0])
        lbl_g.next_to([x0, yg, 0], LEFT, buff=0.15)
        lbl_r.next_to([x0, yr, 0], LEFT, buff=0.15)
        self.play(FadeIn(lbl_g), FadeIn(lbl_r))

        def block(start, length, y, col):
            rect = Rectangle(width=length * u, height=0.6, fill_color=col, fill_opacity=0.85,
                             stroke_color=WHITE, stroke_width=1.5)
            rect.move_to([x0 + (start + length / 2) * u, y, 0])
            txt = T(f"{length}", 18, BLACK).move_to(rect)
            return VGroup(rect, txt)

        first = True
        while True:
            if g <= r:
                b = block(g, 12, yg, GREEN)
                g += 12
                num = T(str(g), 20, GREEN).move_to([x0 + g * u, yg + 0.55, 0])
            else:
                b = block(r, 14, yr, RED_)
                r += 14
                num = T(str(r), 20, RED_).move_to([x0 + r * u, yr - 0.55, 0])
            self.play(FadeIn(b, shift=RIGHT * 0.3), FadeIn(num), run_time=0.45 if not first else 0.8)
            first = False
            if g == r:
                break
        line = DashedLine([x0 + 84 * u, 2.0, 0], [x0 + 84 * u, -1.9, 0], color=YEL, stroke_width=4)
        self.play(Create(line))
        res = T("NWW(12, 14) = 84", 40, YEL, BOLD).to_edge(DOWN, buff=0.7)
        box = SurroundingRectangle(res, color=YEL, buff=0.25)
        grp = VGroup(res, box)
        self.play(Write(res), Create(box))
        sub = T("najmniejsza wspólna wielokrotność (różna od 0)", 24).next_to(grp, UP, buff=0.2)
        self.play(FadeIn(sub))
        self.wait(2)


class NWDKartka(Scene):
    def construct(self):
        title = T("Kartka 18 cm × 24 cm – jakie kwadraty?", 30, ORANGE_, BOLD).to_edge(UP)
        self.play(Write(title))
        u = 0.2
        W, H = 24, 18
        rect = Rectangle(width=W * u, height=H * u, stroke_color=WHITE, stroke_width=3,
                         fill_color="#2c3446", fill_opacity=1).shift(LEFT * 2.6 + DOWN * 0.3)
        self.play(Create(rect))
        ox, oy = rect.get_corner(DL)[0], rect.get_corner(DL)[1]
        info = VGroup().to_edge(RIGHT)
        prev = None
        prev_info = None
        lines_info = []
        for d, ok in [(1, True), (2, True), (3, True), (4, False), (6, True)]:
            grid = VGroup()
            cols = W // d
            rows = H // d
            for i in range(cols):
                for j in range(rows):
                    sq = Square(side_length=d * u, stroke_width=1.2 if d > 1 else 0.6,
                                stroke_color=BLUE_ if ok else RED_,
                                fill_color=BLUE_ if ok else RED_, fill_opacity=0.15)
                    sq.move_to([ox + (i + 0.5) * d * u, oy + (j + 0.5) * d * u, 0])
                    grid.add(sq)
            extra = VGroup()
            if not ok:
                rest = H - rows * d
                strip = Rectangle(width=W * u, height=rest * u, fill_color=RED_, fill_opacity=0.6,
                                  stroke_width=0).move_to([ox + W * u / 2, oy + (rows * d + rest / 2) * u, 0])
                extra.add(strip)
            mark = "✓" if ok else "✗  (18 : 4 ma resztę)"
            line = T(f"bok {d} cm  {mark}", 26, GREEN if ok else RED_)
            anims = [Create(grid, lag_ratio=0.002, run_time=1.2)]
            if prev is not None:
                anims.append(FadeOut(prev))
            self.play(*anims)
            if len(extra):
                self.play(FadeIn(extra))
            lines_info.append(line)
            VGroup(*lines_info).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.7).shift(UP * 0.8)
            self.play(FadeIn(line, shift=LEFT * 0.2), run_time=0.5)
            self.wait(0.5)
            prev = VGroup(grid, extra)
        # final: color the 6 cm squares
        self.play(prev.animate.set_fill(YEL, opacity=0.5).set_stroke(YEL, width=3))
        res = T("NWD(18, 24) = 6", 38, YEL, BOLD).to_edge(DOWN, buff=0.5).shift(RIGHT * 3)
        sub = T("największy wspólny dzielnik", 24).next_to(res, UP, buff=0.15)
        self.play(Write(res), FadeIn(sub))
        self.wait(2)


class DzielnikiPary(Scene):
    def construct(self):
        title = T("Sposób Marty: szukamy par iloczynów", 30, ORANGE_, BOLD).to_edge(UP)
        self.play(Write(title))
        s = 0.24
        n = 36
        sqs = VGroup(*[Square(side_length=s, stroke_width=1.2, stroke_color=WHITE,
                              fill_color=BLUE_, fill_opacity=0.7) for _ in range(n)])

        def layout(rows, cols):
            pts = []
            for k in range(n):
                i, j = k % cols, k // cols
                pts.append(np.array([(i - (cols - 1) / 2) * s, (j - (rows - 1) / 2) * s + 0.4, 0]))
            return pts

        for k, p in enumerate(layout(1, 36)):
            sqs[k].move_to(p)
        self.play(FadeIn(sqs, lag_ratio=0.02))
        pairs = [(1, 36), (2, 18), (3, 12), (4, 9), (6, 6)]
        found = VGroup()
        label = None
        for idx, (a, b) in enumerate(pairs):
            if idx > 0:
                self.play(*[sqs[k].animate.move_to(p) for k, p in enumerate(layout(a, b))], run_time=1.1)
            new_label = T(f"36 = {a} · {b}", 36, YEL, BOLD).move_to(DOWN * 1.6)
            if label is None:
                self.play(Write(new_label))
            else:
                self.play(ReplacementTransform(label, new_label))
            label = new_label
            item = T(f"{a} · {b}", 26, WHITE)
            found.add(item)
            found.arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.45)
            self.play(FadeIn(item), run_time=0.4)
            self.wait(0.4)
        stop = T("6 · 6 – dalej pary by się powtarzały, więc koniec!", 24, GREEN).next_to(label, UP, buff=0.25)
        self.play(FadeIn(stop))
        self.wait(1)
        self.play(FadeOut(sqs), FadeOut(stop), FadeOut(label))
        divs = [1, 2, 3, 4, 6, 9, 12, 18, 36]
        row = VGroup(*[T(str(d), 40, WHITE) for d in divs]).arrange(RIGHT, buff=0.55).shift(UP * 0.3)
        hd = T("Dzielniki liczby 36:", 30, ORANGE_).next_to(row, UP, buff=0.5)
        self.play(FadeIn(hd), LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in row], lag_ratio=0.1))
        cols = [GREEN, BLUE_, RED_, YEL]
        arcs = VGroup()
        for i in range(4):
            a = row[i]
            b = row[len(divs) - 1 - i]
            arc = ArcBetweenPoints(a.get_bottom() + DOWN * 0.1, b.get_bottom() + DOWN * 0.1,
                                   angle=PI * 0.6, color=cols[i], stroke_width=4)
            arcs.add(arc)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3))
        circ = Circle(radius=0.4, color=ORANGE_).move_to(row[4])
        self.play(Create(circ))
        tot = T("36 ma 9 dzielników", 30, YEL).next_to(arcs, DOWN, buff=0.4)
        self.play(Write(tot))
        self.wait(2)


class CechyPodzielnosci(Scene):
    def construct(self):
        title = T("Cecha podzielności przez 4", 32, ORANGE_, BOLD).to_edge(UP)
        self.play(Write(title))
        num = T("2748", 72, WHITE, BOLD).shift(UP * 1.4)
        self.play(Write(num))
        split = T("2700 + 48", 60).shift(UP * 0.1)
        self.play(TransformFromCopy(num, split))
        b1 = SurroundingRectangle(split[0:4], color=BLUE_)
        b2 = SurroundingRectangle(split[5:7], color=GREEN)
        t1 = T("27 · 100 – zawsze dzieli się przez 4,\nbo 100 = 4 · 25", 22, BLUE_).next_to(b1, DOWN, buff=0.3).shift(LEFT * 1.5)
        self.play(Create(b1), FadeIn(t1))
        t2 = T("48 : 4 = 12 ✓", 26, GREEN).next_to(b2, DOWN, buff=0.3).shift(RIGHT * 1.3)
        self.play(Create(b2), FadeIn(t2))
        concl = T("Wystarczy sprawdzić dwie ostatnie cyfry!", 30, YEL, BOLD).to_edge(DOWN, buff=0.7)
        self.play(Write(concl))
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in [num, split, b1, b2, t1, t2, concl, title]])

        title2 = T("Cechy podzielności przez 3 i przez 9", 32, ORANGE_, BOLD).to_edge(UP)
        self.play(Write(title2))
        rows = [("327", [3, 2, 7]), ("5841", [5, 8, 4, 1]), ("122", [1, 2, 2])]
        y = 1.6
        for s, digs in rows:
            n = T(s, 50, WHITE, BOLD).move_to([-5.0, y, 0])
            self.play(FadeIn(n))
            parts = []
            for i, d in enumerate(digs):
                parts.append(str(d))
                if i < len(digs) - 1:
                    parts.append("+")
            sm = sum(digs)
            eq = T(" ".join(parts) + f" = {sm}", 36).move_to([-0.7, y, 0])
            copies = [n[i].copy() for i in range(len(digs))]
            self.play(*[c.animate.move_to(eq[2 * i if 2 * i < len(eq) else -1]) for i, c in enumerate(copies)],
                      run_time=0.8)
            self.play(FadeIn(eq), *[FadeOut(c) for c in copies], run_time=0.5)
            by3 = sm % 3 == 0
            by9 = sm % 9 == 0
            v = T(("przez 3 ✓" if by3 else "przez 3 ✗") + "   " + ("przez 9 ✓" if by9 else "przez 9 ✗"),
                  28, GREEN if by3 else RED_).move_to([4.4, y, 0])
            self.play(FadeIn(v, shift=LEFT * 0.2))
            y -= 1.4
        concl = T("Liczba dzieli się przez 3 (przez 9),\ngdy suma jej cyfr dzieli się przez 3 (przez 9).", 26, YEL).to_edge(DOWN, buff=0.4)
        self.play(Write(concl))
        self.wait(2.5)


class SitoEratostenesa(Scene):
    def construct(self):
        title = T("Sito Eratostenesa – liczby pierwsze do 100", 30, ORANGE_, BOLD).to_edge(UP, buff=0.3)
        self.play(Write(title))
        cell = 0.62
        cells = {}
        grid = VGroup()
        for k in range(1, 101):
            i, j = (k - 1) % 10, (k - 1) // 10
            sq = Square(side_length=cell, stroke_width=1, stroke_color=GREY_B, fill_color="#2c3446", fill_opacity=1)
            sq.move_to([(i - 4.5) * cell - 2.2, (4.5 - j) * cell - 0.45, 0])
            t = T(str(k), 18).move_to(sq)
            g = VGroup(sq, t)
            cells[k] = g
            grid.add(g)
        self.play(FadeIn(grid, lag_ratio=0.005))
        legend = VGroup().to_edge(RIGHT)
        note = T("1 nie jest ani pierwsza,\nani złożona", 22, GREY_B).move_to([4.3, 2.3, 0])
        self.play(cells[1][0].animate.set_fill(GREY_D), cells[1][1].animate.set_color(GREY_C), FadeIn(note))
        cols = {2: GREEN, 3: BLUE_, 5: ORANGE_, 7: "#ce93d8"}
        y = 1.0
        for p in [2, 3, 5, 7]:
            c = cols[p]
            self.play(cells[p][0].animate.set_fill(c, opacity=1), cells[p][1].animate.set_color(BLACK), run_time=0.4)
            mult = [m for m in range(p * p, 101, p)]
            crossed = []
            for m in range(2 * p, 101, p):
                crossed.append(cells[m][0].animate.set_fill(c, opacity=0.18))
                crossed.append(cells[m][1].animate.set_color(GREY_D))
            txt = T(f"skreślamy wielokrotności {p}", 22, c).move_to([4.3, y, 0])
            self.play(FadeIn(txt), LaggedStart(*crossed, lag_ratio=0.02, run_time=1.6))
            y -= 0.55
        rest = [k for k in range(11, 101) if all(k % p for p in [2, 3, 5, 7])]
        self.play(LaggedStart(*[AnimationGroup(cells[k][0].animate.set_fill(YEL, opacity=1),
                                               cells[k][1].animate.set_color(BLACK)) for k in rest],
                              lag_ratio=0.05, run_time=2))
        res = T("Zostało 25 liczb pierwszych\nmniejszych od 100", 26, YEL, BOLD).move_to([4.3, -2.1, 0])
        self.play(Write(res))
        self.wait(2.5)
