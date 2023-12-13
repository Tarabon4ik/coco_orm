from .image import Collection as ImageCollectionCls
from .annotation import Collection as AnnotationCollectionCls
from .category import Collection as CategoryCollectionCls
from .license import Collection as LicenseCollectionCls


"""
API. Global variables holiding references to collection classes.
"""
ImageCollection = ImageCollectionCls
AnnotationCollection = AnnotationCollectionCls
CategoryCollection = CategoryCollectionCls
LicenseCollection = LicenseCollectionCls