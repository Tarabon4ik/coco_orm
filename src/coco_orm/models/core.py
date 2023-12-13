from abc import ABC, abstractmethod
from typing import Dict

ID = "id"

class BaseModel():
    """
    BaseModel contains all common implementations shared by child classes.
    All models must inherit that class in order to work properly in the COCO environment.

    """
    def __str__(self):
        """
        Returns a string representation of an model.

        Returns:
            str: a dictionarized repressentaion of a model.
        """
        return f'{self.to_dict()}'

    def to_dict(self) -> Dict:
        """
        Get dictionarized representation of a model.

        Returns:
            dict: a dict containing model data.
        """
        return vars(self)


class BaseEntityModel(BaseModel):
    """
    BaseEntityModel has a basic structure for entities used as collection.
    All collection entity models must inherit that class in order to work properly in the COCO environment.

    Args/Attributes:
        id (in): an id of an entity represented by the model.
    """
    def __init__(self, id: int):
        self.id = id


class AbstractFactory(ABC):
    """
    AbstractFactory defines common abstract methods.
    All factories must inherit that class in order to work properly in the COCO environment.
    """

    @abstractmethod
    def __new__(self) -> BaseModel:
        """
        Returns an instance of BaseModel (object-oriented model) when an AbstractFactory is instanciated.

        Returns:
            BaseModel: an instance of BaseModel implementation containing entity data.
        """
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data: Dict) -> BaseModel:
        """
        Create an instance of BaseModel implementation from dictionary data.

        Args:
            data: (dict): a dictionary containing entity data.

        Returns:
            BaseModel: an instance of BaseModel implementation containing entity data.
        """
        pass