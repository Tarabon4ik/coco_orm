from typing import Optional

from .core import BaseCollection

from ..models.license import Model, Factory
from ..filters.license import Filters
    

class Collection(BaseCollection):
    """
    Collection inherits BaseCollection class and contains methods to simplify and standardize COCO categories processing.

    To instantiate an Collection class, use following example:
    >>> from coco_orm.collections import LicenseCollection
    >>> license_collection = LicenseCollection()
    """
    def __init__(self, entities):
        super().__init__(Factory, Filters, entities)

    def __call__(self, entities):
        """Override. Return a Collection instance."""
        return Collection(Factory, Filters, entities)

    def get_by_name(self, value: str) -> Optional[Model]:
        """
        Get license by name.

        Args:
            value (str): a name of an entity to search for.

        Returns:
            Optional[Model]: an instance of Model containing entity data if one is found, else None
        """
        return next((entity for entity in self if entity.name == value), None)
    
    def get_by_url(self, value: str) -> Optional[Model]:
        """
        Get license by url.

        Args:
            value (str): a url of an entity to search for.

        Returns:
            Optional[Model]: an instance of Model containing entity data if one is found, else None
        """
        return next((entity for entity in self if entity.url == value), None)
