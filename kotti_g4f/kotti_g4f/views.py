"""
Views for kotti_g4f plugin.
"""
import json
import uuid
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound

from kotti_g4f import _
from kotti_g4f import get_g4f_settings
from kotti_g4f import is_enabled


class G4FChatView:
    """Chat view for g4f integration."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        route_name="g4f_chat",
        renderer="kotti_g4f:templates/chat.pt",
        permission="view",
    )
    def chat(self):
        """Render the chat interface."""
        if not is_enabled(self.request):
            raise HTTPNotFound()

        settings = get_g4f_settings(self.request)

        return {
            "title": _("AI Chat"),
            "model": settings["model"],
            "enabled": settings["enabled"],
        }


class G4FAPIView:
    """API endpoint for g4f chat."""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        route_name="g4f_api",
        request_method="POST",
        renderer="json",
        permission="view",
    )
    def chat_api(self):
        """Handle chat API requests."""
        if not is_enabled(self.request):
            raise HTTPNotFound()

        try:
            body = json.loads(self.request.body)
        except json.JSONDecodeError:
            raise HTTPBadRequest(json_body={"error": "Invalid JSON"})

        message = body.get("message", "").strip()
        if not message:
            raise HTTPBadRequest(json_body={"error": "Message is required"})

        conversation_id = body.get("conversation_id") or str(uuid.uuid4())

        # Get conversation history from session
        session = self.request.session
        conversations = session.get("g4f_conversations", {})
        history = conversations.get(conversation_id, [])

        # Add user message to history
        history.append({"role": "user", "content": message})

        # Get settings
        settings = get_g4f_settings(self.request)
        model = settings["model"]
        provider = settings["provider"]

        # Call g4f
        try:
            response_text = self._call_g4f(history, model, provider)
        except Exception as e:
            return {
                "error": str(e),
                "conversation_id": conversation_id,
            }

        # Add assistant response to history
        history.append({"role": "assistant", "content": response_text})

        # Save to session
        conversations[conversation_id] = history
        session["g4f_conversations"] = conversations

        return {
            "response": response_text,
            "conversation_id": conversation_id,
        }

    def _call_g4f(self, history, model, provider=None):
        """Call g4f to generate a response.

        :param history: List of message dicts with 'role' and 'content'.
        :param model: Model name to use.
        :param provider: Provider name (optional).
        :returns: Generated response text.
        """
        try:
            from g4f.client import Client
            from g4f.models import ModelUtils
        except ImportError:
            return "Error: g4f is not installed. Please install it with: pip install g4f"

        client = Client(provider=provider)

        # Convert history to g4f format
        messages = []
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"],
            })

        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

    @view_config(
        route_name="g4f_api",
        request_method="GET",
        renderer="json",
        permission="view",
    )
    def get_conversations(self):
        """Get conversation history."""
        if not is_enabled(self.request):
            raise HTTPNotFound()

        session = self.request.session
        conversations = session.get("g4f_conversations", {})

        # Return list of conversation IDs with preview
        result = []
        for conv_id, history in conversations.items():
            # Get first user message as preview
            preview = ""
            for msg in history:
                if msg["role"] == "user":
                    preview = msg["content"][:50]
                    if len(msg["content"]) > 50:
                        preview += "..."
                    break
            result.append({
                "id": conv_id,
                "preview": preview,
                "message_count": len(history),
            })

        return {"conversations": result}

    @view_config(
        route_name="g4f_api",
        request_method="DELETE",
        renderer="json",
        permission="view",
    )
    def clear_conversations(self):
        """Clear all conversations."""
        if not is_enabled(self.request):
            raise HTTPNotFound()

        session = self.request.session
        if "g4f_conversations" in session:
            del session["g4f_conversations"]

        return {"success": True}


def includeme(config):
    """Include the views in the configuration."""
    config.scan(__name__)
