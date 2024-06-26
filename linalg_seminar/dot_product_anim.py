import numpy as np
from manim import *

from dot_product_config import *


class DotProduct(MovingCameraScene):
    def get_axes(self):
        axes = Axes(
            x_range=[-6, 6],
            y_range=[-3, 3],
            axis_config={"color": Colors.axes, "stroke_width": 1},
        )
        return axes.set_opacity(0.75)

    def get_vectors(self, axes):
        vectors = VGroup(
            Vector(
                axes.coords_to_point(-2, 0.5),
                color=Colors.vectors,
                tip_length=General.tip_length,
            ),
            Vector(
                axes.coords_to_point(3, 2),
                color=Colors.vectors,
                tip_length=General.tip_length,
            ),
            Vector(
                axes.coords_to_point(3.5, -2),
                color=Colors.vectors,
                tip_length=General.tip_length,
            ),
            Vector(
                axes.coords_to_point(-1, -1),
                color=Colors.vectors,
                tip_length=General.tip_length,
            ),
            Vector(
                axes.coords_to_point(1, 1),
                color=Colors.vectors,
                tip_length=General.tip_length,
            ),
            Vector(
                axes.coords_to_point(-3, 1),
                color=Colors.vectors,
                tip_length=General.tip_length,
            ),
        )

        return vectors

    def construct(self):
        # Vectors to Dots
        self.next_section(name="Many Dots", skip_animations=SkipScene.many_dots)

        axes = self.get_axes()
        self.play(Create(axes))

        vectors = self.get_vectors(axes)
        self.play(Create(vectors))

        dots = VGroup(*[Dot(v.get_end(), color=Colors.vectors) for v in vectors])

        self.wait()

        self.play(*[Transform(vectors[i], dots[i]) for i in range(len(vectors))])

        self.wait()

        # Projection Line
        self.next_section(
            name="Projection Line", skip_animations=SkipScene.projection_line
        )

        u = Vector(
            axes.coords_to_point(np.sqrt(3) / 2, 1 / 2),
            color=Colors.projection_line,
            tip_length=General.tip_length,
        )
        self.play(FadeIn(u))

        u_label = MathTex("\\mathbf{u}", color=Colors.projection_line).next_to(
            u.get_end(), direction=LEFT, buff=0.4
        )
        self.play(Write(u_label))

        u_line = Line(
            -5 * u.get_end(),
            5 * u.get_end(),
            color=Colors.projection_line,
            stroke_width=2,
        )
        self.play(Create(u_line))

        self.wait()

        # Perpendicular lines and projections
        self.next_section(
            name="Perpendicular Lines", skip_animations=SkipScene.perpendicular_lines
        )

        dot_projections = VGroup(
            *[
                Dot(u_line.get_projection(d.get_center()), color=Colors.projections)
                for d in dots
            ]
        )
        perp_lines = VGroup(
            *[
                DashedLine(
                    dots[i].get_center(),
                    dot_projections[i].get_center(),
                    color=Colors.vectors,
                )
                for i in range(len(dots))
            ]
        )
        self.play(*[Create(line) for line in perp_lines])

        self.wait()

        self.play(*[Transform(dots[i], dot_projections[i]) for i in range(len(dots))])

        self.wait()

        # Zoom in scene
        self.next_section(name="Zoom In", skip_animations=SkipScene.zoom_in)

        self.play(
            *[FadeOut(perp_lines[i]) for i in range(1, len(perp_lines))],
            *[FadeOut(dots[i]) for i in range(1, len(dots))],
            *[FadeOut(vectors[i]) for i in range(1, len(vectors))]
        )

        self.camera.frame.save_state()
        self.play(
            self.camera.frame.animate.set(width=10).move_to(dots[0].get_center()),
        )

        self.wait()

        # Dot back to vector
        self.next_section(
            name="Dot Back to Vector", skip_animations=SkipScene.dot_vector
        )

        v = vectors[0]
        self.play(
            Transform(
                v,
                Vector(
                    v.get_end(), color=Colors.vectors, tip_length=General.tip_length
                ),
            )
        )

        v_label = MathTex("\\mathbf{v}", color=Colors.vectors).next_to(
            v.get_center(), direction=UR, buff=0.1
        )
        self.play(Write(v_label))

        w = Vector(
            dot_projections[0].get_center(),
            color=Colors.projections,
            tip_length=General.tip_length,
        )
        self.play(ReplacementTransform(dots[0], w))

        w_label = MathTex("t \\cdot \\mathbf{u}", color=Colors.projections).next_to(
            w.get_end(), direction=DR, buff=0.1
        )
        self.play(Write(w_label))

        self.wait()

        # Linearity
        self.next_section(
            name="Multiplication", skip_animations=SkipScene.multiplication
        )

        linearity_text = MathTex(
            "L",
            "(",
            "\\mathbf{v}",
            ")",
            "=",
            "t \\cdot \\|\\mathbf{u}\\|",
            "=",
            "t",
            substrings_to_isolate=[
                "L",
                "\\mathbf{v}",
                "t \\cdot \\|\\mathbf{u}\\|",
                "t",
            ],
            tex_to_color_map={
                "L": Colors.mapping,
                "\\mathbf{v}": Colors.vectors,
                "t \\cdot \\|\\mathbf{u}\\|": Colors.projections,
                "t": Colors.projections,
            },
        ).move_to(2 * DOWN + 1.5 * RIGHT)
        self.play(Write(linearity_text))
        linearity_text[2].set_color(Colors.vectors)

        self.wait()

        ## Double vector v
        v.save_state()
        v_label.save_state()
        v2 = Vector(
            2 * v.get_end(), color=Colors.vectors, tip_length=General.tip_length
        )
        self.play(
            Transform(v, v2),
            Transform(
                v_label,
                MathTex("2\\mathbf{v}", color=Colors.vectors).next_to(
                    v2.get_center(), direction=UR, buff=0.1
                ),
            ),
        )

        perp_line2 = DashedLine(
            v2.get_end(),
            2 * dot_projections[0].get_center(),
            color=Colors.vectors,
        )
        self.play(Create(perp_line2))

        ## Double vector w
        w.save_state()
        w_label.save_state()
        w2 = Vector(
            2 * w.get_end(), color=Colors.projections, tip_length=General.tip_length
        )
        self.play(
            Transform(w, w2),
            Transform(
                w_label,
                MathTex("2t \\cdot \\mathbf{u}", color=Colors.projections).next_to(
                    w2.get_end(), direction=DR, buff=0.1
                ),
            ),
        )

        self.wait()

        self.play(
            Transform(
                linearity_text,
                MathTex(
                    "L",
                    "(",
                    "2\\mathbf{v}",
                    ")",
                    "=",
                    "2t",
                    substrings_to_isolate=[
                        "L",
                        "2\\mathbf{v}",
                        "2t",
                    ],
                    tex_to_color_map={
                        "L": Colors.mapping,
                        "2\\mathbf{v}": Colors.vectors,
                        "2t": Colors.projections,
                    },
                ).move_to(2 * DOWN + 1.5 * RIGHT),
            )
        )

        self.wait()

        # Reset
        self.next_section(name="Reset", skip_animations=SkipScene.reset)

        shorter_linearity_text = MathTex(
            "L",
            "(",
            "\\mathbf{v}",
            ")",
            "=",
            "t",
            substrings_to_isolate=[
                "L",
                "\\mathbf{v}",
                "t",
            ],
            tex_to_color_map={
                "L": Colors.mapping,
                "\\mathbf{v}": Colors.vectors,
                "t": Colors.projections,
            },
        ).move_to(2 * DOWN + 1.5 * RIGHT)
        shorter_linearity_text[2].set_color(Colors.vectors)

        self.play(
            Restore(v),
            Restore(v_label),
            Restore(w),
            Restore(w_label),
            Transform(linearity_text, shorter_linearity_text),
            FadeOut(perp_line2),
        )
        linearity_text.save_state()

        # Addition
        self.next_section(name="Addition", skip_animations=SkipScene.addition)

        v2 = Vector(
            axes.coords_to_point(-3, -0.75),
            color=Colors.vectors,
            tip_length=General.tip_length,
        )
        v2_label = MathTex("\\mathbf{v_2}", color=Colors.vectors).next_to(
            v2.get_center(), direction=UP + 7 * LEFT, buff=0.05
        )
        self.play(Create(v2), Write(v2_label))

        w2 = Vector(
            u_line.get_projection(v2.get_end()),
            color=Colors.projections,
            tip_length=General.tip_length,
        )
        perp_line3 = DashedLine(
            v2.get_end(),
            w2.get_end(),
            color=Colors.vectors,
        )
        w2_label = MathTex("s \\cdot \\mathbf{u}", color=Colors.projections).next_to(
            w2.get_end(), direction=DR, buff=0.1
        )
        self.play(Create(perp_line3), Create(w2))
        self.play(Write(w2_label))

        self.wait()

        v_copy = v.copy()
        v_label_copy = v_label.copy()
        v_label_copy.add_updater(
            lambda m: m.next_to(v_copy.get_center(), direction=DOWN, buff=0.2)
        )
        self.play(
            FadeIn(v_label_copy), v_copy.animate.move_to(v2.get_end(), aligned_edge=DR)
        )

        self.wait()

        w3 = Vector(
            u_line.get_projection(v_copy.get_end()),
            color=Colors.projections,
            tip_length=General.tip_length,
        )
        perp_line4 = DashedLine(
            v_copy.get_end(),
            w3.get_end(),
            color=Colors.vectors,
        )

        self.play(Create(perp_line4), Create(w3))

        self.wait()

        self.play(
            Transform(
                linearity_text,
                MathTex(
                    "L",
                    "(",
                    "\\mathbf{v_2}",
                    "+",
                    "\\mathbf{v}",
                    ")",
                    "=",
                    "s + t",
                    substrings_to_isolate=[
                        "L",
                        "\\mathbf{v}",
                        "s + t",
                        "\\mathbf{v_2}",
                    ],
                    tex_to_color_map={
                        "L": Colors.mapping,
                        "\\mathbf{v}": Colors.vectors,
                        "\\mathbf{v_2}": Colors.vectors,
                        "s + t": Colors.projections,
                    },
                ).move_to(2 * DOWN + 1 * RIGHT),
            )
        )

        self.wait()

        # Reset again
        self.play(
            Restore(v),
            Restore(v_label),
            Restore(w),
            Restore(w_label),
            Restore(linearity_text),
            FadeOut(perp_line3),
            FadeOut(perp_line4),
            FadeOut(v2),
            FadeOut(v2_label),
            FadeOut(w2),
            FadeOut(w2_label),
            FadeOut(v_copy),
            FadeOut(v_label_copy),
            FadeOut(w3),
            FadeOut(u_line),
        )

        self.wait()

        # Canonical basis
        self.next_section(
            name="Canonical Basis", skip_animations=SkipScene.canonical_basis
        )

        e1 = Vector(
            axes.coords_to_point(1, 0),
            color=Colors.canonical,
            tip_length=General.scale_tip_length,
            stroke_width=General.scale_width,
        )
        e2 = Vector(
            axes.coords_to_point(0, 1),
            color=Colors.canonical,
            tip_length=General.scale_tip_length,
            stroke_width=General.scale_width,
        )
        e1_label = (
            MathTex(
                "\\mathbf{e_1}",
                color=Colors.canonical,
                font_size=General.scale_font_size,
            )
            .next_to(e1.get_center(), direction=DOWN, buff=0.1)
            .set_opacity(0.7)
        )
        e2_label = (
            MathTex(
                "\\mathbf{e_2}",
                color=Colors.canonical,
                font_size=General.scale_font_size,
            )
            .next_to(e2.get_center(), direction=LEFT, buff=0.1)
            .set_opacity(0.7)
        )

        self.play(
            AnimationGroup(
                FadeOut(v, w, perp_lines[0], v_label, w_label, linearity_text),
                self.camera.frame.animate.set(width=4).move_to(u.get_end()),
                lag_ratio=0.4,
            )
        )
        self.play(
            Create(e1),
            Create(e2),
            Write(e1_label),
            Write(e2_label),
            Transform(
                u_label,
                MathTex(
                    "\\mathbf{u}",
                    color=Colors.projection_line,
                    font_size=General.scale_font_size,
                )
                .next_to(u.get_center(), direction=UL, buff=0.05)
                .set_opacity(0.7),
            ),
            Transform(
                u,
                Vector(
                    u.get_end(),
                    color=Colors.projection_line,
                    tip_length=General.scale_tip_length,
                    stroke_width=General.scale_width,
                ),
            ),
        )

        self.wait()

        # Matrix

        self.next_section(name="Matrix", skip_animations=SkipScene.matrix)
        matrix_text = MathTex(
            "\\big(",
            "u_1",
            "\\;\\;",
            "u_2",
            "\\big)",
            "\\mathbf{v}" "=",
            "L",
            "(",
            "\\mathbf{v}",
            ")",
            substrings_to_isolate=["\\mathbf{v}", "L", "u_1", "u_2"],
            tex_to_color_map={
                "\\mathbf{v}": Colors.vectors,
                "L": Colors.mapping,
                "u_1": Colors.projection_line,
                "u_2": Colors.projection_line,
            },
            font_size=General.scale_font_size,
        ).move_to(1.2 * (UP + 1.5 * RIGHT))
        self.play(Write(matrix_text[0]), Write(matrix_text[4:]))

        self.wait()

        # Bisector line

        self.next_section(name="Bisector Line", skip_animations=SkipScene.bisector_line)

        midpoint = u.get_end() + e2.get_end()
        bisector_line = DashedLine(
            -midpoint,
            midpoint,
            color=Colors.bisector,
            stroke_width=General.scale_width_line,
            z_index=-1,
        ).set_opacity(0.7)
        self.play(Create(bisector_line))

        self.wait()

        # Double Projection

        self.next_section(
            name="Double Projection", skip_animations=SkipScene.double_proj
        )

        e2_line = Line(
            -e2.get_end(),
            e2.get_end(),
        )
        u_proj = Dot(
            e2_line.get_projection(u.get_end()),
            color=Colors.projection_line_light,
            radius=General.scale_dot_radius,
        )
        e2_proj = Dot(
            u_line.get_projection(e2.get_end()),
            color=Colors.canonical_light,
            radius=General.scale_dot_radius,
        )

        perp_line = DashedLine(
            e2.get_end(),
            e2_proj.get_center(),
            color=Colors.canonical_light,
            stroke_width=General.scale_width_line,
        )
        perp_line2 = DashedLine(
            u.get_end(),
            u_proj.get_center(),
            color=Colors.projection_line_light,
            stroke_width=General.scale_width_line,
        )

        self.play(
            AnimationGroup(
                FadeOut(u_label), Create(perp_line), Create(e2_proj), lag_ratio=0.5
            )
        )
        self.wait()

        self.play(AnimationGroup(Create(perp_line2), Create(u_proj), lag_ratio=0.5))

        self.wait()

        # Second u coordinate

        self.next_section(
            name="Second Coordinate", skip_animations=SkipScene.second_coor
        )

        u2 = Vector(
            u_proj.get_center(),
            color=Colors.projection_line_light,
            tip_length=General.scale_tip_length,
            stroke_width=General.scale_width,
        )
        u2_label = MathTex(
            r"\begin{pmatrix} 0 \\ u_2 \end{pmatrix}",
            color=Colors.projection_line_light,
            font_size=General.scale_font_size // 2,
        ).next_to(u2.get_center(), direction=LEFT, buff=0.1)

        e2_label.save_state()
        self.play(
            AnimationGroup(
                FadeOut(e2_label), Transform(u_proj, u2), Write(u2_label), lag_ratio=0.5
            )
        )

        self.wait()

        e22 = Vector(
            e2_proj.get_center(),
            color=Colors.canonical_light,
            tip_length=General.scale_tip_length,
            stroke_width=General.scale_width,
        )

        self.play(Transform(e2_proj, e22))

        self.wait()

        self.next_section(
            name="Second Coordinate Text", skip_animations=SkipScene.second_coor_text
        )

        coor_text = MathTex(
            "L",
            "(",
            "\\mathbf{e_2}",
            ")",
            "=",
            "u_2",
            substrings_to_isolate=[
                "L",
                "\\mathbf{e_2}",
                "u_2",
            ],
            tex_to_color_map={
                "L": Colors.mapping,
                "\\mathbf{e_2}": Colors.canonical,
                "u_2": Colors.projection_line_light,
            },
            font_size=General.scale_font_size,
        ).move_to(0.4 * DOWN + 2 * RIGHT)
        self.play(Write(coor_text))

        self.wait()

        self.next_section(name="Second Reset", skip_animations=SkipScene.second_reset)

        self.play(
            FadeOut(
                u_proj,
                e2_proj,
                perp_line,
                perp_line2,
                u2,
                u2_label,
                e22,
                bisector_line,
            ),
            FadeIn(e2_label),
            Write(matrix_text[3]),
        )

        self.wait()

        # First coor
        self.next_section(name="First Coordinate", skip_animations=SkipScene.first_coor)

        new_coor_text = MathTex(
            "L",
            "(",
            "\\mathbf{e_1}",
            ")",
            "=",
            "u_1",
            substrings_to_isolate=[
                "L",
                "\\mathbf{e_1}",
                "u_1",
            ],
            tex_to_color_map={
                "L": Colors.mapping,
                "\\mathbf{e_1}": Colors.canonical,
                "u_1": Colors.projection_line_light,
            },
            font_size=General.scale_font_size,
        ).move_to(0.4 * DOWN + 2 * RIGHT)

        self.play(Transform(coor_text, new_coor_text))

        self.play(Write(matrix_text[1]))

        self.wait()

        # Non-unit vectors
        self.next_section(name="Non Unit", skip_animations=SkipScene.non_unit)

        u.save_state()
        new_u_label = (
            MathTex(
                r"\frac{1}{\|\mathbf{u}\|} \cdot \mathbf{u}",
                color=Colors.projection_line,
                font_size=(3 * General.scale_font_size) // 4,
            )
            .set_opacity(0.7)
            .next_to(u.get_center(), direction=UP, buff=0.1)
        )

        u.generate_target()
        u.target = Vector(
            1.5 * u.get_end(),
            color=Colors.projection_line,
            tip_length=General.scale_tip_length,
            stroke_width=General.scale_width,
        )
        self.play(Unwrite(coor_text))
        self.play(
            MoveToTarget(u),
            u_label.animate.set_opacity(0.7).next_to(
                u.target.get_center(), direction=UP, buff=0.1
            ),
        )

        self.wait()

        # Back to unit vector
        self.next_section(name="Back to Unit", skip_animations=SkipScene.back_to_unit)

        self.play(
            Restore(u),
            Transform(u_label, new_u_label),
        )

        matrix_text.generate_target()
        matrix_text.target = MathTex(
            r"\frac{1}{\|\mathbf{u}\|}",
            "\\big(",
            "u_1",
            "\\;\\;",
            "u_2",
            "\\big)",
            "\\mathbf{v}",
            "=",
            "L",
            "(",
            "\\mathbf{v}",
            ")",
            "\\cdot",
            "\\|\\mathbf{u}\\|",
            substrings_to_isolate=[
                "\\mathbf{v}",
                "L",
                "u_1",
                "u_2",
                r"\frac{1}{\|\mathbf{u}\|}",
                "\\|\\mathbf{u}\\|",
            ],
            tex_to_color_map={
                "\\mathbf{v}": Colors.vectors,
                "L": Colors.mapping,
                "u_1": Colors.projection_line,
                "u_2": Colors.projection_line,
                r"\frac{1}{\|\mathbf{u}\|}": Colors.projection_line,
                "\\|\\mathbf{u}\\|": Colors.projection_line,
            },
            font_size=General.scale_font_size,
        ).move_to(1.2 * (UP + 1.5 * RIGHT))

        matrix_text.target[-1].set_opacity(0)
        matrix_text.target[-2].set_opacity(0)
        self.play(MoveToTarget(matrix_text))

        self.wait()

        # Matrix text change
        self.next_section(
            name="Matrix Text Change", skip_animations=SkipScene.matrix_text_change
        )

        matrix_text.generate_target()
        matrix_text.target.move_to(3 * UP)
        matrix_text.target.scale(2)

        self.play(
            Restore(self.camera.frame),
            FadeOut(axes, u, u_label, e1, e2, e1_label, e2_label),
            MoveToTarget(matrix_text),
        )

        matrix_text.generate_target()
        matrix_text.target = MathTex(
            "\\big(",
            "u_1",
            "\\;\\;",
            "u_2",
            "\\big)",
            "\\mathbf{v}",
            "=",
            "L",
            "(",
            "\\mathbf{v}",
            ")",
            "\\|\\mathbf{u}\\|",
            substrings_to_isolate=[
                "\\mathbf{v}",
                "L",
                "u_1",
                "u_2",
                "\\|\\mathbf{u}\\|",
            ],
            tex_to_color_map={
                "\\mathbf{v}": Colors.vectors,
                "L": Colors.mapping,
                "u_1": Colors.projection_line,
                "u_2": Colors.projection_line,
                "\\|\\mathbf{u}\\|": Colors.projection_line,
            },
        ).move_to(1.5 * UP)

        self.play(MoveToTarget(matrix_text))

        self.wait()

        next_text = MathTex(
            r"\mathbf{u}",
            r"\cdot",
            r"\mathbf{v}",
            "=",
            "L",
            "(",
            "\\mathbf{v}",
            ")",
            r"\|\mathbf{u}\|",
            substrings_to_isolate=[
                r"\mathbf{v}",
                "L",
                r"\mathbf{u}",
                r"\|\mathbf{u}\|",
            ],
            tex_to_color_map={
                r"\mathbf{v}": Colors.vectors,
                "L": Colors.mapping,
                r"\mathbf{u}": Colors.projection_line,
                r"\|\mathbf{u}\|": Colors.projection_line,
            },
        ).next_to(matrix_text, direction=DOWN, buff=0.5)

        self.play(FadeIn(next_text, shift=DOWN))

        self.wait()

        next_text2 = MathTex(
            r"\mathbf{u}",
            r"\cdot",
            r"\mathbf{v}",
            "=",
            "(",
            r"\text{velikost projekce }",
            r"\mathbf{v}",
            r"\text{ na }",
            r"\mathrm{LO}(",
            r"\mathbf{u}",
            ")",
            ")",
            r"(",
            r"\text{velikost }",
            r"\mathbf{u}",
            ")",
            substrings_to_isolate=[
                r"\mathbf{v}",
                r"\mathbf{u}",
            ],
            tex_to_color_map={
                r"\mathbf{v}": Colors.vectors,
                r"\mathbf{u}": Colors.projection_line,
            },
        ).next_to(next_text, direction=DOWN, buff=0.5)

        self.play(FadeIn(next_text2, shift=DOWN))

        self.wait()

        next_text3 = MathTex(
            r"\mathbf{v}",
            r"\cdot",
            r"\mathbf{u}",
            "=",
            "(",
            r"\text{velikost projekce }",
            r"\mathbf{u}",
            r"\text{ na }",
            r"\mathrm{LO}(",
            r"\mathbf{v}",
            ")",
            ")",
            r"(",
            r"\text{velikost }",
            r"\mathbf{v}",
            ")",
            substrings_to_isolate=[
                r"\mathbf{v}",
                r"\mathbf{u}",
            ],
            tex_to_color_map={
                r"\mathbf{v}": Colors.vectors,
                r"\mathbf{u}": Colors.projection_line,
            },
        ).next_to(next_text2, direction=DOWN, buff=0.5)

        self.play(FadeIn(next_text3, shift=DOWN))

        self.wait()

        self.next_section(name="Question", skip_animations=SkipScene.question)

        question = MathTex(
            r"L_{\mathbf{u}}(\mathbf{v})",
            r"\overset{?}{=}",
            r"\|\mathbf{v}\|",
            r"\cos",
            "(" r"\text{úhel mezi }",
            r"\mathbf{u}",
            r"\text{ a }",
            r"\mathbf{v}",
            ")",
            substrings_to_isolate=[
                r"L_{\mathbf{u}}(\mathbf{v})",
                r"\mathbf{v}",
                r"\|\mathbf{v}\|",
                r"\mathbf{u}",
            ],
            tex_to_color_map={
                r"L_{\mathbf{u}}(\mathbf{v})": Colors.projections,
                r"\mathbf{v}": Colors.vectors,
                r"\|\mathbf{v}\|": Colors.vectors,
                r"\mathbf{u}": Colors.projection_line,
            },
        ).move_to(ORIGIN)
        question[0].set_color(Colors.projections)

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Unwrite(matrix_text),
                    Unwrite(next_text),
                    Unwrite(next_text2),
                    Unwrite(next_text3),
                    lag_ratio=0,
                ),
                Write(question),
                lag_ratio=0.8,
            )
        )

        self.play(question.animate.shift(3.5 * UP), FadeIn(axes))

        self.wait()

        self.next_section(name="New Vectors", skip_animations=SkipScene.new_vectors)

        u = Vector(
            axes.coords_to_point(3, 1),
            color=Colors.projection_line,
            tip_length=General.tip_length,
        )

        v = Vector(
            axes.coords_to_point(1, 2),
            color=Colors.vectors,
            tip_length=General.tip_length,
        )

        u_line = Line(
            -2 * u.get_end(),
            2 * u.get_end(),
            color=Colors.projection_line,
            stroke_width=2,
        )

        self.play(Create(u), Create(v))
        self.play(Create(u_line))

        self.wait()

        # Rotation and triangle
        self.next_section(name="Triangle", skip_animations=SkipScene.triangle)

        v_proj = Dot(u_line.get_projection(v.get_end()), color=Colors.cos, radius=0.12)
        perp_line = DashedLine(
            v.get_end(),
            v_proj.get_center(),
            color=Colors.sin,
        )

        self.play(AnimationGroup(Create(perp_line), Create(v_proj), lag_ratio=0.5))

        self.play(
            Transform(
                v_proj,
                Line(ORIGIN, v_proj.get_center(), color=Colors.cos, stroke_width=8),
            ),
        )

        self.wait()

        self.play(
            u.animate.rotate(-0.32, about_point=ORIGIN),
            v.animate.rotate(-0.32, about_point=ORIGIN),
            u_line.animate.rotate(-0.32, about_point=ORIGIN),
            perp_line.animate.rotate(-0.32, about_point=ORIGIN),
            v_proj.animate.rotate(-0.32, about_point=ORIGIN),
        )

        self.wait()

        theta = Angle(v, u, radius=1, other_angle=True, color=Colors.angle, z_index=-1)
        theta_label = MathTex(r"\theta", color=Colors.angle, font_size=36).next_to(
            theta.point_from_proportion(0.5), direction=UR, buff=0.1
        )
        self.play(Create(theta), Write(theta_label))

        v_length_label = (
            MathTex(r"\|\mathbf{v}\|", color=Colors.vectors, font_size=36)
            .next_to(v.get_end(), direction=LEFT, buff=0.6)
            .shift(0.2 * DOWN)
        )
        cos_label = MathTex(
            r"\|\mathbf{v}\|\cos\theta", color=Colors.cos, font_size=36
        ).next_to(v_proj.get_center(), direction=DOWN, buff=0.2)
        sin_label = MathTex(
            r"\|\mathbf{v}\|\sin\theta", color=Colors.sin, font_size=36
        ).next_to(perp_line.get_center(), direction=RIGHT, buff=0.2)

        self.play(Write(v_length_label), Write(cos_label), Write(sin_label))

        self.wait()
