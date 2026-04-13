"""
Test fixtures for kotti_g4f.
"""
from pytest import fixture

# Import Kotti test fixtures
pytest_plugins = "kotti"


@fixture(scope="session")
def custom_settings():
    """Override to add kotti_g4f settings."""
    from kotti_g4f import DEFAULT_SETTINGS

    settings = DEFAULT_SETTINGS.copy()
    settings["kotti.g4f.enabled"] = True
    settings["kotti.g4f.model"] = "gpt-4"
    return settings
