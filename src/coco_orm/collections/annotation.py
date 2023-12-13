from .core import BaseCollection
from ..models.annotation import Factory
from ..filters.annotation import Filters

class Collection(BaseCollection):
    """
    Collection inherits BaseCollection class and contains methods to simplify and standardize COCO annotations processing.

    To instantiate an Collection class, use following example:
    >>> from coco_orm.collections import AnnotationCollection
    >>> annotation_collection = AnnotationCollection()
    """
    def __init__(self, entities):
        super().__init__(Factory, Filters, entities)

    def __call__(self, entities):
        """Override. Return a Collection instance."""
        return Collection(Factory, Filters, entities)
