"""
Tests for kotti_g4f plugin.
"""


class TestKottiConfigure:
    """Test the kotti_configure function."""

    def test_kotti_configure_adds_defaults(self):
        """Test that kotti_configure adds default settings."""
        from kotti_g4f import kotti_configure
        from kotti_g4f import DEFAULT_SETTINGS

        settings = {"pyramid.includes": ""}
        kotti_configure(settings)

        for key, value in DEFAULT_SETTINGS.items():
            assert settings[key] == value

    def test_kotti_configure_preserves_existing(self):
        """Test that existing settings are preserved."""
        from kotti_g4f import kotti_configure

        settings = {
            "pyramid.includes": "",
            "kotti.g4f.enabled": False,
            "kotti.g4f.model": "gpt-3.5-turbo",
        }
        kotti_configure(settings)

        assert settings["kotti.g4f.enabled"] is False
        assert settings["kotti.g4f.model"] == "gpt-3.5-turbo"

    def test_kotti_configure_adds_includes(self):
        """Test that pyramid.includes is updated."""
        from kotti_g4f import kotti_configure

        settings = {"pyramid.includes": "some.module"}
        kotti_configure(settings)

        assert "kotti_g4f" in settings["pyramid.includes"]


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

            def add_route(self, name, pattern):
                self.routes.append((name, pattern))

            def add_translation_dirs(self, dirs):
                self.translations.append(dirs)

            def scan(self, name):
                pass

        config = MockConfig()
        includeme(config)

        assert ("g4f_chat", "/@@g4f-chat") in config.routes
        assert ("g4f_api", "/@@g4f-api") in config.routes


class TestCallG4F:
    """Test the _call_g4f method."""

    def test_call_g4f_returns_string(self):
        """Test that _call_g4f returns a string."""
        from unittest.mock import patch, MagicMock
        from kotti_g4f.views import G4FAPIView

        # Mock the g4f client at the import location
        with patch('g4f.client.Client') as mock_client_class:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test response"
            mock_client.chat.completions.create.return_value = mock_response
            mock_client_class.return_value = mock_client

            view = G4FAPIView(None, None)
            result = view._call_g4f([], "gpt-4")

            assert isinstance(result, str)
            assert result == "Test response"

    def test_call_g4f_with_history(self):
        """Test that _call_g4f handles history."""
        from unittest.mock import patch, MagicMock
        from kotti_g4f.views import G4FAPIView

        with patch('g4f.client.Client') as mock_client_class:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "History response"
            mock_client.chat.completions.create.return_value = mock_response
            mock_client_class.return_value = mock_client

            view = G4FAPIView(None, None)
            history = [
                {"role": "user", "content": "Hello"},
                {"role": "assistant", "content": "Hi there!"},
                {"role": "user", "content": "How are you?"},
            ]
            result = view._call_g4f(history, "gpt-4")

            assert isinstance(result, str)
            assert result == "History response"

    def test_call_g4f_import_error(self):
        """Test that _call_g4f handles ImportError gracefully."""
        from unittest.mock import patch
        from kotti_g4f.views import G4FAPIView

        # Simulate ImportError when g4f module is not installed
        with patch.dict('sys.modules', {'g4f': None, 'g4f.client': None}):
            view = G4FAPIView(None, None)
            result = view._call_g4f([], "gpt-4")

            assert "Error: g4f is not installed" in result


class TestG4FChatView:
    """Test the chat view."""

    def test_chat_view_disabled_raises_404(self):
        """Test that chat view raises 404 when disabled."""
        from pyramid.httpexceptions import HTTPNotFound
        from kotti_g4f.views import G4FChatView

        class MockRegistry:
            settings = {"kotti.g4f.enabled": False}

        class MockRequest:
            registry = MockRegistry()

        view = G4FChatView(None, MockRequest())

        try:
            view.chat()
            assert False, "Should have raised HTTPNotFound"
        except HTTPNotFound:
            pass


class TestG4FAPIView:
    """Test the API view."""

    def test_chat_api_disabled_raises_404(self):
        """Test that API raises 404 when disabled."""
        from pyramid.httpexceptions import HTTPNotFound
        from kotti_g4f.views import G4FAPIView

        class MockRegistry:
            settings = {"kotti.g4f.enabled": False}

        class MockRequest:
            registry = MockRegistry()
            body = '{"message": "test"}'

        view = G4FAPIView(None, MockRequest())

        try:
            view.chat_api()
            assert False, "Should have raised HTTPNotFound"
        except HTTPNotFound:
            pass

    def test_chat_api_invalid_json(self):
        """Test that API handles invalid JSON."""
        from pyramid.httpexceptions import HTTPBadRequest
        from kotti_g4f.views import G4FAPIView

        class MockRegistry:
            settings = {"kotti.g4f.enabled": True}

        class MockRequest:
            registry = MockRegistry()
            body = "not valid json"

        view = G4FAPIView(None, MockRequest())

        try:
            view.chat_api()
            assert False, "Should have raised HTTPBadRequest"
        except HTTPBadRequest:
            pass

    def test_chat_api_missing_message(self):
        """Test that API handles missing message."""
        from pyramid.httpexceptions import HTTPBadRequest
        from kotti_g4f.views import G4FAPIView

        class MockRegistry:
            settings = {"kotti.g4f.enabled": True}

        class MockRequest:
            registry = MockRegistry()
            body = '{"other": "data"}'

        view = G4FAPIView(None, MockRequest())

        try:
            view.chat_api()
            assert False, "Should have raised HTTPBadRequest"
        except HTTPBadRequest:
            pass

    def test_chat_api_empty_message(self):
        """Test that API handles empty message."""
        from pyramid.httpexceptions import HTTPBadRequest
        from kotti_g4f.views import G4FAPIView

        class MockRegistry:
            settings = {"kotti.g4f.enabled": True}

        class MockRequest:
            registry = MockRegistry()
            body = '{"message": ""}'

        view = G4FAPIView(None, MockRequest())

        try:
            view.chat_api()
            assert False, "Should have raised HTTPBadRequest"
        except HTTPBadRequest:
            pass
