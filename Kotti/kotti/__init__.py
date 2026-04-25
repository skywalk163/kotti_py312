import os.path
import warnings

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import BeforeRender
from pyramid.session import SignedCookieSessionFactory
from pyramid.threadlocal import get_current_registry
from pyramid.util import DottedNameResolver
from sqlalchemy import MetaData
from sqlalchemy import engine_from_config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from zope.sqlalchemy import register

from kotti.compat import get_distribution_version
from kotti.sqla import Base as KottiBase

metadata = MetaData()
DBSession = scoped_session(sessionmaker(autoflush=True))
register(DBSession)
Base = declarative_base(cls=KottiBase)
Base.metadata = metadata
Base.query = DBSession.query_property()
TRUE_VALUES = ("1", "y", "yes", "t", "true")
FALSE_VALUES = ("0", "n", "no", "f", "false", "none")


def authtkt_factory(**settings):
    from kotti.security import list_groups_callback

    kwargs = dict(
        secret=settings["kotti.secret2"],
        hashalg="sha512",
        callback=list_groups_callback,
    )
    try:
        return AuthTktAuthenticationPolicy(**kwargs)
    except TypeError:
        # BBB with Pyramid < 1.4
        kwargs.pop("hashalg")
        return AuthTktAuthenticationPolicy(**kwargs)


def acl_factory(**settings):
    return ACLAuthorizationPolicy()


def signed_cookie_session_factory(**settings):
    """Create a signed cookie session factory using Pyramid's built-in.
    
    This is a secure alternative to pyramid_beaker which had security vulnerabilities
    (CVE-2013-7489 - pickle deserialization vulnerability).
    
    **IMPORTANT**: This session factory stores session data in the client cookie.
    Cookie size is limited to ~4KB. If you need to store large amounts of session
    data, consider using pyramid_beaker with server-side storage, but be aware
    of the security implications.
    
    Configuration options (can be set in INI file):
        kotti.session.secret - Secret key for signing (required, defaults to kotti.secret)
        kotti.session.cookie_name - Cookie name (default: 'kotti_session')
        kotti.session.timeout - Session timeout in seconds (default: 3600)
        kotti.session.reissue_time - Reissue cookie after N seconds (default: 120)
        kotti.session.max_age - Max cookie age (default: None)
        kotti.session.path - Cookie path (default: '/')
        kotti.session.domain - Cookie domain (default: None)
        kotti.session.secure - HTTPS only (default: False)
        kotti.session.httponly - HTTP only flag (default: True)
    """
    secret = settings.get('kotti.session.secret', settings.get('kotti.secret', 'changeme'))
    cookie_name = settings.get('kotti.session.cookie_name', 'kotti_session')
    timeout = int(settings.get('kotti.session.timeout', 3600))
    reissue_time = int(settings.get('kotti.session.reissue_time', 120))
    max_age = settings.get('kotti.session.max_age')
    if max_age:
        max_age = int(max_age)
    
    return SignedCookieSessionFactory(
        secret=secret,
        cookie_name=cookie_name,
        timeout=timeout,
        reissue_time=reissue_time,
        max_age=max_age,
        path=settings.get('kotti.session.path', '/'),
        domain=settings.get('kotti.session.domain'),
        secure=settings.get('kotti.session.secure', 'false').lower() in TRUE_VALUES,
        httponly=settings.get('kotti.session.httponly', 'true').lower() in TRUE_VALUES,
    )


def beaker_session_factory(**settings):
    """Create a Beaker session factory (requires pyramid_beaker).
    
    **SECURITY WARNING**: Beaker uses pickle for serialization which can lead to
    remote code execution vulnerabilities (CVE-2013-7489). Use with caution.
    
    Consider using 'kotti.signed_cookie_session_factory' instead for improved security,
    but note that cookie-based sessions have a ~4KB size limit.
    
    To use this factory, install pyramid_beaker:
        pip install pyramid_beaker
    
    Configuration options are passed through to Beaker. Common options:
        session.type - Storage type: 'file', 'memory', 'dbm', 'ext:memcached'
        session.data_dir - Directory for file-based storage
        session.lock_dir - Directory for lock files
        session.key - Cookie name
        session.secret - Secret key for signing
    """
    try:
        from pyramid_beaker import session_factory_from_settings
    except ImportError:
        raise ImportError(
            "pyramid_beaker is required for beaker_session_factory. "
            "Install it with: pip install pyramid_beaker\n"
            "Alternatively, use 'kotti.signed_cookie_session_factory' for a secure "
            "cookie-based session (note: ~4KB size limit)."
        )
    
    warnings.warn(
        "Beaker session factory uses pickle serialization which has known security "
        "vulnerabilities (CVE-2013-7489). Consider using 'kotti.signed_cookie_session_factory' "
        "instead. Note: cookie-based sessions have a ~4KB size limit.",
        UserWarning,
        stacklevel=2,
    )
    
    return session_factory_from_settings(settings)


