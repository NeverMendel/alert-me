from abc import ABC, abstractmethod
from functools import singledispatchmethod
import logging
from typing import Any, Dict, List


class Plugin(ABC):
    name: str = ""
    required_init_params: dict["str", type] = {}
    required_notify_params: dict["str", type] = {}

    @singledispatchmethod
    def __init__(self, init_params):
        raise ValueError(f"Invalid type for init_params: {type(init_params)}")

    @__init__.register
    def _from_dict(self, init_params: Dict[str, Any]):
        if self.name.strip() == "":
            raise Exception("Plugin name cannot be empty")
        self.init_params = init_params
        check_params(self.required_init_params, self.init_params)

    @__init__.register
    def _from_args(self, *args: List[Any]):
        init_params = _args_to_dict(self.required_init_params, *args)
        self.__init__(init_params)

    @abstractmethod
    def notify(self, **notify_params: dict[str, Any]) -> None:
        check_params(self.required_notify_params, notify_params)

    def notify_args(self, *args: []) -> None:
        notify_params = _args_to_dict(self.required_notify_params, *args)
        self.notify(**notify_params)


def check_params(required_params: dict[str, type], params: dict[str, Any]) -> None:
    for param_name, param_type in required_params.items():
        if param_name not in params:
            raise Exception(f"Missing required parameter {param_name}")
        if param_type != type(params[param_name]):
            raise Exception(
                f"Wrong type for parameter {param_name}. Expected {param_type}, got {type(params[param_name])}"
            )


def _args_to_dict(expected_dict: dict[str, Any], *args: []):
    if len(args) < len(expected_dict):
        logging.warning(
            f"Insufficient arguments. Expected {len(expected_dict)}, got {len(args)}"
        )
    if len(args) > len(expected_dict):
        logging.warning(
            f"Wrong number of arguments. Expected {len(expected_dict)}, got {len(args)}"
        )
    res: dict[str, Any] = {}
    param_names = list(expected_dict.keys())

    for i, arg in enumerate(args):
        if i >= len(param_names):
            break

        param_name = param_names[i]
        param_type = expected_dict[param_name]

        res[param_name] = arg

    check_params(expected_dict, res)