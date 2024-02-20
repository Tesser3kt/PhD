import numpy as np
from manim import *

from dot_product_config import *


class DotProduct(Scene):
    def get_axes(self):
        axes = Axes(
            x_range=[-6, 6],
            y_range=[-3, 3],
            axis_config={"color": Colors.axes},
        )
        return axes

    def get_vectors(self, axes):
        vectors = VGroup(
            Vector(axes.coords_to_point(3, 2), color=Colors.vectors),
            Vector(axes.coords_to_point(3, -2), color=Colors.vectors),
            Vector(axes.coords_to_point(-1, 2), color=Colors.vectors),
            Vector(axes.coords_to_point(-1, -1), color=Colors.vectors),
            Vector(axes.coords_to_point(1, 1), color=Colors.vectors),
            Vector(axes.coords_to_point(-3, 0), color=Colors.vectors),
        )

        return vectors

    def construct(self):
        # Vectors to Dots
        self.next_section(name="Many Dots", skip_animations=SkipScene.many_dots)

        axes = self.get_axes()
        self.play(Create(axes))

        vectors = self.get_vectors(axes)
        self.play(Create(vectors))

        self.wait()

        self.play(
            *[
                Transform(
                    vectors[i],
                    Dot(vectors[i].get_end(), color=Colors.vectors),
                )
                for i in range(len(vectors))
            ]
        )

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

        # Perpendicular lines
        self.next_section(
            name="Perpendicular Lines", skip_animations=SkipScene.perpendicular_lines
        )

        perp_lines = VGroup()
        self.add(perp_lines)

        self.wait()
