"""Failure messages for `osiris-test`.

An assertion failure is an ordinary `AssertionError`, which pytest and unittest
both report without an adapter. This module only builds the message and tracks
the `testing` descriptions surrounding it, so nothing here needs to know which
runner is in use.
"""

from __future__ import annotations

from typing import Any, Callable

_contexts: list[str] = []


def within(description: object, body: Callable[[], Any]) -> None:
    """Run `body` with `description` pushed onto the surrounding context.

    A test runs to completion before the next one starts, so one stack is
    enough. The pop is unconditional: a failing assertion must not leave its
    description attached to whatever runs next.
    """
    _contexts.append(str(description))
    try:
        body()
    finally:
        _contexts.pop()


def _prefix(message: object) -> str:
    parts = list(_contexts)
    if message is not None:
        parts.append(str(message))
    return "".join(part + "\n" for part in parts)


def comparison_failure(
    form: object, left: object, right: object, message: object = None
) -> AssertionError:
    """Build the failure for a comparison, reporting both sides.

    Both sides were bound once before the comparison, so these are the values the
    assertion saw rather than a re-evaluation that might disagree with it.

    An `AssertionError` is returned rather than raised so the caller raises it —
    that keeps the raise at the assertion's own source position, which is what a
    runner reports and what a source map points at.
    """
    return AssertionError(
        "%s%s\n  left:  %r\n  right: %r" % (_prefix(message), form, left, right)
    )


def predicate_failure(form: object, message: object = None) -> AssertionError:
    return AssertionError("%s%s" % (_prefix(message), form))
