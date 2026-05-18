from __future__ import annotations

from contextlib import contextmanager
from collections.abc import Iterator

from opentelemetry import trace


def get_tracer(name: str) -> trace.Tracer:
    return trace.get_tracer(name)


@contextmanager
def traced_span(name: str, **attributes: str | int | float | bool) -> Iterator[None]:
    tracer = get_tracer(__name__)
    with tracer.start_as_current_span(name) as span:
        for key, value in attributes.items():
            span.set_attribute(key, value)
        yield

