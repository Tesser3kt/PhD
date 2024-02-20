from dataclasses import dataclass
from manim import *


@dataclass
class Colors:
    axes = BLUE
    vectors = PINK
    projection_line = YELLOW
    projections = TEAL


@dataclass
class SkipScene:
    many_dots: bool = True
    projection_line: bool = True
    perpendicular_lines: bool = True
    zoom_in: bool = True