def none_factory(**kwargs):  # pragma: no cover
    return None


# All of these can be set by passing them in the Paste Deploy settings:
conf_defaults = {
    "kotti.alembic_dirs": "kotti:alembic",
    "kotti.asset_overrides": "",
    "kotti.authn_policy_factory": "kotti.authtkt_factory",
    "kotti.authz_policy_factory": "kotti.acl_factory",
    "kotti.available_types": " ".join(
        ["kotti.resources.Document", "kotti.resources.File"]
    ),
    "kotti.base_includes": " ".join(
        [
            "kotti",
            "kotti.traversal",
            "kotti.filedepot",
            "kotti.events",
            "kotti.sanitizers",
            "kotti.views",
            "kotti.views.cache",
            "kotti.views.view",
            "kotti.views.edit",
            "kotti.views.edit.actions",
            "kotti.views.edit.content",
            "kotti.views.edit.default_views",
            "kotti.views.edit.upload",
            "kotti.views.file",
            "kotti.views.login",
            "kotti.views.navigation",
            "kotti.views.users",
        ]
    ),
    "kotti.caching_policy_chooser": (
        "kotti.views.cache.default_caching_policy_chooser"
    ),
    "kotti.configurators": "",
    "kotti.date_format": "medium",
    "kotti.datetime_format": "medium",
    "kotti.depot_mountpoint": "/depot",
    "kotti.depot_replace_wsgi_file_wrapper": False,
    "kotti.depot.0.backend": "kotti.filedepot.DBFileStorage",
    "kotti.depot.0.name": "dbfiles",
    "kotti.fanstatic.edit_needed": "kotti.fanstatic.edit_needed",
    "kotti.fanstatic.view_needed": "kotti.fanstatic.view_needed",
    "kotti.login_success_callback": "kotti.views.login.login_success_callback",
    "kotti.max_file_size": "10",
    "kotti.modification_date_excludes": " ".join(["kotti.resources.Node.position"]),
    "kotti.populators": "kotti.populate.populate",
    "kotti.principals_factory": "kotti.security.principals_factory",
    "kotti.register": "False",
    "kotti.register.group": "",
    "kotti.register.role": "",
    "kotti.request_factory": "kotti.request.Request",
    "kotti.reset_password_callback": "kotti.views.login.reset_password_callback",  # noqa
    "kotti.root_factory": "kotti.resources.default_get_root",
    "kotti.sanitizers": " ".join(
        [
            "xss_protection:kotti.sanitizers.xss_protection",
            "minimal_html:kotti.sanitizers.minimal_html",
            "no_html:kotti.sanitizers.no_html",
        ]
    ),
    "kotti.sanitize_on_write": " ".join(
        [
            "kotti.resources.Document.body:xss_protection",
            "kotti.resources.Content.title:no_html",
            "kotti.resources.Content.description:no_html",
        ]
    ),
    "kotti.search_content": "kotti.views.util.default_search_content",
    "kotti.session_factory": "kotti.beaker_session_factory",
    "kotti.static.edit_needed": "",  # BBB
    "kotti.static.view_needed": "",  # BBB
    "kotti.templates.api": "kotti.views.util.TemplateAPI",
    "kotti.time_format": "medium",
    "kotti.url_normalizer": "kotti.url_normalizer.url_normalizer",
    "kotti.url_normalizer.map_non_ascii_characters": True,
    "kotti.use_tables": "",
    "kotti.use_workflow": "kotti:workflow.zcml",
    "kotti.zcml_includes": " ".join([]),
    "pyramid.includes": "",
    "pyramid_deform.template_search_path": "kotti:templates/deform",
}

