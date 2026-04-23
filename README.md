# Kotti2 - Python 3.12 + SQLAlchemy 2.0

Kotti2 是 Kotti CMS 的分支版本，支持 Python 3.12 和 SQLAlchemy 2.0。

## 项目结构

```
dumatework/
├── Kotti/              # Kotti2 CMS 核心 (PyPI: Kotti2)
│   └── kotti/          # Python 模块: import kotti
├── kotti_image/        # 图片内容类型插件 (PyPI: kotti2_image)
│   └── kotti_image/    # Python 模块: import kotti_image
├── kotti_tinymce/      # TinyMCE 编辑器插件 (PyPI: kotti2_tinymce)
│   └── kotti_tinymce/  # Python 模块: import kotti_tinymce
└── kotti_g4f/          # GPT4Free AI 聊天插件 (PyPI: kotti2_g4f)
    └── kotti_g4f/      # Python 模块: import kotti_g4f
```

## 环境要求

- **Python**: 3.8 - 3.12
- **SQLAlchemy**: 2.0.49
- **数据库**: SQLite / PostgreSQL / MySQL

## 安装

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
pip install kotti2_image
pip install kotti2_tinymce
pip install kotti2_g4f
```

## 配置

在 INI 配置文件中添加：

```ini
kotti.configurators =
    kotti_image.kotti_configure
    kotti_tinymce.kotti_configure
    kotti_g4f.kotti_configure
```

## 运行

```bash
pserve development.ini
```

访问 http://localhost:5000

## 测试通过率

| 项目 | PyPI 包名 | 版本 | 测试通过率 |
|------|----------|------|-----------|
| Kotti2 | Kotti2 | 3.0.0 | 379/379 (100%) |
| kotti2_image | kotti2_image | 3.0.0 | 3/3 (100%) |
| kotti2_tinymce | kotti2_tinymce | 3.0.0 | 6/6 (100%) |
| kotti2_g4f | kotti2_g4f | 3.0.0 | 23/23 (100%) |

## 主要变更 (相对于 Kotti 2.x)

### SQLAlchemy 2.0 兼容性

| 变更项 | 旧 API | 新 API |
|--------|--------|--------|
| 关系定义 | `relation()` | `relationship()` |
| 多态查询 | `query(Node).with_polymorphic(Node)` | `query(with_polymorphic(Node, '*'))` |
| 延迟加载 | `enable_eagerloads(False)` | `lazyload('*')` |
| 字段选择 | `load_only("path", "type")` | `load_only(Node.path, Node.type)` |
| 查询语法 | `select([col], where)` | `select(col).where(where)` |

### Python 3.12 兼容性

- 移除 `cgi.FieldStorage` → 使用自定义 `kotti.compat.FieldStorage`
- 移除 `pkg_resources` → 使用 `importlib.metadata`

## 开发指南

### 从源码安装

```bash
# Kotti2
cd Kotti
pip install -e ".[testing]"

# kotti2_image
cd kotti_image
pip install -e ".[testing]"

# kotti2_tinymce
cd kotti_tinymce
pip install -e ".[testing]"

# kotti2_g4f
cd kotti_g4f
pip install -e ".[testing]"
```

### 运行测试

```bash
# Kotti2
cd Kotti
pytest --tb=short -q

# kotti2_g4f
cd kotti_g4f
pytest -v
```

## 参考链接

- [Kotti 官方文档](http://kotti.readthedocs.io/)
- [SQLAlchemy 2.0 迁移指南](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [Python 3.12 有什么新功能](https://docs.python.org/zh-cn/3.12/whatsnew/3.12.html)

## 版本历史

- **3.0.0** - 2026-04-23
  - PyPI 包名改为 Kotti2、kotti2_image、kotti2_tinymce、kotti2_g4f
  - 升级支持 Python 3.12
  - 升级支持 SQLAlchemy 2.0.49
  - 新增 kotti2_g4f AI 聊天插件
