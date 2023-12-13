from typing import List, Dict, Optional, Union

from ..models.core import BaseEntityModel, AbstractFactory as AbstractEntityFactory
from ..filters.core import BaseFilter

class BaseCollection(list):
    """
    BaseCollection inherits structure and features of standard python list that allows to use the collection instances as a list.
    BaseCollection contains common implementations shared by child instances to simplify and standardize COCO dataset collections processing.
    
    All collection classes must inherit that class in order to work properly in the COCO environment.
    All COCO collections have already been implemented.  See ``coco_orm.collections``
       
    Args:
        entities (list[dict] | list[BaseEntityModel] | None), default = None: pass a list of dicts or BaseEntityModel implementation instances to create a collection containing entities, 
                or nothing to create an empty collection.
        entity_factory (AbstractEntityFactory): a reference to AbstractEntityFactory implementation.
        filters (BaseFilter): a reference to BaseFilter implementation. 

    Attributes:
        entity_factory (AbstractEntityFactory): an AbstractEntityFactory implementation reference, used to initialize entities of the collection. 
                To initialize an entity, use the class property as follows: ``entity = collection.entity_factory(id=1)``
                Please, reffer to AbstractEntityFactory class to see all possible ways of creating collection entities.
        filters_builder (BaseFilter): an BaseFilter implementation reference, used to build collection filters.
                To build a filter instance, use the class property as follows: 
                >>> filters = (collection.filters_builder().
                ...     ids([1, 2, 3]).
                ...     OR.
                ...     ids([4, 5, 6])
                ... )
                There are two ways of applying filters to the collection. 
                    1) Call ``filter`` BaseCollection method with filters object passed as an argument:
                        >>> filtered_collection = collection.filter(filters)
                    2) Call ``apply`` BaseFilter method with collection object passed as an argument:
                        >>> filtered_collection = filters.apply(collection)
    """
    def __init__(self, entity_factory: AbstractEntityFactory, filters: BaseFilter, entities: Union[List[Dict], List[BaseEntityModel], None] = None):
        self.entity_factory = entity_factory # reference to AbstractEntityFactory
        self.filters_builder = filters # reference to BaseFilter 
        super().__init__(self._process_entities(entities) if entities else []) # type: list[BaseEntityModel]

    def __call__(self, entities: Union[List[Dict], List[BaseEntityModel], None], entity_factory: AbstractEntityFactory, filters: BaseFilter):
        """
        Allows invoking a class instance as a function.
        Used by filters objects to instanciate a collection with filtered entities.
        Please, reffer to ``BaseFilter.apply_on`` method to see how filters use collection instances.

        Args:
            entities (list[dict] | list[BaseEntityModel] | list | None): pass a list of dicts or BaseEntityModel instances to create a collection containing entities, 
                    or an empty list / None to create an empty collection.
            entity_factory (AbstractEntityFactory): a reference to AbstractEntityFactory implementation.
            filters (BaseFilter): a reference to BaseFilter implementation. 

        Returns:
            BaseCollection: a BaseCollection instance.
        """
        return BaseCollection(entities, entity_factory, filters)

    def __str__(self):
        """
        Returns a string representation of an object.

        Returns:
            str: a dictionarized repressentaion of collection entities.
        """
        return f'{self.to_dict()}'
    
    def get_by_id(self, value: int) -> Optional[BaseEntityModel]:
        """
        Get entity by id. 

        Args:
            value (int): id of an entity to search for.

        Returns:
            Optional[BaseEntityModel]: an BaseEntityModel implementation instance containing entity data if one is found, else None
        """
        return next((entity for entity in self if entity.id == value), None)

    def append(self, entity: BaseEntityModel) -> int: 
        """
        Append an entity into the collection. 

        Args:
            entity (BaseEntityModel): an instance of BaseEntityModel implementation containing entity data.

        Returns:
            int: id of an appended entity.
        """
        entity.id = self.last_id + 1 if entity.id == 0 else entity.id
        super().append(entity)
        return entity.id

    def update(self, entity: BaseEntityModel) -> Optional[int]: 
        """
        Update an entity of the collection. 

        Args:
            entity (BaseEntityModel): an instance of BaseEntityModel implementation containing entity data.

        Returns:
            Optional[int]: id if an entity has been found and updated, None if not.
        """
        for idx, item in enumerate(self):
            if item.id == entity.id:
                self[idx] = entity
                return entity.id
        return None

    def delete(self, id: int) -> Optional[BaseEntityModel]: 
        """
        Delete an entity from the collection. 

        Args:
            entity (BaseEntityModel): an instance of BaseEntityModel implementation containing entity data.

        Returns:
            Optional[BaseEntityModel]: an instance of BaseEntityModel implementation if entity with given id is found, None if not
        """
        for idx, item in enumerate(self):
            if item.id == id:
                del self[idx]
                return item
        return None

    @property
    def last_id(self) -> int:
        """id of the last element in the collection."""
        if self:
            last_entity = max(self, key=lambda entity: entity.id)
            return last_entity.id
        return 0
    
    @property
    def num_of_entities(self) -> int:
        """a number of entities in the collection."""
        return len(self)
    
    def to_dict(self) -> List[Dict]:
        """
        Get dictionarized representation of the collection.
        
        Returns:
            list[dict]: a list of dictionaries containing entities data.
        """
        return [entity.to_dict() for entity in self]
    
    def filter(self, filters: BaseFilter, inplace: bool = False):
        """
        Filter the collection by given filters.

        Args:
            filters (BaseFilter): an instance of BaseFilter implementation, containing filters.
            inplace (bool): replace the collection with a filtered one

        Returns:
            BaseEntityModel: an instance of BaseEntityModel implementation.
        """
        filtered_entities = filters.apply(self)
        if inplace:
            self.clear()
            self.extend(filtered_entities)
        return BaseCollection(entities=filtered_entities, entity_factory=self.entity_factory, filters=self.filters_builder)

    def _process_entities(self, entities: Union[List[Dict], List[BaseEntityModel]]) -> List[BaseEntityModel]:
        """
        Private method. Transforms a collection of list[dict] type to list[BaseEntityModel] if provided of such type.

        Args:
            entities (list[dict] | list[BaseEntityModel]): a list of dictionaries containing data.

        Returns:
            list[BaseEntityModel]: a list of BaseEntityModel implementation instances.
        """
        return [self.entity_factory.from_dict(entity) for entity in entities] if isinstance(entities[0], dict) else entities