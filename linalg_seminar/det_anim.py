from manim import *

class DeformGrid(Scene):
    def construct(self):
        def create_dot_grid(color) -> VGroup:
            """Create a grid of dots"""
            dots = VGroup()
            for x in range(-5, 6):
                for y in range(-5, 6):
                    dots.add(Dot([x, y, 0], color=color))
            return dots

        # Create number plane
        plane = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            axis_config={"include_tip": False},
            background_line_style={
                "stroke_color": GREY,
                "stroke_width": 1,
                "stroke_opacity": 0.5,
            }
        )
        grid = create_dot_grid(YELLOW)
        self.play(Create(plane))
        self.play(Create(grid))
        self.wait()