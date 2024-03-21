import numpy as np
from manim import *


class LeastSquares(MovingCameraScene):
    def construct(self):
        self.next_section("Intro", skip_animations=False)

        self.camera.frame_center = 3 * UP + 3 * RIGHT
        plane = NumberPlane(
            x_range=[-20, 20, 1],
            y_range=[-20, 20, 1],
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            },
            axis_config={"color": WHITE},
        )
        self.play(Create(plane))

        A = (
            MathTex(r"A = \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix}")
            .set_color(YELLOW)
            .move_to(6 * UP + 8 * RIGHT)
        )

        self.play(Write(A))
        self.wait()

        self.next_section("Random vectors to Im A", skip_animations=False)

        vectors = [
            Vector([-1, 1], color=RED, tip_length=0.2),
            Vector([2, 2], color=RED, tip_length=0.2),
            Vector([1, 3], color=RED, tip_length=0.2),
        ]
        vector_labels = [
            MathTex(r"v_1", color=RED, font_size=32)
            .next_to(vectors[0].get_end(), UP)
            .add_updater(lambda m: m.next_to(vectors[0].get_end(), UP)),
            MathTex(r"v_2", color=RED, font_size=32)
            .next_to(vectors[1].get_end(), UP)
            .add_updater(lambda m: m.next_to(vectors[1].get_end(), UP)),
            MathTex(r"v_3", color=RED, font_size=32)
            .next_to(vectors[2].get_end(), DOWN)
            .add_updater(lambda m: m.next_to(vectors[2].get_end(), UP)),
        ]

        self.play(*[Create(v) for v in vectors])
        self.play(*[Write(l) for l in vector_labels])

        self.wait()

        new_vectors = [
            Vector([-1, 0], color=YELLOW, tip_length=0.2),
            Vector([2, 0], color=YELLOW, tip_length=0.2),
            Vector([1, 0], color=YELLOW, tip_length=0.2),
        ]
        new_labels = [
            MathTex(r"Av_1", color=YELLOW, font_size=32)
            .next_to(new_vectors[0].get_end(), UP)
            .add_updater(lambda m: m.next_to(new_vectors[0].get_end(), UP)),
            MathTex(r"Av_2", color=YELLOW, font_size=32)
            .next_to(new_vectors[1].get_end(), UP)
            .add_updater(lambda m: m.next_to(new_vectors[1].get_end(), UP)),
            MathTex(r"Av_3", color=YELLOW, font_size=32)
            .next_to(new_vectors[2].get_end(), DOWN)
            .add_updater(lambda m: m.next_to(new_vectors[2].get_end(), UP)),
        ]
        self.play(
            *[ReplacementTransform(v, nv) for v, nv in zip(vectors, new_vectors)],
            *[ReplacementTransform(l, nl) for l, nl in zip(vector_labels, new_labels)],
        )

        self.wait()

        imA = Line(
            start=5 * LEFT,
            end=10 * RIGHT,
            color=YELLOW,
            stroke_width=4,
        )
        imA_label = MathTex(r"\mathrm{im}\,A", color=YELLOW).next_to(
            imA.get_end(), UL, buff=0.3
        )

        self.play(
            *[FadeOut(nv) for nv in new_vectors],
            *[FadeOut(nl) for nl in new_labels],
            Create(imA),
            Write(imA_label),
        )

        self.next_section("Least squares", skip_animations=False)

        b = Vector([3, 3], color=TEAL, tip_length=0.2)
        b_label = MathTex(r"b", color=TEAL, font_size=48).next_to(b.get_end(), UP)
        b_text = MathTex(
            r"b = \begin{pmatrix} 3 \\ 3 \end{pmatrix}", color=TEAL
        ).move_to(6 * UP + 8 * RIGHT)

        self.play(
            AnimationGroup(A.animate.shift(2.5 * LEFT), Write(b_text), lag_ratio=0.2)
        )
        self.play(Create(b), Write(b_label))

        self.wait()

        b_dot = Dot(b.get_end(), radius=0.12, color=TEAL)
        self.play(Transform(b, b_dot))

        self.wait()

        Ax = Vector([1.5, 0], color=PINK, tip_length=0.2)
        Ax_label = (
            MathTex(r"A\hat{x}", color=PINK, font_size=48)
            .next_to(Ax.get_end(), DOWN)
            .add_updater(lambda m: m.next_to(Ax.get_end(), DOWN))
        )

        self.play(Create(Ax), Write(Ax_label))

        Ax_dot = Dot(Ax.get_end(), radius=0.12, color=PINK)
        self.play(Transform(Ax, Ax_dot))

        Ax_b = DashedLine(
            Ax.get_end(), b.get_end(), color=WHITE, stroke_width=4, z_index=-1
        ).add_updater(lambda m: m.put_start_and_end_on(Ax.get_end(), b.get_end()))
        Ax_b_label = MathTex(r"\| A\hat{x} - b \|", color=WHITE).add_updater(
            lambda m: m.next_to(Ax_b.get_center(), RIGHT, buff=0.2)
        )

        self.play(Create(Ax_b), Write(Ax_b_label))

        self.wait()

        d = (
            DecimalNumber(0, num_decimal_places=2, color=WHITE)
            .next_to(Ax_b.get_center(), RIGHT, buff=0.2)
            .add_updater(
                lambda m: m.set_value(
                    np.linalg.norm(
                        np.array((Ax.get_end()[0], Ax.get_end()[1]))
                        - np.array((b.get_end()[0], b.get_end()[1]))
                    )
                ).next_to(Ax_b.get_center(), RIGHT, buff=0.2)
            )
        )
        self.play(FadeOut(Ax_b_label), Write(d))

        self.next_section("Moving Ax", skip_animations=False)

        self.play(Ax.animate.shift(4 * RIGHT), run_time=2)
        self.wait()
        self.play(Ax.animate.shift(2 * LEFT), run_time=2)
        self.play(Ax.animate.move_to([3, 0, 0]), run_time=2)

        self.wait()

        Ax_label.generate_target()
        Ax_label.target = MathTex(r"A^TA\hat{x}", color=PINK, font_size=48).next_to(
            Ax.get_end(), DOWN
        )
        self.play(MoveToTarget(Ax_label))

        b.generate_target()
        b.target = Dot([3, 0, 0], radius=0.17, color=TEAL)

        self.play(MoveToTarget(b), FadeOut(d), FadeOut(b_label))

        Ax_b.suspend_updating()

        Ax_label.generate_target()
        Ax_label.target = MathTex(
            r"A^T \! A\hat{x}", r"=", r"A^Tb", font_size=48
        ).next_to(Ax.get_end(), DOWN)
        Ax_label.target[0].set_color(PINK)
        Ax_label.target[1].set_color(WHITE)
        Ax_label.target[2].set_color(TEAL)

        self.play(MoveToTarget(Ax_label))

        self.wait()
