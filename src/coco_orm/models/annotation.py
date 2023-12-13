from typing import List, Dict, Optional
from .core import BaseEntityModel, AbstractFactory, ID


"""Constants defining dictionary keys."""
ID = ID
IMAGE_ID = "image_id"
CATEGORY_ID = "category_id"
SEGMENTATION = "segmentation"
AREA = "area"
BBOX = "bbox"
ISCROWD = "iscrowd"

"""Constants bbox list indicies."""
BBOX_X_IDX = 0
BBOX_Y_IDX = 1
BBOX_WIDTH_IDX = 2
BBOX_HEIGHT_IDX = 3


class Model(BaseEntityModel):
    """
    COCO annotation object-oriented model.

    Args/Attributes:
        id: (int): id
        image_id: (int): image id
        category_id: (int): category id
        bbox (list[int]): a list of bbox coordinates
        iscrowd (int): is bbox contains crowd?
        segmentation (Optional[List]): a list of polygons
        area (Optional[float]): an area of bbox, px
    """
    def __init__(
        self,
        id: int, 
        image_id: int, 
        category_id: int, 
        bbox: List[int],
        iscrowd: int,
        segmentation: Optional[List] = None, 
        area: Optional[float] = None
    ):
        super().__init__(id)
        self.image_id = image_id
        self.category_id = category_id
        self.segmentation = segmentation
        self.area = area
        self.bbox = bbox
        self.iscrowd = iscrowd


class Factory(AbstractFactory):
    """
    Factory used to create an instance of object-oriented model

    There are two ways of accessing the class:
        1) Using entity_factory property of Annotation Collection class:
            >>> from coco_orm.collections import AnnotationCollection
            >>> annotation_collection = AnnotationCollection()
            >>> annotation = annotation_collection.entity_factory(id=1, image_id=1, category_id=1, bbox=[24, 67, 12, 21])
        2) Importing from models module:
            >>> from coco_orm.models import Annotation
            >>> annotation = Annotation(id=1, image_id=1, category_id=1, bbox=[24, 67, 12, 21])
    """

    def __new__(
        cls,
        image_id: int, 
        category_id: int, 
        bbox: List[int], 
        segmentation: Optional[List] = None, 
        area: Optional[float] = None, 
        iscrowd: int = 0,
        id: int = 0
    ) -> Model:
        """
        Implementation of the abstract method. Called whenever a Factory class is instantianted.

        Args:
            image_id: (int): image id
            category_id: (int): category id
            bbox (list[int]): a list of bbox coordinates
            segmentation (Optional[List]): a list of polygons
            area (Optional[float]): an area of bbox, px
            iscrowd (int), default = 0: is bbox crowd?
            id: (int), default = 0: id. If not specified: id = collection.last_element_id + 1 + 1

        Returns:
            Model: a instance of Model class containing entity data.
        """
        return Model(id, image_id, category_id, bbox, iscrowd, segmentation, area)


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
            image_id = int(data[IMAGE_ID]),
            category_id = int(data[CATEGORY_ID]),
            bbox = list(map(int, data[BBOX])),
            segmentation = data[SEGMENTATION] if data.get(SEGMENTATION) is not None else None,
            area = float(data[AREA]) if data.get(AREA) is not None else None,
            iscrowd = int(data[ISCROWD]) if data.get(ISCROWD) is not None else 0
        )