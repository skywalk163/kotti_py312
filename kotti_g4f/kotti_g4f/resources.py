# -*- coding: utf-8 -*-
"""
Resources for kotti_g4f - GPT4Free integration for Kotti CMS
"""

from kotti.resources import Content
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import Text
from zope.interface import implementer

from kotti_g4f import _
from kotti_g4f.interfaces import IG4FChat


@implementer(IG4FChat)
class G4FChat(Content):
    """G4FChat is a content type that provides an AI chat interface.

    Users can add this content type to their site to create
    AI-powered chat pages using GPT4Free.
    """

    #: Primary key column in the DB
    id = Column(Integer(), ForeignKey("contents.id"), primary_key=True)

    #: System prompt for the AI assistant
    system_prompt = Column(Text())

    #: Welcome message shown to users
    welcome_message = Column(Unicode(500))

    #: Model to use (e.g., "gpt-4", "gpt-3.5-turbo")
    model = Column(Unicode(100))

    type_info = Content.type_info.copy(
        name="G4FChat",
        title=_("G4F Chat"),
        add_view="add_g4f_chat",
        addable_to=["Document"],
        selectable_default_views=[],
        edit_links=[],
    )

    def __init__(self, system_prompt=None, welcome_message=None, model=None, **kwargs):
        """Constructor

        :param system_prompt: System prompt for the AI assistant
        :type system_prompt: str

        :param welcome_message: Welcome message shown to users
        :type welcome_message: unicode

        :param model: Model to use (e.g., "gpt-4")
        :type model: unicode

        :param **kwargs: Arguments passed to base class
        :type **kwargs: see :class:`kotti.resources.Content`
        """
        super(G4FChat, self).__init__(**kwargs)
        self.system_prompt = system_prompt
        self.welcome_message = welcome_message
        self.model = model
