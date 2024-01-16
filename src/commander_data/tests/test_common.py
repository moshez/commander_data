import unittest

from hamcrest import assert_that, equal_to

from .. import common


class TestPython(unittest.TestCase):
    def test_local(self):
        assert_that(
            list(common.PATH_PYTHON.pip.install(r="requirements.txt")),
            equal_to("python -m pip install -r requirements.txt".split()),
        )

    def test_just_python(self):
        assert_that(list(common.PATH_PYTHON), equal_to(["python"]))

    def test_python_file(self):
        assert_that(
            list(common.PATH_PYTHON("script.py")), equal_to(["python", "script.py"])
        )

    def test_python_getattr(self):
        assert_that(
            list(common.PATH_PYTHON.some_script), equal_to(["python", "some-script"])
        )

    def test_env_python(self):
        cmd = "/home/me/venvs/my-env/bin/python -m pip install -r requirements.txt"
        assert_that(
            list(
                common.env_python("/home/me/venvs/my-env").pip.install(
                    r="requirements.txt"
                )
            ),
            cmd.split(),
        )
