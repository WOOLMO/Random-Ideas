from manim import *
import numpy as np

# ─────────────────────────────────────────────
#  COLOUR PALETTE
# ─────────────────────────────────────────────
BG        = "#0D0D0D"
CREAM     = "#F5E6C8"
GOLD      = "#D4A017"
RED_DARK  = "#C0392B"
BLUE_DARK = "#1A3A5C"
BLUE_MID  = "#2471A3"
GRAY      = "#888888"
GREEN     = "#1E8449"
PURPLE    = "#6C3483"

# ─────────────────────────────────────────────
#  STICK-FIGURE BUILDER
#  Each of the 26 letters gets a UNIQUE pose via
#  arm/leg angles so the alphabet looks varied.
# ─────────────────────────────────────────────
POSES = [
    # (left_arm_angle, right_arm_angle, left_leg_angle, right_leg_angle)
    # angles relative to body vertical, in degrees
    (30,  30,  40,  40),   # A
    (60,  10,  30,  50),   # B
    (90,  30,  45,  30),   # C
    (10,  90,  30,  45),   # D
    (45,  45,  60,  20),   # E  ← most common
    (80,  80,  35,  55),   # F
    (20,  70,  55,  25),   # G
    (70,  20,  25,  55),   # H
    (90,  90,  45,  45),   # I
    (15,  60,  60,  15),   # J
    (60,  15,  15,  60),   # K
    (35,  85,  50,  20),   # L
    (85,  35,  20,  50),   # M
    (50,  50,  70,  10),   # N
    (10,  50,  50,  70),   # O
    (75,  25,  40,  60),   # P
    (25,  75,  60,  40),   # Q
    (90,  10,  30,  60),   # R
    (10,  90,  60,  30),   # S
    (55,  55,  55,  55),   # T
    (40,  80,  20,  70),   # U
    (80,  40,  70,  20),   # V
    (30,  60,  65,  15),   # W
    (60,  30,  15,  65),   # X
    (90,  60,  50,  50),   # Y
    (60,  90,  50,  50),   # Z
]

def make_dancer(letter_flag=False, color=CREAM, scale=0.55, letter_index=0):
    g = VGroup()
    la, ra, ll, rl = POSES[letter_index % 26]

    head = Circle(radius=0.18, color=color, fill_color=color, fill_opacity=1)
    head.move_to(UP * 0.75)
    body = Line(UP * 0.57, ORIGIN, color=color, stroke_width=3)

    # Legs
    leg_l = Line(ORIGIN, rotate_vector(DOWN*0.52, np.radians( ll)), color=color, stroke_width=3)
    leg_r = Line(ORIGIN, rotate_vector(DOWN*0.52, np.radians(-rl)), color=color, stroke_width=3)

    # Arms
    arm_l_end = rotate_vector(LEFT*0.38, np.radians(-la+90))
    arm_r_end = rotate_vector(RIGHT*0.38, np.radians( ra-90))
    arm_anchor = UP*0.28
    arm_l = Line(arm_anchor, arm_anchor + arm_l_end, color=color, stroke_width=3)
    arm_r = Line(arm_anchor, arm_anchor + arm_r_end, color=color, stroke_width=3)

    g.add(head, body, leg_l, leg_r, arm_l, arm_r)

    if letter_flag:
        flag = Square(side_length=0.14, color=GOLD, fill_color=GOLD, fill_opacity=1)
        flag.move_to(arm_anchor + arm_r_end + UP*0.12 + RIGHT*0.06)
        g.add(flag)

    g.scale(scale)
    return g


def letter_to_idx(ch):
    ch = ch.upper()
    if 'A' <= ch <= 'Z':
        return ord(ch) - ord('A')
    return 0


def text_to_dancers(text, scale=0.55, color=CREAM):
    text_upper = text.upper()
    row = VGroup()
    for i, ch in enumerate(text_upper):
        if ch == " ":
            spacer = Rectangle(width=0.28, height=0.1,
                                color=BG, fill_opacity=0, stroke_opacity=0)
            row.add(spacer)
        else:
            flag = (i < len(text_upper)-1 and
                    i+1 < len(text_upper) and
                    text_upper[i+1] == " ")
            d = make_dancer(letter_flag=flag, color=color,
                             scale=scale, letter_index=letter_to_idx(ch))
            row.add(d)
    row.arrange(RIGHT, buff=0.12)
    return row


