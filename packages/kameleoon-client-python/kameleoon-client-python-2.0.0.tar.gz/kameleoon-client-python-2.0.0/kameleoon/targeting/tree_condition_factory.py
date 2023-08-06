from enum import Enum
from typing import Optional
from kameleoon.targeting.condition import Condition

class ConditionType(Enum):
    """Targeting condition types"""
    CUSTOM_DATUM: str = "CUSTOM_DATUM"
    TARGET_EXPERIMENT: str = "TARGET_EXPERIMENT"
    EXCLUSIVE_EXPERIMENT: str = "EXCLUSIVE_EXPERIMENT"

class TreeConditionFactory(object):
    """Factory of targeting condition types"""
    @staticmethod
    def get_condition(condition_json) -> Optional[Condition]:
        from kameleoon.targeting.conditions.custom_datum import CustomDatum
        from kameleoon.targeting.conditions.target_experiment import TargetExperiment
        from kameleoon.targeting.conditions.exclusive_experiment import ExclusiveExperiment
        condition: Optional[Condition] = None
        if condition_json['targetingType'] == ConditionType.CUSTOM_DATUM.value:
            condition = CustomDatum(condition_json)
        elif condition_json['targetingType'] == ConditionType.TARGET_EXPERIMENT.value:
            condition = TargetExperiment(condition_json)
        elif condition_json['targetingType'] == ConditionType.EXCLUSIVE_EXPERIMENT.value:
            condition = ExclusiveExperiment(condition_json)
        return condition