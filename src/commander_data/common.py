import dataclasses
import sys

from .api import COMMAND

@dataclasses.dataclass(frozen=True)
class _Python:
    _run: type(COMMAND)
    module: type(COMMAND)
    pip: type(COMMAND)

    def __getattr__(self, name: str):
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

LOCAL_PYTHON = _Python(COMMAND(sys.executable))
PATH_PYTHON = _Python(COMMAND.python)
BASE_PYTHON = _Python(COMMAND(sys.base_exec_prefix + "/bin/python3"))

DOCKER = COMMAND.docker

CONDA = COMMAND.conda

