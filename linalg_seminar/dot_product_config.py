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
    cos = TEAL
    sin = RED
    angle = PURPLE


@dataclass
class SkipScene:
    many_dots: bool = False
    projection_line: bool = False
    perpendicular_lines: bool = False
    zoom_in: bool = False
    dot_vector: bool = False
    multiplication: bool = False
    reset: bool = False
    addition: bool = False
    canonical_basis: bool = False
    matrix: bool = False
    bisector_line: bool = False
    double_proj: bool = False
    second_coor: bool = False
    second_coor_text: bool = False
    second_reset: bool = False
    first_coor: bool = False
    non_unit: bool = False
    back_to_unit: bool = False
    matrix_text_change: bool = False
    question: bool = False
    new_vectors: bool = False
    triangle: bool = False
