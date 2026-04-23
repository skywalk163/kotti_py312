# -*- coding: utf-8 -*-
"""
AI Assistant Views.

Contains:
- AI Assistant chat interface
- Idea optimization API
- Tag suggestion API
"""

from pyramid.view import view_config
from pyramid.response import Response
from pyramid.view import view_defaults

from kotti.resources import Document
from kotti.views.util import template_api

import json


@view_config(
    name="ai-assistant",
    context=Document,
    renderer="kotti_ai_community:templates/ai_assistant.pt",
    permission="view",
)
def ai_assistant(context, request):
    """AI Assistant chat interface."""
    return {
        "api": template_api(context, request),
    }


@view_config(
    name="api/ai/optimize-idea",
    context=Document,
    renderer="json",
    permission="edit",
    request_method="POST",
)
def api_optimize_idea(context, request):
    """API: Optimize idea description (returns prompt for frontend)."""
    try:
        data = request.json_body
        idea_data = {
            "title": data.get("title", ""),
            "category": data.get("category", ""),
            "description": data.get("description", ""),
            "neededResources": data.get("needed_resources", ""),
            "expectedOutcome": data.get("expected_outcome", ""),
        }

        # Return prompt for frontend to call g4f
        prompt = (
            "Please help optimize the following AI idea description, "
            "making it clearer, more professional and attractive:\n\n"
            "Title: {title}\n"
            "Category: {category}\n"
            "Description: {description}\n"
            "Needed Resources: {needed}\n"
            "Expected Outcome: {expected}\n\n"
            "Please optimize from:\n"
            "1. Background and motivation\n"
            "2. Core innovation points\n"
            "3. Technical feasibility analysis\n"
            "4. Expected value and impact\n"
            "5. Implementation suggestions\n\n"
            "Please respond in Chinese with clear formatting."
        ).format(
            title=idea_data["title"],
            category=idea_data["category"],
            description=idea_data["description"],
            needed=idea_data["neededResources"] or "Not provided",
            expected=idea_data["expectedOutcome"] or "Not provided",
        )

        return {
            "success": True,
            "prompt": prompt,
            "system_prompt": (
                "You are an AI product expert and technical consultant, "
                "skilled at helping users improve and optimize AI project ideas."
            ),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@view_config(
    name="api/ai/suggest-tags",
    context=Document,
    renderer="json",
    permission="view",
    request_method="POST",
)
def api_suggest_tags(context, request):
    """API: Generate tag suggestions."""
    try:
        data = request.json_body
        content = data.get("content", "")
        content_type = data.get("type", "idea")

        type_label = "Idea" if content_type == "idea" else "Resource"
        prompt = (
            "Based on the following content, generate 5-10 appropriate tags:\n\n"
            "Type: {type}\n"
            "Content: {content}\n\n"
            "Requirements:\n"
            "1. Tags should accurately reflect the content topic\n"
            "2. Include technical domain tags (e.g., NLP, CV, LLM)\n"
            "3. Include application scenario tags\n"
            "4. Keep tags concise, 2-8 characters each\n"
            "5. Output only tags, separated by commas"
        ).format(type=type_label, content=content)

        return {
            "success": True,
            "prompt": prompt,
            "system_prompt": (
                "You are a tag classification expert, "
                "skilled at generating accurate classification tags for content."
            ),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


@view_config(
    name="api/ai/match",
    context=Document,
    renderer="json",
    permission="view",
    request_method="POST",
)
def api_match(context, request):
    """API: Match ideas with resources."""
    try:
        data = request.json_body
        idea = data.get("idea", {})
        resource = data.get("resource", {})

        prompt = (
            "Analyze the match between the following idea and resource:\n\n"
            "Idea:\n"
            "- Title: {idea_title}\n"
            "- Description: {idea_desc}\n"
            "- Needed Resources: {idea_res}\n\n"
            "Resource:\n"
            "- Title: {res_title}\n"
            "- Description: {res_desc}\n"
            "- Category: {res_cat}\n\n"
            "Please analyze:\n"
            "1. Match score (0-100)\n"
            "2. Match reasons\n"
            "3. Usage suggestions"
        ).format(
            idea_title=idea.get("title", ""),
            idea_desc=idea.get("description", ""),
            idea_res=idea.get("needed_resources", ""),
            res_title=resource.get("title", ""),
            res_desc=resource.get("description", ""),
            res_cat=resource.get("category", ""),
        )

        return {
            "success": True,
            "prompt": prompt,
            "system_prompt": (
                "You are a project matching expert, "
                "skilled at analyzing the fit between ideas and resources."
            ),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
