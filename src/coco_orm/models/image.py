from typing import Dict, Optional
from .core import BaseEntityModel, AbstractFactory, ID


"""Constants defining dictionary keys."""
ID = ID
WIDTH = "width"
HEIGHT = "height"
FILE_NAME = "file_name"
LICENSE = "license"
FLICKR_URL = "flickr_url"
COCO_URL = "coco_url"
DATE_CAPTURED = "date_captured"


class Model(BaseEntityModel):
    """
    COCO image object-oriented model.

    Args/Attributes:
        id: (int): id
        file_name: (str): file name
        width (Optional[int]): width, px
        height (Optional[int]): height, px
        license (Optional[str]): license id
        flickr_url (Optional[str]): flickr image url
        coco_url (Optional[str]): coco image url
        date_captured (Optional[str]): date captured

    """
    def __init__(
        self,
        id: int, 
        file_name: str, 
        width: Optional[int] = None, 
        height: Optional[int] = None, 
        license: Optional[str] = None, 
        flickr_url: Optional[str] = None, 
        coco_url: Optional[str] = None, 
        date_captured: Optional[str] = None
    ):
        super().__init__(id)
        self.file_name = file_name
        self.width = width
        self.height = height
        self.license = license
        self.flickr_url = flickr_url
        self.coco_url = coco_url
        self.date_captured = date_captured



class Factory(AbstractFactory):
    """
    Factory used to create an instance of object-oriented model

    There are two ways of accessing the class:
        1) Using entity_factory property of Image Collection class:
            >>> from coco_orm.collections import ImageCollection
            >>> image_collection = ImageCollection()
            >>> image = image_collection.entity_factory(id=1, file_name="1.jpg")
        2) Importing from models module:
            >>> from coco_orm.models import Image
            >>> image = Image(id=1, file_name="1.jpg")
    """

    def __new__(
        cls,
        file_name: str, 
        width: Optional[int] = None, 
        height: Optional[int] = None, 
        license: Optional[str] = None, 
        flickr_url: Optional[str] = None, 
        coco_url: Optional[str] = None, 
        date_captured: Optional[str] = None,
        id: int = 0
    ) -> Model:
        """
        Implementation of the abstract method. Called whenever a Factory class is instantianted.

        Args:
            id: (int): id. If not specified: id = last_element_id + 1
            file_name: (str): file name
            width (Optional[int]): width, px
            height (Optional[int]): height, px
            license (Optional[str]): license id
            flickr_url (Optional[str]): flickr image url
            coco_url (Optional[str]): coco image url
            date_captured (Optional[str]): date captured

        Returns:
            Model: a instance of Model class containing entity data.
        """
        return Model(id, file_name, width, height, license, flickr_url, coco_url, date_captured)

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
            file_name = str(data[FILE_NAME]),
            width = int(data[WIDTH]) if data.get(WIDTH) is not None else None,
            height = int(data[HEIGHT]) if data.get(HEIGHT) is not None else None,
            license = int(data[LICENSE]) if data.get(LICENSE) is not None else None,
            flickr_url = str(data[FLICKR_URL]) if data.get(FLICKR_URL) is not None else None,
            coco_url = str(data[COCO_URL]) if data.get(COCO_URL) is not None else None,
            date_captured = str(data[DATE_CAPTURED]) if data.get(DATE_CAPTURED) is not None else None
        )