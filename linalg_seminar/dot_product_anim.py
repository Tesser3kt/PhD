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
            "t \\cdot \\mathbf{u}",
            substrings_to_isolate=["L", "\\mathbf{v}", "t \\cdot \\mathbf{u}"],
            tex_to_color_map={
                "L": Colors.mapping,
                "\\mathbf{v}": Colors.vectors,
                "t \\cdot \\mathbf{u}": Colors.projections,
            },
        ).move_to(2 * DOWN + 1.5 * RIGHT)
        self.play(Write(linearity_text))
        linearity_text.save_state()

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
                    "2t \\cdot \\mathbf{u}",
                    substrings_to_isolate=[
                        "L",
                        "2\\mathbf{v}",
                        "2t \\cdot \\mathbf{u}",
                    ],
                    tex_to_color_map={
                        "L": Colors.mapping,
                        "2\\mathbf{v}": Colors.vectors,
                        "2t \\cdot \\mathbf{u}": Colors.projections,
                    },
                ).move_to(2 * DOWN + 1.5 * RIGHT),
            )
        )

        self.wait()

        # Reset
        self.next_section(name="Reset", skip_animations=SkipScene.reset)

        self.play(
            Restore(v),
            Restore(v_label),
            Restore(w),
            Restore(w_label),
            Restore(linearity_text),
            FadeOut(perp_line2),
        )

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
                    "(s + t) \\cdot \\mathbf{u}",
                    substrings_to_isolate=[
                        "L",
                        "\\mathbf{v}",
                        "(s + t) \\cdot \\mathbf{u}",
                        "\\mathbf{v_2}",
                    ],
                    tex_to_color_map={
                        "L": Colors.mapping,
                        "\\mathbf{v}": Colors.vectors,
                        "\\mathbf{v_2}": Colors.vectors,
                        "(s + t) \\cdot \\mathbf{u}": Colors.projections,
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
            "\\hphantom{u_x}",
            "\\;\\;",
            "\\hphantom{u_y}",
            "\\big)",
            "\\mathbf{v}" "=",
            "L",
            "(",
            "\\mathbf{v}",
            ")",
            substrings_to_isolate=["\\mathbf{v}", "L"],
            tex_to_color_map={
                "\\mathbf{v}": Colors.vectors,
                "L": Colors.mapping,
            },
            font_size=General.scale_font_size,
        ).move_to(1.2 * (UP + 1.5 * RIGHT))
        self.play(Write(matrix_text))

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
        e22_label = MathTex(
            r"u_2 \cdot \mathbf{u}",
            color=Colors.canonical_light,
            font_size=General.scale_font_size // 2,
        ).next_to(e22.get_end(), direction=DR, buff=0.05)

        self.play(
            AnimationGroup(Transform(e2_proj, e22), Write(e22_label), lag_ratio=0.5)
        )

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
            "u_2 \\cdot \\| \\mathbf{u} \\|",
            "=",
            "u_2",
            substrings_to_isolate=[
                "L",
                "\\mathbf{e_2}",
                "u_2",
                "u_2 \\cdot \\| \\mathbf{u} \\|",
            ],
            tex_to_color_map={
                "L": Colors.mapping,
                "\\mathbf{e_2}": Colors.canonical,
                "u_2": Colors.projection_line_light,
                "u_2 \\cdot \\| \\mathbf{u} \\|": Colors.projection_line_light,
            },
            font_size=General.scale_font_size,
        ).move_to(0.5 * DOWN + 1.5 * RIGHT)
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
                e22_label,
                bisector_line,
            ),
            FadeIn(e2_label),
        )

        self.wait()
