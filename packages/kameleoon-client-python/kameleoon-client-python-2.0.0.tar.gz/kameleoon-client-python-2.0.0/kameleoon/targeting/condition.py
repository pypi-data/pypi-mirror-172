from kameleoon.exceptions import NotFoundError
from typing import Any, Union, Dict


class Condition:

    def __init__(self, json_condition: Dict[str, Union[str, Any]]):
        self.type_ = json_condition.get('targetingType')
        if ('include' not in json_condition or json_condition['include'] is None) and ('isInclude' not in json_condition or json_condition['isInclude'] is None):
            raise NotFoundError('include / isInclude missed')
        self.include = json_condition['include'] if 'include' in json_condition else json_condition['isInclude']            

    def check(self, conditions):
        raise NotImplementedError