import unittest
from hamcrest import assert_that, equal_to, contains_string

from .. import __version__, COMMAND, run_all


class TestInit(unittest.TestCase):
    def test_version(self):
        assert_that(__version__, contains_string("."))


class TestRunAll(unittest.TestCase):
    def test_simple_run_all(self):
        keep = []
        run_all(
            keep.append,
            ["git", "commit"],
        )
        assert_that(keep, equal_to([["git", "commit"]]))


class TestCommand(unittest.TestCase):
    def test_basic(self):
        assert_that(list(COMMAND), equal_to([]))

    def test_attribute(self):
        assert_that(list(COMMAND.git), equal_to(["git"]))

    def test_call_args(self):
        assert_that(list(COMMAND.git.init(".")), equal_to(["git", "init", "."]))

    def test_call_kwargs(self):
        assert_that(
            list(COMMAND.git.commit(all=None)), equal_to(["git", "commit", "--all"])
        )

    def test_call_kwargs_list(self):
        assert_that(
            list(COMMAND.copier(data=["a=b", "c=d"])),
            equal_to(["copier", "--data", "a=b", "--data", "c=d"]),
        )

    def test_call_kwargs_str(self):
        assert_that(
            list(COMMAND.git.commit(message="checkpoint")),
            equal_to(["git", "commit", "--message", "checkpoint"]),
        )

    def test_short_arg(self):
        assert_that(
            list(COMMAND.python(m=None).venv("my-env")),
            equal_to("python -m venv my-env".split()),
        )
