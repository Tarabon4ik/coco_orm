from typing import Dict, Optional
from .core import BaseEntityModel, AbstractFactory, ID


"""Constants defining dictionary keys."""
ID = ID
NAME = "name"
URL = "url"


class Model(BaseEntityModel):
    """
    COCO license object-oriented model.

    Args/Attributes:
        id: (int): id
        name: (str): file name
        url (Optional[str]): url
    """
    def __init__(
        self,
        id: int, 
        name: str, 
        url: Optional[str] = None
    ):
        super().__init__(id)
        self.name = name
        self.url = url


class Factory(AbstractFactory):
    """
    Factory used to create an instance of object-oriented model

    There are two ways of accessing the class:
        1) Using entity_factory property of License Collection class:
            >>> from coco_orm.collections import LicenseCollection
            >>> license_collection = LicenseCollection()
            >>> license = license_collection.entity_factory(id=1, name="GNU")
        2) Importing from models module:
            >>> from coco_orm.models import License
            >>> license = License(id=1, name="GNU")
    """

    def __new__(
        cls,
        name: str, 
        url: Optional[str] = None,
        id: int = 0
    ) -> Model:
        """
        Implementation of the abstract method.

        Args:
            id: (int), default=0: If not specified: id = collection.last_element_id + 1
            name: (str): file name
            url (Optional[str]): url

        Returns:
            Model: a instance of Model class containing entity data.
        """
        return Model(id, name, url)

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
            url = str(data[URL]) if data.get(URL) is not None else None
        )