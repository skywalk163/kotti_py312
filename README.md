# Kotti2 - Python 3.12 CMS

[![SQLite Tests](https://github.com/skywalk163/kotti_py312/actions/workflows/sqlite.yml/badge.svg)](https://github.com/skywalk163/kotti_py312/actions/workflows/sqlite.yml)
[![PostgreSQL Tests](https://github.com/skywalk163/kotti_py312/actions/workflows/postgres.yml/badge.svg)](https://github.com/skywalk163/kotti_py312/actions/workflows/postgres.yml)
[![MySQL Tests](https://github.com/skywalk163/kotti_py312/actions/workflows/mysql.yml/badge.svg)](https://github.com/skywalk163/kotti_py312/actions/workflows/mysql.yml)
[![PyPI version](https://img.shields.io/pypi/v/Kotti2.svg)](https://pypi.org/project/Kotti2/)
[![Python Versions](https://img.shields.io/pypi/pyversions/Kotti2.svg)](https://pypi.org/project/Kotti2/)
[![License](https://img.shields.io/pypi/l/Kotti2.svg)](http://www.repoze.org/LICENSE.txt)

**Kotti2** 是 Kotti CMS 的分支版本，支持 Python 3.10-3.12。

Kotti 是一个基于 Pyramid 和 SQLAlchemy 的高级 Pythonic Web 应用框架，包含一个可扩展的内容管理系统（CMS）。

## 项目结构

```
kotti_py312/
├── Kotti/              # Kotti2 CMS 核心 (PyPI: Kotti2)
│   └── kotti/          # Python 模块: import kotti
├── kotti_image/        # 图片内容类型插件 (PyPI: kotti2_image)
│   └── kotti_image/    # Python 模块: import kotti_image
├── kotti_tinymce/      # TinyMCE 编辑器插件 (PyPI: kotti2_tinymce)
│   └── kotti_tinymce/  # Python 模块: import kotti_tinymce
├── kotti_g4f/          # GPT4Free AI 聊天插件 (PyPI: kotti2_g4f)
│   └── kotti_g4f/      # Python 模块: import kotti_g4f
└── .github/
    └── workflows/      # CI/CD 工作流
```

## 环境要求

| 依赖 | 版本要求 |
|------|---------|
| Python | 3.10 - 3.12 |
| SQLAlchemy | >= 1.4.36, < 2 |
| 数据库 | SQLite / PostgreSQL / MySQL |

## 特性

### Kotti CMS 主要功能

- **用户友好**: 编辑内容时所见即所得，界面直观
- **富文本编辑器**: 内置 TinyMCE 编辑器，支持 HTML 源代码编辑
- **响应式设计**: 基于 Bootstrap，适配桌面和移动端
- **模板系统**: 几乎无需编程即可自定义外观
- **插件系统**: 通过 INI 配置文件安装和配置插件
- **权限管理**: 高级用户和权限管理，适合大型组织
- **国际化**: 完全支持 Unicode 和多语言

### Kotti2 新增功能

- **EmbeddedPage 内容类型**: 支持通过 iframe 嵌入外部网页（如 AI 服务聚合页面）
- **AI 聊天集成**: kotti_g4f 插件提供 GPT4Free AI 聊天功能
- **Python 3.12 支持**: 完整兼容 Python 3.10-3.12
- **CodeMirror 集成**: TinyMCE 编辑器支持 HTML 源代码编辑

## 安装

### 从 PyPI 安装

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 安装 Kotti2
pip install Kotti2

# 安装插件
pip install kotti2_image kotti2_tinymce kotti2_g4f
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/skywalk163/kotti_py312.git
cd kotti_py312

# 安装 Kotti2
cd Kotti
pip install -e ".[testing]"

# 安装插件
cd ../kotti_image && pip install -e ".[testing]"
cd ../kotti_tinymce && pip install -e ".[testing]"
cd ../kotti_g4f && pip install -e ".[testing]"
```

## 配置

在 INI 配置文件中添加插件配置：

```ini
[app:main]
kotti.configurators =
    kotti_image.kotti_configure
    kotti_tinymce.kotti_configure
    kotti_g4f.kotti_configure
```

### 安全配置（推荐）

Kotti2 默认使用 Beaker 作为 session 后端，但 Beaker 存在已知安全漏洞 (CVE-2013-7489)。

**对于小型应用**（session 数据 < 4KB），建议使用安全的 cookie-based session：

```ini
kotti.session_factory = kotti.signed_cookie_session_factory
```

**对于大型应用**（session 数据 > 4KB），配置服务器端存储：

```ini
session.type = file
session.data_dir = /path/to/sessions/data
session.lock_dir = /path/to/sessions/lock
```

## 运行

```bash
# 创建初始配置
kotti-migrate upgrade development.ini

# 启动服务器
pserve development.ini
```

访问 http://localhost:5000

默认管理员账号: `admin` / `secret`

## 测试

### 测试通过率

| 项目 | PyPI 包名 | 测试通过率 |
|------|----------|-----------|
| Kotti2 | Kotti2 | 404/404 (100%) |
| kotti2_image | kotti2_image | 3/3 (100%) |
| kotti2_tinymce | kotti2_tinymce | 6/6 (100%) |
| kotti2_g4f | kotti2_g4f | 23/23 (100%) |

### 运行测试

```bash
# Kotti2 核心
cd Kotti
pytest kotti/tests/ -v --tb=short

# 使用 PostgreSQL
KOTTI_TEST_DB_STRING=postgresql://user:pass@localhost/dbname pytest

# 使用 MySQL
KOTTI_TEST_DB_STRING=mysql://user:pass@localhost/dbname pytest
```

## 主要变更 (相对于 Kotti 2.x)

### Python 3.12 兼容性

- 移除 `cgi.FieldStorage` → 使用自定义 `kotti.compat.FieldStorage`
- 更新类型注解语法
- 兼容 Python 3.10-3.12

### 新增内容类型

**EmbeddedPage** - iframe 嵌入页面：

```python
from kotti.resources import EmbeddedPage

page = EmbeddedPage(
    title="AI Dashboard",
    embed_url="https://example.com/dashboard",
    iframe_height=800,
    allow_fullscreen=True,
    sandbox_attrs="allow-scripts allow-same-origin",
)
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| embed_url | String | 要嵌入的 URL |
| iframe_height | Integer | iframe 高度（像素） |
| allow_fullscreen | Boolean | 是否允许全屏 |
| sandbox_attrs | String | iframe sandbox 属性 |
| fallback_content | Text | iframe 不支持时的回退内容 |

## CI/CD

本项目使用 GitHub Actions 进行持续集成：

| 工作流 | 说明 | 触发条件 |
|--------|------|---------|
| [SQLite](https://github.com/skywalk163/kotti_py312/actions/workflows/sqlite.yml) | SQLite 数据库测试 | push/PR 到 main |
| [PostgreSQL](https://github.com/skywalk163/kotti_py312/actions/workflows/postgres.yml) | PostgreSQL 数据库测试 | push/PR 到 main |
| [MySQL](https://github.com/skywalk163/kotti_py312/actions/workflows/mysql.yml) | MySQL 数据库测试 | push/PR 到 main |
| [Publish](https://github.com/skywalk163/kotti_py312/actions/workflows/publish.yml) | 发布到 PyPI | 创建 Release |

## 参考链接

- [Kotti 官方文档](https://kotti.readthedocs.io/)
- [PyPI - Kotti2](https://pypi.org/project/Kotti2/)

## 版本历史

- **3.0.2** - 2026-04-27
  - 修复 CodeMirror HTML 源代码编辑器
  - 添加数据库迁移脚本
  - 更新文档

- **3.0.1** - 2026-04-25
  - 新增 EmbeddedPage 内容类型（iframe 嵌入支持）
  - 新增单元测试（404 个测试用例）
  - 添加 CI/CD 工作流（SQLite/PostgreSQL/MySQL）

- **3.0.0** - 2026-04-23
  - PyPI 包名改为 Kotti2、kotti2_image、kotti2_tinymce、kotti2_g4f
  - 升级支持 Python 3.10-3.12
  - 新增 kotti2_g4f AI 聊天插件

## License

Kotti2 采用 BSD-derived [Repoze Public License](http://repoze.org/license.html) 开源协议。
