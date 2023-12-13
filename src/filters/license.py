from typing import List
from ..operators.core import EQUAL, IN
from .core import BaseFilter
from .properties import ValueProperty, ValuesProperty, Intersection
from .utils import extract_unique_attr_values
from ..models.license import NAME, URL
from ..models.image import LICENSE


class Filters(BaseFilter):
    def name(self, value: str, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=NAME))
        return self

    def names(self, values: List[str], membership_operator: str = IN):
        self.append(ValuesProperty(values, membership_operator, name=NAME))
        return self

    def url(self, value: str, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=URL))
        return self

    def urls(self, values: List[str], membership_operator: str = IN):
        self.append(ValuesProperty(values, membership_operator, name=URL))
        return self

    def intersection(self, image_collection):
        intersection = Intersection()
        intersection.append(self.ids(extract_unique_attr_values(image_collection, LICENSE)))
        self.append(intersection)
        return self