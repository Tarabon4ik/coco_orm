from .image import Factory as ImageFactory
from .annotation import Factory as AnnotationFactory
from .category import Factory as CategoryFactory
from .license import Factory as LicenseFactory
from .info import Factory as InfoFactory


"""
API. Global variables holiding references to model factories.
"""
Image = ImageFactory
Annotation = AnnotationFactory
Category = CategoryFactory
License = LicenseFactory
Info = InfoFactory