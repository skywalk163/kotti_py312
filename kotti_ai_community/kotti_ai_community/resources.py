# -*- coding: utf-8 -*-
"""
AI共创社区内容类型定义

包含:
- Idea: 点子内容类型
- ResourceItem: 资源内容类型
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
# 点子状态枚举
# ============================================================================
IDEA_STATUS = {
    "draft": _("草稿"),
    "brainstorming": _("构思中"),
    "recruiting": _("招募中"),
    "in_progress": _("进行中"),
    "completed": _("已完成"),
    "archived": _("已归档"),
}

IDEA_CATEGORIES = {
    "tool": _("工具/应用"),
    "research": _("研究/实验"),
    "startup": _("创业/商业"),
    "learning": _("学习/教育"),
    "creative": _("创意/艺术"),
    "other": _("其他"),
}

DIFFICULTY_LEVELS = {
    "beginner": _("入门级"),
    "intermediate": _("中级"),
    "advanced": _("高级"),
    "expert": _("专家级"),
}


# ============================================================================
# 资源类型枚举
# ============================================================================
RESOURCE_CATEGORIES = {
    "model": _("模型/权重"),
    "dataset": _("数据集"),
    "tool": _("工具/框架"),
    "api": _("API 服务"),
    "compute": _("算力资源"),
    "funding": _("资金支持"),
    "mentor": _("导师/指导"),
    "other": _("其他"),
}

ACCESS_TYPES = {
    "free": _("免费开放"),
    "freemium": _("部分免费"),
    "paid": _("付费"),
    "application": _("申请制"),
    "invite": _("邀请制"),
}


# ============================================================================
# Idea - 点子内容类型
# ============================================================================
@implementer(IContent)
class Idea(Content):
    """点子内容类型

    用于发布 AI 相关的点子、想法和项目构思
    """

    __tablename__ = "ideas"
    __mapper_args__ = dict(polymorphic_identity="idea")

    #: 关联到 Content 的 id
    id = Column(Integer, ForeignKey("contents.id"), primary_key=True)

    #: 点子分类
    category = Column(String(50), default="other")

    #: 难度等级
    difficulty = Column(String(50), default="beginner")

    #: 状态
    status = Column(String(50), default="draft")

    #: 标签 (JSON 数组)
    tags = Column(JsonType, default=list)

    #: 详细描述
    description = Column(UnicodeText())

    #: 需要的资源描述
    needed_resources = Column(UnicodeText())

    #: 预期成果
    expected_outcome = Column(UnicodeText())

    #: 预计时间 (天)
    estimated_days = Column(Integer, default=0)

    #: 关注者数量
    followers_count = Column(Integer, default=0)

    #: 点赞数
    likes_count = Column(Integer, default=0)

    #: 浏览数
    views_count = Column(Integer, default=0)

    #: AI 生成的建议 (可选)
    ai_suggestions = Column(UnicodeText())

    type_info = Content.type_info.copy(
        name="idea",
        title=_("点子"),
        add_view="add_idea",
        addable_to=["Document"],
        edit_links=[],
    )

    def __init__(self, title=None, description=None, **kwargs):
        """初始化点子"""
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
        """获取状态的显示文本"""
        return IDEA_STATUS.get(self.status, self.status)

    def get_category_display(self):
        """获取分类的显示文本"""
        return IDEA_CATEGORIES.get(self.category, self.category)

    def get_difficulty_display(self):
        """获取难度的显示文本"""
        return DIFFICULTY_LEVELS.get(self.difficulty, self.difficulty)


# ============================================================================
# ResourceItem - 资源内容类型
# ============================================================================
@implementer(IContent)
class ResourceItem(Content):
    """资源内容类型

    用于分享 AI 相关的资源，如模型、数据集、工具等
    """

    __tablename__ = "resource_items"
    __mapper_args__ = dict(polymorphic_identity="resource_item")

    #: 关联到 Content 的 id
    id = Column(Integer, ForeignKey("contents.id"), primary_key=True)

    #: 资源分类
    category = Column(String(50), default="other")

    #: 访问方式
    access_type = Column(String(50), default="free")

    #: 标签 (JSON 数组)
    tags = Column(JsonType, default=list)

    #: 详细描述
    description = Column(UnicodeText())

    #: 资源链接
    url = Column(Unicode(500))

    #: 使用说明
    usage_guide = Column(UnicodeText())

    #: 限制条件
    limitations = Column(UnicodeText())

    #: 可用性状态
    availability = Column(String(50), default="available")

    #: 被引用次数
    references_count = Column(Integer, default=0)

    #: 点赞数
    likes_count = Column(Integer, default=0)

    #: 浏览数
    views_count = Column(Integer, default=0)

    type_info = Content.type_info.copy(
        name="resource_item",
        title=_("资源"),
        add_view="add_resource_item",
        addable_to=["Document"],
        edit_links=[],
    )

    def __init__(self, title=None, description=None, **kwargs):
        """初始化资源"""
        super(ResourceItem, self).__init__(title=title, **kwargs)
        self.description = description
        self.tags = kwargs.get("tags", [])
        self.category = kwargs.get("category", "other")
        self.access_type = kwargs.get("access_type", "free")
        self.url = kwargs.get("url", "")
        self.usage_guide = kwargs.get("usage_guide", "")
        self.limitations = kwargs.get("limitations", "")

    def get_category_display(self):
        """获取分类的显示文本"""
        return RESOURCE_CATEGORIES.get(self.category, self.category)

    def get_access_type_display(self):
        """获取访问方式的显示文本"""
        return ACCESS_TYPES.get(self.access_type, self.access_type)
