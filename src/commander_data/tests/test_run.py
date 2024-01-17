import argparse
import unittest
from hamcrest import (
    assert_that,
    equal_to,
    has_property,
    calling,
    raises,
    starts_with,
    all_of,
    has_item,
)

from .. import run
from .. import COMMAND


class TestRunner(unittest.TestCase):
    def test_basic_runner(self):
        runner = run.Runner()
        res = runner.safe_run(COMMAND.echo("hello"))
        assert_that(res.stdout.strip(), equal_to("hello"))

    def test_dry_runner(self):
        runner = run.Runner()
        res = runner.run(COMMAND.echo("hello"))
        assert_that(res.stdout.strip(), equal_to(""))

    def test_no_dry_runner(self):
        runner = run.Runner(no_dry_run=True)
        res = runner.run(COMMAND.echo("hello"))
        assert_that(res.stdout.strip(), equal_to("hello"))

    def test_args_runner(self):
        runner = run.Runner.from_args(argparse.Namespace())
        res = runner.safe_run(COMMAND.echo("hello"))
        assert_that(res.stdout.strip(), equal_to("hello"))

    def test_runner_fail(self):
        runner = run.Runner.from_args(argparse.Namespace())
        assert_that(
            calling(runner.safe_run).with_args(COMMAND.false),
            raises(
                Exception,
                matching=has_property(
                    "__notes__",
                    all_of(
                        has_item(starts_with("STDOUT:")),
                        has_item(starts_with("STDERR:")),
                    ),
                ),
            ),
        )
