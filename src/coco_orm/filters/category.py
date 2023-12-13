from typing import List, Optional
from ..operators.core import EQUAL, IN
from .core import BaseFilter
from .properties import ValueProperty, ValuesProperty, Intersection
from .utils import extract_unique_attr_values, filter_collection
from ..models.category import ID, NAME, SUPERCATEGORY
from ..models.annotation import CATEGORY_ID, IMAGE_ID
from ..models.image import LICENSE


class Filters(BaseFilter):
    def name(self, value: str, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=NAME))
        return self

    def names(self, values: List[str], membership_operator: str = IN):
        self.append(ValuesProperty(values, membership_operator, name=NAME))
        return self

    def supercategory(self, value: str, comparison_operator: str = EQUAL):
        self.append(ValueProperty(value, comparison_operator, name=SUPERCATEGORY))
        return self

    def supercategories(self, values: List[str], membership_operator: str = IN):
        self.append(ValuesProperty(values, membership_operator, name=SUPERCATEGORY))
        return self

    def intersection(
        self,
        annotation_collection, 
        image_collection = None, 
        license_collection = None
    ):
        intersection = Intersection()
        if image_collection:
            if license_collection:
                image_collection = filter_collection(image_collection, attr_name=LICENSE, attr_values=extract_unique_attr_values(license_collection, ID))
            annotation_collection = filter_collection(annotation_collection, attr_name=IMAGE_ID, attr_values=extract_unique_attr_values(image_collection, ID))
        intersection.append(self.ids(extract_unique_attr_values(annotation_collection, CATEGORY_ID)))
        self.append(intersection)
        return self
    