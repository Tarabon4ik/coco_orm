from typing import List, Optional
from ..operators.core import EQUAL, IN, LESS_THAN_OR_EQUAL_TO, GREATER_THAN_OR_EQUAL_TO
from .core import BaseFilter
from .properties import ValueProperty, ValuesProperty, RangeProperty, BboxProperty, BboxRangeProperty, Intersection
from .utils import extract_unique_attr_values, filter_collection
from ..models.annotation import ID, IMAGE_ID, CATEGORY_ID, AREA, ISCROWD, BBOX_WIDTH_IDX, BBOX_HEIGHT_IDX
from ..models.image import LICENSE


"""Constants defining property names"""
BBOX_WIDTH = "bbox_width"
BBOX_HEIGHT = "bbox_height"


class Filters(BaseFilter):
    def image_id(self, value: int, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=IMAGE_ID))
        return self

    def image_ids(self, values: List[int], membership_operator: str = IN):
        self.append(ValuesProperty(values, membership_operator, name=IMAGE_ID))
        return self

    def category_id(self, value: int, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=CATEGORY_ID))
        return self

    def category_ids(self, values: List[int], membership_operator: str = IN):
        self.append(ValuesProperty(values, membership_operator, name=CATEGORY_ID))
        return self

    def area(self, value: float, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=AREA))
        return self

    def area_range(self, min_value: float, max_value: float, min_comparison_operator: str = GREATER_THAN_OR_EQUAL_TO, max_comparison_operator: str = LESS_THAN_OR_EQUAL_TO):
        self.append(RangeProperty(min_value, max_value, min_comparison_operator, max_comparison_operator, name=AREA))
        return self

    def bbox_width(self, value: float, comparison_operator: str = EQUAL):
        self.append(BboxProperty(value, comparison_operator, name=BBOX_WIDTH, idx=BBOX_WIDTH_IDX))
        return self

    def bbox_width_range(self, min_value: float, max_value: float, min_comparison_operator: str = GREATER_THAN_OR_EQUAL_TO, max_comparison_operator: str = LESS_THAN_OR_EQUAL_TO):
        self.append(BboxRangeProperty(min_value, max_value, min_comparison_operator, max_comparison_operator, name=BBOX_WIDTH, idx=BBOX_WIDTH_IDX))
        return self

    def bbox_height(self, value: float, comparison_operator: str = EQUAL):
        self.append(BboxProperty(value, comparison_operator, name=BBOX_HEIGHT,  idx=BBOX_HEIGHT_IDX))
        return self

    def bbox_height_range(self, min_value: float, max_value: float, min_comparison_operator: str = GREATER_THAN_OR_EQUAL_TO, max_comparison_operator: str = LESS_THAN_OR_EQUAL_TO):
        self.append(BboxRangeProperty(min_value, max_value, min_comparison_operator, max_comparison_operator, name=BBOX_HEIGHT, idx=BBOX_HEIGHT_IDX))
        return self

    def iscrowd(self, value: int, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=ISCROWD))
        return self

    def intersection(
        self, 
        image_collection = None, 
        category_collection = None, 
        license_collection = None
    ):
        intersection = Intersection()
        if image_collection:
            if license_collection:
                image_collection = filter_collection(image_collection, attr_name=LICENSE, attr_values=extract_unique_attr_values(license_collection, ID))
            intersection.append(self.image_ids(extract_unique_attr_values(image_collection, ID)))
        if category_collection: 
            intersection.append(self.category_ids(extract_unique_attr_values(category_collection, ID)))
        self.append(intersection)
        return self