def wipe(scene, t=0.45):
    if scene.mobjects:
        scene.play(FadeOut(Group(*scene.mobjects)), run_time=t)
    scene.clear()


def section_title(scene, number, name, color=GOLD):
    """Animated chapter banner."""
    bar = Rectangle(width=14, height=0.9,
                    fill_color=BLUE_DARK, fill_opacity=0.9,
                    stroke_opacity=0)
    bar.to_edge(UP, buff=0)
    txt = Text(f"Chapter {number}  ·  {name}",
               font="Georgia", color=color).scale(0.44)
    txt.move_to(bar)
    scene.play(FadeIn(bar), FadeIn(txt), run_time=0.5)
    return Group(bar, txt)


# ═══════════════════════════════════════════════════════════
#  MASTER SCENE
# ═══════════════════════════════════════════════════════════
class DancingMenFull(Scene):
    def construct(self):
        self.camera.background_color = BG
        self.ch1_hook()
        wipe(self)
        self.ch2_story()
        wipe(self)
        self.ch3_what_is_cipher()
        wipe(self)
        self.ch4_substitution_deep()
        wipe(self)
        self.ch5_frequency_analysis()
        wipe(self)
        self.ch6_flag_trick()
        wipe(self)
        self.ch7_cracking_step_by_step()
        wipe(self)
        self.ch8_full_alphabet()
        wipe(self)
        self.ch9_encode_live()
        wipe(self)
        self.ch10_real_messages()
        wipe(self)
        self.ch11_why_weak()
        wipe(self)
        self.ch12_outro()

    # ───────────────────────────────────────────
    #  CH 1 – HOOK / TITLE  (~50 s)
    # ───────────────────────────────────────────
    def ch1_hook(self):
        line_t = Line(LEFT*7, RIGHT*7, color=GOLD, stroke_width=1.5).shift(UP*3.4)
        line_b = line_t.copy().shift(DOWN*7.4)
        self.play(Create(line_t), Create(line_b), run_time=0.6)

        title = Text("The Dancing Men Cipher",
                     font="Georgia", color=GOLD).scale(1.12)
        sub = Text(
            "A Sherlock Holmes puzzle  ·  Substitution ciphers  ·  Frequency analysis",
            font="Georgia", color=CREAM).scale(0.40)
        sub.next_to(title, DOWN, buff=0.30)
        self.play(Write(title), run_time=1.8)
        self.play(FadeIn(sub, shift=UP*0.2))

        row = text_to_dancers("SHERLOCK HOLMES", scale=0.48, color=GOLD)
        row.next_to(sub, DOWN, buff=0.52)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in row],
                               lag_ratio=0.07), run_time=1.8)

        question = Text(
            "What if a criminal sent messages that looked like\n"
            "innocent children's drawings?  Holmes found out.",
            font="Georgia", color=CREAM, line_spacing=1.5
        ).scale(0.46)
        question.shift(DOWN*2.3)
        self.play(FadeIn(question, shift=UP*0.15), run_time=1.0)
        self.wait(1.2)

    # ───────────────────────────────────────────
    #  CH 2 – THE STORY  (~70 s)
    # ───────────────────────────────────────────
    def ch2_story(self):
        hdr = section_title(self, 1, "The Story — Ridling Thorpe Manor")

        # Victorian silhouette (Holmes)
        sil = VGroup()
        body  = Rectangle(width=0.55, height=1.0, color=CREAM,
                           fill_color=CREAM, fill_opacity=0.9)
        hat   = Polygon(LEFT*0.33+UP*0.50, RIGHT*0.33+UP*0.50,
                        RIGHT*0.22+UP*0.92, LEFT*0.22+UP*0.92,
                        color=CREAM, fill_color=CREAM, fill_opacity=0.9)
        head  = Circle(radius=0.21, color=CREAM,
                       fill_color=CREAM, fill_opacity=0.9).move_to(UP*0.32)
        pipe  = Line(RIGHT*0.28+UP*0.08, RIGHT*0.65+UP*0.18,
                     color=GOLD, stroke_width=4)
        sil.add(body, hat, head, pipe)
        sil.scale(0.95).shift(LEFT*5.0 + UP*0.6)
        self.play(FadeIn(sil, shift=RIGHT*0.3))

        story_lines = [
            ("1903", "Published in The Strand Magazine"),
            ("Client", "Hilton Cubitt — Norfolk country squire"),
            ("Problem", "Wife Elsie gets anonymous chalk messages"),
            ("The messages", "Look like rows of dancing stick figures"),
            ("Elsie's reaction", "She turns pale and begs Cubitt to ignore them"),
            ("Holmes's verdict", "\"These are not childish scribbles — they are code.\""),
            ("Stakes", "A criminal from Elsie's past is closing in"),
        ]
        rows = VGroup()
        for key, val in story_lines:
            k = Text(key + ":", font="Georgia", color=GOLD).scale(0.40)
            v = Text(val,       font="Georgia", color=CREAM).scale(0.38)
            r = VGroup(k, v).arrange(RIGHT, buff=0.18)
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        rows.next_to(sil, RIGHT, buff=0.55).shift(DOWN*0.2)

        for r in rows:
            self.play(FadeIn(r, shift=RIGHT*0.12), run_time=0.45)

        # First message on parchment
        parch = RoundedRectangle(width=9, height=1.35, corner_radius=0.12,
                                 color=GOLD, fill_color="#221100",
                                 fill_opacity=0.95, stroke_width=2)
        parch.shift(DOWN*3.0)
        plbl = Text("First message found on the windowsill:",
                    font="Georgia", color=GRAY).scale(0.34)
        plbl.next_to(parch, UP, buff=0.10)
        msg = text_to_dancers("AM HERE", scale=0.48, color=CREAM)
        msg.move_to(parch.get_center())
        self.play(FadeIn(parch), FadeIn(plbl))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in msg],
                               lag_ratio=0.12), run_time=1.1)
        self.wait(1.0)

    # ───────────────────────────────────────────
    #  CH 3 – WHAT IS A CIPHER?  (~60 s)
    # ───────────────────────────────────────────
    def ch3_what_is_cipher(self):
        section_title(self, 2, "What Is a Cipher?")

        defn = Text(
            "A cipher is a system for hiding the meaning of a message\n"
            "by transforming it according to a secret rule.",
            font="Georgia", color=CREAM, line_spacing=1.5
        ).scale(0.47)
        defn.shift(UP*2.5)
        self.play(Write(defn), run_time=1.5)

        # Three cipher families
        families = [
            (GOLD,     "Substitution",  "Replace each letter with a symbol or different letter"),
            (BLUE_MID, "Transposition", "Rearrange the order of letters without changing them"),
            (GREEN,    "Modern (AES)",  "Mathematical operations on blocks of bits"),
        ]
        boxes = VGroup()
        for i, (col, name, desc) in enumerate(families):
            box = RoundedRectangle(width=3.6, height=1.55, corner_radius=0.12,
                                   color=col, fill_color=col,
                                   fill_opacity=0.15, stroke_width=1.8)
            n = Text(name, font="Georgia", color=col).scale(0.44)
            d = Text(desc, font="Georgia", color=CREAM,
                     line_spacing=1.3).scale(0.32)
            d.next_to(n, DOWN, buff=0.14)
            content = VGroup(n, d)
            content.move_to(box)
            boxes.add(VGroup(box, content))
        boxes.arrange(RIGHT, buff=0.35).shift(DOWN*0.3)
        self.play(LaggedStart(*[FadeIn(b, scale=0.9) for b in boxes],
                               lag_ratio=0.2), run_time=1.2)

        arrow = Arrow(boxes[0].get_bottom()+DOWN*0.05,
                      boxes[0].get_bottom()+DOWN*0.7,
                      color=GOLD, stroke_width=2.5)
        note  = Text("← The Dancing Men uses this one",
                     font="Georgia", color=GOLD).scale(0.38)
        note.next_to(arrow, RIGHT, buff=0.15)
        self.play(GrowArrow(arrow), FadeIn(note))

        key_idea = Text(
            "Key idea: the RULE is secret, but the transformed message is visible to everyone.",
            font="Georgia", color=CREAM
        ).scale(0.38)
        key_idea.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(key_idea))
        self.wait(1.0)

    # ───────────────────────────────────────────
    #  CH 4 – SUBSTITUTION CIPHERS IN DEPTH  (~70 s)
    # ───────────────────────────────────────────
    def ch4_substitution_deep(self):
        section_title(self, 3, "Substitution Ciphers — How They Work")

        intro = Text(
            "Every letter maps to exactly one symbol.\n"
            "Same letter → same symbol, always, everywhere.",
            font="Georgia", color=CREAM, line_spacing=1.5
        ).scale(0.47)
        intro.shift(UP*2.6)
        self.play(Write(intro), run_time=1.4)

        # Live mapping: WATSON
        word = "WATSON"
        plain_grp  = VGroup()
        dancer_grp = VGroup()
        arrows     = VGroup()

        for i, ch in enumerate(word):
            pl = Text(ch, font="Georgia", color=CREAM).scale(0.80)
            pl.move_to(LEFT*2.8 + RIGHT*i*0.92 + UP*1.1)
            d  = make_dancer(color=GOLD, scale=0.52,
                              letter_index=letter_to_idx(ch))
            d.move_to(LEFT*2.8 + RIGHT*i*0.92 + DOWN*0.4)
            arr = Arrow(pl.get_bottom()+DOWN*0.04, d.get_top()+UP*0.04,
                        buff=0.04, color=GRAY, stroke_width=1.8,
                        max_tip_length_to_length_ratio=0.18)
            plain_grp.add(pl); dancer_grp.add(d); arrows.add(arr)

        plain_label  = Text("Plaintext",  font="Georgia", color=GOLD).scale(0.40)
        cipher_label = Text("Ciphertext", font="Georgia", color=GOLD).scale(0.40)
        plain_label.next_to(plain_grp,  LEFT, buff=0.3)
        cipher_label.next_to(dancer_grp, LEFT, buff=0.3)
        self.play(FadeIn(plain_label), FadeIn(cipher_label))
        for pl, arr, d in zip(plain_grp, arrows, dancer_grp):
            self.play(FadeIn(pl), GrowArrow(arr), FadeIn(d, scale=0.5), run_time=0.38)

        # Properties box
        prop = RoundedRectangle(width=9.2, height=1.05, corner_radius=0.12,
                                color=BLUE_DARK, fill_color=BLUE_DARK,
                                fill_opacity=0.55, stroke_width=1.5)
        prop.shift(DOWN*2.35)
        pt = Text(
            "Encryption: plaintext → ciphertext   |   Decryption: ciphertext → plaintext\n"
            "Key = the mapping table (which symbol = which letter)",
            font="Georgia", color=CREAM, line_spacing=1.4
        ).scale(0.36)
        pt.move_to(prop)
        self.play(FadeIn(prop), Write(pt), run_time=1.1)

        weakness = Text("⚠  Because the mapping is fixed, letter PATTERNS survive encryption.",
                        font="Georgia", color=RED_DARK).scale(0.40)
        weakness.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(weakness, scale=0.95))
        self.wait(1.0)

    # ───────────────────────────────────────────
    #  CH 5 – FREQUENCY ANALYSIS  (~80 s)
    # ───────────────────────────────────────────
    def ch5_frequency_analysis(self):
        section_title(self, 4, "Frequency Analysis — The Codebreaker's Superpower")

        intro = Text(
            "In any sufficiently long English text,\n"
            "letters appear with predictable frequencies.",
            font="Georgia", color=CREAM, line_spacing=1.5
        ).scale(0.47)
        intro.shift(UP*2.6)
        self.play(Write(intro), run_time=1.3)

        freqs = [
            ("E",12.7,GOLD),("T",9.1,CREAM),("A",8.2,CREAM),("O",7.5,CREAM),
            ("I",7.0,CREAM),("N",6.7,CREAM),("S",6.3,CREAM),("H",6.1,CREAM),
            ("R",6.0,CREAM),("D",4.3,CREAM),("L",4.0,CREAM),("U",2.8,CREAM),
        ]
        chart_o = LEFT*5.2 + DOWN*0.6
        bw, bg  = 0.50, 0.16
        maxf    = 14.0

        bars = VGroup(); labs = VGroup(); vals = VGroup()
        for i, (letter, freq, col) in enumerate(freqs):
            h = (freq/maxf)*2.8
            bar = Rectangle(width=bw, height=h,
                            color=col, fill_color=col, fill_opacity=0.88)
            bar.move_to(chart_o + RIGHT*i*(bw+bg) + UP*(h/2))
            lab = Text(letter, font="Georgia", color=CREAM).scale(0.38)
            lab.next_to(bar, DOWN, buff=0.10)
            val = Text(f"{freq}", font="Georgia", color=GRAY).scale(0.28)
            val.next_to(bar, UP, buff=0.05)
            bars.add(bar); labs.add(lab); vals.add(val)

        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars],
                               lag_ratio=0.06), run_time=1.6)
        self.play(LaggedStart(*[FadeIn(l) for l in labs], lag_ratio=0.04))
        self.play(LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.04))

        pct = Text("(%)", font="Georgia", color=GRAY).scale(0.28)
        pct.next_to(vals[0], UP, buff=0.05).shift(UP*0.15)
        self.play(FadeIn(pct))

        # Highlight E
        hl = SurroundingRectangle(bars[0], color=RED_DARK, stroke_width=2.5)
        self.play(Create(hl))
        e_ann = Text("E = 12.7 %\nMost common letter\nin English",
                     font="Georgia", color=RED_DARK, line_spacing=1.3).scale(0.36)
        e_ann.next_to(hl, RIGHT, buff=0.25)
        self.play(FadeIn(e_ann))

        # How Holmes uses this
        how = Text(
            "Strategy: count which dancer symbol appears most → that symbol = 'E'\n"
            "Then use E to anchor more guesses and unravel the whole alphabet.",
            font="Georgia", color=CREAM, line_spacing=1.4
        ).scale(0.38)
        how.to_edge(DOWN, buff=0.45)
        self.play(Write(how), run_time=1.4)
        self.wait(1.0)

    # ───────────────────────────────────────────
    #  CH 6 – THE FLAG TRICK  (~60 s)
    # ───────────────────────────────────────────
    def ch6_flag_trick(self):
        section_title(self, 5, "The Flag Trick — Word Boundaries")

        expl = Text(
            "Doyle built a clever extra clue into the cipher:\n"
            "the last dancer of each word holds a tiny flag.",
            font="Georgia", color=CREAM, line_spacing=1.5
        ).scale(0.47)
        expl.shift(UP*2.6)
        self.play(Write(expl), run_time=1.4)

        phrase = "COME HERE"
        words  = phrase.split()
        dancer_row = VGroup()
        plain_row  = VGroup()
        for word in words:
            for ci, ch in enumerate(word):
                flag = (ci == len(word)-1)
                d = make_dancer(letter_flag=flag, color=CREAM, scale=0.60,
                                 letter_index=letter_to_idx(ch))
                dancer_row.add(d)
                pl = Text(ch, font="Georgia", color=GOLD).scale(0.44)
                plain_row.add(pl)
        dancer_row.arrange(RIGHT, buff=0.22).shift(UP*0.6)
        for d, pl in zip(dancer_row, plain_row):
            pl.next_to(d, DOWN, buff=0.18)

        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dancer_row],
                               lag_ratio=0.10), run_time=1.4)
        self.play(LaggedStart(*[FadeIn(pl) for pl in plain_row], lag_ratio=0.08))

        # Flag callout arrows
        flag_dancers = [dancer_row[3], dancer_row[7]]  # last of COME, last of HERE
        for fd in flag_dancers:
            arr = Arrow(fd.get_top()+UP*0.6, fd.get_top()+UP*0.1,
                        color=GOLD, stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.25)
            lbl = Text("flag →\nword end", font="Georgia",
                       color=GOLD, line_spacing=1.2).scale(0.32)
            lbl.next_to(arr, UP, buff=0.05)
            self.play(GrowArrow(arr), FadeIn(lbl), run_time=0.5)

        # Braces
        b1 = Brace(dancer_row[:4], DOWN, color=GOLD)
        t1 = b1.get_text('"COME" — 4 letters').set_color(GOLD).scale(0.44)
        b2 = Brace(dancer_row[4:], DOWN, color=BLUE_MID)
        t2 = b2.get_text('"HERE" — 4 letters').set_color(CREAM).scale(0.44)
        self.play(GrowFromCenter(b1), FadeIn(t1))
        self.play(GrowFromCenter(b2), FadeIn(t2))

        insight = Text(
            "Knowing word lengths is huge — short words (A, I, AM, AT, IS, THE)\n"
            "can be guessed directly, immediately revealing 2-3 letters for free.",
            font="Georgia", color=CREAM, line_spacing=1.4
        ).scale(0.38)
        insight.to_edge(DOWN, buff=0.45)
        self.play(Write(insight), run_time=1.3)
        self.wait(1.0)

    # ───────────────────────────────────────────
    #  CH 7 – CRACKING STEP BY STEP  (~90 s)
    # ───────────────────────────────────────────
    def ch7_cracking_step_by_step(self):
        section_title(self, 6, "Holmes Cracks the Code — Step by Step")

        steps = [
            (GOLD,     "Step 1 — Collect all messages",
             "Holmes waits for Cubitt to bring every scrap of paper."),
            (GOLD,     "Step 2 — Count symbol frequencies",
             "15 messages, 160 symbols. The most common symbol: ♦  (appears 23×)"),
            (CREAM,    "Step 3 — Assign E",
             "♦ = E. Now every ♦ in every message is replaced with 'E'."),
            (CREAM,    "Step 4 — Use flags for word structure",
             "A 1-letter flagged word = 'A' or 'I'. A 3-letter: THE, AND, etc."),
            (BLUE_MID, "Step 5 — Guess common words",
             "A 3-letter group ending in known E: _ _ E → THE, ARE, HE, SHE…"),
            (BLUE_MID, "Step 6 — Bootstrap the alphabet",
             "Each confirmed letter unlocks more words. Momentum builds fast."),
            (GREEN,    "Step 7 — Full plaintext",
             "\"COME HERE AT ONCE\" — Holmes now knows who sent it."),
            (GREEN,    "Step 8 — Holmes acts",
             "He lures the criminal (Abe Slaney) into a trap. Case closed."),
        ]

        for i, (col, label, desc) in enumerate(steps):
            lbl  = Text(label, font="Georgia", color=col).scale(0.40)
            dt   = Text(desc,  font="Georgia", color=CREAM).scale(0.36)
            row  = VGroup(lbl, dt).arrange(RIGHT, buff=0.22)
            row.move_to(UP*(2.8 - i*0.72) + LEFT*0.2)
            self.play(FadeIn(row, shift=RIGHT*0.15), run_time=0.50)

        # Final decoded banner
        banner = RoundedRectangle(width=9.4, height=1.05, corner_radius=0.12,
                                  color=GOLD, fill_color="#1A0E00",
                                  fill_opacity=1, stroke_width=2)
        banner.to_edge(DOWN, buff=0.28)
        decoded = Text("COME HERE AT ONCE  —  ABE SLANEY",
                       font="Georgia", color=GOLD).scale(0.52)
        decoded.move_to(banner)
        self.play(FadeIn(banner))
        self.play(Write(decoded), run_time=1.3)
        self.wait(1.1)

    # ───────────────────────────────────────────
    #  CH 8 – FULL ALPHABET GRID  (~60 s)
    # ───────────────────────────────────────────
    def ch8_full_alphabet(self):
        section_title(self, 7, "The Complete 26-Symbol Alphabet")

        note = Text(
            "After cracking the cipher, Holmes reconstructed every symbol.\n"
            "Here is the full Dancing Men alphabet — each pose = one letter.",
            font="Georgia", color=CREAM, line_spacing=1.5
        ).scale(0.43)
        note.shift(UP*2.7)
        self.play(Write(note), run_time=1.3)

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        grid = VGroup()
        for ch in letters:
            d = make_dancer(color=GOLD, scale=0.38, letter_index=letter_to_idx(ch))
            l = Text(ch, font="Georgia", color=CREAM).scale(0.34)
            l.next_to(d, DOWN, buff=0.07)
            grid.add(VGroup(d, l))
        grid.arrange_in_grid(rows=2, cols=13, buff=(0.22, 0.40))
        grid.shift(DOWN*0.52)

        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in grid],
                               lag_ratio=0.03), run_time=2.4)

        # Highlight E and T (the two most common)
        for idx, lbl_txt, col in [(4,"E — most common",RED_DARK),(19,"T — second",BLUE_MID)]:
            rect = SurroundingRectangle(grid[idx], color=col, stroke_width=2.5)
            lbl  = Text(lbl_txt, font="Georgia", color=col).scale(0.34)
            lbl.next_to(rect, DOWN, buff=0.15)
            self.play(Create(rect), FadeIn(lbl), run_time=0.5)

        self.wait(1.0)

    # ───────────────────────────────────────────
    #  CH 9 – LIVE ENCODING  (~70 s)
    # ───────────────────────────────────────────
    def ch9_encode_live(self):
        section_title(self, 8, "Encode a Message — Try It Yourself")

        prompt = Text("Let's encrypt the phrase:  WATSON HELP",
                      font="Georgia", color=CREAM).scale(0.50)
        prompt.shift(UP*2.6)
        self.play(Write(prompt), run_time=0.9)

        message = "WATSON HELP"
        plain_title  = Text("Plaintext →", font="Georgia", color=GOLD).scale(0.42)
        cipher_title = Text("Ciphertext →", font="Georgia", color=GOLD).scale(0.42)
        plain_title.shift(LEFT*5.5 + UP*1.2)
        cipher_title.shift(LEFT*5.5 + DOWN*0.3)
        self.play(FadeIn(plain_title), FadeIn(cipher_title))

        plain_row  = VGroup()
        dancer_row = VGroup()
        for ch in message:
            if ch == " ":
                sp = Rectangle(width=0.30, height=0.05,
                                fill_opacity=0, stroke_opacity=0)
                plain_row.add(sp.copy())
                dancer_row.add(sp.copy())
            else:
                pl = Text(ch, font="Georgia", color=CREAM).scale(0.72)
                d  = make_dancer(color=GOLD, scale=0.50,
                                  letter_index=letter_to_idx(ch))
                plain_row.add(pl)
                dancer_row.add(d)
        plain_row.arrange(RIGHT, buff=0.10).shift(UP*1.2 + RIGHT*0.8)
        dancer_row.arrange(RIGHT, buff=0.10).shift(DOWN*0.3 + RIGHT*0.8)

        self.play(LaggedStart(*[FadeIn(p) for p in plain_row], lag_ratio=0.07),
                  run_time=0.8)
        arrows = VGroup()
        for p, d in zip(plain_row, dancer_row):
            if abs(p.width - 0.30) < 0.01:
                continue
            arr = Arrow(p.get_bottom()+DOWN*0.05, d.get_top()+UP*0.05,
                        buff=0.03, color=GRAY, stroke_width=1.6,
                        max_tip_length_to_length_ratio=0.18)
            arrows.add(arr)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.07),
                  run_time=0.8)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dancer_row],
                               lag_ratio=0.07), run_time=0.8)

        # Decrypt demonstration
        decrypt_note = Text(
            "To decrypt: look up each dancer in the key table → read the letters.",
            font="Georgia", color=CREAM).scale(0.38)
        decrypt_note.shift(DOWN*1.9)
        self.play(FadeIn(decrypt_note))

        tip = Text(
            "Without the key table, an outsider just sees  'dancing men' — harmless doodles.",
            font="Georgia", color=GRAY, slant=ITALIC).scale(0.36)
        tip.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(tip))
        self.wait(1.1)

    # ───────────────────────────────────────────
    #  CH 10 – REAL MESSAGES FROM THE STORY  (~65 s)
    # ───────────────────────────────────────────
    def ch10_real_messages(self):
        section_title(self, 9, "The Real Messages in the Story")

        intro = Text(
            "There are five distinct messages in the story.\n"
            "Here is how Holmes decoded each one:",
            font="Georgia", color=CREAM, line_spacing=1.5
        ).scale(0.46)
        intro.shift(UP*2.6)
        self.play(Write(intro), run_time=1.2)

        messages = [
            ("Message 1", "AM HERE  ABE SLANEY",     "Slaney announces his arrival"),
            ("Message 2", "AT ELRIGE",                "A meeting place in the village"),
            ("Message 3", "COME ELSIE",               "Slaney calling Elsie to flee"),
            ("Message 4", "NEVER",                    "Elsie refuses to go with him"),
            ("Message 5", "ELSIE PREPARE TO MEET",    "A deadly threat — Cubitt is shot"),
        ]
        rows = VGroup()
        for num, plain, meaning in messages:
            n = Text(num + ":", font="Georgia", color=GOLD).scale(0.38)
            p = Text(plain,    font="Georgia", color=CREAM).scale(0.36)
            m = Text("→  " + meaning, font="Georgia", color=GRAY, slant=ITALIC).scale(0.33)
            row = VGroup(n, p, m).arrange(RIGHT, buff=0.18)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.30).shift(UP*0.3)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT*0.12), run_time=0.48)

        # Show message 3 as dancers
        parch = RoundedRectangle(width=6.5, height=1.2, corner_radius=0.10,
                                 color=GOLD, fill_color="#1A0E00",
                                 fill_opacity=0.95, stroke_width=2)
        parch.to_edge(DOWN, buff=0.35)
        m3 = text_to_dancers("COME ELSIE", scale=0.46, color=GOLD)
        m3.move_to(parch)
        lbl3 = Text("Message 3 in Dancing Men:", font="Georgia",
                    color=GRAY).scale(0.33)
        lbl3.next_to(parch, UP, buff=0.08)
        self.play(FadeIn(parch), FadeIn(lbl3))
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in m3],
                               lag_ratio=0.10), run_time=1.0)
        self.wait(1.0)

    # ───────────────────────────────────────────
    #  CH 11 – WHY IT FAILS  (~65 s)
    # ───────────────────────────────────────────
    def ch11_why_weak(self):
        section_title(self, 10, "Security in Hindsight — Why It Fails")

        title2 = Text("The cipher is elegant fiction — but terrible security.",
                      font="Georgia", color=RED_DARK).scale(0.50)
        title2.shift(UP*2.5)
        self.play(Write(title2), run_time=1.0)

        weaknesses = [
            ("✗ No secret key",       "The mapping never changes — anyone with the table can read any message."),
            ("✗ Frequency attack",    "English stats + 160 symbols → solved in < 5 minutes by hand."),
            ("✗ Flag leakage",        "Word boundaries reduce guessing enormously."),
            ("✗ Tiny key space",      "26! ≈ 4 × 10²⁶ — sounds big, but cribs make it trivial."),
            ("✗ No diffusion",        "One letter change → one symbol change. No cascading effect."),
            ("✗ Known-plaintext",     "One confirmed word breaks open the rest of the alphabet."),
        ]
        rows = VGroup()
        for label, desc in weaknesses:
            l = Text(label, font="Georgia", color=RED_DARK).scale(0.38)
            d = Text(desc,  font="Georgia", color=CREAM).scale(0.34)
            row = VGroup(l, d).arrange(RIGHT, buff=0.20)
            rows.add(row)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.27).shift(UP*0.35)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT*0.12), run_time=0.48)

        # Comparison to modern crypto
        comp = RoundedRectangle(width=9.4, height=0.90, corner_radius=0.12,
                                color=GREEN, fill_color=GREEN,
                                fill_opacity=0.12, stroke_width=1.5)
        comp.to_edge(DOWN, buff=0.35)
        ct = Text(
            "Modern AES-256: 2²⁵⁶ possible keys ≈ atoms in the observable universe — unbreakable by brute force.",
            font="Georgia", color=GREEN
        ).scale(0.34)
        ct.move_to(comp)
        self.play(FadeIn(comp), Write(ct), run_time=1.2)
        self.wait(1.0)

    # ───────────────────────────────────────────
    #  CH 12 – OUTRO / RECAP  (~55 s)
    # ───────────────────────────────────────────
    def ch12_outro(self):
        title = Text("Recap", font="Georgia", color=GOLD).scale(0.82)
        title.shift(UP*3.2)
        self.play(Write(title))

        recap = [
            "The Dancing Men is a simple monoalphabetic substitution cipher",
            "Each of 26 stick-figure poses encodes exactly one letter",
            "Flags on raised arms mark the end of each word",
            "Holmes used frequency analysis — E is the key anchor",
            "Short flagged words (A, I, AM) give free letters instantly",
            "He decoded five messages and unmasked Abe Slaney",
            "Beautiful in fiction — far too weak for real secrecy",
        ]
        bullets = VGroup()
        for item in recap:
            dot  = Dot(color=GOLD, radius=0.07)
            text = Text(item, font="Georgia", color=CREAM).scale(0.40)
            row  = VGroup(dot, text).arrange(RIGHT, buff=0.22)
            bullets.add(row)
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.28).shift(UP*0.55)
        for b in bullets:
            self.play(FadeIn(b, shift=UP*0.08), run_time=0.45)

        # Final dancing men row
        final = text_to_dancers("ELEMENTARY", scale=0.50, color=GOLD)
        final.shift(DOWN*2.6)
        quote = Text('"Elementary, my dear Watson."',
                     font="Georgia", color=GRAY, slant=ITALIC).scale(0.44)
        quote.next_to(final, DOWN, buff=0.30)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in final],
                               lag_ratio=0.08), run_time=1.2)
        self.play(FadeIn(quote))
        self.wait(1.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)


# ── Individual scene shortcuts (for testing) ───────────────
for _name, _method in [
    ("S1",  "ch1_hook"), ("S2",  "ch2_story"),
    ("S3",  "ch3_what_is_cipher"), ("S4",  "ch4_substitution_deep"),
    ("S5",  "ch5_frequency_analysis"), ("S6",  "ch6_flag_trick"),
    ("S7",  "ch7_cracking_step_by_step"), ("S8",  "ch8_full_alphabet"),
    ("S9",  "ch9_encode_live"), ("S10", "ch10_real_messages"),
    ("S11", "ch11_why_weak"), ("S12", "ch12_outro"),
]:
    def _make(m):
        class _S(DancingMenFull):
            def construct(self):
                self.camera.background_color = BG
                getattr(self, m)()
        return _S
    globals()[_name] = _make(_method)