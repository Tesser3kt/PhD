from dataclasses import dataclass
from manim import *


@dataclass
class General:
    tip_length = 0.2
    scale_font_size = 24
    scale_tip_length = 0.1
    scale_width = 2
    scale_width_line = 1
    scale_dot_radius = 0.05


@dataclass
class Colors:
    axes = WHITE
    vectors = PINK
    projection_line = YELLOW
    projection_line_light = YELLOW_A
    projections = TEAL
    mapping = GREEN
    canonical = BLUE
    canonical_light = BLUE_A
    bisector = WHITE


@dataclass
class SkipScene:
    many_dots: bool = True
    projection_line: bool = True
    perpendicular_lines: bool = True
    zoom_in: bool = True
    dot_vector: bool = True
    multiplication: bool = True
    reset: bool = True
    addition: bool = True
    canonical_basis: bool = True
    matrix: bool = True
    bisector_line: bool = True
    double_proj: bool = True
    second_coor: bool = False
