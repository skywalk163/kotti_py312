# kotti-py312

Kotti CMS 及其插件，升级支持 Python 3.12。

## 项目结构

```
dumatework/
├── Kotti/              # Kotti CMS 核心
├── kotti_tinymce/      # TinyMCE 编辑器插件
├── kotti_image/        # 图片内容类型插件
└── .gitignore
```

## 环境要求

- **Python**: 3.8 - 3.12
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

# 安装 Kotti
cd Kotti
pip install -e ".[testing]"

# 安装插件
cd ../kotti_tinymce
pip install -e ".[testing]"

cd ../kotti_image
pip install -e ".[testing]"
```

## 运行

```bash
cd Kotti
pserve development.ini
```

访问 http://localhost:5000

## 升级到 Python 3.12 的主要变更

### 1. 移除的模块

Python 3.12 移除了以下模块，需要替换：

| 移除模块 | 替代方案 | 影响文件 |
|----------|----------|----------|
| `cgi.FieldStorage` | 自定义 `kotti.compat.FieldStorage` | `kotti/util.py`, `kotti/filedepot.py`, `kotti/resources.py`, `kotti/views/edit/upload.py` |
| `pkg_resources` | `importlib.metadata`, `importlib.resources` | `kotti/__init__.py`, `kotti/migrate.py`, `docs/conf.py` |

### 2. 依赖版本锁定

以下依赖需要锁定特定版本以确保兼容性：

| 依赖 | 版本 | 原因 |
|------|------|------|
| `deform` | `==2.0.14` | deform 2.0.15+ 更改了 `get_widget_requirements()` API，与 `js.deform` 不兼容 |
| `bleach` | `>=5.0.0,<6` | bleach 5.x 移除了 `styles` 参数 |
| `PasteDeploy` | `>=3.0` | 旧版本不兼容 Python 3.12 的 `ConfigParser` |
| `bcrypt` | `>=4.0.0` | 旧版本编译问题 |
| `venusian` | `>=3.1.1` | 修复 Python 3.12 的 `FileFinder` 兼容性 |

### 3. 代码修改

#### kotti/compat.py (新增)

新增兼容性模块，提供：
- `FieldStorage` - 替代 `cgi.FieldStorage`
- `get_distribution_version()` - 替代 `pkg_resources.require()[0].version`
- `get_resource_filename()` - 替代 `pkg_resources.resource_filename()`

#### kotti/sanitizers.py

移除 `styles` 参数，适配 bleach 5.x：

```python
# 旧代码
sanitized = clean(html, tags=[], attributes={}, styles=[], strip=True)

# 新代码
sanitized = clean(html, tags=[], attributes={}, strip=True)
```

### 4. 已知问题

#### pyramid_chameleon 兼容性警告

`pyramid_chameleon` 内部使用 `pkg_resources`，会触发弃用警告。这不影响功能，等待上游更新。

#### 测试通过率

| 项目 | 通过率 | 说明 |
|------|--------|------|
| Kotti | 98.7% (374/379) | 失败测试由 `pyramid_chameleon` 的 `pkg_resources` 兼容性问题导致 |
| kotti_tinymce | 100% (6/6) | 全部通过 |
| kotti_image | 100% (3/3) | 全部通过 |

## 开发指南

### 运行测试

```bash
# Kotti
cd Kotti
pytest kotti/tests/ -v

# kotti_tinymce
cd kotti_tinymce
pytest kotti_tinymce/tests/ -v

# kotti_image
cd kotti_image
pytest kotti_image/tests/ -v
```

### 添加新依赖

在 `setup.py` 的 `install_requires` 中添加，注意：
- 检查依赖是否支持 Python 3.12
- 如果是可选依赖，添加到 `extras_require`
- 更新 `requirements.txt`

## 参考链接

- [Python 3.12 有什么新功能](https://docs.python.org/zh-cn/3.12/whatsnew/3.12.html)
- [PEP 594 - 移除死电池](https://peps.python.org/pep-0594/)
- [Kotti 官方文档](http://kotti.readthedocs.io/)

## 版本历史

- **2.0.10.dev0** - 升级支持 Python 3.12
  - 替换 `cgi` 模块
  - 替换 `pkg_resources` 模块
  - 更新依赖版本
  - 修复 bleach 5.x 兼容性
