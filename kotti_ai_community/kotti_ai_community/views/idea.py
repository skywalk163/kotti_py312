# -*- coding: utf-8 -*-
"""
点子广场视图

包含:
- 点子列表视图
- 点子详情视图
- 点子创建/编辑视图
- 点子搜索视图
"""

from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti import DBSession
from kotti.resources import Document
from kotti.views.util import template_api

from kotti_ai_community.resources import Idea
from kotti_ai_community.resources import IDEA_CATEGORIES
from kotti_ai_community.resources import IDEA_STATUS
from kotti_ai_community.resources import DIFFICULTY_LEVELS


# ============================================================================
# 点子视图
# ============================================================================
@view_defaults(context=Idea, permission="view")
class IdeaViews:
    """点子视图类"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(name="view", renderer="kotti_ai_community:templates/idea_view.pt")
    def view(self):
        """点子详情视图"""
        # 增加浏览计数
        self.context.views_count += 1
        return {"api": template_api(self.context, self.request)}

    @view_config(name="edit", renderer="kotti_ai_community:templates/idea_edit.pt")
    def edit(self):
        """点子编辑视图"""
        return {"api": template_api(self.context, self.request)}


# ============================================================================
# 点子列表视图
# ============================================================================
@view_config(
    name="ideas",
    context=Document,
    renderer="kotti_ai_community:templates/idea_list.pt",
    permission="view",
)
def idea_list(context, request):
    """点子列表视图"""
    session = DBSession()

    # 获取查询参数
    category = request.params.get("category", "")
    status = request.params.get("status", "")
    difficulty = request.params.get("difficulty", "")
    search = request.params.get("search", "")

    # 构建查询
    query = session.query(Idea)

    if category:
        query = query.filter(Idea.category == category)
    if status:
        query = query.filter(Idea.status == status)
    if difficulty:
        query = query.filter(Idea.difficulty == difficulty)
    if search:
        query = query.filter(
            Idea.title.contains(search) | Idea.description.contains(search)
        )

    # 排序
    sort = request.params.get("sort", "created")
    if sort == "created":
        query = query.order_by(Idea.creation_date.desc())
    elif sort == "likes":
        query = query.order_by(Idea.likes_count.desc())
    elif sort == "views":
        query = query.order_by(Idea.views_count.desc())

    ideas = query.all()

    return {
        "api": template_api(context, request),
        "ideas": ideas,
        "categories": IDEA_CATEGORIES,
        "statuses": IDEA_STATUS,
        "difficulties": DIFFICULTY_LEVELS,
        "filters": {
            "category": category,
            "status": status,
            "difficulty": difficulty,
            "search": search,
            "sort": sort,
        },
    }


@view_config(
    name="add_idea",
    context=Document,
    renderer="kotti_ai_community:templates/idea_add.pt",
    permission="edit",
)
def add_idea(context, request):
    """添加点子视图"""
    return {
        "api": template_api(context, request),
        "categories": IDEA_CATEGORIES,
        "statuses": IDEA_STATUS,
        "difficulties": DIFFICULTY_LEVELS,
    }
