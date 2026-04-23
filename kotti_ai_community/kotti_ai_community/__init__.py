# -*- coding: utf-8 -*-
"""
AI Community Plugin for Kotti CMS.

An AI resource sharing platform based on Kotti CMS.
"""

from kotti_ai_community.resources import Idea
from kotti_ai_community.resources import ResourceItem


def kotti_configure(settings):
    """Configure the plugin."""
    # Add pyramid includes
    if "pyramid.includes" in settings:
        if "kotti_ai_community" not in settings["pyramid.includes"]:
            settings["pyramid.includes"] += " kotti_ai_community"
    else:
        settings["pyramid.includes"] = "kotti_ai_community"

    # Add to available types
    if "kotti.available_types" in settings:
        types = settings["kotti.available_types"].split()
        if "kotti_ai_community.resources.Idea" not in types:
            settings["kotti.available_types"] += (
                "\n    kotti_ai_community.resources.Idea"
                "\n    kotti_ai_community.resources.ResourceItem"
            )
    else:
        settings["kotti.available_types"] = (
            "kotti.resources.Document\n"
            "kotti.resources.File\n"
            "kotti_ai_community.resources.Idea\n"
            "kotti_ai_community.resources.ResourceItem"
        )


def includeme(config):
    """Pyramid includeme hook."""
    # Scan the entire kotti_ai_community package
    config.scan("kotti_ai_community")
