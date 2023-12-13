from typing import Dict, Optional
from .core import BaseModel, AbstractFactory


"""Constants defining dictionary keys."""
YEAR = "year"
VERSION = "version"
DESCRIPTION = "description"
CONTRIBUTOR = "contributor"
URL = "url"
DATE_CREATED = "date_created"


class Model(BaseModel):
    """
    COCO info object-oriented model.

    Args/Attributes:
        year (Optional[int]): year
        version (Optional[str]): version
        description (Optional[str]): description
        contributor (Optional[str]): contributor
        url (Optional[str]): url
        date_created (Optional[str]): date_created
    """
    def __init__(
        self,
        year: Optional[int] = None, 
        version: Optional[str] = None, 
        description: Optional[str] = None, 
        contributor: Optional[str] = None, 
        url: Optional[str] = None, 
        date_created: Optional[str] = None
    ):
        self.year = year
        self.version = version
        self.description = description
        self.contributor = contributor
        self.url = url
        self.date_created = date_created


class Factory(AbstractFactory):
    """
    Factory used to create an instance of object-oriented model.

    To access the class, import it from models module.:
        >>> from coco_orm.models import Info
        >>> info = Info(id=1, year="2023")
    """

    def __new__(
        cls,
        year: Optional[int] = None, 
        version: Optional[str] = None, 
        description: Optional[str] = None, 
        contributor: Optional[str] = None, 
        url: Optional[str] = None, 
        date_created: Optional[str] = None
    ) -> Model:
        """
        Implementation of the abstract method.

        Args:
            year (Optional[int]): year
            version (Optional[str]): version
            description (Optional[str]): description
            contributor (Optional[str]): contributor
            url (Optional[str]): url
            date_created (Optional[str]): date_created

        Returns:
            Model: a instance of Model class containing info data.
        """
        return Model(year, version, description, contributor, url, date_created)

    @staticmethod
    def from_dict(data: Dict) -> Model:
        """
        Implementation of the abstract method.
        Builds an object-oriented info model from dictionary data.

        Args:
            data: (dict): a dictionary containing info data.

        Returns:
            Model: a instance of Model class containing info data.
        """
        return Model(
            year = int(data[YEAR]) if data.get(YEAR) is not None else None,
            version = str(data[VERSION]) if data.get(VERSION) is not None else None,
            description = str(data[DESCRIPTION]) if data.get(DESCRIPTION) is not None else None,
            contributor = str(data[CONTRIBUTOR]) if data.get(CONTRIBUTOR) is not None else None,
            url = str(data[URL]) if data.get(URL) is not None else None,
            date_created = str(data[DATE_CREATED]) if data.get(DATE_CREATED) is not None else None
        )