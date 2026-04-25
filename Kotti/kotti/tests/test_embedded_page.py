"""Tests for EmbeddedPage content type."""

import pytest

from kotti.resources import EmbeddedPage
from kotti.testing import DummyRequest


class TestEmbeddedPageResource:
    """Tests for EmbeddedPage resource class."""

    def test_create_minimal(self, db_session, root):
        """Test creating an EmbeddedPage with minimal arguments."""
        page = EmbeddedPage(title="Test Page")
        root["test-page"] = page

        db_session.flush()
        db_session.expire_all()

        assert page.title == "Test Page"
        assert page.embed_url == ""
        assert page.fallback_content == ""
        assert page.iframe_height == 600
        assert page.allow_fullscreen is True
        assert page.sandbox_attrs == "allow-scripts allow-same-origin allow-popups allow-forms"
        assert page.css_class == ""

    def test_create_full(self, db_session, root):
        """Test creating an EmbeddedPage with all arguments."""
        page = EmbeddedPage(
            title="AI Dashboard",
            description="AI services aggregator",
            embed_url="https://example.com/dashboard",
            fallback_content="<p>iframe not supported</p>",
            iframe_height=800,
            allow_fullscreen=False,
            sandbox_attrs="allow-scripts allow-popups",
            css_class="ai-iframe-container",
        )
        root["ai-dashboard"] = page

        db_session.flush()
        db_session.expire_all()

        assert page.title == "AI Dashboard"
        assert page.description == "AI services aggregator"
        assert page.embed_url == "https://example.com/dashboard"
        assert page.fallback_content == "<p>iframe not supported</p>"
        assert page.iframe_height == 800
        assert page.allow_fullscreen is False
        assert page.sandbox_attrs == "allow-scripts allow-popups"
        assert page.css_class == "ai-iframe-container"

    def test_type_info(self):
        """Test type_info configuration."""
        assert EmbeddedPage.type_info.name == "EmbeddedPage"
        assert EmbeddedPage.type_info.title == "Embedded Page"
        assert EmbeddedPage.type_info.add_view == "add_embedded_page"
        assert "Document" in EmbeddedPage.type_info.addable_to
        assert "Folder" in EmbeddedPage.type_info.addable_to

    def test_get_sandbox_value_default(self):
        """Test get_sandbox_value with default sandbox_attrs."""
        page = EmbeddedPage(title="Test")
        assert page.get_sandbox_value() == "allow-scripts allow-same-origin allow-popups allow-forms"

    def test_get_sandbox_value_custom(self):
        """Test get_sandbox_value with custom sandbox_attrs."""
        page = EmbeddedPage(
            title="Test",
            sandbox_attrs="allow-scripts allow-popups"
        )
        assert page.get_sandbox_value() == "allow-scripts allow-popups"

    def test_get_sandbox_value_empty(self):
        """Test get_sandbox_value with empty sandbox_attrs."""
        page = EmbeddedPage(title="Test", sandbox_attrs="")
        # Empty string should still return default
        assert page.get_sandbox_value() == "allow-scripts allow-same-origin allow-popups allow-forms"

    def test_get_sandbox_value_none(self):
        """Test get_sandbox_value with None sandbox_attrs."""
        page = EmbeddedPage(title="Test")
        page.sandbox_attrs = None
        assert page.get_sandbox_value() == "allow-scripts allow-same-origin allow-popups allow-forms"


