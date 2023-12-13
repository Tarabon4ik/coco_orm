from typing import Dict, Optional
from .core import BaseEntityModel, AbstractFactory, ID

"""Constants defining dictionary keys."""
ID = ID
NAME = "name"
SUPERCATEGORY = "supercategory"


class Model(BaseEntityModel):
    """
    COCO category object-oriented model.

    Args/Attributes:
        id: (int): id
        name: (str): category name
        supercategory (Optional[str]): supercategory name
    """
    def __init__(
        self,
        id: int, 
        name: str, 
        supercategory: Optional[str] = None
    ):
        super().__init__(id)
        self.name = name
        self.supercategory = supercategory


class Factory(AbstractFactory):
    """
    Factory used to create an instance of object-oriented model

    There are two ways of accessing the class:
        1) Using entity_factory property of Category Collection class:
            >>> from coco_orm.collections import CategoryCollection
            >>> category_collection = CategoryCollection()
            >>> category = category_collection.entity_factory(id=1, image_id="car")
        2) Importing from models module:
            >>> from coco_orm.models import Category
            >>> category = Category(id=1, image_id="car")
    """

    def __new__(
        cls,
        name: str, 
        supercategory: Optional[str] = None,
        id: int = 0
    ) -> Model:
        """
        Implementation of the abstract method. Called whenever a Factory class is instantianted.

        Args:
            id: (int), default = 0: id. If not specified: id = collection.last_element_id + 1
            name: (str): file name
            supercategory (Optional[str]): supercategory name

        Returns:
            Model: a instance of Model class containing entity data.
        """
        return Model(id, name, supercategory)

    @staticmethod
    def from_dict(data: Dict) -> Model:
        """
        Implementation of the abstract method.
        Builds an object-oriented entity model from dictionary data.

        Args:
            data: (dict): a dictionary containing entity data.

        Returns:
            Model: a instance of Model class containing entity data.
        """
        return Model(
            id = int(data[ID]) if data.get(ID) is not None else 0,
            name = str(data[NAME]),
            supercategory = str(data[SUPERCATEGORY]) if data.get(SUPERCATEGORY) is not None else None
        )