conf_dotted = {
    "kotti.authn_policy_factory",
    "kotti.authz_policy_factory",
    "kotti.available_types",
    "kotti.base_includes",
    "kotti.caching_policy_chooser",
    "kotti.configurators",
    "kotti.fanstatic.edit_needed",
    "kotti.fanstatic.view_needed",
    "kotti.login_success_callback",
    "kotti.modification_date_excludes",
    "kotti.populators",
    "kotti.principals_factory",
    "kotti.request_factory",
    "kotti.reset_password_callback",
    "kotti.root_factory",
    "kotti.search_content",
    "kotti.session_factory",
    "kotti.templates.api",
    "kotti.url_normalizer",
}


def get_version():
    version = get_distribution_version("Kotti")
    if version is None:
        # Fallback for development installs
        version = "2.0.10dev0"
    return version


def get_settings():
    return get_current_registry().settings


def _resolve_dotted(d, keys=conf_dotted):
    resolved = d.copy()

    for key in keys:
        value = resolved[key]
        if not isinstance(value, str):
            continue
        new_value = []
        for dottedname in value.split():
            new_value.append(DottedNameResolver().resolve(dottedname))
        resolved[key] = new_value

    return resolved


def main(global_config, **settings):
    # This function is a 'paste.app_factory' and returns a WSGI
    # application.

    from kotti.resources import initialize_sql

    config = base_configure(global_config, **settings)
    engine = engine_from_config(config.registry.settings)
    initialize_sql(engine)
    return config.make_wsgi_app()


def base_configure(global_config, **settings):
    # Resolve dotted names in settings, include plug-ins and create a
    # Configurator.

    from kotti.resources import get_root

    for key, value in conf_defaults.items():
        settings.setdefault(key, value)

    for key, value in settings.items():
        if key.startswith("kotti") and isinstance(value, bytes):
            settings[key] = value.decode("utf8")

    # Allow extending packages to change 'settings' w/ Python:
    k = "kotti.configurators"
    for func in _resolve_dotted(settings, keys=(k,))[k]:
        func(settings)

    settings = _resolve_dotted(settings)
    secret1 = settings["kotti.secret"]
    settings.setdefault("kotti.secret2", secret1)

    # We'll process ``pyramid_includes`` later by hand, to allow
    # overrides of configuration from ``kotti.base_includes``:
    pyramid_includes = settings.pop("pyramid.includes", "")

    config = Configurator(
        request_factory=settings["kotti.request_factory"][0], settings=settings
    )
    config.begin()

    config.hook_zca()
    config.include("pyramid_zcml")

    # Chameleon bindings were removed from Pyramid core since pyramid>=1.5a2
    config.include("pyramid_chameleon")

    config.registry.settings["pyramid.includes"] = pyramid_includes

    # Include modules listed in 'kotti.base_includes':
    for module in settings["kotti.base_includes"]:
        config.include(module)
    config.commit()

    # Modules in 'pyramid.includes' and 'kotti.zcml_includes' may
    # override 'kotti.base_includes':
    if pyramid_includes:
        for module in pyramid_includes.split():
            config.include(module)

    for name in settings["kotti.zcml_includes"].strip().split():
        config.load_zcml(name)

    config.commit()

    config._set_root_factory(get_root)

    return config


def includeme(config):
    """ Pyramid includeme hook.

    :param config: app config
    :type config: :class:`pyramid.config.Configurator`
    """

    import kotti.views.util

    settings = config.get_settings()

    authentication_policy = settings["kotti.authn_policy_factory"][0](**settings)
    authorization_policy = settings["kotti.authz_policy_factory"][0](**settings)
    session_factory = settings["kotti.session_factory"][0](**settings)
    if authentication_policy:
        config.set_authentication_policy(authentication_policy)
    if authorization_policy:
        config.set_authorization_policy(authorization_policy)
    config.set_session_factory(session_factory)

    config.add_subscriber(kotti.views.util.add_renderer_globals, BeforeRender)

    for override in [
        a.strip() for a in settings["kotti.asset_overrides"].split() if a.strip()
    ]:
        config.override_asset(to_override="kotti", override_with=override)

    config.add_translation_dirs(f"{os.path.dirname(__file__)}/locale")
    # used to be
    # config.add_translation_dirs("kotti:locale")
    # which fails with recent pytest (works in non testing though)

    workflow = settings["kotti.use_workflow"]
    if workflow.lower() not in FALSE_VALUES:
        config.load_zcml(workflow)

    return config
