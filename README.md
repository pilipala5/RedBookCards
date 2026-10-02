# RedBookCards

<div align="center">
  <img src="resources/icons/icon_256x256.png" alt="RedBookCards Logo" width="128" height="128">
</div>

将 Markdown 文本转换为小红书风格的竖版卡片。支持自动分页、实时预览、12 种主题与批量图片导出，适合制作知识分享、读书笔记和教程。

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.5%2B-green)](https://doc.qt.io/qtforpython/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-lightgrey)](https://github.com/pilipala5/RedBookCards/releases/latest)

[下载桌面版](https://github.com/pilipala5/RedBookCards/releases/latest) · [快速开始](#快速开始) · [使用指南](#使用指南) · [开发与打包](#开发与打包) · [问题反馈](https://github.com/pilipala5/RedBookCards/issues)

## 效果展示

![RedBookCards 编辑与预览效果](resources/效果图.png)

## 核心功能

- **自动分页**：按内容高度拆分卡片，并关联标题与后续内容；也可通过 `<!-- pagebreak -->` 手动分页。
- **12 种主题**：小红书经典、Instagram 渐变、微信简约、抖音酷黑、知乎蓝、Notion 极简、优雅紫、海洋蓝、日落橙、森林绿、深色模式、午夜紫。
- **实时预览**：编辑后自动更新，支持适应窗口与实际大小两种预览模式。
- **Markdown 排版**：支持标题、列表、任务列表、表格、嵌套代码块，以及行内和块级 LaTeX 公式。
- **批量导出**：将所有分页导出为 PNG 或 JPEG，按 `card_01.png`、`card_02.png` 等名称保存。

| 卡片尺寸 | 分辨率 | 适用场景 |
| --- | --- | --- |
| Small | 720 × 960 px | 手机预览与轻量分享 |
| Medium | 1080 × 1440 px | 常规图文发布 |
| Large | 1440 × 1920 px | 高清图片导出 |

## 快速开始

### 下载桌面版（推荐）

无需安装 Python。前往 [最新 Release](https://github.com/pilipala5/RedBookCards/releases/latest)，根据系统选择安装包：

| 系统 | 下载文件 | 解压后运行 |
| --- | --- | --- |
| Windows x64 | `RedBookCards-Windows-x64.zip` | `RedBookCards.exe` |
| macOS Apple Silicon（M 系列芯片） | `RedBookCards-macOS-AppleSilicon.zip` | `RedBookCards.app` |
| macOS Intel | `RedBookCards-macOS-Intel.zip` | `RedBookCards.app` |

macOS 用户可在“关于本机”中确认芯片类型。当前 macOS 安装包尚未进行 Apple Developer ID 签名与公证；若首次打开被系统拦截，请在确认下载来源后，按“系统设置 → 隐私与安全性”中的提示允许打开。

### 从源码运行

需要 **Python 3.10 或更高版本**；建议使用与 CI 一致的 **Python 3.12**。

```bash
git clone https://github.com/pilipala5/RedBookCards.git
cd RedBookCards

python -m venv .venv
```

激活虚拟环境：

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

macOS / Linux 上若没有 `python` 命令，可用 `python3` 创建虚拟环境。激活后安装依赖并启动：

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

目前提供 Windows 和 macOS 桌面安装包；Linux 暂无官方安装包。

## 使用指南

### 制作一组卡片

1. 在左侧编辑器输入或粘贴 Markdown 文本。
2. 在右侧预览区检查排版与分页。
3. 通过工具栏选择主题和卡片尺寸。
4. 按需插入手动分页符，调整每张卡片的内容。
5. 点击“导出图片”，选择格式和保存目录。

### Markdown 语法

| 类型 | 支持内容 | 示例 |
| --- | --- | --- |
| 标题 | H1–H6 | `# 一级标题` |
| 文本样式 | 粗体、斜体、删除线 | `**粗体**`、`*斜体*`、`~~删除线~~` |
| 列表 | 有序与无序列表 | `- 项目`、`1. 项目` |
| 任务列表 | 待办与完成状态 | `- [ ] 待办`、`- [x] 完成` |
| 引用 | 多级引用 | `> 引用内容` |
| 代码 | 行内代码、代码块、列表内嵌套代码块 | `` `code` `` |
| 表格 | 列对齐 | `\| 列1 \| 列2 \|` |
| 链接与图片 | 文本链接、图片 | `[文本](url)`、`![图片](url)` |
| 分隔线 | 水平分隔线 | `---` |
| 数学公式 | 行内与块级 LaTeX，渲染为 MathML | `$E=mc^2$`、`$$E=mc^2$$` |
| Emoji | Unicode 表情 | 😊 🎉 ⭐ |

块级公式建议单独成段：

```markdown
行内公式：$E=mc^2$

$$
\frac{a}{b} = c
$$
```

### 手动分页

在希望开启下一张卡片的位置，单独插入一行 `<!-- pagebreak -->`：

```markdown
# 第一张卡片

这里是第一页的内容。

<!-- pagebreak -->

# 第二张卡片

这里从新的一页开始。
```

### 预览操作

- **适应窗口**：卡片随预览区缩放，滚轮可切换页面。
- **实际大小**：按导出像素尺寸显示，滚轮上下滚动，`Shift + 滚轮` 横向滚动。

## 开发与打包

### 主要模块

界面使用 PySide6，预览和导出使用 Qt WebEngine；Markdown 经解析与分页后，由 HTML/CSS 完成卡片排版。

| 模块 | 作用 |
| --- | --- |
| [`src/core/markdown_processor.py`](src/core/markdown_processor.py) | Markdown 解析、任务列表、代码高亮与公式转换 |
| [`src/utils/paginator.py`](src/utils/paginator.py) | 内容高度估算、自动分页与手动分页 |
| [`src/utils/style_manager.py`](src/utils/style_manager.py) | 主题配置与 CSS 生成 |
| [`src/core/html_generator.py`](src/core/html_generator.py) | 卡片 HTML、布局与装饰元素 |
| [`src/ui/preview_widget.py`](src/ui/preview_widget.py) | 预览模式与页面导航 |
| [`src/utils/exporter.py`](src/utils/exporter.py) | 图片渲染与批量导出 |

### 运行测试

安装依赖后，在项目根目录执行：

```bash
python -m unittest discover -s tests -v
```

现有回归测试覆盖列表内嵌套代码块、数学公式、代码块中的任务列表字面量、页面尺寸和分页高度。

### 本地打包

在目标系统上安装依赖后运行：

```bash
python build.py
```

- Windows 默认生成单文件程序：`dist/RedBookCards.exe`。
- macOS 默认生成应用包：`dist/RedBookCards.app`。
- 可使用 `--mode onefile` 或 `--mode onedir` 指定打包模式，使用 `--no-clean` 保留已有构建目录。

GitHub Actions 会运行测试，并分别构建 Windows x64、macOS Apple Silicon 和 macOS Intel 版本；推送 `v*` 标签后，会将 ZIP 安装包附加到 Release。

## 开发路线图

- [x] Windows / macOS 桌面构建
- [x] LaTeX 数学公式支持
- [ ] Linux 平台支持
- [ ] 自定义主题编辑器
- [ ] Markdown 模板库
- [ ] 云端同步
- [ ] 批量处理模式
- [ ] 插件系统
- [ ] AI 内容优化
- [ ] 移动端适配

## 参与贡献

欢迎通过 [Issues](https://github.com/pilipala5/RedBookCards/issues) 报告问题或提出建议。反馈时请附上系统版本、应用版本、复现步骤；排版问题可附一段最小 Markdown 示例。

提交代码时，请 Fork 仓库，在独立分支完成修改并运行测试，再发起 Pull Request。

## 致谢与联系

- [PySide6](https://doc.qt.io/qtforpython/) 提供桌面界面与 WebEngine。
- [Python-Markdown](https://python-markdown.github.io/) 与 [PyMdown Extensions](https://facelessuser.github.io/pymdown-extensions/) 提供 Markdown 扩展。
- [latex2mathml](https://github.com/roniemartinez/latex2mathml) 提供公式转换。
- 小红书提供设计灵感，Claude 提供 AI 开发辅助。
- 作者：[@pilipala5](https://github.com/pilipala5) · [yuhan.huang@whu.edu.cn](mailto:yuhan.huang@whu.edu.cn)

本项目采用 MIT 协议开源。

如果这个项目对你有帮助，欢迎点一个 Star。

[![Star History Chart](https://api.star-history.com/svg?repos=pilipala5/RedBookCards&type=Date)](https://star-history.com/#pilipala5/RedBookCards&Date)

Made with ❤️ by Yuhan Huang
