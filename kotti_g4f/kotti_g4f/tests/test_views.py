"""
Tests for kotti_g4f plugin.
"""


class TestKottiConfigure:
    """Test the kotti_configure function."""

    def test_kotti_configure_adds_defaults(self):
        """Test that kotti_configure adds default settings."""
        from kotti_g4f import kotti_configure
        from kotti_g4f import DEFAULT_SETTINGS

        settings = {"pyramid.includes": "", "kotti.alembic_dirs": "", "kotti.available_types": ""}
        kotti_configure(settings)

        for key, value in DEFAULT_SETTINGS.items():
            assert settings[key] == value

    def test_kotti_configure_preserves_existing(self):
        """Test that existing settings are preserved."""
        from kotti_g4f import kotti_configure

        settings = {
            "pyramid.includes": "",
            "kotti.alembic_dirs": "",
            "kotti.available_types": "",
            "kotti.g4f.enabled": False,
            "kotti.g4f.model": "gpt-3.5-turbo",
        }
        kotti_configure(settings)

        assert settings["kotti.g4f.enabled"] is False
        assert settings["kotti.g4f.model"] == "gpt-3.5-turbo"

    def test_kotti_configure_adds_includes(self):
        """Test that pyramid.includes is updated."""
        from kotti_g4f import kotti_configure

        settings = {"pyramid.includes": "some.module", "kotti.alembic_dirs": "", "kotti.available_types": ""}
        kotti_configure(settings)

        assert "kotti_g4f" in settings["pyramid.includes"]

    def test_kotti_configure_adds_content_type(self):
        """Test that G4FChat content type is registered."""
        from kotti_g4f import kotti_configure

        settings = {"pyramid.includes": "", "kotti.alembic_dirs": "", "kotti.available_types": ""}
        kotti_configure(settings)

        assert "kotti_g4f.resources.G4FChat" in settings["kotti.available_types"]

    def test_kotti_configure_adds_alembic_dirs(self):
        """Test that alembic directories are added."""
        from kotti_g4f import kotti_configure

        settings = {"pyramid.includes": "", "kotti.alembic_dirs": "", "kotti.available_types": ""}
        kotti_configure(settings)

        assert "kotti_g4f:alembic" in settings["kotti.alembic_dirs"]


class TestGetG4FSettings:
    """Test the get_g4f_settings function."""

    def test_get_g4f_settings_returns_dict(self):
        """Test that get_g4f_settings returns a dictionary."""
        from kotti_g4f import get_g4f_settings

        # Create a mock request
        class MockRegistry:
            settings = {
                "kotti.g4f.enabled": True,
                "kotti.g4f.model": "gpt-4",
                "kotti.g4f.provider": None,
            }

        class MockRequest:
            registry = MockRegistry()

        result = get_g4f_settings(MockRequest())

        assert isinstance(result, dict)
        assert "enabled" in result
        assert "model" in result
        assert "provider" in result

    def test_get_g4f_settings_with_custom_values(self):
        """Test that custom settings are returned."""
        from kotti_g4f import get_g4f_settings

        class MockRegistry:
            settings = {
                "kotti.g4f.enabled": False,
                "kotti.g4f.model": "gpt-3.5-turbo",
                "kotti.g4f.provider": "custom",
            }

        class MockRequest:
            registry = MockRegistry()

        result = get_g4f_settings(MockRequest())

        assert result["enabled"] is False
        assert result["model"] == "gpt-3.5-turbo"
        assert result["provider"] == "custom"

    def test_get_g4f_settings_defaults(self):
        """Test that defaults are returned when settings are missing."""
        from kotti_g4f import get_g4f_settings

        class MockRegistry:
            settings = {}

        class MockRequest:
            registry = MockRegistry()

        result = get_g4f_settings(MockRequest())

        assert result["enabled"] is True
        assert result["model"] == "gpt-4"
        assert result["provider"] is None


class TestIsEnabled:
    """Test the is_enabled function."""

    def test_is_enabled_true_by_default(self):
        """Test that is_enabled returns True by default."""
        from kotti_g4f import is_enabled

        class MockRegistry:
            settings = {}

        class MockRequest:
            registry = MockRegistry()

        assert is_enabled(MockRequest()) is True

    def test_is_enabled_false_when_disabled(self):
        """Test that is_enabled returns False when disabled."""
        from kotti_g4f import is_enabled

        class MockRegistry:
            settings = {"kotti.g4f.enabled": False}

        class MockRequest:
            registry = MockRegistry()

        assert is_enabled(MockRequest()) is False


