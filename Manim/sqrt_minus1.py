"""
Manim Animation: Why √(-1) is Impossible in ℝ but Possible in ℂ
================================================================
Run with:
    manim -pql sqrt_minus1.py SqrtMinusOne        # low quality preview
    manim -pqh sqrt_minus1.py SqrtMinusOne        # high quality
    manim -pqk sqrt_minus1.py SqrtMinusOne        # 4K
"""

from manim import *

# ── Palette ──────────────────────────────────────────────────────────────────
REAL_COLOR    = BLUE_C
COMPLEX_COLOR = GOLD_C
NEG_COLOR     = RED_C
POS_COLOR     = GREEN_C
HIGHLIGHT     = YELLOW


# ═══════════════════════════════════════════════════════════════════════════════
class SqrtMinusOne(Scene):
# ═══════════════════════════════════════════════════════════════════════════════

    def construct(self):
        self.camera.background_color = "#0d0d1a"

        self._title_card()
        self._part1_real_number_line()
        self._part2_squaring_is_always_positive()
        self._part3_parabola_proof()
        self._part4_enter_complex()
        self._part5_complex_plane()
        self._part6_rotation_proof()
        self._part7_euler_formula()
        self._finale()

    # ──────────────────────────────────────────────────────────────────────────
    # 0. TITLE CARD
    # ──────────────────────────────────────────────────────────────────────────
    def _title_card(self):
        title = MathTex(r"\sqrt{-1}", font_size=120, color=HIGHLIGHT)
        q1    = Text("Impossible?", font_size=44, color=NEG_COLOR).next_to(title, DOWN, buff=0.4)
        q2    = Text("Or just misunderstood?", font_size=36, color=COMPLEX_COLOR).next_to(q1, DOWN, buff=0.2)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(q1, shift=UP*0.3))
        self.play(FadeIn(q2, shift=UP*0.3))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, q1, q2)))

    # ──────────────────────────────────────────────────────────────────────────
    # 1. THE REAL NUMBER LINE
    # ──────────────────────────────────────────────────────────────────────────
    def _part1_real_number_line(self):
        header = Text("Part 1: The Real Numbers ℝ", font_size=36, color=REAL_COLOR)
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        # Number line
        nl = NumberLine(x_range=[-4, 4, 1], length=9,
                        include_numbers=True, include_tip=True,
                        color=REAL_COLOR)
        label_R = MathTex(r"\mathbb{R}", font_size=48, color=REAL_COLOR)
        label_R.next_to(nl, RIGHT, buff=0.3)

        self.play(Create(nl), Write(label_R))
        self.wait(0.5)

        # Highlight positive side
        pos_label = Text("Every positive number lives here", font_size=28, color=POS_COLOR)
        pos_label.next_to(nl, DOWN, buff=0.5).shift(RIGHT)
        pos_brace = Brace(nl, DOWN, buff=0.1, color=POS_COLOR)
        self.play(GrowFromCenter(pos_brace), FadeIn(pos_label))
        self.wait(1)

        # Mark -1 on the line
        dot_neg1 = Dot(nl.n2p(-1), color=NEG_COLOR, radius=0.14)
        label_neg1 = MathTex("-1", color=NEG_COLOR, font_size=36).next_to(dot_neg1, UP, buff=0.3)
        self.play(FadeOut(pos_brace), FadeOut(pos_label))
        self.play(FadeIn(dot_neg1), Write(label_neg1))

        question = MathTex(r"\text{What number squares to } {-1}\,?",
                           font_size=34, color=HIGHLIGHT)
        question.next_to(nl, DOWN, buff=0.7)
        self.play(Write(question))
        self.wait(1.5)

        self.play(FadeOut(VGroup(header, nl, label_R, dot_neg1, label_neg1, question)))

    # ──────────────────────────────────────────────────────────────────────────
    # 2. SQUARING IS ALWAYS NON-NEGATIVE ON ℝ
    # ──────────────────────────────────────────────────────────────────────────
    def _part2_squaring_is_always_positive(self):
        header = Text("Squaring on ℝ: always ≥ 0", font_size=34, color=REAL_COLOR)
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        # Proof by cases
        cases = VGroup(
            MathTex(r"x > 0 \;\Rightarrow\; x^2 > 0", font_size=38),
            MathTex(r"x = 0 \;\Rightarrow\; x^2 = 0", font_size=38),
            MathTex(r"x < 0 \;\Rightarrow\; x^2 > 0 \quad (\text{negative} \times \text{negative})",
                    font_size=38),
        ).arrange(DOWN, buff=0.6).shift(UP*0.3)

        for i, case in enumerate(cases):
            color = [POS_COLOR, WHITE, POS_COLOR][i]
            case.set_color_by_tex_to_color_map({"0": HIGHLIGHT})
            self.play(Write(case), run_time=1)
            self.wait(0.4)

        conclusion = MathTex(
            r"\therefore \quad \forall\, x \in \mathbb{R},\quad x^2 \geq 0",
            font_size=42, color=NEG_COLOR)
        conclusion.next_to(cases, DOWN, buff=0.7)
        box = SurroundingRectangle(conclusion, color=NEG_COLOR, buff=0.2)
        self.play(Write(conclusion), Create(box))
        self.wait(1)

        killer = MathTex(r"\Rightarrow\; x^2 = -1 \text{ has NO solution in } \mathbb{R}",
                         font_size=36, color=HIGHLIGHT)
        killer.next_to(box, DOWN, buff=0.5)
        self.play(Write(killer))
        self.wait(2)

        self.play(FadeOut(VGroup(header, cases, conclusion, box, killer)))

    # ──────────────────────────────────────────────────────────────────────────
    # 3. PARABOLA VISUAL PROOF
    # ──────────────────────────────────────────────────────────────────────────
    def _part3_parabola_proof(self):
        header = Text("Visual Proof: y = x² never goes below 0", font_size=32, color=REAL_COLOR)
        header.to_edge(UP, buff=0.3)
        self.play(Write(header))

        axes = Axes(x_range=[-3, 3, 1], y_range=[-1.5, 5, 1],
                    x_length=7, y_length=5,
                    axis_config={"color": WHITE, "include_tip": True},
                    x_axis_config={"numbers_to_include": range(-3, 4)},
                    y_axis_config={"numbers_to_include": range(0, 6)})
        axes.shift(DOWN*0.3)

        parabola = axes.plot(lambda x: x**2, color=REAL_COLOR, stroke_width=3)
        para_label = MathTex("y = x^2", color=REAL_COLOR, font_size=30)
        para_label.next_to(axes.c2p(2, 4), RIGHT, buff=0.1)

        # Horizontal dashed line at y = -1
        dashed = DashedLine(
            axes.c2p(-3, -1), axes.c2p(3, -1),
            color=NEG_COLOR, stroke_width=2, dash_length=0.15)
        dashed_label = MathTex("y = -1", color=NEG_COLOR, font_size=28)
        dashed_label.next_to(axes.c2p(3, -1), RIGHT, buff=0.1)

        # Shaded forbidden region
        forbidden = axes.get_area(
            axes.plot(lambda x: -1.5, color=NEG_COLOR),
            x_range=[-3, 3], bounded_graph=axes.plot(lambda x: 0, color=REAL_COLOR),
            color=NEG_COLOR, opacity=0.18)

        forbidden_text = Text("Forbidden zone\n(no real square root)", font_size=22, color=NEG_COLOR)
        forbidden_text.move_to(axes.c2p(0, -1))

        self.play(Create(axes), run_time=1.2)
        self.play(Create(parabola), Write(para_label), run_time=1.2)
        self.play(Create(dashed), Write(dashed_label))
        self.play(FadeIn(forbidden), Write(forbidden_text))
        self.wait(2)

        # Show the gap
        arrow = Arrow(axes.c2p(0, -0.2), axes.c2p(0, -0.85), color=HIGHLIGHT, buff=0)
        gap_text = Text("Parabola never\nreaches here!", font_size=24, color=HIGHLIGHT)
        gap_text.next_to(axes.c2p(0.5, -0.5), RIGHT, buff=0.1)
        self.play(GrowArrow(arrow), Write(gap_text))
        self.wait(2)

        self.play(FadeOut(VGroup(header, axes, parabola, para_label, dashed, dashed_label,
                                  forbidden, forbidden_text, arrow, gap_text)))

    # ──────────────────────────────────────────────────────────────────────────
    # 4. ENTER COMPLEX NUMBERS
    # ──────────────────────────────────────────────────────────────────────────
    def _part4_enter_complex(self):
        header = Text("Part 2: Extend the Number System → ℂ", font_size=34, color=COMPLEX_COLOR)
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        idea = MathTex(r"\text{What if we just } \textit{define} \text{ a number } i \text{ such that:}",
                       font_size=32)
        defn = MathTex(r"i^2 = -1", font_size=72, color=HIGHLIGHT)
        sub  = MathTex(r"i = \sqrt{-1}", font_size=52, color=COMPLEX_COLOR)

        group = VGroup(idea, defn, sub).arrange(DOWN, buff=0.6).shift(UP*0.2)
        self.play(Write(idea))
        self.play(Write(defn), run_time=1.2)
        self.play(Write(sub))
        self.wait(1)

        # Show that ℝ ⊂ ℂ
        embed = MathTex(
            r"\mathbb{R} \subset \mathbb{C}, \quad z = a + bi \quad (a,b \in \mathbb{R})",
            font_size=36, color=WHITE)
        embed.next_to(group, DOWN, buff=0.6)
        self.play(Write(embed))
        self.wait(2)

        self.play(FadeOut(VGroup(header, group, embed)))

    # ──────────────────────────────────────────────────────────────────────────
    # 5. THE COMPLEX PLANE
    # ──────────────────────────────────────────────────────────────────────────
    def _part5_complex_plane(self):
        header = Text("The Complex Plane (Argand Diagram)", font_size=32, color=COMPLEX_COLOR)
        header.to_edge(UP, buff=0.3)
        self.play(Write(header))

        plane = ComplexPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6, y_length=6,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1},
            axis_config={"color": WHITE}).shift(DOWN*0.3)
        plane.add_coordinates()

        real_label = Text("Real axis →", font_size=22, color=REAL_COLOR).next_to(plane, RIGHT, buff=0.1)
        imag_label = Text("Imaginary\naxis ↑", font_size=22, color=COMPLEX_COLOR)
        imag_label.next_to(plane.n2p(0 + 3j), UP, buff=0.1)

        self.play(Create(plane), run_time=1.5)
        self.play(Write(real_label), Write(imag_label))

        # Mark i on the plane
        dot_i = Dot(plane.n2p(0 + 1j), color=COMPLEX_COLOR, radius=0.12)
        label_i = MathTex("i", font_size=36, color=COMPLEX_COLOR).next_to(dot_i, RIGHT, buff=0.15)
        dot_neg_i = Dot(plane.n2p(0 - 1j), color=COMPLEX_COLOR, radius=0.12)
        label_neg_i = MathTex("-i", font_size=36, color=COMPLEX_COLOR).next_to(dot_neg_i, RIGHT, buff=0.15)
        dot_neg1 = Dot(plane.n2p(-1), color=NEG_COLOR, radius=0.12)
        label_neg1 = MathTex("-1", font_size=32, color=NEG_COLOR).next_to(dot_neg1, DOWN, buff=0.15)

        self.play(FadeIn(dot_i), Write(label_i))
        self.play(FadeIn(dot_neg_i), Write(label_neg_i))
        self.play(FadeIn(dot_neg1), Write(label_neg1))
        self.wait(1.5)

        # Arrow from i to -1: multiply by i = rotate 90°
        arc_arrow = CurvedArrow(
            plane.n2p(0 + 1j), plane.n2p(-1),
            angle=-TAU/4, color=HIGHLIGHT, stroke_width=3)
        arc_label = MathTex(r"\times\, i \;(90°)", font_size=26, color=HIGHLIGHT)
        arc_label.move_to(plane.n2p(-0.6 + 0.7j))

        self.play(Create(arc_arrow), Write(arc_label))
        self.wait(2)

        self.play(FadeOut(VGroup(header, plane, real_label, imag_label,
                                  dot_i, label_i, dot_neg_i, label_neg_i,
                                  dot_neg1, label_neg1, arc_arrow, arc_label)))

    # ──────────────────────────────────────────────────────────────────────────
    # 6. ROTATION PROOF: i² = –1 via 90° rotation
    # ──────────────────────────────────────────────────────────────────────────
    def _part6_rotation_proof(self):
        header = Text("Why i² = –1: Rotation by 90°", font_size=32, color=HIGHLIGHT)
        header.to_edge(UP, buff=0.3)
        self.play(Write(header))

        plane = ComplexPlane(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1],
            x_length=5.5, y_length=5.5,
            background_line_style={"stroke_color": GREY_D, "stroke_width": 1},
            axis_config={"color": WHITE}).shift(DOWN*0.2 + LEFT*0.5)

        self.play(Create(plane), run_time=1)

        # Unit circle
        circle = Circle(radius=plane.get_x_unit_size(), color=GREY_B, stroke_width=1.5)
        circle.move_to(plane.n2p(0))
        self.play(Create(circle))

        # Start: 1 on real axis
        dot = Dot(plane.n2p(1), color=REAL_COLOR, radius=0.13)
        vec  = Arrow(plane.n2p(0), plane.n2p(1), buff=0, color=REAL_COLOR, stroke_width=4)
        lbl1 = MathTex("1", font_size=30, color=REAL_COLOR).next_to(plane.n2p(1), DOWN+RIGHT, buff=0.1)

        self.play(GrowArrow(vec), FadeIn(dot), Write(lbl1))

        # Explanation box
        explain = VGroup(
            MathTex(r"\text{Multiply by } i = \text{rotate } 90°", font_size=26),
            MathTex(r"1 \xrightarrow{\times i} i \xrightarrow{\times i} i^2 = -1", font_size=30, color=COMPLEX_COLOR),
        ).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.5).shift(UP*0.5)
        self.play(Write(explain[0]))

        # First rotation: 1 → i
        self.play(
            Rotate(vec, angle=PI/2, about_point=plane.n2p(0)),
            dot.animate.move_to(plane.n2p(0 + 1j)),
            run_time=1.2)
        lbl2 = MathTex("i", font_size=30, color=COMPLEX_COLOR).next_to(plane.n2p(0+1j), UP+RIGHT, buff=0.1)
        lbl1.become(lbl2)
        self.wait(0.5)

        # Second rotation: i → -1
        self.play(
            Rotate(vec, angle=PI/2, about_point=plane.n2p(0)),
            dot.animate.move_to(plane.n2p(-1)),
            run_time=1.2)
        lbl3 = MathTex("-1", font_size=30, color=NEG_COLOR).next_to(plane.n2p(-1), UP+RIGHT, buff=0.1)
        lbl1.become(lbl3)
        self.play(Write(explain[1]))
        self.wait(0.5)

        # Flash the result
        result_box = MathTex(r"i \cdot i = i^2 = -1", font_size=42, color=HIGHLIGHT)
        result_box.next_to(header, DOWN, buff=0.3)
        box = SurroundingRectangle(result_box, color=HIGHLIGHT)
        self.play(Write(result_box), Create(box))
        self.wait(2)

        self.play(FadeOut(VGroup(header, plane, circle, dot, vec, lbl1,
                                  explain, result_box, box)))

    # ──────────────────────────────────────────────────────────────────────────
    # 7. EULER'S FORMULA BONUS
    # ──────────────────────────────────────────────────────────────────────────
    def _part7_euler_formula(self):
        header = Text("Bonus: Euler's Formula — i in full glory", font_size=30, color=COMPLEX_COLOR)
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        euler = MathTex(r"e^{i\pi} + 1 = 0", font_size=96, color=HIGHLIGHT)
        self.play(Write(euler), run_time=2)
        self.wait(0.5)

        breakdown = VGroup(
            MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta", font_size=38, color=COMPLEX_COLOR),
            MathTex(r"\theta = \pi \;\Rightarrow\; e^{i\pi} = \cos\pi + i\sin\pi = -1 + 0 = -1",
                    font_size=30, color=WHITE),
        ).arrange(DOWN, buff=0.4).next_to(euler, DOWN, buff=0.5)

        self.play(Write(breakdown[0]))
        self.play(Write(breakdown[1]))
        self.wait(2)

        self.play(FadeOut(VGroup(header, euler, breakdown)))

    # ──────────────────────────────────────────────────────────────────────────
    # 8. FINALE SUMMARY
    # ──────────────────────────────────────────────────────────────────────────
    def _finale(self):
        title = Text("Summary", font_size=48, color=HIGHLIGHT)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        lines = VGroup(
            MathTex(r"\text{In } \mathbb{R}: \quad x^2 \geq 0 \;\;\forall x",
                    r"\;\Rightarrow\; x^2 = -1 \text{ impossible}",
                    font_size=32),
            MathTex(r"\text{In } \mathbb{C}: \quad i \text{ is defined by } i^2 = -1",
                    r"\quad\Rightarrow \sqrt{-1} = i",
                    font_size=32),
            MathTex(r"\mathbb{C} \text{ is the algebraically closed extension of } \mathbb{R}",
                    font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.55).shift(DOWN*0.2)

        lines[0].set_color_by_tex_to_color_map({"impossible": NEG_COLOR})
        lines[1].set_color_by_tex_to_color_map({"i": COMPLEX_COLOR})

        for line in lines:
            self.play(Write(line), run_time=1.2)
            self.wait(0.5)

        final = MathTex(r"\sqrt{-1} = i \in \mathbb{C}", font_size=72, color=HIGHLIGHT)
        final.next_to(lines, DOWN, buff=0.7)
        self.play(Write(final), run_time=1.5)
        self.play(Wiggle(final, scale_value=1.15, n_wiggles=2))
        self.wait(3)
