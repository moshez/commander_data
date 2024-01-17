import argparse
import functools
import io
import subprocess
from typing import Callable, Sequence, Protocol, Self

import attrs

class CalledProcessLike(Protocol): # pragma: no cover
    @property
    def stdout(self) -> io.TextIOBase | io.TextIOWrapper:
        ...
    def stderr(self) -> io.TextIOBase | io.TextIOWrapper:
        ...


@attrs.frozen
class _FakeCalledProcess:
    stdout: io.TextIOBase = attrs.field(factory=io.StringIO, init=False)
    stderr: io.TextIOBase = attrs.field(factory=io.StringIO, init=False)
    

def _really_run(orig_run: Callable, cmdargs: Sequence[str], *args: Any, **kwargs: Any) -> CalledProcessLike:
    LOGGER.info("Running %s", cmdargs)
    real_kwargs = dict(check=True, capture_output=True, text=True)
    real_kwargs.update(kwargs)
    try:
        return orig_run(cmdargs, *args, **real_kwargs)
    except subprocess.CalledProcessError as exc:
        exc.add_note(f"STDERR: {exc.stderr}")
        exc.add_note(f"STDOUT: {exc.stdout}")
        raise

@attrs.frozen
class Runner:
    _orig_run: Callable = attrs.field(default=subprocess.run)
    _no_dry_run: bool = attrs.field(default=False, kw_only=True)

    @functools.wraps(subprocess.run)
    def run(self, cmdargs: Sequence[str], *args: Any, **kwargs: Any) -> CalledProcessLike:
        if self._no_dry_run:
            return _really_run(self._orig_run, cmdargs, *args, **kwargs)
        else:
            LOGGER.info("Dry run, not running %s", cmdargs)
            return _FakeCalledProcess()

    @functools.wraps(subprocess.run)
    def safe_run(self, cmdargs: Sequence[str], *args: Any, **kwargs: Any) -> CalledProcessLike:
        return _really_run(self._orig_run, cmdargs, *args, **kwargs)

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> Self:
        return cls(
            orig_run=getattr(args, "orig_run", subprocess.run),
            no_dry_run=getattr(args, "no_dry_run", False),
        )
            
        
    