class TestEmbeddedPageIsUrlAllowed:
    """Tests for is_url_allowed method."""

    def test_no_whitelist_allows_all(self):
        """Test that no whitelist means all URLs are allowed."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://malicious-site.com"
        )
        assert page.is_url_allowed() is True
        assert page.is_url_allowed(None) is True

    def test_empty_whitelist_allows_all(self):
        """Test that empty whitelist means all URLs are allowed."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://example.com"
        )
        assert page.is_url_allowed([]) is True

    def test_exact_domain_match(self):
        """Test exact domain matching."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://example.com/page"
        )
        assert page.is_url_allowed(["example.com"]) is True
        assert page.is_url_allowed(["other.com"]) is False

    def test_subdomain_match(self):
        """Test subdomain matching."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://sub.example.com/page"
        )
        assert page.is_url_allowed(["example.com"]) is True
        assert page.is_url_allowed(["other.com"]) is False

    def test_www_prefix_handling(self):
        """Test that www. prefix is handled correctly."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://www.example.com/page"
        )
        assert page.is_url_allowed(["example.com"]) is True

    def test_domain_in_whitelist_with_www(self):
        """Test domain in whitelist with www. prefix."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://example.com/page"
        )
        # Whitelist has www., URL doesn't - should still match
        assert page.is_url_allowed(["www.example.com"]) is True

    def test_multiple_allowed_domains(self):
        """Test with multiple allowed domains."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://baidu.com/page"
        )
        assert page.is_url_allowed(["google.com", "baidu.com", "example.com"]) is True
        assert page.is_url_allowed(["google.com", "example.com"]) is False

    def test_case_insensitive_matching(self):
        """Test case-insensitive domain matching."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://Example.COM/page"
        )
        assert page.is_url_allowed(["example.com"]) is True
        assert page.is_url_allowed(["EXAMPLE.COM"]) is True

    def test_invalid_url(self):
        """Test with invalid URL."""
        page = EmbeddedPage(
            title="Test",
            embed_url="not-a-valid-url"
        )
        # Should return False for invalid URLs when whitelist is provided
        assert page.is_url_allowed(["example.com"]) is False

    def test_empty_url(self):
        """Test with empty URL."""
        page = EmbeddedPage(title="Test", embed_url="")
        assert page.is_url_allowed(["example.com"]) is False

    def test_port_in_url(self):
        """Test URL with port number."""
        page = EmbeddedPage(
            title="Test",
            embed_url="https://example.com:8080/page"
        )
        # Port is included in netloc, so this won't match
        assert page.is_url_allowed(["example.com"]) is False


class TestEmbeddedPageAddForm:
    """Tests for EmbeddedPageAddForm."""

    def test_schema_factory(self):
        """Test that schema factory returns correct schema."""
        from kotti.views.edit.content import EmbeddedPageAddForm, EmbeddedPageSchema

        form = EmbeddedPageAddForm(EmbeddedPage.__class__, DummyRequest())
        schema = form.schema_factory()
        assert isinstance(schema, EmbeddedPageSchema)

    def test_item_type(self):
        """Test that item_type is set correctly."""
        from kotti.views.edit.content import EmbeddedPageAddForm

        form = EmbeddedPageAddForm(EmbeddedPage.__class__, DummyRequest())
        assert form.item_type == "Embedded Page"


class TestEmbeddedPageEditForm:
    """Tests for EmbeddedPageEditForm."""

    def test_schema_factory(self):
        """Test that schema factory returns correct schema."""
        from kotti.views.edit.content import EmbeddedPageEditForm, EmbeddedPageSchema

        page = EmbeddedPage(
            title="Test Page",
            embed_url="https://example.com",
        )
        form = EmbeddedPageEditForm(page, DummyRequest())
        schema = form.schema_factory()
        assert isinstance(schema, EmbeddedPageSchema)


class TestEmbeddedPageViews:
    """Tests for EmbeddedPage views."""

    def test_view_embedded_page(self, dummy_request):
        """Test the view_embedded_page view."""
        from kotti.views.view import view_embedded_page

        page = EmbeddedPage(
            title="Test Page",
            embed_url="https://example.com",
        )
        result = view_embedded_page(page, dummy_request)
        assert result == {}


class TestEmbeddedPageIntegration:
    """Integration tests for EmbeddedPage."""

    def test_inherit_description_from_content(self, db_session, root):
        """Test that description is inherited from Content base class."""
        page = EmbeddedPage(
            title="Test",
            description="This is the description",
        )
        root["test"] = page

        db_session.flush()
        db_session.expire_all()

        assert page.description == "This is the description"

    def test_inherit_tags_from_content(self, db_session, root):
        """Test that tags are inherited from Content base class."""
        page = EmbeddedPage(
            title="Test",
        )
        page.tags = ["tag1", "tag2"]
        root["test"] = page

        db_session.flush()
        db_session.expire_all()

        assert page.tags == ["tag1", "tag2"]

    def test_persistence(self, db_session, root):
        """Test that EmbeddedPage is persisted correctly."""
        page = EmbeddedPage(
            title="Persistent Page",
            description="A test page",
            embed_url="https://example.com/embed",
            fallback_content="Fallback",
            iframe_height=900,
            allow_fullscreen=False,
            sandbox_attrs="allow-scripts",
            css_class="test-class",
        )
        root["persistent-page"] = page

        db_session.flush()
        db_session.expire_all()

        # Retrieve from database
        retrieved = root["persistent-page"]
        assert retrieved.title == "Persistent Page"
        assert retrieved.description == "A test page"
        assert retrieved.embed_url == "https://example.com/embed"
        assert retrieved.fallback_content == "Fallback"
        assert retrieved.iframe_height == 900
        assert retrieved.allow_fullscreen is False
        assert retrieved.sandbox_attrs == "allow-scripts"
        assert retrieved.css_class == "test-class"
