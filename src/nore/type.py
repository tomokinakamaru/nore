from typing import Any
from typing import Callable
from typing import TypeVar


Func = TypeVar('Func', bound=Callable[..., Any])
