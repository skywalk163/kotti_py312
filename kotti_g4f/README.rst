kotti_g4f
================

A Kotti plugin that integrates g4f (GPT4Free) AI chat functionality.

Installation
------------

Add to your ``pip requirements`` or ``setup.py`` dependencies::

    kotti_g4f

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

After installation, navigate to ``/@@g4f-chat`` to access the AI chat interface.

The chat interface provides:
- Real-time AI chat using g4f
- Chat history storage in session
- Configurable model and provider

API Endpoint
------------

POST ``/@@g4f-api``

Send a chat message and receive AI response.

Request body (JSON)::

    {
        "message": "Your question here",
        "conversation_id": "optional-conversation-id"
    }

Response (JSON)::

    {
        "response": "AI response text",
        "conversation_id": "conversation-id"
    }
