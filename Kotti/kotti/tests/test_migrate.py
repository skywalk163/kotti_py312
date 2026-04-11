from alembic.migration import MigrationContext
from mock import patch
import os


def _path_endswith(path, suffix):
    """Check if path ends with suffix, handling both Unix and Windows path separators."""
    normalized = path.replace("\\", "/")
    return normalized.endswith(suffix)


class TestScriptDirectoryWithDefaultEnvPy:
    def make(self):
        from kotti.migrate import ScriptDirectoryWithDefaultEnvPy
        from kotti.migrate import KOTTI_SCRIPT_DIR

        return ScriptDirectoryWithDefaultEnvPy(KOTTI_SCRIPT_DIR)

    def test_env_py_location(self):
        scripts = self.make()
        assert _path_endswith(scripts.env_py_location, "kotti/alembic/env.py")

    def test_env_py_location_default(self):
        # We allow add-ons to use Kotti's version of 'env.py' if they
        # don't come with their own.
        scripts = self.make()
        with patch("kotti.migrate.os.path.exists") as exists:
            exists.return_value = False
            assert _path_endswith(scripts.env_py_location, "kotti/alembic/env.py")

    def test_run_env(self):
        with patch("kotti.migrate.load_python_file") as lpf:
            self.make().run_env()
            assert lpf.call_count == 1
            assert _path_endswith(lpf.call_args[0][0], "kotti/alembic")
            assert lpf.call_args[0][1] == "env.py"


class TestPackageEnvironment:
    def make(self):
        from kotti.migrate import PackageEnvironment
        from kotti.migrate import DEFAULT_LOCATION

        with patch(
            "kotti.migrate.get_settings",
            return_value={"sqlalchemy.url": "database_url"},
        ):
            return PackageEnvironment(DEFAULT_LOCATION)

    def test_pkg_name(self, db_session, events):
        assert self.make().pkg_name == "kotti"

    def test_version_table(self):
        assert self.make().version_table == "kotti_alembic_version"

    def test_run_env(self):
        pkg_env = self.make()
        called = []

        def func(rev, context):
            # assert rev is None  # XXX
            assert isinstance(context, MigrationContext)
            assert context.script == pkg_env.script_dir
            called.append((rev, context))
            return []

        pkg_env.run_env(func)
        assert called
