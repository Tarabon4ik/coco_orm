from typing import Optional, Union, Tuple

from PIL import Image
import numpy as np

from .core import BaseCollection
from ..models.image import Model, Factory
from ..filters.image import Filters
from .image_repository import Repository as ImageRepository, Factory as ImageRepositoryFactory
from .utils import check_and_fix_img_type


class Collection(BaseCollection):
    """
    Collection inherits BaseCollection class and contains methods to simplify and standardize COCO categories processing.

    To instantiate an Collection class, use following example:
    >>> from coco_orm.collections import ImageCollection
    >>> image_collection = ImageCollection()

    Args:
        dir_path (Optional[str]): a path to directory containing COCO dataset images.

    Attributes:
        repository (ImageRepository): an instance of ImageRepository with implemented CRUD operations on image files.
                To get access to the repo, use ``repository`` class property
                >>> img = image_collection.repository.read("1.jpg")
                >>> image_collection.repository.delete("1.jpg")
    """
    def __init__(self, entities, dir_path: Optional[str] = None):
        super().__init__(Factory, Filters, entities)
        self.repository = ImageRepositoryFactory(dir_path) # type: ImageRepository

    def __call__(self, entities):
        """Override. Return a Collection instance."""
        return Collection(Factory, Filters, entities)

    def get_by_id(self, value: int, img: bool = False) -> Tuple[Optional[Model], Optional[Image.Image]]:
        """
        Override. Get entity by id.
        Use as follows:
        >>> img_annotation = image_collection.get_by_id(1)
        >>> img_annotation, img = image_collection.get_by_id(1, img=True)

        Args:
            value (int): an id of an entity to search for.
            img (bool): return an image as PIL.Image if True, None if False 

        Returns:
            Tuple[Optional[Model], Optional[Image.Image]]: a tuple containing Model and Image if ones found, else Nones.      
        """
        # invoke parent method
        annotation = super().get_by_id(value) # type: Optional[Model]
        if annotation and img:
            img = self.repository.read(annotation.file_name)
        return annotation, check_and_fix_img_type(img)

    def get_by_file_name(self, value: str, img: bool = False) -> Tuple[Optional[Model], Optional[Image.Image]]:
        """
        Override. Get entity by file name.
        Use as follows:
        >>> img_annotation = image_collection.get_by_file_name("1.jpg")
        >>> img_annotation, img = image_collection.get_by_file_name("1.jpg", img=True)

        Args:
            value (str): an file name of an entity to search for.
            img (bool): return an image as PIL.Image if True, None if False

        Returns:
            Tuple[Optional[Model], Optional[Image.Image]]: a tuple containing Model and Image if ones found, else Nones.      
        """
        annotation = next((entity for entity in self if entity.file_name == value), None) # type: Optional[Model]
        if annotation and img:
            img = self.repository.read(annotation.file_name)
        return annotation, check_and_fix_img_type(img)

    def append(self, annotation: Model, img: Union[Image.Image, np.ndarray, None] = None):
        """
        Override. Append an image and its annotation into the collection. 

        Args:
            annotation (Model): an instance of Model containing image data.
            img (Image.Image | np.ndarray | None): an image to write to dataset directory, None if not needed.

        Returns:
            int: id of an appended image.
        """
        id = super().append(annotation) # invoke parent method
        if id and img:
            self.repository.save(img, annotation.file_name)
        return id

    def update(self, annotation: Model, img: Union[Image.Image, np.ndarray, None] = None):
        """
        Override. Update an image and its annotation.

        Args:
            annotation (Model): an instance of Model containing image data.
            img (Image.Image | np.ndarray | None): an image to write to dataset directory, None if not needed.

        Returns:
            int: id of an updated image.
        """
        id = super().update(annotation) # invoke parent method
        if id and img:
            self.repository.delete(annotation.file_name)
            self.repository.save(img, annotation.file_name)
        return id

    def delete(self, id: int, img: bool = False) -> Optional[Model]:
        """
        Override. Delete an image and its annotation.

        Args:
            id (int): id of an image to delete.
            img (bool): delete an image file from dataset directory if True.

        Returns:
            Optional[Model]: an annotation of deleted image.
        """
        annotation = super().delete(id) # type: Optional[Model]
        if annotation and img:
            self.repository.delete(annotation.file_name)
        return annotation
    
    def delete_by_file_name(self, value: str, img: bool = False) -> Optional[Model]:
        """
        Delete an image and its annotation by file name.

        Args:
            value (str): a file name of an image to delete.
            img (bool): delete an image file from dataset directory if True.

        Returns:
            Optional[Model]: an annotation of deleted image.
        """
        annotation, img = self.get_by_file_name(value, img) # type: Optional[Model]
        if annotation and img:
            self.repository.delete(annotation.file_name)
        return annotation
    
    def copy_to_dir(self, dir_path: str):
        """
        Copy image collection to a given dir

        Args:
            dir_path (str): a path to directory to copy images to.
        """
        for image in self: 
            self.repository.copy(image.file_name, dir_path)

