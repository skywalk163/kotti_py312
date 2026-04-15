# -*- coding: utf-8 -*-
"""
View for G4FChat content type - displays the chat interface
"""

import json
import logging
from pyramid.view import view_config
from pyramid.response import Response

from kotti_g4f import _
from kotti_g4f.resources import G4FChat

logger = logging.getLogger(__name__)

# Security limits
MAX_MESSAGE_LENGTH = 10000  # Maximum message length in characters
MAX_HISTORY_LENGTH = 50     # Maximum number of history items
ALLOWED_MODELS = {          # Whitelist of allowed models
    "gpt-4", "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo",
    "claude-3-opus", "claude-3-sonnet", "claude-3-haiku",
    "gemini-pro", "gemini-1.5-pro",
}


def validate_message(message):
    """Validate user message.

    :param message: User message to validate
    :returns: Tuple of (is_valid, error_message)
    """
    if not message:
        return False, _("Message is required")
    if len(message) > MAX_MESSAGE_LENGTH:
        return False, _("Message is too long (max {} characters)").format(MAX_MESSAGE_LENGTH)
    return True, None


def validate_history(history):
    """Validate chat history.

    :param history: Chat history to validate
    :returns: Tuple of (is_valid, error_message)
    """
    if not isinstance(history, list):
        return False, _("Invalid history format")
    if len(history) > MAX_HISTORY_LENGTH:
        return False, _("Too many history items (max {})").format(MAX_HISTORY_LENGTH)
    for item in history:
        if not isinstance(item, dict):
            return False, _("Invalid history item format")
        if "role" not in item or "content" not in item:
            return False, _("History item missing required fields")
        if item["role"] not in ("user", "assistant", "system"):
            return False, _("Invalid role in history")
        if len(str(item.get("content", ""))) > MAX_MESSAGE_LENGTH:
            return False, _("History item too long")
    return True, None


def validate_model(model):
    """Validate model name.

    :param model: Model name to validate
    :returns: Valid model name or default
    """
    if model and model in ALLOWED_MODELS:
        return model
    return "gpt-4"  # Default model


@view_config(
    context=G4FChat,
    name="view",
    permission="view",
    renderer="kotti_g4f:templates/chat_content.pt",
)
def view_g4f_chat(context, request):
    """View for G4FChat content type - displays the chat interface."""
    return {
        "title": context.title,
        "description": context.description,
        "welcome_message": context.welcome_message or _("Welcome to AI Chat!"),
        "system_prompt": context.system_prompt or "",
        "model": validate_model(context.model),
    }


@view_config(
    context=G4FChat,
    name="api",
    permission="view",
    request_method="POST",
    renderer="json",
)
def g4f_chat_api(context, request):
    """API endpoint for G4FChat content type."""
    try:
        data = request.json_body
    except (json.JSONDecodeError, ValueError):
        logger.warning("Invalid JSON in request body")
        return {"error": _("Invalid request format")}

    message = data.get("message", "")
    if isinstance(message, str):
        message = message.strip()
    else:
        message = ""

    history = data.get("history", [])

    # Validate message
    is_valid, error = validate_message(message)
    if not is_valid:
        return {"error": error}

    # Validate history
    is_valid, error = validate_history(history)
    if not is_valid:
        return {"error": error}

    # Import g4f client
    try:
        from g4f.client import Client
    except ImportError:
        logger.error("g4f is not installed")
        return {"error": _("AI service is not available. Please contact the administrator.")}

    # Build messages list
    messages = []

    # Add system prompt if configured
    if context.system_prompt:
        messages.append({"role": "system", "content": context.system_prompt})

    # Add validated history
    messages.extend(history)

    # Add current message
    messages.append({"role": "user", "content": message})

    # Get validated model
    model = validate_model(context.model)

    try:
        client = Client()
        response = client.chat.completions.create(
            model=model,
            messages=messages,
        )
        reply = response.choices[0].message.content

        logger.info("G4F chat request completed for model: %s", model)
        return {"response": reply}

    except Exception as e:
        # Log the actual error for debugging, but return a generic message
        logger.exception("G4F API error: %s", str(e))
        return {"error": _("An error occurred while processing your request. Please try again later.")}
