from __future__ import annotations

from typing import Iterable, TypeVar

T = TypeVar("T")


def chunked(items: Iterable[T], size: int) -> list[list[T]]:
    buf: list[T] = []
    out: list[list[T]] = []
    for x in items:
        buf.append(x)
        if len(buf) >= size:
            out.append(buf)
            buf = []
    if buf:
        out.append(buf)
    return out
