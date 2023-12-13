from typing import Optional, Union
import os
import shutil

import numpy as np
from PIL import Image

from .utils import handle_exceptions

class Repository():
    """
    Repository class contains implementation of CRUD operations for image files.

    There are two ways of using the repo:
        1) Accessing the repo from ImageCollection instance:
            >>> img = image_collection.repository.read("1.jpg")
            Please, refer to ``coco_orm.collections.image.Collection`` to find more.
        2) Importing from collections module:
            >>> from coco_orm.collections.image.repository import ImageRepository
            >>> image_repo = ImageRepository("/images/dir")
            >>> img = image_repo.read("1.jpg")

    Args/Attributes:
        dir_path (str): a path to dirctory containing images.
    """
    def __init__(self, dir_path: str):
        self.dir_path = dir_path
    
    def _get_image_filepath(self, file_name: str) -> str:
        """
        Private method. Get image filepath.

        Args:
            file_name (str): a file name of an image.

        Returns:
            str: a file path of an image.
        """
        return os.path.join(self.dir_path, file_name)

    def read(self, file_name: str) -> Image.Image:
        """
        Read an image file.

        Args:
            file_name (str): a file name of an image.

        Returns:
            Image.Image: a image of PIL type.
        """
        return Image.open(self._get_image_filepath(file_name))

    @handle_exceptions
    def save(self, img: Union[Image.Image, np.ndarray], file_name: str) -> bool:
        """
        Save an image file.
        @handle_exceptions decorator is applied to the function to standardize return value to bool.

        Args:
            img (Image.Image | np.ndarray): image to save.
            file_name (str): a file name of an image.

        Returns:
            bool: True if an image is successfuly saved, False if not.
        """
        if isinstance(img, np.ndarray):
            img = Image.fromarray(img)
        img.save(self._get_image_filepath(file_name))
        img.close()

    @handle_exceptions
    def delete(self, file_name: str) -> bool:
        """
        Delete an image file.
        @handle_exceptions decorator is applied to the function to standardize return value to bool.

        Args:
            file_name (str): a file name of an image.

        Returns:
            bool: True if an image is successfuly deleted, False if not.
        """
        os.remove(self._get_image_filepath(file_name))

    @handle_exceptions
    def copy(self, file_name: str, dst_dir_path: str) -> bool:
        """
        Copy an image file.
        @handle_exceptions decorator is applied to the function to standardize return value to bool.

        Args:
            file_name (str): a file name of an image.

        Returns:
            bool: True if an image is successfuly copied, False if not.
        """
        shutil.copy(self._get_image_filepath(file_name), os.path.join(dst_dir_path, file_name))
        


class Factory():
    """
    Factory class responsible for creating of Repository instances

    When instanciated, the __new__ method is called.
    """
    def __new__(cls, dir_path: Optional[str] = None) -> Repository:
        """
        Create a Repository instance/reference.

        Args:
            dir_path (Optional[str]): a directory path containing images.

        Returns:
            Repository: an instance of Repository if dir_path is provided, else a reference to Repository.
        """
        return Repository(dir_path) if dir_path else Repository



# Global instance of Repository Factory to be used by users.
ImageRepository = Factory
