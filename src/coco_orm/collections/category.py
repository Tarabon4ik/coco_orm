# python 
from typing import Optional
# library modules
from .core import BaseCollection
from ..models.category import Model, Factory
from ..filters.category import Filters
    

class Collection(BaseCollection):
    """
    Collection inherits BaseCollection class and contains methods to simplify and standardize COCO categories processing.

    To instantiate an Collection class, use following example:
    >>> from coco_orm.collections import CategoryCollection
    >>> category_collection = CategoryCollection()
    """
    def __init__(self, entities):
        super().__init__(Factory, Filters, entities)

    def __call__(self, entities):
        """Override. Return a Collection instance."""
        return Collection(Factory, Filters, entities)

    def get_by_name(self, value: str) -> Optional[Model]:
        """
        Get entity by name.

        Args:
            value (str): a name of an entity to search for.

        Returns:
            Optional[Model]: an instance of Model containing entity data if one is found, None if not
        """
        return next((entity for entity in self if entity.name == value), None)
    

