# -*- coding: utf-8 -*-
"""
资源库视图

包含:
- 资源列表视图
- 资源详情视图
- 资源创建/编辑视图
- 资源搜索视图
"""

from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti import DBSession
from kotti.resources import Document
from kotti.views.util import template_api

from kotti_ai_community.resources import ResourceItem
from kotti_ai_community.resources import RESOURCE_CATEGORIES
from kotti_ai_community.resources import ACCESS_TYPES


# ============================================================================
# 资源视图
# ============================================================================
@view_defaults(context=ResourceItem, permission="view")
class ResourceItemViews:
    """资源视图类"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(
        name="view", renderer="kotti_ai_community:templates/resource_view.pt"
    )
    def view(self):
        """资源详情视图"""
        # 增加浏览计数
        self.context.views_count += 1
        return {"api": template_api(self.context, self.request)}

    @view_config(
        name="edit", renderer="kotti_ai_community:templates/resource_edit.pt"
    )
    def edit(self):
        """资源编辑视图"""
        return {"api": template_api(self.context, self.request)}


# ============================================================================
# 资源列表视图
# ============================================================================
@view_config(
    name="resources",
    context=Document,
    renderer="kotti_ai_community:templates/resource_list.pt",
    permission="view",
)
def resource_list(context, request):
    """资源列表视图"""
    session = DBSession()

    # 获取查询参数
    category = request.params.get("category", "")
    access_type = request.params.get("access_type", "")
    search = request.params.get("search", "")

    # 构建查询
    query = session.query(ResourceItem)

    if category:
        query = query.filter(ResourceItem.category == category)
    if access_type:
        query = query.filter(ResourceItem.access_type == access_type)
    if search:
        query = query.filter(
            ResourceItem.title.contains(search)
            | ResourceItem.description.contains(search)
        )

    # 排序
    sort = request.params.get("sort", "created")
    if sort == "created":
        query = query.order_by(ResourceItem.creation_date.desc())
    elif sort == "likes":
        query = query.order_by(ResourceItem.likes_count.desc())
    elif sort == "views":
        query = query.order_by(ResourceItem.views_count.desc())
    elif sort == "references":
        query = query.order_by(ResourceItem.references_count.desc())

    resources = query.all()

    return {
        "api": template_api(context, request),
        "resources": resources,
        "categories": RESOURCE_CATEGORIES,
        "access_types": ACCESS_TYPES,
        "filters": {
            "category": category,
            "access_type": access_type,
            "search": search,
            "sort": sort,
        },
    }


@view_config(
    name="add_resource_item",
    context=Document,
    renderer="kotti_ai_community:templates/resource_add.pt",
    permission="edit",
)
def add_resource_item(context, request):
    """添加资源视图"""
    return {
        "api": template_api(context, request),
        "categories": RESOURCE_CATEGORIES,
        "access_types": ACCESS_TYPES,
    }
