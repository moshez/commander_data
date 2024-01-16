import dataclasses
import pathlib
import os
import sys

from .api import COMMAND, CommandProtocol


@dataclasses.dataclass(frozen=True)
class _Python:
    _run: CommandProtocol
    module: CommandProtocol
    pip: CommandProtocol

    def __getattr__(self, name: str) -> CommandProtocol:
        return getattr(self._run, name)

    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)

    def __iter__(self):
        return iter(self._run)

    @classmethod
    def create(cls, python):
        module = python("-m")
        pip = module("pip")
        return cls(_run=python, module=module, pip=pip)


GIT = COMMAND.git

LOCAL_PYTHON = _Python.create(COMMAND(sys.executable))
PATH_PYTHON = _Python.create(COMMAND.python)
BASE_PYTHON = _Python.create(COMMAND(sys.base_exec_prefix + "/bin/python3"))


def env_python(env: str | pathlib.Path) -> CommandProtocol:
    """
    Return a virtual-env-specific Python

    Args:
        env: The directory of the virtual environment.

    Return:
        A command object with this Python
    """
    python_bin = os.fspath(pathlib.Path(env) / "bin" / "python")
    return _Python.create(COMMAND(python_bin))


DOCKER = COMMAND.docker

CONDA = COMMAND.conda
