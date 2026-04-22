# -*- coding: utf-8 -*-
"""
首页视图

包含:
- 首页视图
- 导航菜单
"""

from pyramid.view import view_config

from kotti import DBSession
from kotti.resources import Document
from kotti.views.util import template_api

from kotti_ai_community.resources import Idea
from kotti_ai_community.resources import ResourceItem


@view_config(
    name="home",
    context=Document,
    renderer="kotti_ai_community:templates/home.pt",
    permission="view",
)
def home(context, request):
    """首页视图"""
    session = DBSession()

    # 获取最新的点子
    latest_ideas = (
        session.query(Idea)
        .filter(Idea.status != "draft")
        .order_by(Idea.creation_date.desc())
        .limit(5)
        .all()
    )

    # 获取最新的资源
    latest_resources = (
        session.query(ResourceItem)
        .order_by(ResourceItem.creation_date.desc())
        .limit(5)
        .all()
    )

    # 获取热门点子
    hot_ideas = (
        session.query(Idea)
        .filter(Idea.status != "draft")
        .order_by(Idea.views_count.desc())
        .limit(5)
        .all()
    )

    # 统计数据
    total_ideas = session.query(Idea).count()
    total_resources = session.query(ResourceItem).count()

    return {
        "api": template_api(context, request),
        "latest_ideas": latest_ideas,
        "latest_resources": latest_resources,
        "hot_ideas": hot_ideas,
        "stats": {
            "total_ideas": total_ideas,
            "total_resources": total_resources,
        },
    }
