kotti2_g4f
===========

.. image:: https://github.com/Kotti/kotti2_g4f/workflows/CI/badge.svg
    :target: https://github.com/Kotti/kotti2_g4f/actions
    :alt: CI Status

.. image:: https://img.shields.io/pypi/v/kotti2_g4f.svg
    :target: https://pypi.org/project/kotti2_g4f/
    :alt: PyPI Version

A Kotti2 plugin that integrates g4f (GPT4Free) AI chat functionality.

**Kotti2** is a fork of Kotti CMS with Python 3.12 and SQLAlchemy 2.0 support.

Features
--------

- **G4FChat Content Type**: Add AI chat pages anywhere in your Kotti2 site
- **Configurable System Prompts**: Customize AI behavior per chat instance
- **Model Selection**: Choose from multiple AI models (GPT-4, GPT-3.5, Claude, Gemini)
- **Security Built-in**: Input validation, model whitelist, XSS protection
- **Chat History**: Session-based conversation history

Installation
------------

Add to your ``pip requirements`` or ``setup.py`` dependencies::

    pip install kotti2_g4f

Then add ``kotti_g4f.kotti_configure`` to your ``kotti.configurators``
setting in your INI file::

    kotti.configurators =
        kotti_g4f.kotti_configure

Configuration
-------------

The plugin can be configured via INI settings:

``kotti.g4f.enabled``
    Enable or disable the g4f integration. Default: ``true``

``kotti.g4f.model``
    The default model to use. Default: ``gpt-4``

``kotti.g4f.provider``
    The provider to use (optional). Default: ``auto``

Usage
-----

Adding a G4FChat Content Type
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Log in to your Kotti2 site as admin
2. Navigate to any Document
3. Click "Add" in the menu
4. Select "G4F Chat"
5. Configure:
   - **Title**: Name of your chat page
   - **Description**: Brief description
   - **System Prompt**: Instructions for the AI (optional)
   - **Welcome Message**: Message shown to users (optional)
   - **Model**: AI model to use (e.g., gpt-4, gpt-3.5-turbo)

Direct Chat Access
~~~~~~~~~~~~~~~~~~

Navigate to ``/@@g4f-chat`` to access the global AI chat interface.

API Endpoint
------------

POST ``/@@g4f-api`` or ``/<g4f-chat-page>/api``

Send a chat message and receive AI response.

Request body (JSON)::

    {
        "message": "Your question here",
        "history": [
            {"role": "user", "content": "Previous question"},
            {"role": "assistant", "content": "Previous answer"}
        ]
    }

Response (JSON)::

    {
        "response": "AI response text"
    }

Security
--------

kotti2_g4f includes several security measures:

- **Input Validation**: Message length limits (10,000 chars), history limits (50 items)
- **Model Whitelist**: Only approved models can be used
- **XSS Protection**: All user input is escaped
- **Error Handling**: Generic error messages, detailed logging

Supported Models
----------------

- GPT-4, GPT-4o, GPT-4-turbo
- GPT-3.5-turbo
- Claude-3-opus, Claude-3-sonnet, Claude-3-haiku
- Gemini-pro, Gemini-1.5-pro

Development
-----------

Running Tests
~~~~~~~~~~~~~

::

    pip install -e ".[testing]"
    pytest

Code Quality
~~~~~~~~~~~~

::

    pip install black isort flake8
    black kotti_g4f
    isort kotti_g4f
    flake8 kotti_g4f

Docker
------

::

    docker-compose up

This starts:
- Kotti web server on port 5000
- PostgreSQL database on port 5432

License
-------

MIT License. See LICENSE.txt for details.

Links
-----

- **Documentation**: https://github.com/Kotti/kotti2_g4f#readme
- **Source Code**: https://github.com/Kotti/kotti2_g4f
- **Issue Tracker**: https://github.com/Kotti/kotti2_g4f/issues
- **Kotti2 CMS**: https://pypi.org/project/Kotti2/
- **g4f**: https://github.com/xtekky/gpt4free
