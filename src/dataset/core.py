from typing import List, Dict, Optional, Union
from .utils import write_json_file, read_json_file, is_url, is_file_exists, download
from ..models.info import Model as InfoModel, Factory as InfoFactory
from ..collections.image import Collection as ImageCollection
from ..collections.annotation import Collection as AnnotationCollection
from ..collections.category import Collection as CategoryCollection
from ..collections.license import Collection as LicenseCollection
from ..filters.image import Filters as ImageFilters
from ..filters.annotation import Filters as AnnotationFilters
from ..filters.category import Filters as CategoryFilters
from ..filters.license import Filters as LicenseFilters

"""Constants defining dictionary keys."""
INFO = "info"
IMAGES = "images"
ANNOTATIONS = "annotations"
CATEGORIES = "categories"
LICENSES = "licenses"

class CocoDataset():
    """
    COCO image object-oriented model.

    Args/Attributes:
        filepath (str): path to the json file containing dataset annotations.
        images (ImageCollection): an instance of ImageCollection class
        annotation (AnnotationCollection): an instance of AnnotationCollection class
        category (CategoryCollection): an instance of CategoryCollection clas
        license (Optional[LicenseCollection]): an instance of LicenseCollection class
        info (Optional[InfoModel]): an instance of InfoModel class
    """
    def __init__(
        self,
        filepath: str,
        images: ImageCollection,
        annotations: AnnotationCollection,
        categories: CategoryCollection,
        licenses: Optional[LicenseCollection] = None,
        info: Optional[InfoModel] = None,
    ):
        self.filepath = filepath
        self.info = info if info else InfoModel() # type: InfoModel
        self.images = images
        self.annotations = annotations
        self.categories = categories
        self.licenses = licenses if licenses else LicenseCollection

    def to_dict(self):
        """
        Transform class object to dictionary.

        Returns:
            dict: a dictionary containing COCO dataset.
        """
        return {
            INFO: self.info.to_dict(),
            IMAGES: self.images.to_dict(),
            ANNOTATIONS: self.annotations.to_dict(),
            CATEGORIES: self.categories.to_dict(),
            LICENSES: self._handle_licenses(),
        }
    
    def _handle_licenses(self):
        try: return self.licenses.to_dict()
        except: return []

    def __str__(self):
        """
        Returns a string representation of COCO dataset.

        Returns:
            str: a dictionarized repressentaion of COCO dataset.
        """
        return f'{self.to_dict()}'

    def save(self, filepath: str = None, images_dir_path: str = None) -> None:
        """
        Save COCO dataset in .json file.

        Args:
            filepath (str): path to the json file to store COCO dataset.
            images_dir_path(Optional[str]): path to yhe directory containing dataset images.
        """
        write_json_file(self.to_dict(), filepath if filepath else self.filepath)
        if images_dir_path:
            self.images.copy_to_dir(images_dir_path)
            
    def filter(self, image_filters: ImageFilters, annotation_filters: AnnotationFilters, category_filters: CategoryFilters, license_filters: Optional[LicenseFilters] = None, images_dir_path: Optional[str] = None, inplace: bool = False):
        """
        Applies filters to the dataset.

        Args:
            image_filters (ImageFilters): filters for image collection.
            annotation_filters (AnnotationFilters): filters for annotation collection.
            category_filters (CategoryFilters): filters for category collection.
            license_filters (Optional[LicenseFilters]): filters for license collection.
            images_dir_path (Optional[str]): a path to the directory containing dataset images.
            inplace (bool): If true - apply filters on self collection, else - return a new one with filters applied.

        Returns:
            CocoDataset: an object containing filtered collections.
        """
        # apply user filters
        filtered_images = self.images.filter(image_filters, inplace) # type: ImageCollection
        filtered_categories = self.categories.filter(category_filters, inplace) # type: CategoryCollection
        filtered_licenses = self.licenses.filter(license_filters, inplace) if license_filters else None
        # apply intersection filters
        filtered_annotations = self.annotations.filter(annotation_filters.intersection(filtered_images, filtered_categories, filtered_licenses), inplace)
        filtered_categories = filtered_categories.filter(filtered_categories.filters_builder().intersection(filtered_annotations), inplace)
        filtered_images = filtered_images.filter(filtered_images.filters_builder().intersection(filtered_annotations), inplace)
        filtered_licenses = filtered_licenses.filter(filtered_licenses.filters_builder().intersection(filtered_images), inplace) if license_filters else None
        dataset = CocoDataset(
            filtered_images,
            filtered_annotations,
            filtered_categories,
            filtered_licenses if filtered_licenses else self.licenses,
            self.info,
            images_dir_path if images_dir_path else self.images.repository.dir_path
        )
        if images_dir_path: dataset.images.copy_to_dir(images_dir_path)
        if inplace: self = dataset
        return dataset


    
