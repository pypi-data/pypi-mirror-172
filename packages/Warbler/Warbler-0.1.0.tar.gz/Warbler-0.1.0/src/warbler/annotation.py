from borb.pdf.canvas.layout.annotation.square_annotation import SquareAnnotation as BorbSquareAnnotation
from borb.pdf.canvas.color.color import Color as BorbColor
from borb.pdf.canvas.geometry.rectangle import Rectangle as BorbRectangle

import typing
from typing import Optional, Union, Tuple
from decimal import Decimal

"""
class SquareAnnotation(BorbSquareAnnotation):
    def __init__(
        self,
        bounding_box: Union[Rectangle, Tuple[NumberType, NumberType, NumberType, NumberType]]
        fill_color: Optional[ColorType] = None,
        stroke_color: Optional[ColorType] = None,
        rectangle_difference: Optional[
            Tuple[NumberType, NumberType, NumberType, NumberType]
        ] = None,
    ):
        super().__init__(bounding_box=bounding_box, fill_color=fill_color, stroke_color=stroke_color, rectangle_difference=rectangle_difference)
        """