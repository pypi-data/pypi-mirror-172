"""Kameleoon Configuration Settings"""

from typing import Any, Dict, Optional


class KameleoonConfigurationSettings:
    """
    KameleoonConfigurationSettings is used for saving setting's parameters, e.g
    state of real time update for site code and etc
    """
    # pylint: disable=R0903
    def __init__(self, configuration: Optional[Dict[str, Any]] = None):
        self.real_time_update: bool = bool(configuration['realTimeUpdate'] if configuration else False)
