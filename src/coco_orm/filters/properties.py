from typing import List

from .utils import check_comparison_operator, check_membership_operator, check_range_comparison_operator


class BaseProperty():
    """
    BaseProperty contain common properties shared by child instances.
    All filter property classes must inherit that class in order to work properly in the COCO environment.

    Instances of the class are used by ExpressionBuilder to build filter expressions. 
    See: ``coco_orm.filters.core.expression.ExpressionBuilder``

    Args/Attributes:
        name (str): a name of a property.
    """
    def __init__(self, name: str):
        self.name = name


class ValueProperty(BaseProperty):
    """
    ValueProperty represents a filter constructed for a single value filtering.

    Args/Attributes:
        value (str): a value to be filtered.
        comparison_operator (str): a type of a comparison operator applied by the filter.
        name (str): a name of a property to be filtered by.
    """
    def __init__(self, value, comparison_operator, name):
        super().__init__(name)
        self.value = value
        self.comparison_operator = check_comparison_operator(name, comparison_operator)


class ValuesProperty(BaseProperty):
    """
    ValuesProperty represents a filter constructed for multiple values filtering.

    Args/Attributes:
        values (list[mixed]): a list of values to be filtered.
        membership_operator (str): a type of a membership operator applied by the filter.
        name (str): a name of a property to be filtered by.
    """
    def __init__(self, values: List, membership_operator: str, name):
        super().__init__(name)
        self.values = values
        self.membership_operator = check_membership_operator(name, membership_operator)


class RangeProperty(BaseProperty):
    """
    RangeProperty represents a filter constructed for range-based filtering.

    Args/Attributes:
        min_value (float): a minimal value of the range.
        min_comparison_operator (str): a type of a comparison operator applied to the min_value.
        max_value (float): a maximum value of the range.
        max_comparison_operator (str): a type of a comparison operator applied to the max_value.
        name (str): a name of a property to be filtered by.
    """
    def __init__(self, min_value: float, min_comparison_operator: str, max_value: float, max_comparison_operator: str, name):
        super().__init__(name)
        self.min_value = min_value
        self.max_value = max_value
        self.min_comparison_operator, self.max_comparison_operator = check_range_comparison_operator(name, min_comparison_operator, max_comparison_operator)


class BboxProperty(ValueProperty):
    """
    BboxProperty represents a filter constructed for bbox properties.

    Args/Attributes:
        value (str): a value to be filtered.
        comparison_operator (str): a type of a comparison operator applied by the filter.
        name (str): a name of a property to be filtered by.
        idx (int): an index of an item of the bbox list.
    """
    def __init__(self, value: float, comparison_operator: str, name, idx: int):
        super().__init__(value, comparison_operator, name)
        self.idx = idx


class BboxRangeProperty(RangeProperty):
    """
    BboxRangeProperty represents a filter constructed for range-based bbox property filtering.

    Args/Attributes:
        min_value (float): a minimal value of the range.
        min_comparison_operator (str): a type of a comparison operator applied to the min_value.
        max_value (float): a maximum value of the range.
        max_comparison_operator (str): a type of a comparison operator applied to the max_value.
        name (str): a name of a property to be filtered by.
        idx (int): an index of an item of the bbox list.
    """
    def __init__(self, min_value: float, min_comparison_operator: str, max_value: float, max_comparison_operator: str, name, idx: int):
        super().__init__(min_value, min_comparison_operator, max_value, max_comparison_operator, name)
        self.idx = idx


# 
class Intersection(list): # type: list[ValuesProperty]
    """
    Intersection represents a filter constructed for collections intersection filtering.
    Basically it is a list of ValuesProperty instances holding collections intersection values.
    """
    def append(self, property: ValuesProperty):
        """
        Append ValuesProperty instance to the Intersection instance.

        Args:
            property (ValuesProperty): an instance of ValuesProperty.
        """
        super().append(property)