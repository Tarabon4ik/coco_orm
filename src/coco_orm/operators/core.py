# Comparison Operators
EQUAL = "=="
NOT_EQUAL = "!="
GREATER_THAN = ">"
LESS_THAN = "<"
GREATER_THAN_OR_EQUAL_TO = ">="
LESS_THAN_OR_EQUAL_TO = "<="
_comparison_operators = [EQUAL, NOT_EQUAL, GREATER_THAN, LESS_THAN, GREATER_THAN_OR_EQUAL_TO, LESS_THAN_OR_EQUAL_TO]
_min_comparison_operators = [GREATER_THAN, GREATER_THAN_OR_EQUAL_TO]
_max_comparison_operators = [LESS_THAN, LESS_THAN_OR_EQUAL_TO]

# Membership Operators
IN = "in"
NOT_IN = "not_in"
_membership_operators = [IN, NOT_IN]

# Logical Operators
AND = "and"
OR = "or"
_logical_operators = [AND, OR]

class ComparisonOperators():
    EQUAL = EQUAL
    NOT_EQUAL = NOT_EQUAL
    GREATER_THAN = GREATER_THAN
    LESS_THAN = LESS_THAN
    GREATER_THAN_OR_EQUAL_TO = GREATER_THAN_OR_EQUAL_TO
    LESS_THAN_OR_EQUAL_TO = LESS_THAN_OR_EQUAL_TO

class MembershipOperators():
    IN = IN
    NOT_IN = NOT_IN

class LogicalOperators():
    AND = AND
    OR = OR

class Operators(ComparisonOperators, MembershipOperators, LogicalOperators):
    pass