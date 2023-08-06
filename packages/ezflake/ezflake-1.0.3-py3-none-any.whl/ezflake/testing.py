import ast
from textwrap import dedent
from typing import Type, Optional

from .plugin import Plugin
from .violation import Violation


def _violation_from_src(plugin_type: Type[Plugin], src: str):
    tree = ast.parse(dedent(src))
    plugin = plugin_type(tree)
    violations = plugin._run()
    if len(violations) == 0:
        return None

    assert len(violations) == 1
    return violations[0]


def assert_violates(plugin_type: Type[Plugin], expected_violation: Optional[Violation], src: str):
    violation = _violation_from_src(plugin_type, src)
    assert violation == expected_violation, f'Expected {expected_violation}, got {violation}'


def assert_not_violates(plugin_type: Type[Plugin], src: str):
    assert_violates(plugin_type, None, src)
