from __future__ import annotations

from dataclasses import dataclass, field
from functools import partial
from typing import Type, Dict, Any, Callable, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .plugin import Plugin


@dataclass
class Violation:
    code: str
    message: str
    line: int
    col: int
    args: Tuple[Any, ...] = ()
    kwargs: Dict[str, Any] = field(default_factory=dict)

    @property
    def full_message(self):
        return f'{self.code} {self.formatted_message}'

    @property
    def formatted_message(self):
        return self.message.format(*self.args, **self.kwargs)

    def as_tuple(self, type_: Type[Plugin]):
        return self.line, self.col, self.full_message, type_


create_violation = partial(partial, Violation)
ViolationFactory = Callable[[int, int, Tuple[Any, ...], Dict[str, Any]], Violation]
