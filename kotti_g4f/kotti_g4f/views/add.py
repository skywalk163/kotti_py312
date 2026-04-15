# -*- coding: utf-8 -*-
"""
Add and edit views for G4FChat content type
"""

import colander
from deform.widget import TextAreaWidget

from kotti.resources import Node
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config

from kotti_g4f import _
from kotti_g4f.resources import G4FChat


class G4FChatSchema(colander.MappingSchema):
    """Schema for G4FChat content type."""

    title = colander.SchemaNode(
        colander.String(),
        title=_("Title"),
        validator=colander.Length(max=Node.title.property.columns[0].type.length),
    )

    description = colander.SchemaNode(
        colander.String(),
        title=_("Description"),
        widget=TextAreaWidget(cols=40, rows=3),
        missing="",
    )

    system_prompt = colander.SchemaNode(
        colander.String(),
        title=_("System Prompt"),
        description=_("System prompt for the AI assistant (optional)"),
        widget=TextAreaWidget(cols=40, rows=5),
        missing="",
    )

    welcome_message = colander.SchemaNode(
        colander.String(),
        title=_("Welcome Message"),
        description=_("Welcome message shown to users (optional)"),
        widget=TextAreaWidget(cols=40, rows=2),
        missing="",
    )

    model = colander.SchemaNode(
        colander.String(),
        title=_("Model"),
        description=_("AI model to use (e.g., gpt-4, gpt-3.5-turbo)"),
        missing="",
    )


@view_config(
    name="add_g4f_chat",
    permission="add",
    renderer="kotti:templates/edit/node.pt",
)
class G4FChatAddForm(AddFormView):
    """Add form for G4FChat content type."""

    schema_factory = G4FChatSchema
    add = G4FChat
    item_type = _("G4F Chat")


@view_config(
    name="edit",
    context=G4FChat,
    permission="edit",
    renderer="kotti:templates/edit/node.pt",
)
class G4FChatEditForm(EditFormView):
    """Edit form for G4FChat content type."""

    schema_factory = G4FChatSchema
