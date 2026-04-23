# -*- coding: utf-8 -*-
"""
AI Community content type definitions.

Contains:
- Idea: Idea content type
- ResourceItem: Resource content type
"""

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy.orm import relationship

from kotti import Base
from kotti.interfaces import IContent
from kotti.interfaces import IDocument
from kotti.resources import Content
from kotti.resources import File
from kotti.sqla import JsonType
from kotti.util import _
from zope.interface import implementer


# ============================================================================
# Idea status enum
# ============================================================================
IDEA_STATUS = {
    "draft": _("Draft"),
    "brainstorming": _("Brainstorming"),
    "recruiting": _("Recruiting"),
    "in_progress": _("In Progress"),
    "completed": _("Completed"),
    "archived": _("Archived"),
}

IDEA_CATEGORIES = {
    "tool": _("Tool/Application"),
    "research": _("Research/Experiment"),
    "startup": _("Startup/Business"),
    "learning": _("Learning/Education"),
    "creative": _("Creative/Art"),
    "other": _("Other"),
}

DIFFICULTY_LEVELS = {
    "beginner": _("Beginner"),
    "intermediate": _("Intermediate"),
    "advanced": _("Advanced"),
    "expert": _("Expert"),
}


# ============================================================================
# Resource type enum
# ============================================================================
RESOURCE_CATEGORIES = {
    "model": _("Model/Weights"),
    "dataset": _("Dataset"),
    "tool": _("Tool/Framework"),
    "api": _("API Service"),
    "compute": _("Compute Resources"),
    "funding": _("Funding"),
    "mentor": _("Mentor/Guidance"),
    "other": _("Other"),
}

ACCESS_TYPES = {
    "free": _("Free/Open"),
    "freemium": _("Freemium"),
    "paid": _("Paid"),
    "application": _("By Application"),
    "invite": _("By Invitation"),
}


# ============================================================================
# Idea - Idea content type
# ============================================================================
@implementer(IContent)
class Idea(Content):
    """Idea content type.

    Used for posting AI-related ideas, thoughts and project concepts.
    """

    __tablename__ = "ideas"
    __mapper_args__ = dict(polymorphic_identity="idea")

    #: Foreign key to Content id
    id = Column(Integer, ForeignKey("contents.id"), primary_key=True)

    #: Idea category
    category = Column(String(50), default="other")

    #: Difficulty level
    difficulty = Column(String(50), default="beginner")

    #: Status
    status = Column(String(50), default="draft")

    #: Tags (JSON array)
    tags = Column(JsonType, default=list)

    #: Detailed description
    description = Column(UnicodeText())

    #: Needed resources description
    needed_resources = Column(UnicodeText())

    #: Expected outcome
    expected_outcome = Column(UnicodeText())

    #: Estimated time (days)
    estimated_days = Column(Integer, default=0)

    #: Followers count
    followers_count = Column(Integer, default=0)

    #: Likes count
    likes_count = Column(Integer, default=0)

    #: Views count
    views_count = Column(Integer, default=0)

    #: AI-generated suggestions (optional)
    ai_suggestions = Column(UnicodeText())

    type_info = Content.type_info.copy(
        name="idea",
        title=_("Idea"),
        add_view="add_idea",
        addable_to=["Document"],
        edit_links=[],
    )

    def __init__(self, title=None, description=None, **kwargs):
        """Initialize the idea."""
        super(Idea, self).__init__(title=title, **kwargs)
        self.description = description
        self.tags = kwargs.get("tags", [])
        self.category = kwargs.get("category", "other")
        self.difficulty = kwargs.get("difficulty", "beginner")
        self.status = kwargs.get("status", "draft")
        self.needed_resources = kwargs.get("needed_resources", "")
        self.expected_outcome = kwargs.get("expected_outcome", "")
        self.estimated_days = kwargs.get("estimated_days", 0)

    def get_status_display(self):
        """Get display text for status."""
        return IDEA_STATUS.get(self.status, self.status)

    def get_category_display(self):
        """Get display text for category."""
        return IDEA_CATEGORIES.get(self.category, self.category)

    def get_difficulty_display(self):
        """Get display text for difficulty."""
        return DIFFICULTY_LEVELS.get(self.difficulty, self.difficulty)


# ============================================================================
# ResourceItem - Resource content type
# ============================================================================
@implementer(IContent)
class ResourceItem(Content):
    """Resource content type.

    Used for sharing AI-related resources like models, datasets, tools, etc.
    """

    __tablename__ = "resource_items"
    __mapper_args__ = dict(polymorphic_identity="resource_item")

    #: Foreign key to Content id
    id = Column(Integer, ForeignKey("contents.id"), primary_key=True)

    #: Resource category
    category = Column(String(50), default="other")

    #: Access type
    access_type = Column(String(50), default="free")

    #: Tags (JSON array)
    tags = Column(JsonType, default=list)

    #: Detailed description
    description = Column(UnicodeText())

    #: Resource URL
    url = Column(Unicode(500))

    #: Usage guide
    usage_guide = Column(UnicodeText())

    #: Limitations
    limitations = Column(UnicodeText())

    #: Availability status
    availability = Column(String(50), default="available")

    #: References count
    references_count = Column(Integer, default=0)

    #: Likes count
    likes_count = Column(Integer, default=0)

    #: Views count
    views_count = Column(Integer, default=0)

    type_info = Content.type_info.copy(
        name="resource_item",
        title=_("Resource"),
        add_view="add_resource_item",
        addable_to=["Document"],
        edit_links=[],
    )

    def __init__(self, title=None, description=None, **kwargs):
        """Initialize the resource."""
        super(ResourceItem, self).__init__(title=title, **kwargs)
        self.description = description
        self.tags = kwargs.get("tags", [])
        self.category = kwargs.get("category", "other")
        self.access_type = kwargs.get("access_type", "free")
        self.url = kwargs.get("url", "")
        self.usage_guide = kwargs.get("usage_guide", "")
        self.limitations = kwargs.get("limitations", "")

    def get_category_display(self):
        """Get display text for category."""
        return RESOURCE_CATEGORIES.get(self.category, self.category)

    def get_access_type_display(self):
        """Get display text for access type."""
        return ACCESS_TYPES.get(self.access_type, self.access_type)