class TestIncludeme:
    """Test the includeme function."""

    def test_includeme_adds_routes(self):
        """Test that routes are added correctly."""
        from kotti_g4f import includeme

        class MockConfig:
            routes = []
            translations = []
            scans = []

            def add_route(self, name, pattern):
                self.routes.append((name, pattern))

            def add_translation_dirs(self, dirs):
                self.translations.append(dirs)

            def scan(self, name):
                self.scans.append(name)

        config = MockConfig()
        includeme(config)

        assert ("g4f_chat", "/@@g4f-chat") in config.routes
        assert ("g4f_api", "/@@g4f-api") in config.routes


class TestG4FChatResource:
    """Test the G4FChat content type."""

    def test_g4f_chat_creation(self):
        """Test that G4FChat can be created."""
        from kotti_g4f.resources import G4FChat

        chat = G4FChat(
            title="Test Chat",
            system_prompt="You are a helpful assistant.",
            welcome_message="Hello! How can I help you?",
            model="gpt-4",
        )

        assert chat.title == "Test Chat"
        assert chat.system_prompt == "You are a helpful assistant."
        assert chat.welcome_message == "Hello! How can I help you?"
        assert chat.model == "gpt-4"

    def test_g4f_chat_type_info(self):
        """Test that G4FChat has correct type_info."""
        from kotti_g4f.resources import G4FChat

        assert G4FChat.type_info.name == "G4FChat"
        assert G4FChat.type_info.add_view == "add_g4f_chat"
        assert "Document" in G4FChat.type_info.addable_to


class TestSecurityValidation:
    """Test security validation functions."""

    def test_validate_message_empty(self):
        """Test that empty message is rejected."""
        from kotti_g4f.views.view import validate_message

        is_valid, error = validate_message("")
        assert is_valid is False
        assert error is not None

    def test_validate_message_too_long(self):
        """Test that overly long message is rejected."""
        from kotti_g4f.views.view import validate_message, MAX_MESSAGE_LENGTH

        long_message = "a" * (MAX_MESSAGE_LENGTH + 1)
        is_valid, error = validate_message(long_message)
        assert is_valid is False
        assert "too long" in str(error).lower()

    def test_validate_message_valid(self):
        """Test that valid message is accepted."""
        from kotti_g4f.views.view import validate_message

        is_valid, error = validate_message("Hello, this is a test message.")
        assert is_valid is True
        assert error is None

    def test_validate_history_invalid_format(self):
        """Test that invalid history format is rejected."""
        from kotti_g4f.views.view import validate_history

        is_valid, error = validate_history("not a list")
        assert is_valid is False

    def test_validate_history_missing_fields(self):
        """Test that history items missing fields are rejected."""
        from kotti_g4f.views.view import validate_history

        is_valid, error = validate_history([{"role": "user"}])
        assert is_valid is False

    def test_validate_history_invalid_role(self):
        """Test that invalid role is rejected."""
        from kotti_g4f.views.view import validate_history

        is_valid, error = validate_history([{"role": "hacker", "content": "test"}])
        assert is_valid is False

    def test_validate_history_valid(self):
        """Test that valid history is accepted."""
        from kotti_g4f.views.view import validate_history

        history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
        is_valid, error = validate_history(history)
        assert is_valid is True

    def test_validate_model_allowed(self):
        """Test that allowed model is accepted."""
        from kotti_g4f.views.view import validate_model

        assert validate_model("gpt-4") == "gpt-4"
        assert validate_model("gpt-3.5-turbo") == "gpt-3.5-turbo"

    def test_validate_model_unknown_returns_default(self):
        """Test that unknown model returns default."""
        from kotti_g4f.views.view import validate_model

        assert validate_model("unknown-model") == "gpt-4"
        assert validate_model(None) == "gpt-4"

    def test_validate_model_malicious_rejected(self):
        """Test that malicious model name is rejected."""
        from kotti_g4f.views.view import validate_model

        # Malicious model names should return default
        assert validate_model("'; DROP TABLE users; --") == "gpt-4"
        assert validate_model("<script>alert('xss')</script>") == "gpt-4"
