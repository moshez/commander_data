import dataclasses
import functools


@functools.singledispatch
def _get_value_parts(value, key):
    yield key
    yield str(value)


@_get_value_parts.register(type(None))
def _get_value_parts_none(value, key):
    yield key


@_get_value_parts.register(list)
def _get_value_parts_list(value, key):
    for item in value:
        yield from _get_value_parts(item, key)


def _parse_kwargs(kwargs):
    for key, value in kwargs.items():
        key = "--" + key.replace("_", "-")
        yield from _get_value_parts(value, key)


@dataclasses.dataclass
class _Command:
    _contents: object = dataclasses.field(default_factory=list)

    def __iter__(self):
        return iter(self._contents)

    def extend(self, things):
        return dataclasses.replace(self, _contents=self._contents + list(things))

    def __getattr__(self, name):
        return self.extend([name.replace("_", "-")])

    def __call__(self, *args, **kwargs):
        return self.extend(_parse_kwargs(kwargs)).extend(args)


COMMAND = _Command()
