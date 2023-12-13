from typing import List

from ..operators.core import IN, AND, OR
from ..models.core import ID
from .properties import ValuesProperty
from .expression import ExpressionBuilder, ENTITY
from ..models.core import BaseEntityModel


class BaseFilter(list):
    """
    BaseFilter inherits structure and features of standard python list that allows to use its instances as a list.
    BaseFilter contains common filters shared by child instances to simplify and standardize COCO dataset filtering.
    
    All filter classes must inherit that class in order to work properly in the COCO environment.
    All COCO filters have already been implemented.  See ``coco_orm.filters``

    BaseFilter has been constructed using builder pattern, meaning that class methods return self property 
    that allows to build filters using chaing. Example:
    >>> filters = (BaseFilter().
    ...     ids([1, 2, 3]).
    ...     OR.
    ...     ids([4, 5, 6])
    ... )

    BaseFilter instances used by coresponding collection instances.
    There are two ways of applying filters to the collection:
        1) Call ``filter`` BaseCollection instance method with filters object passed as an argument:
            >>> filtered_collection = collection.filter(filters)
        2) Call ``apply`` BaseFilter instance method with collection object passed as an argument:
            >>> filtered_collection = filters.apply(collection)


    Attributes:
        AND (str): and logical operator. Used for inclusive filters chaining.
        OR (str): or logical operator. Used for exclusive filters chaining.
    """
    @property
    def AND(self):
        """AND logical operator. Used for inclusive filters chaining."""
        self.append(AND)
        return self

    @property
    def OR(self):
        """OR logical operator. Used for exclusive filters chaining."""
        self.append(OR)
        return self

    def ids(self, values: List[int], membership_operator: str = IN):
        """
        Filter entities by its ids.

        Args:
            values (list[int]): an list of entities ids to filter.
            membership_operator (str): defines how to apply the filter to collection (inclusively (IN) or exclusively (NOT IN))

        Returns:
            self
        """
        self.append(ValuesProperty(values, membership_operator, name=ID))
        return self

    def intersection(self):
        """
        Abstract method. Child classes must implement that method.

        The filter is used to filter multiple collections by its intersection (leaving only those entities that is shared accross collections).
        """
        pass

    def apply(self, collection: List[BaseEntityModel]) -> List:
        """
        Apply filters to a given collection.

        Args:
            collection (list[Dict]): a list of dicts containing entities data.

        Returns:
            List[Dict]: a list of dicts containing filtered entities data.
        """
        expression = ExpressionBuilder(self)
        # filter collection by built expression
        # return a new collection object containing queried entities, None if no entities are found.
        return [entity for entity in collection if eval(expression, {ENTITY: entity})]
