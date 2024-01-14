import dataclasses
import functools
from typing import Any, Callable, Iterator, Iterable, Mapping, Protocol, Self


@functools.singledispatch
def _get_value_parts(value: Any, key: str) -> Iterator[str]:
    yield key
    yield str(value)


@_get_value_parts.register(type(None))
def _get_value_parts_none(value: None, key: str) -> Iterator[str]:
    yield key


@_get_value_parts.register(list)
def _get_value_parts_list(value: Iterable[Any], key: str) -> Iterator[str]:
    for item in value:
        yield from _get_value_parts(item, key)


def _parse_kwargs(kwargs: Mapping[str, Any]) -> Iterator[str]:
    for key, value in kwargs.items():
        if len(key) == 1:
            key = "-" + key
        else:
            key = "--" + key.replace("_", "-")
        yield from _get_value_parts(value, key)


class CommandProtocol(Protocol):  # pragma: no cover
    def __iter__(self) -> Iterator[str]:
        ...

    def __getattr__(self, name: str) -> Self:
        ...

    def __call__(self, *args: str, **kwargs: Any) -> Self:
        ...


@dataclasses.dataclass
class _Command:
    _contents: list[str] = dataclasses.field(default_factory=list)

    def __iter__(self) -> Iterator[str]:
        return iter(self._contents)

    def extend(self, things: Iterable[str]) -> Self:
        return dataclasses.replace(self, _contents=self._contents + list(things))

    def __getattr__(self, name: str) -> Self:
        return self.extend([name.replace("_", "-")])

    def __call__(self, *args: str, **kwargs: Any) -> Self:
        return self.extend(_parse_kwargs(kwargs)).extend(args)


COMMAND = _Command()


def run_all(run: Callable, *commands: Iterable[str], **kwargs: Any):
    for a_command in commands:
        run(a_command, **kwargs)
