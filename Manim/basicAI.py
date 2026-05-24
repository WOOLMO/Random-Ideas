"""
Manim Animation: How AI is Trained — The Basics
================================================
Run with:
    manim -pql how_ai_trains.py HowAITrains        # quick preview
    manim -pqh how_ai_trains.py HowAITrains        # high quality 1080p
"""

from manim import *
import numpy as np

# ── Palette ──────────────────────────────────────────────────────────────────
BG_COLOR     = "#0d0d1a"
BRAIN_COLOR  = "#a78bfa"   # purple
DATA_COLOR   = "#34d399"   # green
LOSS_COLOR   = "#f87171"   # red
WEIGHT_COLOR = "#fbbf24"   # gold
PRED_COLOR   = "#60a5fa"   # blue
RIGHT_COLOR  = "#34d399"
WRONG_COLOR  = "#f87171"
HIGHLIGHT    = YELLOW


# ═══════════════════════════════════════════════════════════════════════════════
class HowAITrains(Scene):
# ═══════════════════════════════════════════════════════════════════════════════

    def construct(self):
        self.camera.background_color = BG_COLOR

        self._title_card()
        self._part1_what_is_a_model()
        self._part2_data()
        self._part3_prediction_and_error()
        self._part4_loss_function()
        self._part5_gradient_descent()
        self._part6_the_loop()
        self._part7_overfitting_hint()
        self._finale()

    # ──────────────────────────────────────────────────────────────────────────
    # 0. TITLE CARD
    # ──────────────────────────────────────────────────────────────────────────
    def _title_card(self):
        line1 = Text("How does an AI", font_size=56, color=WHITE)
        line2 = Text("actually learn?", font_size=72, color=ManimColor(BRAIN_COLOR), weight=BOLD)
        group = VGroup(line1, line2).arrange(DOWN, buff=0.3)

        self.play(FadeIn(line1, shift=UP*0.3), run_time=0.8)
        self.play(Write(line2), run_time=1.2)
        self.wait(1.5)
        self.play(FadeOut(group))

    # ──────────────────────────────────────────────────────────────────────────
    # 1. WHAT IS A MODEL — knobs analogy
    # ──────────────────────────────────────────────────────────────────────────
    def _part1_what_is_a_model(self):
        header = Text("Step 1: The Model = A Machine with Knobs", font_size=32, color=ManimColor(BRAIN_COLOR))
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        # Draw a simple box = the model
        box = RoundedRectangle(width=3.5, height=2.2, corner_radius=0.3,
                               color=ManimColor(BRAIN_COLOR), fill_color=ManimColor("#1a1a2e"),
                               fill_opacity=1, stroke_width=3)
        box_label = Text("AI Model", font_size=28, color=ManimColor(BRAIN_COLOR)).move_to(box)
        model = VGroup(box, box_label).shift(LEFT*0.5)

        # Knobs (weights)
        knob_positions = [UP*0.6+RIGHT*0.3, DOWN*0.05+RIGHT*0.3, DOWN*0.7+RIGHT*0.3]
        knobs = VGroup()
        knob_labels = VGroup()
        for i, pos in enumerate(knob_positions):
            k = Circle(radius=0.22, color=ManimColor(WEIGHT_COLOR),
                       fill_color=ManimColor("#3d2c00"), fill_opacity=1).move_to(box.get_right()+pos+LEFT*0.4)
            lbl = Text(f"w{i+1}", font_size=18, color=ManimColor(WEIGHT_COLOR)).move_to(k)
            knobs.add(k)
            knob_labels.add(lbl)

        weight_label = Text("Weights (knobs)", font_size=22, color=ManimColor(WEIGHT_COLOR))
        weight_label.next_to(knobs, RIGHT, buff=0.3)

        self.play(FadeIn(model))
        self.play(LaggedStart(*[GrowFromCenter(k) for k in knobs], lag_ratio=0.2))
        self.play(Write(knob_labels), Write(weight_label))
        self.wait(0.5)

        explanation = Text(
            "The model is just math.\nWeights are numbers that control its behavior.",
            font_size=24, color=GREY_A, line_spacing=1.4)
        explanation.next_to(model, DOWN, buff=0.6)
        self.play(Write(explanation))
        self.wait(1.5)

        # Wiggle the knobs — "training = tuning these"
        tune_text = Text("Training = finding the RIGHT values for all knobs",
                         font_size=26, color=HIGHLIGHT)
        tune_text.next_to(explanation, DOWN, buff=0.4)
        self.play(
            LaggedStart(*[Wiggle(k, scale_value=1.3) for k in knobs], lag_ratio=0.15),
            Write(tune_text))
        self.wait(2)

        self.play(FadeOut(VGroup(header, model, knobs, knob_labels,
                                  weight_label, explanation, tune_text)))

    # ──────────────────────────────────────────────────────────────────────────
    # 2. DATA — the fuel
    # ──────────────────────────────────────────────────────────────────────────
    def _part2_data(self):
        header = Text("Step 2: Feed it Data", font_size=32, color=ManimColor(DATA_COLOR))
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        # Show input → label pairs
        pairs = [
            ("🐱 Photo of a cat",   "→ Label: Cat"),
            ("🐶 Photo of a dog",   "→ Label: Dog"),
            ("🐱 Another cat",      "→ Label: Cat"),
            ("🐶 Another dog",      "→ Label: Dog"),
        ]

        rows = VGroup()
        for inp, lbl in pairs:
            inp_box = Text(inp, font_size=24, color=WHITE)
            lbl_box = Text(lbl, font_size=24, color=ManimColor(DATA_COLOR))
            row = VGroup(inp_box, lbl_box).arrange(RIGHT, buff=0.8)
            rows.add(row)

        rows.arrange(DOWN, buff=0.35).shift(UP*0.2)

        for row in rows:
            self.play(FadeIn(row, shift=RIGHT*0.3), run_time=0.5)

        self.wait(0.5)

        caption = Text(
            "Each example has an INPUT and a correct ANSWER (label).\nThis is called Supervised Learning.",
            font_size=24, color=GREY_A, line_spacing=1.4)
        caption.next_to(rows, DOWN, buff=0.5)
        self.play(Write(caption))
        self.wait(2)

        scale_text = Text("Millions of these examples → that's the training data",
                          font_size=26, color=HIGHLIGHT)
        scale_text.next_to(caption, DOWN, buff=0.3)
        self.play(Write(scale_text))
        self.wait(1.5)

        self.play(FadeOut(VGroup(header, rows, caption, scale_text)))

    # ──────────────────────────────────────────────────────────────────────────
    # 3. PREDICTION AND ERROR
    # ──────────────────────────────────────────────────────────────────────────
    def _part3_prediction_and_error(self):
        header = Text("Step 3: Guess → Check → How Wrong?", font_size=32, color=ManimColor(PRED_COLOR))
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        # Input box
        inp = RoundedRectangle(width=2.5, height=1.1, corner_radius=0.2,
                               color=ManimColor(DATA_COLOR), fill_color=ManimColor("#0d2e1e"), fill_opacity=1)
        inp_lbl = Text("🐱 Cat photo", font_size=22).move_to(inp)
        inp_group = VGroup(inp, inp_lbl).shift(LEFT*4)

        # Model box
        model_box = RoundedRectangle(width=2.2, height=1.1, corner_radius=0.2,
                                     color=ManimColor(BRAIN_COLOR), fill_color=ManimColor("#1a1a2e"), fill_opacity=1)
        model_lbl = Text("Model", font_size=24, color=ManimColor(BRAIN_COLOR)).move_to(model_box)
        model_group = VGroup(model_box, model_lbl)

        # Output
        out_box = RoundedRectangle(width=2.5, height=1.1, corner_radius=0.2,
                                   color=ManimColor(WRONG_COLOR), fill_color=ManimColor("#2e0d0d"), fill_opacity=1)
        out_lbl = Text('Guess: "Dog" 🐶', font_size=20, color=ManimColor(WRONG_COLOR)).move_to(out_box)
        out_group = VGroup(out_box, out_lbl).shift(RIGHT*4)

        # Arrows
        arr1 = Arrow(inp_group.get_right(), model_group.get_left(), color=WHITE, buff=0.1)
        arr2 = Arrow(model_group.get_right(), out_group.get_left(), color=WHITE, buff=0.1)

        self.play(FadeIn(inp_group))
        self.play(GrowArrow(arr1), FadeIn(model_group))
        self.play(GrowArrow(arr2), FadeIn(out_group))
        self.wait(0.5)

        # Correct answer
        correct = Text('Correct answer: "Cat" 🐱', font_size=26, color=ManimColor(RIGHT_COLOR))
        correct.next_to(out_group, DOWN, buff=0.5)
        self.play(Write(correct))

        # Error
        error_arrow = Arrow(out_group.get_bottom(), correct.get_top(), color=LOSS_COLOR, buff=0.1)
        error_label = Text("ERROR!", font_size=32, color=ManimColor(LOSS_COLOR), weight=BOLD)
        error_label.next_to(error_arrow, RIGHT, buff=0.2)
        self.play(GrowArrow(error_arrow), Write(error_label))
        self.wait(1)

        # The key insight
        insight = Text(
            "The model made a wrong guess.\nWe can MEASURE how wrong it was.",
            font_size=26, color=GREY_A, line_spacing=1.4)
        insight.to_edge(DOWN, buff=0.5)
        self.play(Write(insight))
        self.wait(2)

        self.play(FadeOut(VGroup(header, inp_group, model_group, out_group,
                                  arr1, arr2, correct, error_arrow, error_label, insight)))

    # ──────────────────────────────────────────────────────────────────────────
    # 4. LOSS FUNCTION
    # ──────────────────────────────────────────────────────────────────────────
    def _part4_loss_function(self):
        header = Text("Step 4: The Loss Function — The Score of Wrongness", font_size=30, color=ManimColor(LOSS_COLOR))
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        analogy = Text(
            "Think of it like a score:\n0 = perfect   |   100 = completely wrong",
            font_size=30, color=WHITE, line_spacing=1.4)
        analogy.shift(UP*1.5)
        self.play(Write(analogy))
        self.wait(0.8)

        # Loss bar
        bar_bg = Rectangle(width=7, height=0.6, color=GREY_D,
                            fill_color=GREY_D, fill_opacity=0.4)
        bar_fill = Rectangle(width=0.01, height=0.6, color=ManimColor(LOSS_COLOR),
                              fill_color=ManimColor(LOSS_COLOR), fill_opacity=1)
        bar_fill.align_to(bar_bg, LEFT)
        bar_group = VGroup(bar_bg, bar_fill).shift(DOWN*0.2)

        zero_lbl = Text("0", font_size=20, color=ManimColor(RIGHT_COLOR)).next_to(bar_bg, LEFT, buff=0.2)
        max_lbl  = Text("100", font_size=20, color=ManimColor(LOSS_COLOR)).next_to(bar_bg, RIGHT, buff=0.2)
        loss_lbl = Text("Loss", font_size=22, color=ManimColor(LOSS_COLOR)).next_to(bar_bg, UP, buff=0.15)

        self.play(FadeIn(bar_bg), Write(zero_lbl), Write(max_lbl), Write(loss_lbl))

        # Animate filling to 85% (bad model)
        target_fill = Rectangle(width=6.0, height=0.6, color=ManimColor(LOSS_COLOR),
                                 fill_color=ManimColor(LOSS_COLOR), fill_opacity=1)
        target_fill.align_to(bar_bg, LEFT)
        bad_text = Text("Untrained model: HIGH loss 😬", font_size=24, color=ManimColor(LOSS_COLOR))
        bad_text.next_to(bar_group, DOWN, buff=0.4)

        self.play(bar_fill.animate.become(target_fill), run_time=1.5)
        self.play(Write(bad_text))
        self.wait(1)

        # Animate shrinking to 5% (good model)
        good_fill = Rectangle(width=0.35, height=0.6, color=ManimColor(RIGHT_COLOR),
                               fill_color=ManimColor(RIGHT_COLOR), fill_opacity=1)
        good_fill.align_to(bar_bg, LEFT)
        good_text = Text("Trained model: LOW loss ✅", font_size=24, color=ManimColor(RIGHT_COLOR))
        good_text.next_to(bar_group, DOWN, buff=0.4)

        self.play(
            bar_fill.animate.become(good_fill),
            FadeOut(bad_text),
            run_time=1.8)
        self.play(Write(good_text))

        goal = Text("Goal of training: make the loss as small as possible",
                    font_size=26, color=HIGHLIGHT)
        goal.to_edge(DOWN, buff=0.5)
        self.play(Write(goal))
        self.wait(2)

        self.play(FadeOut(VGroup(header, analogy, bar_group, zero_lbl, max_lbl,
                                  loss_lbl, good_text, good_fill, goal)))

    # ──────────────────────────────────────────────────────────────────────────
    # 5. GRADIENT DESCENT — rolling downhill
    # ──────────────────────────────────────────────────────────────────────────
    def _part5_gradient_descent(self):
        header = Text("Step 5: Gradient Descent — Rolling Downhill", font_size=30, color=HIGHLIGHT)
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        axes = Axes(x_range=[-3.5, 3.5, 1], y_range=[-0.3, 5, 1],
                    x_length=8, y_length=4.5,
                    axis_config={"color": GREY_B, "include_tip": True})
        axes.shift(DOWN*0.5)

        # Loss landscape curve (bowl shape)
        curve = axes.plot(lambda x: x**2 + 0.3, color=ManimColor(LOSS_COLOR), stroke_width=3)
        x_lbl = Text("Weight value", font_size=20, color=GREY_A).next_to(axes.x_axis, RIGHT, buff=0.1)
        y_lbl = Text("Loss", font_size=20, color=ManimColor(LOSS_COLOR)).next_to(axes.y_axis, UP, buff=0.1)

        self.play(Create(axes), Create(curve), Write(x_lbl), Write(y_lbl), run_time=1.2)

        # Ball rolling down
        start_x = 3.0
        ball = Dot(axes.c2p(start_x, start_x**2 + 0.3), color=ManimColor(BRAIN_COLOR), radius=0.18)
        ball_label = Text("Current\nweights", font_size=18, color=ManimColor(BRAIN_COLOR))
        ball_label.next_to(ball, UP+RIGHT, buff=0.1)

        self.play(FadeIn(ball), Write(ball_label))
        self.wait(0.5)

        # Step down the curve
        steps = [2.2, 1.4, 0.8, 0.3, 0.05]
        for x_val in steps:
            new_pos = axes.c2p(x_val, x_val**2 + 0.3)
            self.play(
                ball.animate.move_to(new_pos),
                ball_label.animate.next_to(new_pos, UP+RIGHT, buff=0.1),
                run_time=0.6)

        # Mark the minimum
        min_dot = Dot(axes.c2p(0, 0.3), color=ManimColor(RIGHT_COLOR), radius=0.15)
        min_label = Text("Minimum Loss\n= Best Weights!", font_size=20, color=ManimColor(RIGHT_COLOR))
        min_label.next_to(axes.c2p(0, 0.3), DOWN+RIGHT, buff=0.2)
        self.play(FadeIn(min_dot), Write(min_label))
        self.wait(1)

        explain = Text(
            "Each step: nudge the weights slightly\nin the direction that reduces loss.",
            font_size=24, color=GREY_A, line_spacing=1.4)
        explain.to_edge(DOWN, buff=0.3)
        self.play(Write(explain))
        self.wait(2)

        self.play(FadeOut(VGroup(header, axes, curve, x_lbl, y_lbl,
                                  ball, ball_label, min_dot, min_label, explain)))

    # ──────────────────────────────────────────────────────────────────────────
    # 6. THE FULL TRAINING LOOP
    # ──────────────────────────────────────────────────────────────────────────
    def _part6_the_loop(self):
        header = Text("The Training Loop", font_size=36, color=HIGHLIGHT)
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        # 4 steps in a cycle
        steps = [
            ("1. Feed data", ManimColor(DATA_COLOR)),
            ("2. Make prediction", ManimColor(PRED_COLOR)),
            ("3. Measure loss", ManimColor(LOSS_COLOR)),
            ("4. Adjust weights", ManimColor(WEIGHT_COLOR)),
        ]

        boxes = VGroup()
        positions = [UP*1.5, RIGHT*3.5, DOWN*1.5, LEFT*3.5]
        for i, ((txt, col), pos) in enumerate(zip(steps, positions)):
            box = RoundedRectangle(width=2.6, height=0.9, corner_radius=0.2,
                                   color=col, fill_color=ManimColor("#0d0d1a"), fill_opacity=1,
                                   stroke_width=2.5).move_to(pos)
            lbl = Text(txt, font_size=22, color=col).move_to(box)
            boxes.add(VGroup(box, lbl))

        # Draw boxes
        for b in boxes:
            self.play(FadeIn(b), run_time=0.4)

        # Draw cycle arrows
        arrows = VGroup()
        for i in range(4):
            src = boxes[i][0].get_center()
            dst = boxes[(i+1) % 4][0].get_center()
            mid = (src + dst) / 2
            arr = CurvedArrow(
                boxes[i][0].get_center(),
                boxes[(i+1)%4][0].get_center(),
                angle=-0.4, color=GREY_B, stroke_width=2)
            arrows.add(arr)

        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.2))
        self.wait(0.5)

        # Repeat label
        repeat = Text("Repeat thousands of times →\nModel gets smarter each loop!",
                      font_size=26, color=WHITE, line_spacing=1.4)
        repeat.to_edge(DOWN, buff=0.4)
        self.play(Write(repeat))

        # Flash loop a few times
        for _ in range(2):
            for b in boxes:
                self.play(b[0].animate.set_stroke(width=5), run_time=0.15)
                self.play(b[0].animate.set_stroke(width=2.5), run_time=0.15)

        self.wait(2)
        self.play(FadeOut(VGroup(header, boxes, arrows, repeat)))

    # ──────────────────────────────────────────────────────────────────────────
    # 7. OVERFITTING HINT
    # ──────────────────────────────────────────────────────────────────────────
    def _part7_overfitting_hint(self):
        header = Text("One Trap: Overfitting", font_size=34, color=ManimColor(LOSS_COLOR))
        header.to_edge(UP, buff=0.4)
        self.play(Write(header))

        analogy = Text(
            "Imagine a student who memorizes\nall the exam answers by heart —",
            font_size=30, color=WHITE, line_spacing=1.4)
        analogy.shift(UP*0.8)
        self.play(Write(analogy))
        self.wait(0.8)

        result = Text(
            "but fails on any NEW question.",
            font_size=34, color=ManimColor(LOSS_COLOR), weight=BOLD)
        result.next_to(analogy, DOWN, buff=0.5)
        self.play(Write(result))
        self.wait(1)

        fix = Text(
            "Solution: test the model on data it has NEVER seen.\nIf it still works → it actually learned.",
            font_size=26, color=ManimColor(DATA_COLOR), line_spacing=1.4)
        fix.next_to(result, DOWN, buff=0.6)
        self.play(Write(fix))
        self.wait(2.5)

        self.play(FadeOut(VGroup(header, analogy, result, fix)))

    # ──────────────────────────────────────────────────────────────────────────
    # 8. FINALE
    # ──────────────────────────────────────────────────────────────────────────
    def _finale(self):
        title = Text("So... How does AI learn?", font_size=42, color=HIGHLIGHT)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        summary = VGroup(
            Text("① Start with random weights (bad guesses)", font_size=28, color=GREY_A),
            Text("② Feed it labeled data", font_size=28, color=ManimColor(DATA_COLOR)),
            Text("③ Measure how wrong it is  (loss)", font_size=28, color=ManimColor(LOSS_COLOR)),
            Text("④ Nudge weights to reduce loss  (gradient descent)", font_size=28, color=ManimColor(WEIGHT_COLOR)),
            Text("⑤ Repeat millions of times", font_size=28, color=ManimColor(BRAIN_COLOR)),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).shift(DOWN*0.2)

        for line in summary:
            self.play(FadeIn(line, shift=RIGHT*0.3), run_time=0.6)
            self.wait(0.2)

        self.wait(1)

        final = Text("That's it. That's how AI learns.", font_size=38, color=HIGHLIGHT, weight=BOLD)
        final.next_to(summary, DOWN, buff=0.6)
        self.play(Write(final))
        self.play(Wiggle(final, scale_value=1.1, n_wiggles=2))
        self.wait(3)