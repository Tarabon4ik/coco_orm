from ..operators.core import AND
from .properties import ValueProperty, ValuesProperty, RangeProperty, BboxProperty, BboxRangeProperty, Intersection
from .utils import check_logical_operator

ENTITY = "entity"

class ExpressionBuilder():
    """
    ExpressionBuilder used to build expressions for filtering using user-defined property collection.

    ExpressionBuilder is used by ``BaseFilter`` to build expression for filtering based on user-defined filters.
    See ``coco_orm.filters.core.BaseFilter.apply``.
    """
    def __new__(cls, filters) -> str:
        """
        Build an expression string for given filters.

        Args:
            filters (BaseFilter): an instance of BaseFilter implementation containing filters.

        Returns:
            str: an expression string used for collection filtering.
        """
        expressions = []
        for arg in filters:
            # construct expression for a current argument based on its structure
            ## add None to the end of each property to further replace it with AND operator if not specified by user.
            if isinstance(arg, ValueProperty): expressions.extend((ExpressionBuilder.value(arg), None))
            elif isinstance(arg, ValuesProperty): expressions.extend((ExpressionBuilder.values(arg), None))
            elif isinstance(arg, RangeProperty): expressions.extend((ExpressionBuilder.range(arg), None))
            elif isinstance(arg, BboxProperty): expressions.extend((ExpressionBuilder.bbox(arg), None))
            elif isinstance(arg, BboxRangeProperty): expressions.extend((ExpressionBuilder.bbox_range(arg), None))
            elif isinstance(arg, Intersection): expressions.extend((ExpressionBuilder.intersection(arg), None))
            elif isinstance(arg, str): # arg type: logical operator
                check_logical_operator(arg)
                # replace last None element with given logical operator by deleting the last None element
                del expressions[-1]
                # append logical operator to the end of the list
                expressions.append(arg)
        # remove the last None element of the list
        del expressions[-1]
        # replace None elements of the list with AND operator (a default one)
        expressions = [AND if elem == None else elem for elem in expressions]
        # add whitespaces between expression elements
        return " ".join(expressions)

    @staticmethod
    def value(property: ValueProperty) -> str:
        """
        Build an expression string for value-based filtering using user-defined property.

        Args:
            property (ValueProperty): an instance of ValueProperty containing filter data.

        Returns:
            str: an expression string used for value-based filtering.
        """
        value = f'"{property.value}"' if isinstance(property.value, str) else property.value
        return f'{ENTITY}.{property.name} {property.comparison_operator} {value}'

    @staticmethod
    def values(property: ValuesProperty) -> str:
        """
        Build an expression string for values-based filtering using user-defined property.

        Args:
            property (ValuesProperty): an instance of ValuesProperty containing filter data.

        Returns:
            str: an expression string used for values-based filtering.
        """
        return f'{ENTITY}.{property.name} {property.membership_operator} {property.values}'

    @staticmethod
    def range(property: RangeProperty) -> str:
        """
        Build an expression string for range-based filtering using user-defined property.

        Args:
            property (RangeProperty): an instance of RangeProperty containing filter data.

        Returns:
            str: an expression string used for range-based filtering.
        """
        return f'{ENTITY}.{property.name} {property.min_comparison_operator} {property.min_value} {AND} {ENTITY}.{property.name} {property.max_comparison_operator} {property.max_value}'

    @staticmethod
    def bbox(property: BboxProperty) -> str:
        """
        Build an expression string for bbox-based filtering using user-defined property.

        Args:
            property (RangeProperty): an instance of RangeProperty containing filter data.

        Returns:
            str: an expression string used for bbox-based filtering.
        """
        return f'{ENTITY}.bbox[{property.idx}] {property.comparison_operator} {property.value}'

    @staticmethod
    def bbox_range(property: BboxRangeProperty) -> str:
        """
        Build an expression string for bbox_range-based filtering using user-defined property.

        Args:
            property (RangeProperty): an instance of RangeProperty containing filter data.

        Returns:
            str: an expression string used for bbox_range-based filtering.
        """
        return f'{ENTITY}.bbox[{property.idx}] {property.min_comparison_operator} {property.min_value} {AND} {ENTITY}.bbox[{property.idx}] {property.max_comparison_operator} {property.max_value}'

    @staticmethod
    def intersection(intersection: Intersection) -> str:
        """
        Build an expression string for intersection-based filtering using user-defined property.

        Args:
            property (RangeProperty): an instance of RangeProperty containing filter data.

        Returns:
            str: an expression string used for intersection-based filtering.
        """
        expressions = [ExpressionBuilder.values(property) for property in intersection]
        return f' {AND} '.join(expressions)

