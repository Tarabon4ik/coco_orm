from typing import List, Optional
from ..operators.core import EQUAL, IN, LESS_THAN_OR_EQUAL_TO, GREATER_THAN_OR_EQUAL_TO
from .core import BaseFilter
from .properties import ValueProperty, ValuesProperty, RangeProperty, Intersection
from .utils import extract_unique_attr_values, filter_collection
from ..models.image import ID, FILE_NAME, WIDTH, HEIGHT, LICENSE, DATE_CAPTURED
from ..models.annotation import CATEGORY_ID, IMAGE_ID


class Filters(BaseFilter):
    def file_name(self, value: str, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=FILE_NAME))
        return self

    def file_names(self, values: List[str], membership_operator: str = IN):
        self.append(ValuesProperty(values, membership_operator, name=FILE_NAME))
        return self

    def width(self, value: float, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=WIDTH))
        return self

    def width_range(self, min_value: float, max_value: float, min_comparison_operator: str = GREATER_THAN_OR_EQUAL_TO, max_comparison_operator: str = LESS_THAN_OR_EQUAL_TO):
        self.append(RangeProperty(min_value, max_value, min_comparison_operator, max_comparison_operator, name=WIDTH))
        return self

    def height(self, value: float, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=HEIGHT))
        return self
    
    def height_range(self, min_value: float, max_value: float, min_comparison_operator: str = GREATER_THAN_OR_EQUAL_TO, max_comparison_operator: str = LESS_THAN_OR_EQUAL_TO):
        self.append(RangeProperty(min_value, max_value, min_comparison_operator, max_comparison_operator, name=HEIGHT))
        return self

    def license(self, value, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=LICENSE))
        return self
    
    def licenses(self, values: List[int], membership_operator: str = IN):
        self.append(ValuesProperty(values, membership_operator, name=LICENSE))
        return self

    def date_captured(self, value, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=DATE_CAPTURED))
        return self

    def date_captured_range(self, min_value, max_value, min_comparison_operator = GREATER_THAN_OR_EQUAL_TO, max_comparison_operator = LESS_THAN_OR_EQUAL_TO):
        self.append(RangeProperty(min_value, max_value, min_comparison_operator, max_comparison_operator, name=DATE_CAPTURED))
        return self

    def intersection(
        self,
        annotation_collection, 
        category_collection = None,
        license_collection = None
    ):
        intersection = Intersection()
        if license_collection: 
            intersection.append(self.licenses(extract_unique_attr_values(license_collection, ID)))
        if category_collection: # if True - filter annotation_collection by category_ids contained in category_collection
            annotation_collection = filter_collection(annotation_collection, attr_name=CATEGORY_ID, attr_values=extract_unique_attr_values(category_collection, ID))
        intersection.append(self.ids(extract_unique_attr_values(annotation_collection, IMAGE_ID)))
        self.append(intersection)
        return self