class Factory():
    def __new__(cls, annotations_filepath: str, images_dir_path: Optional[str] = None) -> CocoDataset:
        """
        Static method. Returns a new object of the class while being instantiated.

        Args:
            annotations_filepath (str): path to the json file containing (or will containt) COCO dataset.
            images_dir_path(Optional[str]): path to yhe directory containing dataset images.

        Returns:
            CocoDataset: a new instance of CocoDataset class.
        """
        if is_url(annotations_filepath): 
            return Factory.from_dict(annotations_filepath, download(annotations_filepath), images_dir_path)
        if is_file_exists(annotations_filepath):
            return Factory.from_dict(annotations_filepath, read_json_file(annotations_filepath), images_dir_path)
        return Factory.new(annotations_filepath, images_dir_path)

    @staticmethod
    def new(filepath: str, images_dir_path: Optional[str] = None) -> CocoDataset:
        return CocoDataset(
            filepath, 
            ImageCollection([], images_dir_path), 
            AnnotationCollection([]), 
            CategoryCollection([]), 
            LicenseCollection([]), 
            InfoFactory()
        )

    @staticmethod
    def from_dict(filepath: str, data: Dict, images_dir_path: Optional[str] = None) -> CocoDataset:
        """
        Static method.
        Builds an object-oriented COCO dataset model from dictionary data.

        Args:
            data: (dict): a dictionary containing COCO dataset.

        Returns:
            CocoDataset: an instance of CocoDataset class.
        """
        return Factory.from_collections(
            filepath = filepath,
            images = data[IMAGES],
            annotations = data[ANNOTATIONS],
            categories = data[CATEGORIES],
            licenses = data[LICENSES] if LICENSES in data else None,
            info = data[INFO] if INFO in data else None,
            images_dir_path = images_dir_path
        )
    
    @staticmethod
    def from_collections(
        filepath: str,
        images: Union[ImageCollection, List[Dict]],
        annotations: Union[AnnotationCollection, List[Dict]],
        categories: Union[CategoryCollection, List[Dict]],
        licenses: Union[LicenseCollection, List[Dict], None] = None,
        info: Union[InfoModel, Dict, None] = None,
        images_dir_path: Optional[str] = None
    ) -> CocoDataset:
        """
        Static method.
        Builds an object-oriented COCO dataset model from collections.

        Args:
            images: Union[ImageCollection, List[Dict]]
            annotations: Union[AnnotationCollection, List[Dict]]
            categories: Union[CategoryCollection, List[Dict]]
            licenses: Union[LicenseCollection, List[Dict], None]
            info: Union[InfoModel, Dict, None]
            images_dir_path: Optional[str]

        Returns:
            CocoDataset: an instance of CocoDataset class.
        """
        if isinstance(images, list): images = ImageCollection(images, images_dir_path)
        if isinstance(annotations, list): annotations = AnnotationCollection(annotations)
        if isinstance(categories, list): categories = CategoryCollection(categories)
        if isinstance(licenses, list): licenses = LicenseCollection(licenses)
        if isinstance(info, dict): info = InfoFactory.from_dict(info)
        return CocoDataset(filepath, images, annotations, categories, licenses, info)
    
    @staticmethod
    def from_obj(dataset: CocoDataset, images_dir_path: Optional[str] = None) -> CocoDataset:
        """
        Static method.
        Builds an object-oriented COCO dataset model from CocoDataset object.

        Args:
            images (CocoDataset): an instance of CocoDataset object
            images_dir_path (Optinal[str]): path to directory containing dataset images.

        Returns:
            CocoDataset: an instance of CocoDataset class.
        """
        return CocoDataset(
            dataset.filepath,
            dataset.images,
            dataset.annotations,
            dataset.annotations,
            dataset.annotations,
            dataset.info,
            images_dir_path if images_dir_path else dataset.images.repository.dir_path
        )