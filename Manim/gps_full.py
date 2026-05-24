# Copy and paste this exact block into your Google Colab cell.
# The custom resolution flags are now hardcoded into the command line correctly.


from manim import *

class BootstrapParadox(Scene):
    def construct(self):
        # =================================================================
        # ACT 1: THE HOOK & THE CRISIS (0:00 - 0:15)
        # =================================================================
        title = Text("The Time Travel\nParadox", color=RED, alignment="center").scale(0.6)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1.5)

        # Create a vertical timeline line showing Past vs Future
        timeline = Line(start=UP * 1.5, end=DOWN * 1.8, color=GRAY_B)
        
        past_marker = Dot(point=UP * 1.0, color=BLUE)
        past_text = Text("1800: Vienna\n(No Beethoven!)", color=BLUE, alignment="center").scale(0.4)
        past_text.next_to(past_marker, LEFT, buff=0.3)
        
        future_marker = Dot(point=DOWN * 1.0, color=PURPLE)
        future_text = Text("2026: You Buy\nThe Music Book", color=PURPLE, alignment="center").scale(0.4)
        future_text.next_to(future_marker, LEFT, buff=0.3)

        self.play(Create(timeline))
        self.play(FadeIn(past_marker), Write(past_text))
        self.play(FadeIn(future_marker), Write(future_text))
        self.wait(3.0) 

        # =================================================================
        # ACT 2: THE RECOGNIZABLE MUSIC BOOK ASSET (0:15 - 0:30)
        # =================================================================
        # Drawing an unmistakable book with horizontal musical staff lines inside
        book_outline = Rectangle(width=1.2, height=1.6, color=GOLD, stroke_width=4)
        book_outline.set_fill(BLACK, opacity=0.9)
        
        staff_lines = VGroup(*[
            Line(start=LEFT * 0.4, end=RIGHT * 0.4, color=WHITE, stroke_width=1).shift(UP * y)
            for y in [0.3, 0.0, -0.3]
        ])
        staff_lines.move_to(book_outline.get_center())
        
        notes = VGroup(
            Dot(point=staff_lines.get_start() + RIGHT * 0.2, radius=0.05, color=GOLD),
            Dot(point=staff_lines.get_center(), radius=0.05, color=GOLD),
            Dot(point=staff_lines.get_end() - RIGHT * 0.2, radius=0.05, color=GOLD)
        )
        
        # Combine into a highly recognizable Music Book asset
        music_book = VGroup(book_outline, staff_lines, notes)
        
        # Spawn the book in the future next to the marker
        music_book.move_to(DOWN * 1.0 + RIGHT * 0.9)
        self.play(FadeIn(music_book, shift=UP))
        self.wait(2.0)

        # Animate TIME TRAVEL: The book travels UP the timeline into the past!
        self.play(
            music_book.animate.move_to(UP * 1.0 + RIGHT * 0.9),
            run_time=2.5,
            rate_func=smooth 
        )
        self.play(Flash(music_book, color=GOLD, num_lines=12, flash_radius=0.6))
        self.wait(3.0) 

        # =================================================================
        # ACT 3: THE INFINITE CLOSED LOOP (0:30 - 0:45)
        # =================================================================
        loop_title = Text("The Closed Loop", color=GOLD).scale(0.65).to_edge(UP, buff=0.4)
        
        self.play(
            FadeOut(past_text), FadeOut(past_marker),
            FadeOut(future_text), FadeOut(future_marker),
            FadeOut(timeline),
            Transform(title, loop_title)
        )

        # Create a massive circular track in the center of the viewport
        center_loop = Circle(radius=1.3, color=BLUE_E, stroke_width=6)
        center_loop.shift(DOWN * 0.2)
        
        self.play(Create(center_loop))
        self.wait(1.0)

        # Snap the book onto the top of the loop track and scale it down slightly
        self.play(music_book.animate.move_to(center_loop.point_at_angle(PI/2)).scale(0.7))
        
        # Drive the book completely around the tracking circle to show eternity
        self.play(
            MoveAlongPath(music_book, center_loop),
            run_time=5.0,
            rate_func=linear 
        )
        self.wait(1.5)

        # =================================================================
        # ACT 4: THE BRAIN-MELTING OUTRO (0:45 - 1:00)
        # =================================================================
        # Draw a clear question banner at the bottom of the phone screen
        bottom_box = Rectangle(width=4.2, height=1.4, color=RED, stroke_width=3)
        bottom_box.to_edge(DOWN, buff=0.6)
        bottom_box.set_fill(BLACK, opacity=0.8)
        
        outro_text = Paragraph(
            "WHO ACTUALLY",
            "COMPOSED THE MUSIC?",
            alignment="center",
            color=WHITE,
            line_spacing=0.6
        ).scale(0.42).move_to(bottom_box.get_center())
        outro_text.set_color_by_text("WHO", RED)

        self.play(Create(bottom_box))
        self.play(Write(outro_text, run_time=2.0))
        
        # Final long pause so the short loops cleanly on YouTube without cutting off phrases
        self.wait(5.0)
