Changelog
=========

3.0.0 (2026-04-23)
------------------

- **Package renamed to kotti2_g4f** for PyPI
- **Major version upgrade**: Python 3.12 + SQLAlchemy 2.0 support
- **New G4FChat content type**: Add AI chat pages anywhere in Kotti2 site
- **Security improvements**:
  - Input validation (message length, history limits)
  - Model whitelist for allowed AI models
  - XSS protection in templates
  - Generic error messages (no sensitive info leakage)
- **Configurable per-instance**:
  - System prompt customization
  - Welcome message customization
  - Model selection per chat instance
- **CI/CD**: GitHub Actions, GitLab CI, Docker support
- **Full test coverage**: 23 tests passing

0.1.0 (2024-04-12)
------------------

- Initial release
- Basic g4f integration
- Chat view and API endpoint
- Configurable via INI settings
