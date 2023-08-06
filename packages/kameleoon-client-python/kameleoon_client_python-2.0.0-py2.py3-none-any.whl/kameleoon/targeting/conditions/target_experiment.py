from typing import Any, Optional, Union, Dict

from kameleoon.exceptions import NotFoundError
from kameleoon.targeting.condition import Condition
from kameleoon.targeting.conditions.constants import Operator

class TargetExperiment(Condition):
    def __init__(self, json_condition: Dict[str, Union[str, int, Any]]):
        super().__init__(json_condition)
        experiment_id_name = 'experiment'
        self.experiment_id = int(json_condition.get(experiment_id_name, -1))
        if self.experiment_id == -1:
            raise NotFoundError(experiment_id_name)
        variation_name = 'variation'
        self.variation = json_condition.get(variation_name)
        operator_name = 'variationMatchType'
        self.operator = json_condition.get(operator_name)
        if self.operator is None:
            raise NotFoundError(operator_name)

    def check(self, datas) -> bool:
        is_targeted = False
        variation_storage = dict[int, int](datas)
        is_saved_variation_storage_exist = bool(variation_storage)
        saved_variation_value = variation_storage.get(self.experiment_id , 0)
        if self.operator == Operator["EXACT"]:
            is_targeted = is_saved_variation_storage_exist and saved_variation_value == self.variation
        elif self.operator == Operator["ANY"]:
            is_targeted = is_saved_variation_storage_exist
        return is_targeted
        
