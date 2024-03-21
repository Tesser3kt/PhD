from manim import *
import sympy as sp


DATA = [(1, 4), (2, 2), (3, 4), (4, 7), (5, 5)]


class RegressionAnimation(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 6],
            y_range=[0, 10],
            axis_config={"color": WHITE},
        )

        dots = VGroup(*[Dot(axes.c2p(x, y), color=BLUE) for x, y in DATA])

        self.play(Create(axes))
        self.play(*[DrawBorderThenFill(dot) for dot in dots])

        self.wait()

        best_fit_line = Line(
            start=axes.c2p(-3, 1 / 5),
            end=axes.c2p(6, 13 / 2),
            color=YELLOW,
        )

        self.play(Create(best_fit_line))

        self.wait()

        x = sp.symbols("x")
        f = (7 / 10) * x + (23 / 10)
        distance_lines = VGroup(
            *[
                DashedLine(
                    dot.get_center(),
                    axes.c2p(datum[0], f.subs(x, datum[0])),
                    color=WHITE,
                    z_index=-1,
                )
                for dot, datum in zip(dots, DATA)
            ]
        )

        self.play(*[Create(line) for line in distance_lines])

        self.wait()

        distance_lines_labels = VGroup(
            *[
                MathTex(f"d_{i+1}", font_size=24).next_to(line, RIGHT, buff=0.1)
                for i, (line, datum) in enumerate(zip(distance_lines, DATA))
            ]
        )
        self.play(*[Write(label) for label in distance_lines_labels])

        self.wait()

        distance_sum_text = MathTex(r"\sum_{i=1}^{5} d_i^2 = ").move_to(
            UP * 3 + RIGHT * 5
        )
        distance_sum_value = DecimalNumber(
            sum((line.get_length() ** 2 for line in distance_lines)),
            num_decimal_places=2,
        ).next_to(distance_sum_text, RIGHT, buff=0.1)

        self.play(Write(distance_sum_text), Write(distance_sum_value))

        self.wait()

        point_labels = VGroup(
            *[
                MathTex("(x_1,y_1)", color=BLUE, font_size=36).next_to(
                    dots[0], UP, buff=0.1
                ),
                MathTex("(x_2,y_2)", color=BLUE, font_size=36).next_to(
                    dots[1], DOWN, buff=0.1
                ),
                MathTex("(x_3,y_3)", color=BLUE, font_size=36).next_to(
                    dots[2], DOWN, buff=0.1
                ),
                MathTex("(x_4,y_4)", color=BLUE, font_size=36).next_to(
                    dots[3], UP, buff=0.1
                ),
                MathTex("(x_5,y_5)", color=BLUE, font_size=36).next_to(
                    dots[4], DOWN, buff=0.1
                ),
            ]
        )

        self.play(*[Write(label) for label in point_labels])

        self.wait()

        line_label = MathTex("y = ax + b", font_size=36, color=YELLOW).next_to(
            best_fit_line.get_end(), DOWN, buff=0.2
        )

        self.play(Write(line_label))

        equations = VGroup(
            *[
                MathTex(r"ax_1 + b = y_1", font_size=36, color=TEAL).move_to(
                    UP * 3 + LEFT * 4
                ),
                MathTex(r"ax_2 + b = y_2", font_size=36, color=TEAL).move_to(
                    UP * 2.5 + LEFT * 4
                ),
                MathTex(r"ax_5 + b = y_5", font_size=36, color=TEAL).move_to(
                    UP * 1.5 + LEFT * 4
                ),
            ]
        )
        vdots = MathTex(r"\vdots", font_size=36, color=TEAL).move_to(UP * 2 + LEFT * 4)
        self.play(
            AnimationGroup(
                *[
                    ReplacementTransform(line_label.copy(), equations[i])
                    for i in range(2)
                ],
                Write(vdots),
                ReplacementTransform(line_label.copy(), equations[2]),
                lag_ratio=0.5,
            )
        )
        self.play(Circumscribe(equations, color=TEAL))

        self.wait()

        M = MathTex(
            r"\left(\begin{array}{cc|c} x_1 & 1 & y_1 \\ x_2 & 1 & y_2 \\ \vdots & \vdots & \vdots \\ x_5 & 1 & y_5 \end{array}\right)",
            color=TEAL,
            font_size=36,
        ).move_to(equations.get_center())
        self.play(ReplacementTransform(equations.add(vdots), M))

        self.wait()

        self.play(
            FadeOut(
                VGroup(
                    distance_lines,
                    distance_lines_labels,
                    distance_sum_text,
                    distance_sum_value,
                    line_label,
                    M,
                )
            )
        )

        def g(x):
            return (1 / 14) * x**2 + (19 / 70) * x + 14 / 5

        g_plot = axes.plot(g, color=RED)
        g_label = MathTex("y = ax^2 + bx + c", font_size=36, color=RED).next_to(
            g_plot.get_end(), UP + LEFT, buff=0.2
        )

        self.play(
            ReplacementTransform(best_fit_line, g_plot),
            Write(g_label),
        )

        distance_lines = VGroup(
            *[
                DashedLine(
                    dot.get_center(),
                    axes.c2p(datum[0], g(datum[0])),
                    color=WHITE,
                    z_index=-1,
                )
                for dot, datum in zip(dots, DATA)
            ]
        )
        self.play(*[Create(line) for line in distance_lines])

        distance_sum_text = MathTex(r"\sum_{i=1}^{5} d_i^2 = ").move_to(
            UP * 3 + RIGHT * 5
        )
        distance_sum_value = DecimalNumber(
            sum((line.get_length() ** 2 for line in distance_lines)),
            num_decimal_places=2,
        ).next_to(distance_sum_text, RIGHT, buff=0.1)

        self.play(Write(distance_sum_text), Write(distance_sum_value))

        self.wait()

        M = MathTex(
            r"\left(\begin{array}{ccc|c} x_1^2 & x_1 & 1 & y_1 \\ x_2^2 & x_2 & 1 & y_2 \\ \vdots & \vdots & \vdots & \vdots \\ x_5^2 & x_5 & 1 & y_5 \end{array}\right)",
            color=TEAL,
            font_size=36,
        ).move_to(equations.get_center())

        self.play(Write(M))

        self.wait()
