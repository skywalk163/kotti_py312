import random

import colander
from colander import SchemaNode
from colander import null
from deform import FileData
from deform.widget import FileUploadWidget
from deform.widget import RichTextWidget
from deform.widget import TextAreaWidget
from deform.widget import TextInputWidget

from kotti.resources import Document
from kotti.resources import EmbeddedPage
from kotti.resources import File
from kotti.resources import Node
from kotti.util import _
from kotti.util import _to_fieldstorage
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.form import FileUploadTempStore
from kotti.views.form import ObjectType
from kotti.views.form import deferred_tag_it_widget
from kotti.views.form import get_appstruct
from kotti.views.form import validate_file_size_limit


class ContentSchema(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=_("Title"),
        validator=colander.Length(max=Node.title.property.columns[0].type.length),
    )
    description = colander.SchemaNode(
        colander.String(),
        title=_("Description"),
        widget=TextAreaWidget(cols=40, rows=5),
        missing="",
    )
    tags = colander.SchemaNode(
        ObjectType(), title=_("Tags"), widget=deferred_tag_it_widget, missing=[]
    )


class DocumentSchema(ContentSchema):
    body = colander.SchemaNode(
        colander.String(),
        title=_("Body"),
        widget=RichTextWidget(
            # theme='advanced', width=790, height=500
            height=500
        ),
        missing="",
    )


class DocumentAddForm(AddFormView):
    schema_factory = DocumentSchema
    add = Document
    item_type = _("Document")


class DocumentEditForm(EditFormView):
    schema_factory = DocumentSchema


# noinspection PyPep8Naming
def FileSchema(tmpstore, title_missing=None):
    class FileSchema(ContentSchema):
        file = SchemaNode(
            FileData(),
            title=_("File"),
            widget=FileUploadWidget(tmpstore),
            validator=validate_file_size_limit,
        )

    # noinspection PyUnusedLocal
    def set_title_missing(node, kw):
        if title_missing is not None:
            node["title"].missing = title_missing

    return FileSchema(after_bind=set_title_missing)


class FileAddForm(AddFormView):
    item_type = _("File")
    item_class = File  # specific to this class

    def schema_factory(self):
        tmpstore = FileUploadTempStore(self.request)
        return FileSchema(tmpstore, title_missing=null)

    def save_success(self, appstruct):
        if not appstruct["title"]:
            appstruct["title"] = appstruct["file"]["filename"]
        return super().save_success(appstruct)

    def add(self, **appstruct):
        filename = appstruct["file"]["filename"]
        item = self.item_class(
            title=appstruct["title"] or filename,
            description=appstruct["description"],
            tags=appstruct["tags"],
            data=_to_fieldstorage(**appstruct["file"]),
        )
        return item


class FileEditForm(EditFormView):
    def before(self, form):
        form.appstruct = get_appstruct(self.context, self.schema)
        if self.context.data is not None:
            form.appstruct.update(
                {
                    "file": {
                        "fp": None,
                        "filename": self.context.data["filename"],  # self.context.name
                        "mimetype": self.context.mimetype,
                        "uid": str(random.randint(1000000000, 9999999999)),
                    }
                }
            )

    def schema_factory(self):
        # File uploads are stored in the session so that you don't need
        # to upload your file again if validation of another schema node
        # fails.
        tmpstore = FileUploadTempStore(self.request)
        return FileSchema(tmpstore)

    def edit(self, **appstruct):
        title = appstruct["title"]
        self.context.title = title
        self.context.description = appstruct["description"]
        self.context.tags = appstruct["tags"]
        if appstruct["file"] and appstruct["file"]["fp"]:
            self.context.data = _to_fieldstorage(**appstruct["file"])


class EmbeddedPageSchema(ContentSchema):
    """Schema for EmbeddedPage content type."""

    embed_url = colander.SchemaNode(
        colander.String(),
        title=_("Embed URL"),
        description=_("URL of the external page to embed via iframe"),
        widget=TextInputWidget(),
        validator=colander.Length(max=2000),
    )

    iframe_height = colander.SchemaNode(
        colander.Integer(),
        title=_("Iframe Height (px)"),
        description=_("Height of the iframe in pixels. Use 0 for auto height."),
        default=600,
        missing=600,
    )

    allow_fullscreen = colander.SchemaNode(
        colander.Boolean(),
        title=_("Allow Fullscreen"),
        description=_("Allow the iframe to enter fullscreen mode"),
        default=True,
        missing=True,
    )

    sandbox_attrs = colander.SchemaNode(
        colander.String(),
        title=_("Sandbox Attributes"),
        description=_(
            "Space-separated sandbox attributes for iframe security. "
            "Default: allow-scripts allow-same-origin allow-popups allow-forms"
        ),
        default="allow-scripts allow-same-origin allow-popups allow-forms",
        missing="allow-scripts allow-same-origin allow-popups allow-forms",
        widget=TextInputWidget(),
    )

    css_class = colander.SchemaNode(
        colander.String(),
        title=_("CSS Class"),
        description=_("Additional CSS classes for the iframe container"),
        missing="",
    )

    fallback_content = colander.SchemaNode(
        colander.String(),
        title=_("Fallback Content"),
        description=_("Content to display when iframe is blocked or unavailable"),
        widget=TextAreaWidget(cols=40, rows=5),
        missing="",
    )


class EmbeddedPageAddForm(AddFormView):
    schema_factory = EmbeddedPageSchema
    add = EmbeddedPage
    item_type = _("Embedded Page")


class EmbeddedPageEditForm(EditFormView):
    schema_factory = EmbeddedPageSchema


def includeme(config):
    """ Pyramid includeme hook.

    :param config: app config
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_view(
        DocumentEditForm,
        context=Document,
        name="edit",
        permission="edit",
        renderer="kotti:templates/edit/node.pt",
    )

    config.add_view(
        DocumentAddForm,
        name=Document.type_info.add_view,
        permission=Document.type_info.add_permission,
        renderer="kotti:templates/edit/node.pt",
    )

    config.add_view(
        FileEditForm,
        context=File,
        name="edit",
        permission="edit",
        renderer="kotti:templates/edit/node.pt",
    )

    config.add_view(
        FileAddForm,
        name=File.type_info.add_view,
        permission=File.type_info.add_permission,
        renderer="kotti:templates/edit/node.pt",
    )

    config.add_view(
        EmbeddedPageEditForm,
        context=EmbeddedPage,
        name="edit",
        permission="edit",
        renderer="kotti:templates/edit/node.pt",
    )

    config.add_view(
        EmbeddedPageAddForm,
        name=EmbeddedPage.type_info.add_view,
        permission=EmbeddedPage.type_info.add_permission,
        renderer="kotti:templates/edit/node.pt",
    )
