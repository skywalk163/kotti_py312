"""
kotti_g4f - GPT4Free integration for Kotti CMS
"""
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory("kotti_g4f")

# Default settings
DEFAULT_SETTINGS = {
    "kotti.g4f.enabled": True,
    "kotti.g4f.model": "gpt-4",
    "kotti.g4f.provider": None,  # auto-select
}


def kotti_configure(settings):
    """Add this to your ``kotti.configurators`` setting to enable
    the kotti_g4f add-on.

    Example::

        kotti.configurators =
            kotti_g4f.kotti_configure

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """
    # Merge default settings with user settings
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value

    # Add pyramid includes - this will call includeme()
    settings["pyramid.includes"] += " kotti_g4f"


def includeme(config):
    """Pyramid includeme hook.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """
    # Add translation directories
    config.add_translation_dirs("kotti_g4f:locale")

    # Add routes
    config.add_route("g4f_chat", "/@@g4f-chat")
    config.add_route("g4f_api", "/@@g4f-api")

    # Scan for views
    config.scan(__name__)


def get_g4f_settings(request):
    """Get g4f settings from the request.

    :param request: Pyramid request object.
    :type request: :class:`pyramid.request.Request`
    :returns: Dictionary of g4f settings.
    :rtype: dict
    """
    settings = request.registry.settings
    return {
        "enabled": settings.get("kotti.g4f.enabled", True),
        "model": settings.get("kotti.g4f.model", "gpt-4"),
        "provider": settings.get("kotti.g4f.provider"),
    }


def is_enabled(request):
    """Check if g4f is enabled.

    :param request: Pyramid request object.
    :type request: :class:`pyramid.request.Request`
    :returns: True if g4f is enabled.
    :rtype: bool
    """
    return get_g4f_settings(request)["enabled"]
