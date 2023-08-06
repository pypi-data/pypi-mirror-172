import inspect
from typing import Callable, List, Optional, Union

from chalk.features.resolver import MachineType
from chalk.streams.StreamResolver import parse_stream_resolver


def stream(
    fn: Optional[Callable] = None,
    environment: Optional[Union[List[str], str]] = None,
    machine_type: Optional[MachineType] = None,
):
    caller_filename = inspect.stack()[1].filename

    def decorator(args, cf=caller_filename):
        return parse_stream_resolver(args, cf, environment, machine_type)

    return decorator(fn) if fn else decorator
