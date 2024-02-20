import numpy as np
from manim import *

from dot_product_config import *


class DotProduct(MovingCameraScene):
    def get_axes(self):
        axes = Axes(
            x_range=[-6, 6],
            y_range=[-3, 3],
            axis_config={"color": Colors.axes},
        )
        return axes

    def get_vectors(self, axes):
        vectors = VGroup(
            Vector(axes.coords_to_point(-2, 2), color=Colors.vectors),
            Vector(axes.coords_to_point(3, 2), color=Colors.vectors),
            Vector(axes.coords_to_point(3.5, -2), color=Colors.vectors),
            Vector(axes.coords_to_point(-1, -1), color=Colors.vectors),
            Vector(axes.coords_to_point(1, 1), color=Colors.vectors),
            Vector(axes.coords_to_point(-3, 1), color=Colors.vectors),
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
            axes.coords_to_point(np.sqrt(3) / 2, 1 / 2), color=Colors.projection_line
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
            self.camera.frame.animate.set(width=8).move_to(u.get_end()),
        )

        self.wait()
