from typing import List, Tuple
from ..operators.core import _logical_operators, _comparison_operators, _membership_operators, _min_comparison_operators, _max_comparison_operators, IN


"""Strings containing valid operators. Used by checker methods for exception message generation."""
_comparison_ops_str = ', '.join(_comparison_operators)
_min_comparison_ops_str = ', '.join(_min_comparison_operators)
_max_comparison_ops_str = ', '.join(_max_comparison_operators)
_membership_ops_str = ', '.join(_membership_operators)
_logical_ops_str = ', '.join(_logical_operators)


def check_comparison_operator(property_name: str, operator: str) -> str:
    """
    Check comparison operator.

    Args:
        property_name (str): a name of a property operator is going to be applied to.
        operator (str): an operator type.

    Raises:
        Exception: if given operator is not valid.

    Returns:
        str: an operator type.
    """
    if operator not in _comparison_operators:
        raise Exception(f"Invalid comparison operator of {property_name} property_name. Supported comparison operators: {_comparison_ops_str}")
    return operator

def check_range_comparison_operator(property_name: str, min_operator: str, max_operator: str) -> Tuple[str, str]:
    """
    Check range comparison operator.

    Args:
        property_name (str): a name of a property operator is going to be applied to.
        min_operator (str): an minimum operator type.
        max_operator (str): an maximum operator type.

    Raises:
        Exception: if given operators are not valid.

    Returns:
        Tuple[str, str]: a tuple containing min/max operator values.
    """
    if min_operator not in _min_comparison_operators: 
        raise Exception(f"Invalid min_value comparison operator of {property_name} property_name. Supported comparison operators: {_min_comparison_ops_str}")
    if max_operator not in _max_comparison_operators: 
        raise Exception(f"Invalid max_value comparison operator of {property_name} property_name. Supported comparison operators: {_max_comparison_ops_str}")
    return min_operator, max_operator

def check_membership_operator(property_name: str, operator: str) -> str:
    """
    Check membership operator.

    Args:
        property_name (str): a name of a property a given operator is going to be applied to.
        operator (str): an operator type.

    Raises:
        Exception: if given operator is not valid.

    Returns:
        str: an operator type.
    """
    if operator not in _membership_operators: 
        raise Exception(f"Invalid membership operator of {property_name} property_name. Supported membership operators: {_membership_ops_str}")
    return operator

def check_logical_operator(operator: str) -> None:
    """
    Check logical operator.

    Args:
        operator (str): an operator type.

    Raises:
        Exception: if given operator is not valid.
    """
    if operator not in _logical_operators:
        raise Exception(f"Invalid logical operator: {operator}. Supported logical operators: {_logical_ops_str}")


def filter_collection(collection: List, attr_name: str, attr_values: List) -> List:
    """
    Filter collection by attribute values.

    Args:
        collection (BaseCollection): an instance of BaseCollection implementation to filter.
        attr_name (str): an attribute name to filter collection by.
        attr_values (List): a list attribute values to filter collection by.

    Returns:
        list: a list containing filtered collection entities.
    """
    return [entity for entity in collection if getattr(entity, attr_name) in attr_values]

def extract_unique_attr_values(collection: List, attr_name: str) -> List:
    """
    Extract unique attribute values from the collection.
    Get all attribute values -> leave unique ones.

    Args:
        collection (BaseCollection): an instance of BaseCollection implementation to filter.
        attr_name (str): an attribute name to extract unique values from.

    Returns:
        list: a list containing unique attribute va;lues.
    """
    return list(set([getattr(entity, attr_name) for entity in collection]))