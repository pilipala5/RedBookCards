### 用户:
项目背景
我正在开发一个 Windows 桌面应用「小红书 Markdown 编辑器」，核心目标是：
- 用户输入 Markdown 文本
- 自动渲染成小红书风格的精美卡片
- 智能分页（3:4 比例，1080×1440px）
- 批量导出高质量图片
 
# 技术栈
- 框架：PySide6 (Qt for Python)
- 渲染：QWebEngineView (基于 Chromium)
- Markdown解析：python-markdown + 扩展
- 样式：HTML + CSS (小红书风格)
- 分页：JavaScript (在 WebEngine 中执行)
 
# 核心架构设计
┌─────────────────────────────────────────┐
│           主窗口 (MainWindow)           │
├─────────────┬──────────────┬────────────┤
│  编辑器组件  │   预览组件    │  工具栏   │
│ (QTextEdit) │(QWebEngineView)│ (QToolBar)│
└─────────────┴──────────────┴────────────┘
↓
┌──────────────┐
│ Markdown解析  │
└──────────────┘
↓
┌──────────────┐
│  HTML生成    │
└──────────────┘
↓
┌──────────────┐
│  智能分页    │
└──────────────┘
↓
┌──────────────┐
│  样式渲染    │
└──────────────┘
↓
┌──────────────┐
│  图片导出    │
└──────────────┘
 
# 项目结构
xiaohongshu-editor/
├── main.py                     # 启动程序，创建 Qt 应用
├── requirements.txt            # 依赖包列表：PySide6、markdown 等
│
src/
├── ui/
│   ├── main_window.py         # 主窗口：左右分栏布局，导出按钮，300ms延迟更新
│   ├── editor_widget.py       # 左侧编辑器：QTextEdit，含示例文本
│   ├── preview_widget.py      # 右侧预览：QWebEngineView，集成分页和导出功能
│   
├── core/
│   ├── markdown_processor.py  # Markdown 转 HTML：使用 python-markdown 库
│   ├── html_generator.py      # 生成完整网页：支持页码、多主题CSS样式
│   
├── utils/
│   ├── paginator.py           # ✅ 智能分页器：HTML元素解析、高度估算、分页优化
│   ├── exporter.py            # ✅ 图片导出器：批量导出、进度追踪、水印添加
│   ├── style_manager.py       # ✅ 样式管理器：多主题支持（小红书/Instagram/微信/知乎/深色）
│   
├── resources/
│   ├── styles/                # �� 预留：未来可存放独立CSS文件
│   └── templates/             # �� 预留：未来可存放HTML模板文件# 核心功能需求
 
## 1. 智能分页算法
- 每页固定尺寸：1080×1440px (3:4比例)
- 分页原则：
  * 段落完整性：不在段落中间分页
  * 标题关联：标题与其后续内容保持同页
  * 列表连续：列表项尽量不分离
  * 代码完整：代码块不跨页
  * 视觉平衡：避免页面过空或过满
 
## 2. 样式系统
- 预设主题：小红书、Instagram、微信、知乎等
- 样式要素：
  * 字体：中文用苹方/微软雅黑，西文用 Helvetica
  * 颜色：主色 #FF2442，文字 #333333
  * 间距：段落间距 20px，行高 1.8
  * 特效：卡片阴影、圆角、渐变背景
 
## 3. 渲染流程
```python
# 伪代码示例
markdown_text → parse_markdown() → generate_html() → apply_styles() → paginate() → render_preview() → export_images()
4. 导出功能
 
格式：PNG/JPEG
质量：支持 1x/2x/3x 分辨率
命名：自动编号，如 card_01.png, card_02.png
批量：一次导出所有分页
 
代码规范
 
使用类型注解 (typing)
遵循 PEP 8
中文注释说明关键逻辑
错误处理要完善
 
性能要求
 
实时预览延迟 < 300ms
支持 10000 字的文档
导出速度：每张卡片 < 1秒
 
问题描述
结合聊天记录，检查我的代码是否有问题
期望输出
修改问题的代码；若修改小则直接告诉我位置，我个人进行修改；若变动大，则给我这个文件的完整代码。使用artifict工具生成代码
5-UI优化.md->->### 用户:
项目背景
我正在开发一个 Windows 桌面应用「小红书 Markdown 编辑器」，核心目标是：
- 用户输入 Markdown 文本
- 自动渲染成小红书风格的精美卡片
- 智能分页（3:4 比例，1080×1440px）
- 批量导出高质量图片
 
# 技术栈
- 框架：PySide6 (Qt for Python)
- 渲染：QWebEngineView (基于 Chromium)
- Markdown解析：python-markdown + 扩展
- 样式：HTML + CSS (小红书风格)
- 分页：JavaScript (在 WebEngine 中执行)
 
# 核心架构设计
┌─────────────────────────────────────────┐
│           主窗口 (MainWindow)           │
├─────────────┬──────────────┬────────────┤
│  编辑器组件  │   预览组件    │  工具栏   │
│ (QTextEdit) │(QWebEngineView)│ (QToolBar)│
└─────────────┴──────────────┴────────────┘
↓
┌──────────────┐
│ Markdown解析  │
└──────────────┘
↓
┌──────────────┐
│  HTML生成    │
└──────────────┘
↓
┌──────────────┐
│  智能分页    │
└──────────────┘
↓
┌──────────────┐
│  样式渲染    │
└──────────────┘
↓
┌──────────────┐
│  图片导出    │
└──────────────┘
 
# 项目结构
xiaohongshu-editor/
├── main.py                     # 启动程序，创建 Qt 应用
├── requirements.txt            # 依赖包列表：PySide6、markdown 等
│
src/
├── ui/
│   ├── main_window.py         # 主窗口：左右分栏布局，导出按钮，300ms延迟更新
│   ├── editor_widget.py       # 左侧编辑器：QTextEdit，含示例文本
│   ├── preview_widget.py      # 右侧预览：QWebEngineView，集成分页和导出功能
│   
├── core/
│   ├── markdown_processor.py  # Markdown 转 HTML：使用 python-markdown 库
│   ├── html_generator.py      # 生成完整网页：支持页码、多主题CSS样式
│   
├── utils/
│   ├── paginator.py           # ✅ 智能分页器：HTML元素解析、高度估算、分页优化
│   ├── exporter.py            # ✅ 图片导出器：批量导出、进度追踪、水印添加
│   ├── style_manager.py       # ✅ 样式管理器：多主题支持（小红书/Instagram/微信/知乎/深色）
│   
├── resources/
│   ├── styles/                # �� 预留：未来可存放独立CSS文件
│   └── templates/             # �� 预留：未来可存放HTML模板文件# 核心功能需求
 
## 1. 智能分页算法
- 每页固定尺寸：1080×1440px (3:4比例)
- 分页原则：
  * 段落完整性：不在段落中间分页
  * 标题关联：标题与其后续内容保持同页
  * 列表连续：列表项尽量不分离
  * 代码完整：代码块不跨页
  * 视觉平衡：避免页面过空或过满
 
## 2. 样式系统
- 预设主题：小红书、Instagram、微信、知乎等
- 样式要素：
  * 字体：中文用苹方/微软雅黑，西文用 Helvetica
  * 颜色：主色 #FF2442，文字 #333333
  * 间距：段落间距 20px，行高 1.8
  * 特效：卡片阴影、圆角、渐变背景
 
## 3. 渲染流程
```python
# 伪代码示例
markdown_text → parse_markdown() → generate_html() → apply_styles() → paginate() → render_preview() → export_images()
4. 导出功能
 
格式：PNG/JPEG
质量：支持 1x/2x/3x 分辨率
命名：自动编号，如 card_01.png, card_02.png
批量：一次导出所有分页
 
代码规范
 
使用类型注解 (typing)
遵循 PEP 8
中文注释说明关键逻辑
错误处理要完善
 
性能要求
 
实时预览延迟 < 300ms
支持 10000 字的文档
导出速度：每张卡片 < 1秒
 
问题描述
现在整个ui界面我觉得还是有点丑，你找个好点的风格美化一下
期望输出
修改问题的代码；若修改小则直接告诉我位置，我个人进行修改；若变动大，则给我这个文件的完整代码
editor_widget.py->text/plain-># ============================================
# src/ui/editor_widget.py
# ============================================
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLabel, QFrame, QHBoxLayout
from PySide6.QtGui import QFont, QTextOption, QPalette, QColor
from PySide6.QtCore import Signal, Qt

class EditorWidget(QWidget):
    textChanged = Signal()
    scrollChanged = Signal(float)  # 发送滚动百分比
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建容器框架
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: rgba(25, 25, 40, 0.95);
                border: 1px solid rgba(0, 224, 255, 0.2);
                border-radius: 16px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # 标题栏
        title_bar = QFrame()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 224, 255, 0.1),
                    stop: 0.5 rgba(0, 150, 255, 0.15),
                    stop: 1 rgba(0, 224, 255, 0.1)
                );
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                border-bottom: 1px solid rgba(0, 224, 255, 0.2);
            }
        """)
        
        # 使用水平布局而不是垂直布局，并设置正确的边距
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 20, 0)  # 左右留出空间
        title_layout.setAlignment(Qt.AlignVCenter)  # 垂直居中
        
        title = QLabel("✍️ Markdown 编辑器")
        title.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.5px;
                background: transparent;
            }
        """)
        title_layout.addWidget(title)
        title_layout.addStretch()  # 添加弹性空间
        
        # 编辑器
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Cascadia Code, Consolas, Monaco", 12))
        self.editor.setLineWrapMode(QTextEdit.WidgetWidth)
        self.editor.setWordWrapMode(QTextOption.WordWrap)
        
        # 设置编辑器样式
        self.editor.setStyleSheet("""
            QTextEdit {
                border: none;
                padding: 25px;
                background-color: rgba(15, 15, 25, 0.6);
                color: #e0e6ed;
                selection-background-color: rgba(0, 224, 255, 0.3);
                selection-color: #ffffff;
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
                font-size: 14px;
                line-height: 1.6;
            }
            QScrollBar:vertical {
                background: rgba(20, 20, 35, 0.5);
                width: 12px;
                border-radius: 6px;
                margin: 5px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.4),
                    stop: 1 rgba(0, 150, 255, 0.3)
                );
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.6),
                    stop: 1 rgba(0, 150, 255, 0.5)
                );
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0;
            }
            QScrollBar:horizontal {
                background: rgba(20, 20, 35, 0.5);
                height: 12px;
                border-radius: 6px;
                margin: 5px;
            }
            QScrollBar::handle:horizontal {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 224, 255, 0.4),
                    stop: 1 rgba(0, 150, 255, 0.3)
                );
                border-radius: 6px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 224, 255, 0.6),
                    stop: 1 rgba(0, 150, 255, 0.5)
                );
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0;
            }
        """)
        
        # 设置默认文本
        self.editor.setPlainText("""# 🌸 小红书笔记标题

## 今日分享

大家好呀～今天给大家分享一个超实用的 **Markdown 编辑器**！

### ✨ 主要功能

1. **实时预览** - 左边写，右边看
2. **智能分页** - 自动适配小红书卡片尺寸
3. **一键导出** - 批量生成精美图片

### 📝 使用方法

- 在左侧输入 Markdown 文本
- 右侧实时显示预览效果
- 点击导出按钮保存图片

> 💡 小贴士：支持所有常用的 Markdown 语法哦～

### 代码示例

```python
def hello():
    print("Hello, 小红书!")
    return "❤️"
```

### 表格示例

| 功能 | 描述 | 状态 |
|------|------|------|
| 编辑 | Markdown编辑器 | ✅ |
| 预览 | 实时渲染 | ✅ |
| 导出 | 图片生成 | ✅ |

---

喜欢的话记得 **点赞收藏** 哦～ ❤️

关注我，获取更多实用工具！""")
        
        # 连接信号
        self.editor.textChanged.connect(self.textChanged.emit)
        self.editor.verticalScrollBar().valueChanged.connect(self.on_scroll)
        
        # 组装布局
        container_layout.addWidget(title_bar)
        container_layout.addWidget(self.editor)
        
        layout.addWidget(container)
        
    def get_text(self):
        """获取编辑器文本"""
        return self.editor.toPlainText()
    
    def on_scroll(self):
        """处理滚动事件"""
        scrollbar = self.editor.verticalScrollBar()
        if scrollbar.maximum() > 0:
            percentage = scrollbar.value() / scrollbar.maximum()
            self.scrollChanged.emit(percentage) main_window.py->text/plain-># ============================================
# src/ui/main_window.py
# ============================================
from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QToolBar, QSplitter, QPushButton,
                               QFileDialog, QMessageBox, QStatusBar, QLabel,
                               QGraphicsDropShadowEffect, QComboBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QIcon, QColor
from src.ui.editor_widget import EditorWidget
from src.ui.preview_widget import PreviewWidget
from src.utils.style_manager import StyleManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 先创建自动更新计时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_preview)
        self.update_timer.setInterval(300)  # 300ms延迟
        
        # 初始化样式管理器
        self.style_manager = StyleManager()
        
        # 然后初始化UI
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("📝 小红书 Markdown 编辑器")
        self.setGeometry(100, 100, 1700, 950)
        
        # 设置窗口样式 - 深色科技风背景
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #0f0f1e,
                    stop: 0.5 #1a1a2e, 
                    stop: 1 #16213e
                );
            }
        """)
        
        # 创建工具栏
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFixedHeight(65)
        toolbar.setStyleSheet("""
            QToolBar {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(30, 30, 45, 0.95),
                    stop: 1 rgba(20, 20, 35, 0.98)
                );
                border: none;
                border-bottom: 2px solid rgba(0, 224, 255, 0.3);
                padding: 10px 15px;
                spacing: 12px;
            }
            QToolButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.15),
                    stop: 1 rgba(0, 150, 255, 0.1)
                );
                border: 1px solid rgba(0, 224, 255, 0.4);
                border-radius: 10px;
                padding: 10px 20px;
                color: #00e0ff;
                font-weight: 600;
                font-size: 14px;
                margin: 0 5px;
                letter-spacing: 0.5px;
                min-width: 120px;
            }
            QToolButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.25),
                    stop: 1 rgba(0, 150, 255, 0.2)
                );
                border: 1px solid rgba(0, 224, 255, 0.6);
                color: #00f0ff;
            }
            QToolButton:pressed {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.35),
                    stop: 1 rgba(0, 150, 255, 0.3)
                );
                border: 1px solid #00e0ff;
                color: white;
            }
        """)
        self.addToolBar(toolbar)
        
        # 添加工具栏按钮
        export_action = QAction("📸 导出图片", self)
        export_action.triggered.connect(self.export_images)
        toolbar.addAction(export_action)
        
        toolbar.addSeparator()
        
        clear_action = QAction("🗑️ 清空内容", self)
        clear_action.triggered.connect(self.clear_content)
        toolbar.addAction(clear_action)
        
        toolbar.addSeparator()
        
        # 主题选择器
        theme_label = QLabel("主题:")
        theme_label.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-size: 14px;
                padding: 0 10px;
                font-weight: 500;
            }
        """)
        toolbar.addWidget(theme_label)
        
        self.theme_selector = QComboBox()
        self.theme_selector.setFixedWidth(160)
        
        # 获取主题列表
        themes = self.style_manager.get_theme_display_names()
        for key, name in themes.items():
            self.theme_selector.addItem(name, key)
        
        self.theme_selector.setCurrentText("小红书经典")
        self.theme_selector.setStyleSheet("""
            QComboBox {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.15),
                    stop: 1 rgba(0, 150, 255, 0.1)
                );
                border: 1px solid rgba(0, 224, 255, 0.4);
                border-radius: 8px;
                padding: 8px 12px;
                color: #00e0ff;
                font-weight: 500;
                font-size: 13px;
            }
            QComboBox:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.25),
                    stop: 1 rgba(0, 150, 255, 0.2)
                );
                border: 1px solid rgba(0, 224, 255, 0.6);
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #00e0ff;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background: rgba(25, 25, 40, 0.98);
                border: 1px solid rgba(0, 224, 255, 0.4);
                color: #00e0ff;
                selection-background-color: rgba(0, 224, 255, 0.3);
                outline: none;
                padding: 5px;
                border-radius: 6px;
            }
            QComboBox QAbstractItemView::item {
                min-height: 32px;
                padding: 6px 10px;
                border-radius: 4px;
                margin: 2px 4px;
            }
            QComboBox QAbstractItemView::item:hover {
                background: rgba(0, 224, 255, 0.2);
            }
            QComboBox QAbstractItemView::item:selected {
                background: rgba(0, 224, 255, 0.3);
                color: white;
            }
        """)
        
        toolbar.addWidget(self.theme_selector)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.status_bar.setFixedHeight(35)
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background: rgba(20, 20, 35, 0.95);
                color: #8a92a6;
                border-top: 1px solid rgba(0, 224, 255, 0.2);
                padding: 6px 15px;
                font-size: 13px;
            }
            QStatusBar::item {
                border: none;
            }
        """)
        self.setStatusBar(self.status_bar)
        
        # 添加状态栏信息
        self.char_count_label = QLabel("字数: 0")
        self.char_count_label.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-weight: 500;
                padding: 4px 12px;
                background: rgba(0, 224, 255, 0.1);
                border: 1px solid rgba(0, 224, 255, 0.3);
                border-radius: 12px;
            }
        """)
        
        # 添加主题信息标签
        self.theme_info_label = QLabel("主题: 小红书经典")
        self.theme_info_label.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-weight: 500;
                padding: 4px 12px;
                background: rgba(0, 224, 255, 0.1);
                border: 1px solid rgba(0, 224, 255, 0.3);
                border-radius: 12px;
                margin-left: 10px;
            }
        """)
        
        self.status_bar.addPermanentWidget(self.theme_info_label)
        self.status_bar.addPermanentWidget(self.char_count_label)
        
        # 创建中心部件
        central_widget = QWidget()
        central_widget.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.2),
                    stop: 0.5 rgba(0, 224, 255, 0.4),
                    stop: 1 rgba(0, 224, 255, 0.2)
                );
                width: 3px;
                border-radius: 1px;
            }
            QSplitter::handle:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.3),
                    stop: 0.5 rgba(0, 224, 255, 0.6),
                    stop: 1 rgba(0, 224, 255, 0.3)
                );
            }
        """)
        
        # 创建编辑器和预览组件
        self.editor = EditorWidget()
        self.preview = PreviewWidget()
        
        # 添加阴影效果
        self.add_shadow_effect(self.editor)
        self.add_shadow_effect(self.preview)
        
        # 添加到分割器
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([850, 850])  # 设置初始宽度
        
        layout.addWidget(splitter)
        
        # 初始更新
        self.update_preview()
        self.update_char_count()
    
    def add_shadow_effect(self, widget):
        """为组件添加阴影效果"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 224, 255, 50))
        widget.setGraphicsEffect(shadow)
        
    def setup_connections(self):
        """设置信号连接"""
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.scrollChanged.connect(self.preview.handle_scroll)
        self.preview.pageChanged.connect(self.on_page_changed)
        
        # 连接主题选择信号
        self.theme_selector.currentIndexChanged.connect(self.on_theme_changed)
        
        # 连接尺寸改变信号（如果预览组件有的话）
        if hasattr(self.preview, 'sizeChanged'):
            self.preview.sizeChanged.connect(self.on_size_changed)
    
    def on_text_changed(self):
        """文本改变时启动计时器"""
        self.update_timer.stop()
        self.update_timer.start()
        self.update_char_count()
        
    def update_preview(self):
        """更新预览"""
        self.update_timer.stop()
        markdown_text = self.editor.get_text()
        self.preview.update_content(markdown_text)
        
    def update_char_count(self):
        """更新字数统计"""
        text = self.editor.get_text()
        char_count = len(text.replace(" ", "").replace("\n", ""))
        self.char_count_label.setText(f"字数: {char_count}")
        
    def on_page_changed(self, current, total):
        """页码改变时更新状态栏"""
        if total > 1:
            self.status_bar.showMessage(f"页面: {current}/{total}", 2000)
        else:
            self.status_bar.showMessage("", 1000)
    
    def on_theme_changed(self, index):
        """处理主题改变"""
        theme_key = self.theme_selector.currentData()
        if theme_key:
            # 通知预览组件更新主题
            self.preview.change_theme(theme_key)
            
            # 更新主题信息标签
            theme_name = self.theme_selector.currentText()
            self.theme_info_label.setText(f"主题: {theme_name}")
            
            # 显示状态提示
            self.status_bar.showMessage(f"已切换到主题: {theme_name}", 3000)
            
            # 可选：添加主题切换动画效果
            self.animate_theme_change()
    
    def on_size_changed(self, size):
        """处理尺寸改变"""
        size_display = {
            "small": "小尺寸 (720×960)",
            "medium": "中尺寸 (1080×1440)",
            "large": "大尺寸 (1440×1920)"
        }
        display_name = size_display.get(size, size)
        self.status_bar.showMessage(f"已切换到: {display_name}", 3000)
    
    def animate_theme_change(self):
        """主题切换动画效果"""
        # 创建一个简单的闪烁效果
        original_style = self.preview.styleSheet()
        
        # 添加高亮效果
        self.preview.setStyleSheet("""
            QWidget {
                border: 2px solid rgba(0, 224, 255, 0.8);
                border-radius: 16px;
            }
        """ + original_style)
        
        # 300ms后恢复
        QTimer.singleShot(300, lambda: self.preview.setStyleSheet(original_style))
        
    def clear_content(self):
        """清空内容"""
        reply = QMessageBox.question(
            self, "确认清空",
            "确定要清空所有内容吗？\n此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.editor.editor.clear()
            self.status_bar.showMessage("内容已清空", 2000)
            
    def export_images(self):
        """导出图片"""
        # 检查是否有内容
        if not self.editor.get_text().strip():
            QMessageBox.warning(
                self, "提示",
                "没有可导出的内容，请先输入一些文本。",
                QMessageBox.Ok
            )
            return
        
        # 选择导出文件夹
        folder = QFileDialog.getExistingDirectory(
            self, 
            "选择导出文件夹",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            try:
                # 获取当前主题和尺寸信息
                theme_name = self.theme_selector.currentText()
                
                # 显示导出信息
                self.status_bar.showMessage(f"正在导出图片 (主题: {theme_name})...", 0)
                
                # 执行导出
                self.preview.export_pages(folder)
                
                # 导出成功提示
                QMessageBox.information(
                    self, "导出成功",
                    f"图片已成功导出到:\n{folder}\n\n主题: {theme_name}",
                    QMessageBox.Ok
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self, "导出失败",
                    f"导出过程中出现错误:\n{str(e)}",
                    QMessageBox.Ok
                )
                self.status_bar.showMessage("导出失败", 3000)
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>小红书 Markdown 编辑器</h2>
        <p>版本: 2.0</p>
        <p>一款专为小红书内容创作者设计的 Markdown 编辑器</p>
        <br>
        <p><b>主要功能:</b></p>
        <ul>
            <li>实时预览 Markdown 内容</li>
            <li>智能分页（3:4 比例）</li>
            <li>多种主题样式</li>
            <li>三种页面尺寸</li>
            <li>批量导出高质量图片</li>
        </ul>
        <br>
        <p>© 2024 - 使用 PySide6 开发</p>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("关于")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        msg.setIcon(QMessageBox.Information)
        msg.exec()
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
        <h3>使用帮助</h3>
        
        <h4>基础操作</h4>
        <ul>
            <li><b>编辑:</b> 在左侧编辑器输入 Markdown 文本</li>
            <li><b>预览:</b> 右侧实时显示渲染效果</li>
            <li><b>翻页:</b> 使用上一页/下一页按钮浏览</li>
        </ul>
        
        <h4>主题切换</h4>
        <ul>
            <li>从工具栏的下拉菜单选择喜欢的主题</li>
            <li>支持12种预设主题风格</li>
            <li>主题会立即应用到预览</li>
        </ul>
        
        <h4>尺寸调整</h4>
        <ul>
            <li><b>小尺寸:</b> 720×960px (适合简短内容)</li>
            <li><b>中尺寸:</b> 1080×1440px (标准尺寸)</li>
            <li><b>大尺寸:</b> 1440×1920px (适合长文)</li>
        </ul>
        
        <h4>导出图片</h4>
        <ul>
            <li>点击"导出图片"按钮</li>
            <li>选择保存文件夹</li>
            <li>图片将按页码自动命名</li>
        </ul>
        
        <h4>快捷键</h4>
        <ul>
            <li><b>Ctrl+S:</b> 导出图片</li>
            <li><b>Ctrl+N:</b> 清空内容</li>
            <li><b>F11:</b> 全屏模式</li>
        </ul>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("使用帮助")
        msg.setTextFormat(Qt.RichText)
        msg.setText(help_text)
        msg.setIcon(QMessageBox.Question)
        msg.exec()
    
    def closeEvent(self, event):
        """关闭窗口事件"""
        # 检查是否有未保存的内容
        if self.editor.get_text().strip():
            reply = QMessageBox.question(
                self, "确认退出",
                "确定要退出吗？\n未导出的内容将会丢失。",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept() preview_widget.py->text/plain-># ============================================
# src/ui/preview_widget.py - 滚轮滚动修复版本
# ============================================
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                               QPushButton, QHBoxLayout, QProgressDialog,
                               QMessageBox, QComboBox, QButtonGroup, QRadioButton,
                               QScrollArea)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Signal, Qt, QSize, QEvent
from PySide6.QtGui import QWheelEvent
from pathlib import Path
from src.core.markdown_processor import MarkdownProcessor
from src.core.html_generator import HTMLGenerator
from src.utils.paginator import SmartPaginator
from src.utils.exporter import ImageExporter

class CustomScrollArea(QScrollArea):
    """自定义滚动区域，处理滚轮事件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.preview_widget = None  # 将在PreviewWidget中设置
        
    def wheelEvent(self, event: QWheelEvent):
        """重写滚轮事件"""
        if self.preview_widget:
            # 适应窗口模式：滚轮翻页
            if self.preview_widget.preview_mode == "fit":
                if event.angleDelta().y() > 0:
                    self.preview_widget.prev_page()
                else:
                    self.preview_widget.next_page()
                event.accept()
                return
            
            # 实际大小模式：检查是否按住Shift进行横向滚动
            elif self.preview_widget.preview_mode == "actual":
                # 如果按住Shift键，实现横向滚动
                if event.modifiers() == Qt.ShiftModifier:
                    # 获取滚动距离
                    delta = event.angleDelta().y()
                    # 横向滚动
                    h_scrollbar = self.horizontalScrollBar()
                    h_scrollbar.setValue(h_scrollbar.value() - delta)
                    event.accept()
                    return
                else:
                    # 正常的垂直滚动
                    super().wheelEvent(event)
                    return
        
        # 默认处理
        super().wheelEvent(event)

class PreviewWidget(QWidget):
    pageChanged = Signal(int, int)  # 当前页，总页数
    sizeChanged = Signal(str)  # 尺寸改变信号
    
    def __init__(self):
        super().__init__()
        self.current_pages = []  # 存储分页后的HTML内容
        self.current_page = 1
        self.total_pages = 1
        self.markdown_text = ""  # 保存原始markdown文本
        self.current_size = "medium"  # 当前页面尺寸
        self.preview_mode = "fit"  # 预览模式: fit(适应窗口) 或 actual(实际大小)
        
        # 初始化处理器
        self.markdown_processor = MarkdownProcessor()
        self.html_generator = HTMLGenerator(page_size="medium")
        self.paginator = SmartPaginator(page_size="medium")
        
        # 初始化UI
        self.init_ui()
        
        # 设置导出器
        self.setup_exporter()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建容器框架
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: rgba(25, 25, 40, 0.95);
                border: 1px solid rgba(0, 224, 255, 0.2);
                border-radius: 16px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # 创建标题栏
        title_bar = self.create_title_bar()
        
        # 创建WebView容器
        self.create_web_view_container()
        
        # 创建控制栏
        control_bar = self.create_control_bar()
        
        # 组装布局
        container_layout.addWidget(title_bar)
        container_layout.addWidget(self.web_container, 1)
        container_layout.addWidget(control_bar)
        
        layout.addWidget(container)
        
        # 连接信号
        self.connect_signals()
        
        # 初始化按钮状态
        self.update_buttons()
    
    def create_title_bar(self):
        """创建标题栏"""
        title_bar = QFrame()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 224, 255, 0.1),
                    stop: 0.5 rgba(0, 150, 255, 0.15),
                    stop: 1 rgba(0, 224, 255, 0.1)
                );
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
                border-bottom: 1px solid rgba(0, 224, 255, 0.2);
            }
        """)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 5, 20, 5)
        title_layout.setSpacing(15)
        
        # 标题
        title = QLabel("👀 实时预览")
        title.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.5px;
                background: transparent;
            }
        """)
        
        # 尺寸选择标签
        size_label = QLabel("尺寸:")
        size_label.setStyleSheet("""
            QLabel {
                color: #8a92a6;
                font-size: 12px;
                background: transparent;
            }
        """)
        
        # 尺寸选择下拉框
        self.size_selector = QComboBox()
        self.size_selector.addItems(["小尺寸 (720×960)", "中尺寸 (1080×1440)", "大尺寸 (1440×1920)"])
        self.size_selector.setCurrentIndex(1)
        self.size_selector.setFixedWidth(150)
        self.size_selector.setStyleSheet(self.get_combobox_style())
        
        # 预览模式选择
        mode_label = QLabel("模式:")
        mode_label.setStyleSheet("""
            QLabel {
                color: #8a92a6;
                font-size: 12px;
                background: transparent;
            }
        """)
        
        # 预览模式按钮组
        self.mode_group = QButtonGroup()
        
        self.fit_mode_btn = QRadioButton("适应窗口")
        self.fit_mode_btn.setChecked(True)
        self.fit_mode_btn.setStyleSheet(self.get_radio_style())
        
        self.actual_mode_btn = QRadioButton("实际大小")
        self.actual_mode_btn.setStyleSheet(self.get_radio_style())
        
        self.mode_group.addButton(self.fit_mode_btn, 0)
        self.mode_group.addButton(self.actual_mode_btn, 1)
        
        # 组装标题栏
        title_layout.addWidget(title)
        title_layout.addSpacing(20)
        title_layout.addWidget(size_label)
        title_layout.addWidget(self.size_selector)
        title_layout.addSpacing(15)
        title_layout.addWidget(mode_label)
        title_layout.addWidget(self.fit_mode_btn)
        title_layout.addWidget(self.actual_mode_btn)
        title_layout.addStretch()
        
        return title_bar
    
    def create_web_view_container(self):
        """创建WebView容器"""
        # 使用自定义滚动区域
        self.web_container = CustomScrollArea()
        self.web_container.preview_widget = self  # 设置引用
        
        self.web_container.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #1a1a2e;
            }
            QScrollBar:vertical {
                background: rgba(30, 30, 45, 0.5);
                width: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 224, 255, 0.3);
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 224, 255, 0.5);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar:horizontal {
                background: rgba(30, 30, 45, 0.5);
                height: 12px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(0, 224, 255, 0.3);
                border-radius: 6px;
                min-width: 30px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(0, 224, 255, 0.5);
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # 创建WebView
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("""
            QWebEngineView {
                border: none;
                background: #1a1a2e;
            }
        """)
        
        # 禁用WebView自身的滚动条和鼠标交互（在实际大小模式下）
        self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.web_view.setFocusPolicy(Qt.StrongFocus)
        
        # 设置滚动区域
        self.web_container.setWidget(self.web_view)
        self.web_container.setWidgetResizable(True)
        self.web_container.setAlignment(Qt.AlignCenter)
        
        # 默认设置为适应窗口模式
        self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    
    def create_control_bar(self):
        """创建控制栏"""
        control_bar = QFrame()
        control_bar.setFixedHeight(60)
        control_bar.setStyleSheet("""
            QFrame {
                background: rgba(20, 20, 35, 0.8);
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
                border-top: 1px solid rgba(0, 224, 255, 0.1);
            }
        """)
        
        control_layout = QHBoxLayout(control_bar)
        control_layout.setContentsMargins(20, 12, 20, 12)
        control_layout.setSpacing(15)
        
        # 创建中心控制区容器
        center_controls = QWidget()
        center_layout = QHBoxLayout(center_controls)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(15)
        
        # 上一页按钮
        self.prev_btn = QPushButton("⬅ 上一页")
        self.prev_btn.setFixedSize(100, 36)
        self.prev_btn.setStyleSheet(self.get_button_style())
        
        # 页面信息标签
        self.page_info_label = QLabel("")
        self.page_info_label.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-size: 14px;
                font-weight: 600;
                padding: 5px 15px;
                background: rgba(0, 224, 255, 0.05);
                border: 1px solid rgba(0, 224, 255, 0.2);
                border-radius: 12px;
                min-width: 100px;
                text-align: center;
            }
        """)
        self.page_info_label.setAlignment(Qt.AlignCenter)
        
        # 下一页按钮
        self.next_btn = QPushButton("下一页 ➡")
        self.next_btn.setFixedSize(100, 36)
        self.next_btn.setStyleSheet(self.get_button_style())
        
        # 组装中心控制区
        center_layout.addWidget(self.prev_btn)
        center_layout.addWidget(self.page_info_label)
        center_layout.addWidget(self.next_btn)
        
        # 快捷提示
        tips_label = QLabel("💡 提示: 滚轮上下翻页 | Shift+滚轮左右滚动(实际大小模式)")
        tips_label.setStyleSheet("""
            QLabel {
                color: #6a7a8a;
                font-size: 11px;
                font-style: italic;
                background: transparent;
            }
        """)
        
        # 组装控制栏
        control_layout.addStretch()
        control_layout.addWidget(center_controls)
        control_layout.addStretch()
        control_layout.addWidget(tips_label)
        
        return control_bar
    
    def connect_signals(self):
        """连接信号"""
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.size_selector.currentIndexChanged.connect(self.on_size_changed)
        self.mode_group.buttonClicked.connect(self.on_mode_changed)
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_PageUp:
            self.prev_page()
        elif event.key() == Qt.Key_PageDown:
            self.next_page()
        elif event.key() == Qt.Key_Home:
            self.go_to_page(1)
        elif event.key() == Qt.Key_End:
            self.go_to_page(self.total_pages)
        else:
            super().keyPressEvent(event)
    
    def on_mode_changed(self):
        """处理预览模式改变"""
        if self.fit_mode_btn.isChecked():
            self.preview_mode = "fit"
            # 适应窗口模式：隐藏滚动条，启用自适应
            self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.web_container.setWidgetResizable(True)
            
            # 清除 WebView 的固定尺寸限制
            self.web_view.setMinimumSize(0, 0)
            self.web_view.setMaximumSize(16777215, 16777215)
            
            # 在适应模式下，WebView不需要处理鼠标事件
            self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            
        else:
            self.preview_mode = "actual"
            # 实际大小模式：显示滚动条
            self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.web_container.setWidgetResizable(False)
            
            # 在实际大小模式下，让WebView透明于鼠标滚轮事件
            # 这样滚轮事件会直接传递给ScrollArea
            self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        # 重新渲染当前页面
        self.display_current_page()
    
    def on_size_changed(self, index):
        """处理尺寸改变"""
        size_map = {0: "small", 1: "medium", 2: "large"}
        new_size = size_map.get(index, "medium")
        
        if new_size != self.current_size:
            self.current_size = new_size
            
            # 更新各组件的尺寸设置
            self.html_generator = HTMLGenerator(page_size=new_size)
            self.paginator.set_page_size(new_size)
            
            # 重新处理内容
            if self.markdown_text:
                self.update_content(self.markdown_text)
            
            # 发送尺寸改变信号
            self.sizeChanged.emit(new_size)
    
    def update_content(self, markdown_text: str):
        """更新预览内容"""
        try:
            self.markdown_text = markdown_text
            
            # 处理 Markdown
            html_content = self.markdown_processor.parse(markdown_text)
            
            # 使用智能分页器进行分页
            self.current_pages = self.paginator.paginate(html_content)
            
            # 优化分页结果
            self.current_pages = self.paginator.optimize_pages(self.current_pages)
            
            self.total_pages = len(self.current_pages)
            self.current_page = 1
            
            # 显示第一页
            self.display_current_page()
            
            # 更新按钮和信息
            self.update_buttons()
            self.update_page_info()
            
        except Exception as e:
            self.show_error(f"预览错误: {str(e)}")
    
    def display_current_page(self):
        """显示当前页"""
        if not self.current_pages:
            return
            
        if 1 <= self.current_page <= len(self.current_pages):
            page_content = self.current_pages[self.current_page - 1]
            
            # 获取目标尺寸
            size_config = {
                "small": (720, 960),
                "medium": (1080, 1440),
                "large": (1440, 1920)
            }
            target_width, target_height = size_config.get(self.current_size, (1080, 1440))
            
            # 根据预览模式生成不同的HTML
            if self.preview_mode == "fit":
                # 适应窗口模式
                full_html = self.generate_fit_html(page_content, target_width, target_height)
                self.web_view.setMinimumSize(0, 0)
                self.web_view.setMaximumSize(16777215, 16777215)
                self.web_container.setWidgetResizable(True)
                
            else:
                # 实际大小模式：添加禁用内部滚动的CSS
                full_html = self.generate_actual_html(page_content, target_width, target_height)
                # 设置WebView为实际尺寸
                self.web_view.setFixedSize(target_width, target_height)
                self.web_container.setWidgetResizable(False)
            
            # 加载到WebView
            self.web_view.setHtml(full_html, QUrl("file:///"))
    
    def generate_actual_html(self, content: str, target_width: int, target_height: int) -> str:
        """生成实际大小模式的HTML（禁用内部滚动）"""
        base_html = self.html_generator.generate(content)
        
        # 添加禁用滚动的CSS和JavaScript
        disable_scroll = """
        <style>
            /* 禁用所有内部滚动 */
            html, body {
                overflow: hidden !important;
                position: fixed !important;
                width: 100% !important;
                height: 100% !important;
                touch-action: none !important;
                user-select: none !important;
                -webkit-user-select: none !important;
                -ms-overflow-style: none !important;
                scrollbar-width: none !important;
            }
            
            html::-webkit-scrollbar,
            body::-webkit-scrollbar {
                display: none !important;
            }
            
            * {
                -ms-overflow-style: none !important;
                scrollbar-width: none !important;
            }
            
            *::-webkit-scrollbar {
                display: none !important;
            }
        </style>
        
        <script>
            // 禁用滚动事件
            document.addEventListener('DOMContentLoaded', function() {
                // 禁用滚轮事件
                document.addEventListener('wheel', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, { passive: false, capture: true });
                
                // 禁用触摸滚动
                document.addEventListener('touchmove', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, { passive: false, capture: true });
                
                // 禁用键盘滚动
                document.addEventListener('keydown', function(e) {
                    const scrollKeys = [32, 33, 34, 35, 36, 37, 38, 39, 40];
                    if (scrollKeys.includes(e.keyCode)) {
                        e.preventDefault();
                        return false;
                    }
                }, false);
                
                // 固定body位置
                document.body.style.position = 'fixed';
                document.body.style.top = '0';
                document.body.style.left = '0';
                document.body.style.width = '100%';
                document.body.style.height = '100%';
                document.body.style.overflow = 'hidden';
            });
        </script>
        """
        
        # 插入到head标签结束前
        full_html = base_html.replace('</head>', disable_scroll + '</head>')
        
        return full_html
    
    def generate_fit_html(self, content: str, target_width: int, target_height: int) -> str:
        """生成适应窗口的HTML"""
        base_html = self.html_generator.generate(content)
        
        scale_script = f"""
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            html, body {{
                width: 100%;
                height: 100%;
                overflow: hidden;
                background: #1a1a2e;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            
            #viewport-container {{
                position: relative;
                width: 100vw;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }}
            
            #content-wrapper {{
                position: relative;
                width: {target_width}px;
                height: {target_height}px;
                transform-origin: center center;
                transition: transform 0.3s ease;
                flex-shrink: 0;
            }}
        </style>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                if (!document.getElementById('viewport-container')) {{
                    const viewportContainer = document.createElement('div');
                    viewportContainer.id = 'viewport-container';
                    
                    const contentWrapper = document.createElement('div');
                    contentWrapper.id = 'content-wrapper';
                    
                    while (document.body.firstChild) {{
                        contentWrapper.appendChild(document.body.firstChild);
                    }}
                    
                    viewportContainer.appendChild(contentWrapper);
                    document.body.appendChild(viewportContainer);
                }}
                
                function adjustScale() {{
                    const wrapper = document.getElementById('content-wrapper');
                    const container = document.getElementById('viewport-container');
                    
                    if (!wrapper || !container) return;
                    
                    const availableWidth = container.clientWidth;
                    const availableHeight = container.clientHeight;
                    
                    const targetWidth = {target_width};
                    const targetHeight = {target_height};
                    
                    const padding = 40;
                    const scaleX = (availableWidth - padding) / targetWidth;
                    const scaleY = (availableHeight - padding) / targetHeight;
                    
                    const scale = Math.min(scaleX, scaleY, 1.0);
                    
                    wrapper.style.transform = `scale(${{scale}})`;
                }}
                
                setTimeout(adjustScale, 100);
                window.addEventListener('resize', adjustScale);
                
                const observer = new ResizeObserver(adjustScale);
                observer.observe(document.getElementById('viewport-container'));
            }});
        </script>
        """
        
        full_html = base_html.replace('</head>', scale_script + '</head>')
        return full_html
    
    # ... 其余方法保持不变 ...
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.go_to_page(self.current_page - 1)
    
    def next_page(self):
        """下一页"""
        if self.current_page < self.total_pages:
            self.go_to_page(self.current_page + 1)
    
    def go_to_page(self, page_num: int):
        """跳转到指定页"""
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num
            self.display_current_page()
            self.update_buttons()
            self.update_page_info()
    
    def update_buttons(self):
        """更新按钮状态"""
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)
        self.pageChanged.emit(self.current_page, self.total_pages)
    
    def update_page_info(self):
        """更新页面信息显示"""
        if self.total_pages > 1:
            self.page_info_label.setText(f"第 {self.current_page} / {self.total_pages} 页")
        else:
            self.page_info_label.setText("第 1 页")
    
    def get_button_style(self) -> str:
        """获取按钮样式"""
        return """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.15),
                    stop: 1 rgba(0, 150, 255, 0.1)
                );
                border: 1px solid rgba(0, 224, 255, 0.4);
                color: #00e0ff;
                padding: 8px 16px;
                border-radius: 8px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.25),
                    stop: 1 rgba(0, 150, 255, 0.2)
                );
                border: 1px solid rgba(0, 224, 255, 0.6);
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(0, 224, 255, 0.35),
                    stop: 1 rgba(0, 150, 255, 0.3)
                );
            }
            QPushButton:disabled {
                background: rgba(30, 30, 45, 0.5);
                border-color: rgba(100, 100, 120, 0.3);
                color: rgba(100, 100, 120, 0.5);
            }
        """
    
    def get_combobox_style(self) -> str:
        """获取下拉框样式"""
        return """
            QComboBox {
                background: rgba(0, 224, 255, 0.1);
                border: 1px solid rgba(0, 224, 255, 0.3);
                color: #00e0ff;
                padding: 5px 10px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 500;
            }
            QComboBox:hover {
                background: rgba(0, 224, 255, 0.15);
                border: 1px solid rgba(0, 224, 255, 0.5);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #00e0ff;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background: rgba(25, 25, 40, 0.98);
                border: 1px solid rgba(0, 224, 255, 0.3);
                color: #00e0ff;
                selection-background-color: rgba(0, 224, 255, 0.2);
                outline: none;
            }
        """
    
    def get_radio_style(self) -> str:
        """获取单选按钮样式"""
        return """
            QRadioButton {
                color: #8a92a6;
                font-size: 12px;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 14px;
                height: 14px;
                border: 2px solid rgba(0, 224, 255, 0.4);
                border-radius: 7px;
                background: transparent;
            }
            QRadioButton::indicator:checked {
                background: qradialgradient(
                    cx: 0.5, cy: 0.5, radius: 0.5,
                    fx: 0.5, fy: 0.5,
                    stop: 0 #00e0ff,
                    stop: 0.6 #00e0ff,
                    stop: 0.7 transparent
                );
                border-color: #00e0ff;
            }
            QRadioButton:checked {
                color: #00e0ff;
            }
        """
    
    def setup_exporter(self):
        """设置导出器"""
        self.exporter = ImageExporter(self.web_view)
        self.exporter.progress.connect(self.on_export_progress)
        self.exporter.finished.connect(self.on_export_finished)
        self.exporter.page_exported.connect(self.on_page_exported)
    
    def export_pages(self, folder: str):
        """导出所有页面为图片"""
        if not self.current_pages:
            QMessageBox.warning(self, "提示", "没有可导出的内容")
            return
        
        # 创建进度对话框
        self.progress_dialog = QProgressDialog(
            "正在导出图片...", 
            "取消", 
            0, 
            self.total_pages, 
            self
        )
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.canceled.connect(self.on_export_canceled)
        
        # 开始导出（始终以实际大小导出）
        self.exporter.export_pages(
            self.current_pages,
            folder,
            self.html_generator,
            format="PNG",
            quality=100
        )
    
    def on_export_progress(self, current: int, total: int):
        """处理导出进度"""
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.setValue(current)
            self.progress_dialog.setLabelText(f"正在导出第 {current}/{total} 页...")
    
    def on_export_finished(self, success: bool, message: str):
        """处理导出完成"""
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            try:
                self.progress_dialog.canceled.disconnect()
                self.progress_dialog.close()
                self.progress_dialog.deleteLater()
            except:
                pass
            finally:
                self.progress_dialog = None
        
        if success:
            size_info = f"({self.current_size}: {self.get_actual_size()}px)"
            QMessageBox.information(self, "导出成功", f"{message}\n尺寸: {size_info}")
        else:
            QMessageBox.warning(self, "导出失败", message)
    
    def on_page_exported(self, page_num: int, file_path: str):
        """处理单页导出完成"""
        print(f"已导出第 {page_num} 页: {file_path}")
    
    def on_export_canceled(self):
        """处理导出取消"""
        self.exporter.cancel_export()
    
    def get_actual_size(self) -> str:
        """获取实际尺寸"""
        size_config = {
            "small": "720×960",
            "medium": "1080×1440",
            "large": "1440×1920"
        }
        return size_config.get(self.current_size, "1080×1440")
    
    def handle_scroll(self, percentage: float):
        """处理编辑器滚动同步（保留接口兼容性）"""
        pass
    
    def show_error(self, message: str):
        """显示错误信息"""
        error_html = f"""
        <html>
        <body style="padding: 20px; font-family: sans-serif; background: #1a1a2e; color: #e0e6ed;">
            <h3 style="color: #ff4757;">错误</h3>
            <p style="color: #8a92a6;">{message}</p>
        </body>
        </html>
        """
        self.web_view.setHtml(error_html)
    
    def change_theme(self, theme: str):
        """切换主题"""
        self.html_generator.set_theme(theme)
        if self.current_pages:
            self.display_current_page()
    
    def resizeEvent(self, event):
        """处理窗口大小改变事件"""
        super().resizeEvent(event)
        # 在适应窗口模式下，重新渲染以适应新尺寸
        if self.preview_mode == "fit" and self.current_pages:
            # 延迟执行以避免频繁重绘
            if hasattr(self, 'resize_timer'):
                self.resize_timer.stop()
            else:
                self.resize_timer = QTimer()
                self.resize_timer.timeout.connect(self.on_resize_finished)
                self.resize_timer.setSingleShot(True)
            self.resize_timer.start(300)
    
    def on_resize_finished(self):
        """窗口大小调整完成后的处理"""
        if self.preview_mode == "fit":
            self.display_current_page() exporter.py->text/plain-># ============================================
# src/utils/exporter.py
# ============================================
from PySide6.QtCore import QObject, Signal, QTimer, QEventLoop, QSize, Qt, QPoint, QRect
from PySide6.QtGui import QImage, QPainter, QFont, QColor, QPageSize, QRegion
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtPrintSupport import QPrinter
from PySide6.QtWidgets import QWidget
from pathlib import Path
from typing import List, Optional
import json
import time

class ImageExporter(QObject):
    """图片导出器"""
    
    # 信号
    progress = Signal(int, int)  # 当前进度，总数
    finished = Signal(bool, str)  # 是否成功，消息
    page_exported = Signal(int, str)  # 页码，文件路径
    
    def __init__(self, web_view: QWebEngineView):
        super().__init__()
        self.web_view = web_view
        self.pages_to_export = []
        self.current_export_index = 0
        self.output_folder = ""
        self.html_generator = None
        self.export_format = "PNG"
        self.quality = 100
        self._is_exporting = False
        
    def export_pages(self, pages: List[str], output_folder: str, html_generator, 
                     format: str = "PNG", quality: int = 100) -> None:
        """
        导出多个页面为图片
        
        Args:
            pages: HTML页面内容列表
            output_folder: 输出文件夹路径
            html_generator: HTML生成器实例
            format: 图片格式 (PNG/JPEG)
            quality: 图片质量 (1-100)
        """
        self.pages_to_export = pages
        self.output_folder = Path(output_folder)
        self.current_export_index = 0
        self.html_generator = html_generator
        self.export_format = format
        self.quality = quality
        self._is_exporting = True
        
        # 确保输出文件夹存在
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # 确保WebView是固定尺寸
        self.web_view.setFixedSize(1080, 1440)
        self.web_view.setZoomFactor(1.0)  # 重置缩放
        
        # 开始导出第一页
        self._export_next_page()
    
    def _export_next_page(self):
        """导出下一页"""
        if not self._is_exporting:
            return
            
        if self.current_export_index >= len(self.pages_to_export):
            # 导出完成
            self._is_exporting = False
            self.finished.emit(True, f"成功导出 {len(self.pages_to_export)} 张图片")
            return
        
        # 发送进度信号
        self.progress.emit(self.current_export_index + 1, len(self.pages_to_export))
        
        # 获取当前页内容
        page_content = self.pages_to_export[self.current_export_index]
        page_num = self.current_export_index + 1
        
        # 生成完整HTML（包含页码信息）
        full_html = self.html_generator.generate(
            page_content, 
            page_num=page_num, 
            total_pages=len(self.pages_to_export)
        )
        
        # 加载HTML到WebView
        self.web_view.setHtml(full_html, "file:///")
        
        # 等待页面加载完成后导出
        QTimer.singleShot(1500, lambda: self._capture_page(page_num))
    
    def _capture_page(self, page_num: int):
        """捕获当前页面为图片"""
        if not self._is_exporting:
            return
            
        # 构建输出文件名
        extension = self.export_format.lower()
        filename = f"card_{page_num:02d}.{extension}"
        output_path = self.output_folder / filename
        
        # 使用精确的捕获方法
        self._capture_fixed_size(output_path, page_num)
    
    def _capture_fixed_size(self, output_path: Path, page_num: int):
        """捕获固定尺寸的页面"""
        try:
            # 从html_generator获取当前尺寸
            target_width = self.html_generator.page_width
            target_height = self.html_generator.page_height
            
            # 创建目标图片
            image = QImage(target_width, target_height, QImage.Format_ARGB32)
            image.fill(Qt.white)
            
            # 创建painter
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            
            # 确保WebView是正确的尺寸
            self.web_view.resize(target_width, target_height)
            
            # 渲染WebView到图片
            # 使用固定的源矩形来确保只捕获卡片区域
            source_rect = QRect(0, 0, target_width, target_height)
            target_rect = QRect(0, 0, target_width, target_height)
            
            # 渲染WebView
            if isinstance(self.web_view, QWidget):
                self.web_view.render(
                    painter,
                    QPoint(0, 0),
                    QRegion(source_rect),
                    QWidget.RenderFlag.DrawWindowBackground | QWidget.RenderFlag.DrawChildren
                )
            
            # 可选：添加导出时间水印
            self._add_export_watermark(painter, page_num)
            
            painter.end()
            
            # 保存图片
            success = image.save(str(output_path), self.export_format, self.quality)
            
            if success:
                self.page_exported.emit(page_num, str(output_path))
                # 继续导出下一页
                self.current_export_index += 1
                QTimer.singleShot(100, self._export_next_page)
            else:
                self._is_exporting = False
                self.finished.emit(False, f"保存图片失败: {output_path}")
                
        except Exception as e:
            self._is_exporting = False
            self.finished.emit(False, f"导出页面 {page_num} 时出错: {str(e)}")
    
    def _add_export_watermark(self, painter: QPainter, page_num: int):
        """添加导出水印（可选）"""
        # 设置水印字体和颜色
        font = QFont("Arial", 9)
        painter.setFont(font)
        painter.setPen(QColor(200, 200, 200, 80))
        
        # 在右下角添加生成时间（非常淡的水印）
        timestamp = time.strftime("%Y%m%d")
        painter.drawText(
            1000, 1420,
            f"{timestamp}"
        )
    
    def export_as_pdf(self, pages: List[str], output_file: str, html_generator):
        """
        导出为PDF文件（所有页面合并为一个PDF）
        
        Args:
            pages: HTML页面内容列表
            output_file: 输出PDF文件路径
            html_generator: HTML生成器实例
        """
        try:
            # 创建PDF打印机
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(output_file)
            
            # 设置页面大小为小红书卡片比例
            # 注意：PDF使用点(point)作为单位，1点 = 1/72英寸
            # 1080px × 1440px 在 96 DPI 下约等于 810pt × 1080pt
            page_size = QPageSize(QSize(810, 1080), QPageSize.Unit.Point)
            printer.setPageSize(page_size)
            printer.setPageMargins(0, 0, 0, 0, QPrinter.Unit.Millimeter)
            
            # 合并所有页面内容
            combined_html = self._combine_pages_for_pdf(pages, html_generator)
            
            # 加载合并后的HTML
            self.web_view.setHtml(combined_html, "file:///")
            
            # 等待加载完成后打印
            loop = QEventLoop()
            
            def on_load_finished():
                self.web_view.page().print(printer, lambda success: loop.quit())
            
            QTimer.singleShot(1000, on_load_finished)
            loop.exec()
            
            self.finished.emit(True, f"PDF导出成功: {output_file}")
            
        except Exception as e:
            self.finished.emit(False, f"PDF导出失败: {str(e)}")
    
    def _combine_pages_for_pdf(self, pages: List[str], html_generator) -> str:
        """合并多个页面为PDF格式"""
        combined_content = ""
        
        for i, page in enumerate(pages, 1):
            if i > 1:
                # 添加分页符
                combined_content += '<div style="page-break-before: always;"></div>'
            
            # 添加页面内容，包装在固定尺寸的容器中
            combined_content += f'''
            <div style="width: 1080px; height: 1440px; position: relative; overflow: hidden;">
                {page}
            </div>
            '''
        
        # 生成完整HTML
        return html_generator.generate(combined_content)
    
    def cancel_export(self):
        """取消导出"""
        self._is_exporting = False
        self.pages_to_export = []
        self.finished.emit(False, "导出已取消") paginator.py->text/plain-># ============================================
# src/utils/paginator.py
# ============================================
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import re

@dataclass
class PageElement:
    """页面元素"""
    type: str  # 'heading', 'paragraph', 'list', 'code', 'blockquote', 'table', 'hr', 'text', 'pagebreak'
    content: str  # HTML内容
    text: str  # 纯文本内容（用于计算高度）
    level: int = 0  # 标题级别或嵌套深度
    height: int = 0  # 估算高度（像素）
    can_break: bool = True  # 是否可以在此处分页
    is_forced_break: bool = False  # 是否是强制分页（用于标记用户添加的分页符）
    
class SmartPaginator:
    """智能分页器 - 支持多尺寸"""
    
    # 元素高度估算（像素）- 调整为更准确的值
    ELEMENT_HEIGHTS = {
        'h1': 90,        # 大标题 + 底部边框
        'h2': 70,        # 二级标题
        'h3': 60,        # 三级标题
        'h4': 50,        # 四级标题
        'h5': 45,        # 五级标题
        'h6': 40,        # 六级标题
        'p_base': 25,    # 段落基础高度
        'p_line': 28,    # 段落每行高度（考虑行高1.8）
        'li': 35,        # 列表项
        'code_block': 40,  # 代码块基础高度
        'code_line': 24,   # 代码每行高度
        'blockquote': 60,  # 引用块基础高度
        'blockquote_line': 28,  # 引用每行高度
        'table_header': 45,  # 表格头
        'table_row': 40,     # 表格行
        'hr': 35,           # 分隔线
        'margin_bottom': 20,  # 元素底部间距
    }
    
    # 页面尺寸配置
    PAGE_SIZES = {
        "small": {
            "width": 720,
            "height": 960,
            "padding_top": 35,
            "padding_bottom": 50,
            "padding_sides": 30
        },
        "medium": {
            "width": 1080,
            "height": 1440,
            "padding_top": 45,
            "padding_bottom": 70,
            "padding_sides": 40
        },
        "large": {
            "width": 1440,
            "height": 1920,
            "padding_top": 55,
            "padding_bottom": 90,
            "padding_sides": 50
        }
    }
    
    # 分页策略参数
    MIN_ORPHAN_LINES = 2  # 孤行控制：段落末尾最少保留行数
    MIN_WIDOW_LINES = 2   # 寡行控制：段落开头最少保留行数
    HEADING_KEEP_WITH = 150  # 标题后至少保留的内容高度
    
    # 字符宽度估算（像素）
    CHAR_WIDTH = 16  # 中文字符平均宽度
    CHAR_WIDTH_EN = 9  # 英文字符平均宽度
    
    def __init__(self, page_size: str = "medium"):
        """
        初始化分页器
        
        Args:
            page_size: 页面尺寸 ("small", "medium", "large")
        """
        self.elements: List[PageElement] = []
        self.set_page_size(page_size)
        self.forced_break_pages = set()  # 记录哪些页面是通过分页符创建的
        
    def set_page_size(self, size: str):
        """设置页面尺寸"""
        if size not in self.PAGE_SIZES:
            size = "medium"
        
        config = self.PAGE_SIZES[size]
        self.page_size_name = size
        self.page_width = config["width"]
        self.page_height = config["height"]
        self.padding_top = config["padding_top"]
        self.padding_bottom = config["padding_bottom"]
        self.padding_sides = config["padding_sides"]
        
        # 计算内容区域
        self.content_width = self.page_width - (self.padding_sides * 2)
        self.content_height = self.page_height - self.padding_top - self.padding_bottom
        
        # 根据尺寸调整分页策略
        if size == "small":
            self.HEADING_KEEP_WITH = 100  # 小尺寸页面，标题后保留空间可以更少
        elif size == "large":
            self.HEADING_KEEP_WITH = 200  # 大尺寸页面，标题后保留更多空间
        else:
            self.HEADING_KEEP_WITH = 150
    
    def get_page_info(self) -> Dict:
        """获取当前页面配置信息"""
        return {
            "size_name": self.page_size_name,
            "width": self.page_width,
            "height": self.page_height,
            "content_width": self.content_width,
            "content_height": self.content_height,
            "padding": {
                "top": self.padding_top,
                "bottom": self.padding_bottom,
                "sides": self.padding_sides
            }
        }
    
    def paginate(self, html_content: str) -> List[str]:
        """
        核心分页方法
        
        Args:
            html_content: HTML内容
            
        Returns:
            分页后的HTML内容列表
        """
        # 重置强制分页记录
        self.forced_break_pages = set()
        
        # 1. 解析HTML为元素列表
        elements = self.parse_html_to_elements(html_content)
        
        if not elements:
            return [html_content] if html_content else []
        
        # 2. 执行分页
        pages = []
        current_page_elements = []
        current_height = 0
        consecutive_breaks = 0  # 追踪连续的分页符数量
        
        i = 0
        while i < len(elements):
            element = elements[i]
            
            # 处理强制分页标记
            if element.type == 'pagebreak':
                consecutive_breaks += 1
                
                # 保存当前页（如果有内容）
                if current_page_elements:
                    pages.append(self._elements_to_html(current_page_elements))
                    self.forced_break_pages.add(len(pages) - 1)  # 记录这是强制分页
                    current_page_elements = []
                    current_height = 0
                elif consecutive_breaks > 1:
                    # 如果是连续的分页符，创建空页
                    pages.append("")
                    self.forced_break_pages.add(len(pages) - 1)  # 记录这是强制分页创建的空页
                
                i += 1
                continue
            
            # 非分页符元素，重置连续分页符计数
            consecutive_breaks = 0
            
            # 检查是否需要分页
            element_height = element.height
            
            # 特殊处理：标题元素
            if element.type == 'heading':
                # 检查标题后是否有足够空间放置内容
                if current_height + element_height + self.HEADING_KEEP_WITH > self.content_height:
                    # 需要分页，标题放到下一页
                    if current_page_elements:
                        pages.append(self._elements_to_html(current_page_elements))
                        current_page_elements = []
                        current_height = 0
            
            # 检查当前元素是否超出页面高度
            if current_height + element_height > self.content_height:
                # 检查是否可以分割元素
                if element.type == 'paragraph' and element_height > self.content_height * 0.3:
                    # 长段落可以尝试分割
                    split_result = self._try_split_paragraph(element, self.content_height - current_height)
                    if split_result:
                        first_part, second_part = split_result
                        if first_part:
                            current_page_elements.append(first_part)
                        pages.append(self._elements_to_html(current_page_elements))
                        current_page_elements = [second_part] if second_part else []
                        current_height = second_part.height if second_part else 0
                    else:
                        # 无法分割，整个元素放到下一页
                        if current_page_elements:
                            pages.append(self._elements_to_html(current_page_elements))
                        current_page_elements = [element]
                        current_height = element_height
                else:
                    # 不可分割的元素或不需要分割，放到下一页
                    if current_page_elements:
                        pages.append(self._elements_to_html(current_page_elements))
                    current_page_elements = [element]
                    current_height = element_height
            else:
                # 当前元素可以放入当前页
                current_page_elements.append(element)
                current_height += element_height
            
            i += 1
        
        # 3. 保存最后一页
        if current_page_elements:
            pages.append(self._elements_to_html(current_page_elements))
        
        # 4. 如果没有生成任何页面，返回原始内容
        if not pages:
            return [html_content]
        
        return pages
    
    def _elements_to_html(self, elements: List[PageElement]) -> str:
        """将元素列表转换回HTML字符串"""
        html_parts = []
        for element in elements:
            if element.type != 'pagebreak':  # 跳过分页标记
                html_parts.append(element.content)
        return '\n'.join(html_parts)
    
    def _try_split_paragraph(self, element: PageElement, available_height: int) -> Optional[Tuple[PageElement, PageElement]]:
        """
        尝试分割段落
        
        Args:
            element: 要分割的段落元素
            available_height: 当前页剩余高度
            
        Returns:
            分割后的两个元素，如果无法分割则返回None
        """
        # 简单实现：暂不分割段落，保持段落完整性
        # 未来可以实现更复杂的分割逻辑
        return None
    
    def _calculate_text_height(self, text: str) -> int:
        """计算纯文本高度"""
        if not text:
            return 0
        
        # 估算文本行数
        chars_per_line = self.content_width // self.CHAR_WIDTH
        total_chars = len(text)
        estimated_lines = max(1, (total_chars + chars_per_line - 1) // chars_per_line)
        
        return self.ELEMENT_HEIGHTS['p_base'] + estimated_lines * self.ELEMENT_HEIGHTS['p_line']
    
    def _calculate_paragraph_height(self, text: str) -> int:
        """计算段落高度"""
        if not text:
            return self.ELEMENT_HEIGHTS['p_base']
        
        # 考虑中英文混合
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_chars = len(text) - chinese_chars
        
        # 计算平均每行字符数
        avg_char_width = (chinese_chars * self.CHAR_WIDTH + english_chars * self.CHAR_WIDTH_EN) / max(1, len(text))
        chars_per_line = self.content_width / avg_char_width
        
        # 计算行数
        lines = max(1, int(len(text) / chars_per_line) + 1)
        
        return self.ELEMENT_HEIGHTS['p_base'] + lines * self.ELEMENT_HEIGHTS['p_line'] + self.ELEMENT_HEIGHTS['margin_bottom']
    
    def _calculate_blockquote_height(self, text: str) -> int:
        """计算引用块高度"""
        if not text:
            return self.ELEMENT_HEIGHTS['blockquote']
        
        # 引用块内容宽度更窄
        effective_width = self.content_width - 60  # 减去左边框和内边距
        chars_per_line = effective_width // self.CHAR_WIDTH
        lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)
        
        return self.ELEMENT_HEIGHTS['blockquote'] + lines * self.ELEMENT_HEIGHTS['blockquote_line'] + self.ELEMENT_HEIGHTS['margin_bottom']
    
    def parse_html_to_elements(self, html: str) -> List[PageElement]:
        """
        将HTML解析为页面元素列表，保持原始顺序
        改进版：使用深度优先遍历，确保所有分页标记都被识别
        """
        elements = []
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # 深度优先遍历所有元素，扁平化处理
        elements = self._flatten_parse(soup)
        
        return elements
    
    def _flatten_parse(self, node) -> List[PageElement]:
        """
        扁平化解析所有节点，确保分页标记被正确识别
        这个方法会遍历整个DOM树，将所有内容扁平化为元素列表
        """
        elements = []
        
        # 如果是文本节点
        if isinstance(node, NavigableString):
            # 跳过注释和空白文本
            if not isinstance(node, Comment):
                text = str(node).strip()
                if text:
                    elements.append(PageElement(
                        type='text',
                        content=f'<p>{text}</p>',
                        text=text,
                        height=self._calculate_text_height(text),
                        can_break=True
                    ))
            return elements
        
        # 如果不是Tag，返回空列表
        if not isinstance(node, Tag):
            return elements
        
        # 首先检查是否是分页标记
        if self._is_pagebreak_marker(node):
            elements.append(PageElement(
                type='pagebreak',
                content='',
                text='',
                height=0,
                can_break=True,
                level=999,
                is_forced_break=True  # 标记为强制分页
            ))
            return elements
        
        # 处理具体的元素类型
        tag_name = node.name.lower()
        
        # 处理块级元素
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            # 标题元素
            level = int(tag_name[1])
            text = node.get_text(strip=True)
            height = self.ELEMENT_HEIGHTS[tag_name] + self.ELEMENT_HEIGHTS['margin_bottom']
            
            elements.append(PageElement(
                type='heading',
                content=str(node),
                text=text,
                level=level,
                height=height,
                can_break=False
            ))
            
        elif tag_name == 'p':
            # 段落元素 - 需要检查内部是否有分页标记
            has_pagebreak = False
            sub_elements = []
            
            # 检查段落内部的所有子节点
            for child in node.children:
                if isinstance(child, Tag) and self._is_pagebreak_marker(child):
                    has_pagebreak = True
                    # 如果段落内有分页标记，需要特殊处理
                    # 先保存分页标记前的内容
                    text_before = ''.join(str(c) for c in list(node.children)[:list(node.children).index(child)])
                    if text_before.strip():
                        sub_elements.append(PageElement(
                            type='paragraph',
                            content=f'<p>{text_before}</p>',
                            text=text_before,
                            height=self._calculate_paragraph_height(text_before),
                            can_break=True
                        ))
                    # 添加分页标记
                    sub_elements.append(PageElement(
                        type='pagebreak',
                        content='',
                        text='',
                        height=0,
                        can_break=True,
                        level=999,
                        is_forced_break=True
                    ))
            
            if has_pagebreak:
                elements.extend(sub_elements)
            else:
                # 正常的段落
                text = node.get_text(strip=True)
                if text:
                    height = self._calculate_paragraph_height(text)
                    elements.append(PageElement(
                        type='paragraph',
                        content=str(node),
                        text=text,
                        height=height,
                        can_break=True
                    ))
                    
        elif tag_name in ['ul', 'ol']:
            # 列表元素
            items = node.find_all('li')
            text = node.get_text(strip=True)
            height = len(items) * self.ELEMENT_HEIGHTS['li'] + self.ELEMENT_HEIGHTS['margin_bottom']
            
            elements.append(PageElement(
                type='list',
                content=str(node),
                text=text,
                height=height,
                can_break=len(items) > 3
            ))
            
        elif tag_name == 'pre':
            # 代码块
            text = node.get_text()
            lines = text.count('\n') + 1
            height = (self.ELEMENT_HEIGHTS['code_block'] + 
                    lines * self.ELEMENT_HEIGHTS['code_line'] +
                    self.ELEMENT_HEIGHTS['margin_bottom'])
            
            elements.append(PageElement(
                type='code',
                content=str(node),
                text=text,
                height=height,
                can_break=lines > 10
            ))
            
        elif tag_name == 'blockquote':
            # 引用块
            text = node.get_text(strip=True)
            height = self._calculate_blockquote_height(text)
            
            elements.append(PageElement(
                type='blockquote',
                content=str(node),
                text=text,
                height=height,
                can_break=True
            ))
            
        elif tag_name == 'table':
            # 表格
            rows = node.find_all('tr')
            headers = node.find_all('th')
            text = node.get_text(strip=True)
            
            height = (len(headers) * self.ELEMENT_HEIGHTS['table_header'] +
                    (len(rows) - len(headers)) * self.ELEMENT_HEIGHTS['table_row'] +
                    self.ELEMENT_HEIGHTS['margin_bottom'])
            
            elements.append(PageElement(
                type='table',
                content=str(node),
                text=text,
                height=height,
                can_break=len(rows) > 5
            ))
            
        elif tag_name == 'hr':
            # 分隔线
            elements.append(PageElement(
                type='hr',
                content=str(node),
                text='',
                height=self.ELEMENT_HEIGHTS['hr'],
                can_break=True
            ))
            
        elif tag_name in ['div', 'section', 'article', 'main', 'aside', 'nav', 'header', 'footer']:
            # 容器元素 - 递归处理子元素
            for child in node.children:
                elements.extend(self._flatten_parse(child))
                
        else:
            # 其他元素 - 递归处理子元素
            # 但首先检查是否有实际内容
            text = node.get_text(strip=True)
            if text:
                # 检查子元素中是否有分页标记
                for child in node.children:
                    child_elements = self._flatten_parse(child)
                    if child_elements:
                        elements.extend(child_elements)
                
                # 如果没有子元素被解析，则将整个元素作为文本处理
                if not elements:
                    elements.append(PageElement(
                        type='text',
                        content=str(node),
                        text=text,
                        height=self._calculate_text_height(text),
                        can_break=True
                    ))
            else:
                # 递归处理子元素
                for child in node.children:
                    elements.extend(self._flatten_parse(child))
        
        return elements
    
    def _is_pagebreak_marker(self, element: Tag) -> bool:
        """
        检查元素是否是分页标记
        支持多种识别方式
        """
        if not isinstance(element, Tag):
            return False
            
        # 检查是否是带有特定class的div
        if element.name.lower() == 'div':
            classes = element.get('class', [])
            if isinstance(classes, str):
                classes = classes.split()
            
            # 检查class名
            if 'pagebreak-marker' in classes:
                return True
            
            # 检查data属性
            if element.get('data-pagebreak') == 'true':
                return True
        
        return False
    
    def optimize_pages(self, pages: List[str]) -> List[str]:
        """
        优化分页结果，合并过短的页面
        修改：保留通过分页符创建的页面，即使是空页
        """
        if len(pages) <= 1:
            return pages
        
        optimized = []
        i = 0
        
        # 根据页面尺寸调整合并阈值
        merge_threshold = 0.35 if self.page_size_name == "small" else 0.4
        
        while i < len(pages):
            current_page = pages[i]
            
            # 检查当前页是否是通过分页符创建的
            is_forced_page = i in self.forced_break_pages
            
            # 如果是强制分页创建的页面，直接保留（即使是空页）
            if is_forced_page:
                optimized.append(current_page)
                i += 1
                continue
            
            # 非强制分页的页面，进行常规优化
            # 过滤掉完全空的页面
            if not current_page or not current_page.strip():
                i += 1
                continue
            
            # 估算当前页面高度
            current_elements = self.parse_html_to_elements(current_page)
            current_height = sum(e.height for e in current_elements)
            
            # 如果页面过短，尝试与下一页合并（但不合并强制分页的页面）
            if current_height < self.content_height * merge_threshold and i < len(pages) - 1:
                next_page_index = i + 1
                # 检查下一页是否是强制分页
                if next_page_index not in self.forced_break_pages:
                    next_page = pages[next_page_index]
                    if next_page and next_page.strip():  # 确保下一页有内容
                        next_elements = self.parse_html_to_elements(next_page)
                        next_height = sum(e.height for e in next_elements)
                        
                        # 如果合并后不超过最大高度，则合并
                        if current_height + next_height <= self.content_height:
                            optimized.append(current_page + next_page)
                            i += 2  # 跳过下一页
                            continue
            
            optimized.append(current_page)
            i += 1
        
        # 如果优化后没有页面，至少返回一个页面
        return optimized if optimized else ['']
    
    def debug_pagination(self, html_content: str) -> List[dict]:
        """调试分页，返回详细信息"""
        elements = self.parse_html_to_elements(html_content)
        pages_info = []
        
        pages = self.paginate(html_content)
        for i, page in enumerate(pages, 1):
            page_elements = self.parse_html_to_elements(page)
            total_height = sum(e.height for e in page_elements)
            
            pages_info.append({
                'page_num': i,
                'page_size': self.page_size_name,
                'content_dimensions': f"{self.content_width}×{self.content_height}px",
                'elements_count': len(page_elements),
                'total_height': total_height,
                'max_height': self.content_height,
                'fill_rate': f"{(total_height / self.content_height * 100):.1f}%",
                'is_forced_break': (i-1) in self.forced_break_pages,  # 标记是否是强制分页
                'elements': [
                    {
                        'type': e.type,
                        'height': e.height,
                        'text_preview': e.text[:50] + '...' if len(e.text) > 50 else e.text
                    }
                    for e in page_elements
                ]
            })
        
        return pages_info style_manager.py->text/plain-># ============================================
# src/utils/style_manager.py
# ============================================
from typing import Dict, Any, Tuple
from dataclasses import dataclass
import colorsys

@dataclass
class ThemeConfig:
    """主题配置"""
    name: str
    primary_color: str
    secondary_color: str
    text_color: str
    background: str
    font_family: str
    heading_font: str
    code_font: str
    accent_color: str = ""  # 强调色
    link_color: str = ""    # 链接色
    
class StyleManager:
    """样式管理器 - 扩展版"""
    
    # 预设主题 - 12种风格
    THEMES = {
        # 社交媒体风格
        "xiaohongshu": ThemeConfig(
            name="小红书经典",
            primary_color="#FF2442",
            secondary_color="#FF6B6B",
            text_color="#2c3e50",
            background="linear-gradient(135deg, #ffeef8 0%, #ffe0f0 100%)",
            font_family='-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Helvetica Neue", sans-serif',
            code_font='"JetBrains Mono", "Cascadia Code", "Consolas", monospace',
            accent_color="#FFB6C1",
            link_color="#FF69B4"
        ),
        
        "instagram": ThemeConfig(
            name="Instagram渐变",
            primary_color="#E4405F",
            secondary_color="#BC2A8D",
            text_color="#262626",
            background="linear-gradient(45deg, #F9ED69 0%, #EE2A7B 50%, #6228D7 100%)",
            font_family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
            heading_font='"Segoe UI", Roboto, sans-serif',
            code_font='"Monaco", "Courier New", monospace',
            accent_color="#FCAF45",
            link_color="#833AB4"
        ),
        
        "wechat": ThemeConfig(
            name="微信简约",
            primary_color="#07C160",
            secondary_color="#4CAF50",
            text_color="#353535",
            background="linear-gradient(180deg, #F7F7F7 0%, #FFFFFF 100%)",
            font_family='"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Microsoft YaHei", sans-serif',
            code_font='"SF Mono", "Monaco", "Inconsolata", monospace',
            accent_color="#95EC69",
            link_color="#576B95"
        ),
        
        "douyin": ThemeConfig(
            name="抖音酷黑",
            primary_color="#FE2C55",
            secondary_color="#25F4EE",
            text_color="#FFFFFF",
            background="linear-gradient(135deg, #000000 0%, #161823 100%)",
            font_family='"PingFang SC", "Helvetica Neue", Arial, sans-serif',
            heading_font='"PingFang SC", "Helvetica Neue", sans-serif',
            code_font='"Fira Code", "Source Code Pro", monospace',
            accent_color="#00F2EA",
            link_color="#FE2C55"
        ),
        
        # 知识平台风格
        "zhihu": ThemeConfig(
            name="知乎蓝",
            primary_color="#0084FF",
            secondary_color="#1890FF",
            text_color="#1A1A1A",
            background="linear-gradient(180deg, #FFFFFF 0%, #F6F6F6 100%)",
            font_family='"PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Helvetica Neue", sans-serif',
            code_font='"Source Code Pro", "Consolas", monospace',
            accent_color="#5BBCFF",
            link_color="#175199"
        ),
        
        "notion": ThemeConfig(
            name="Notion极简",
            primary_color="#000000",
            secondary_color="#2F3437",
            text_color="#37352F",
            background="linear-gradient(180deg, #FFFFFF 0%, #FAFAFA 100%)",
            font_family='"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            heading_font='"Inter", -apple-system, sans-serif',
            code_font='"SFMono-Regular", "Consolas", "Liberation Mono", monospace',
            accent_color="#EB5757",
            link_color="#0070F3"
        ),
        
        # 优雅风格
        "elegant_purple": ThemeConfig(
            name="优雅紫",
            primary_color="#6B46C1",
            secondary_color="#9333EA",
            text_color="#1F2937",
            background="linear-gradient(135deg, #F9FAFB 0%, #F3E8FF 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Playfair Display", "PingFang SC", serif',
            code_font='"JetBrains Mono", "Cascadia Code", monospace',
            accent_color="#A78BFA",
            link_color="#7C3AED"
        ),
        
        "ocean_blue": ThemeConfig(
            name="海洋蓝",
            primary_color="#0EA5E9",
            secondary_color="#06B6D4",
            text_color="#0F172A",
            background="linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 50%, #BAE6FD 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Fira Code", "Consolas", monospace',
            accent_color="#38BDF8",
            link_color="#0284C7"
        ),
        
        "sunset_orange": ThemeConfig(
            name="日落橙",
            primary_color="#F97316",
            secondary_color="#FB923C",
            text_color="#1C1917",
            background="linear-gradient(135deg, #FFF7ED 0%, #FED7AA 50%, #FDBA74 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Source Code Pro", "Monaco", monospace',
            accent_color="#FCD34D",
            link_color="#EA580C"
        ),
        
        "forest_green": ThemeConfig(
            name="森林绿",
            primary_color="#059669",
            secondary_color="#10B981",
            text_color="#064E3B",
            background="linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 50%, #A7F3D0 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"JetBrains Mono", monospace',
            accent_color="#34D399",
            link_color="#047857"
        ),
        
        # 深色主题
        "dark_mode": ThemeConfig(
            name="深色模式",
            primary_color="#00E0FF",
            secondary_color="#0096FF",
            text_color="#E0E6ED",
            background="linear-gradient(135deg, #0F0F1E 0%, #1A1A2E 50%, #16213E 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Fira Code", "JetBrains Mono", monospace',
            accent_color="#00F0FF",
            link_color="#00B8D4"
        ),
        
        "midnight": ThemeConfig(
            name="午夜紫",
            primary_color="#B794F4",
            secondary_color="#9F7AEA",
            text_color="#E9D8FD",
            background="linear-gradient(135deg, #1A202C 0%, #2D3748 50%, #4A5568 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Cascadia Code", "Fira Code", monospace',
            accent_color="#D6BCFA",
            link_color="#B794F4"
        )
    }
    
    def __init__(self, theme: str = "xiaohongshu"):
        self.current_theme = theme
        self.custom_styles = {}
        
    def get_theme(self, theme_name: str = None) -> ThemeConfig:
        """获取主题配置"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.THEMES.get(theme_name, self.THEMES["xiaohongshu"])
    
    def get_theme_list(self) -> list:
        """获取所有主题列表"""
        return list(self.THEMES.keys())
    
    def get_theme_display_names(self) -> Dict[str, str]:
        """获取主题显示名称"""
        return {key: theme.name for key, theme in self.THEMES.items()}
    
    def set_theme(self, theme_name: str):
        """设置当前主题"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """十六进制颜色转RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """RGB转十六进制"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def lighten_color(self, hex_color: str, amount: float) -> str:
        """使颜色变浅（amount: 0-1）"""
        r, g, b = self.hex_to_rgb(hex_color)
        # 转换为HSL
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        # 增加亮度
        l = min(1.0, l + (1 - l) * amount)
        # 转回RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return self.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def darken_color(self, hex_color: str, amount: float) -> str:
        """使颜色变深（amount: 0-1）"""
        r, g, b = self.hex_to_rgb(hex_color)
        # 转换为HSL
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        # 降低亮度
        l = max(0.0, l * (1 - amount))
        # 转回RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return self.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def add_alpha(self, hex_color: str, alpha: float) -> str:
        """添加透明度（返回rgba格式）"""
        r, g, b = self.hex_to_rgb(hex_color)
        return f"rgba({r}, {g}, {b}, {alpha})"
    
    def generate_css(self, theme_name: str = None, font_size: int = 18) -> str:
        """生成主题CSS"""
        theme = self.get_theme(theme_name)
        
        # 生成派生颜色
        primary_light = self.lighten_color(theme.primary_color, 0.9)
        primary_dark = self.darken_color(theme.primary_color, 0.2)
        secondary_light = self.lighten_color(theme.secondary_color, 0.9)
        
        # 检查是否为深色主题
        is_dark = theme_name in ["dark_mode", "midnight", "douyin"]
        
        return f"""
        /* 主题: {theme.name} */
        :root {{
            --primary-color: {theme.primary_color};
            --secondary-color: {theme.secondary_color};
            --accent-color: {theme.accent_color or theme.secondary_color};
            --text-color: {theme.text_color};
            --link-color: {theme.link_color or theme.primary_color};
            --font-family: {theme.font_family};
            --heading-font: {theme.heading_font};
            --code-font: {theme.code_font};
            --primary-light: {primary_light};
            --primary-dark: {primary_dark};
            --secondary-light: {secondary_light};
            --base-font-size: {font_size}px;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: var(--font-family);
            background: {theme.background};
            color: var(--text-color);
            font-size: var(--base-font-size);
            line-height: 1.85;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* 标题样式 */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--heading-font);
            color: var(--primary-color);
            font-weight: 700;
            letter-spacing: -0.02em;
        }}
        
        h1 {{
            font-size: calc(var(--base-font-size) + 16px);
            margin-bottom: 28px;
            padding-bottom: 16px;
            border-bottom: 3px solid {self.add_alpha(theme.primary_color, 0.2)};
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        h2 {{
            font-size: calc(var(--base-font-size) + 10px);
            margin-top: 38px;
            margin-bottom: 22px;
            position: relative;
            padding-left: 20px;
        }}
        
        h2::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 5px;
            height: 24px;
            background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
            border-radius: 3px;
            box-shadow: 0 2px 8px {self.add_alpha(theme.primary_color, 0.3)};
        }}
        
        h3 {{
            font-size: calc(var(--base-font-size) + 5px);
            margin-top: 30px;
            margin-bottom: 18px;
            color: {theme.text_color if not is_dark else theme.secondary_color};
        }}
        
        /* 段落样式 */
        p {{
            margin-bottom: 22px;
            font-size: var(--base-font-size);
            color: var(--text-color);
            text-align: justify;
            line-height: 1.85;
        }}
        
        /* 强调样式 */
        strong {{
            color: var(--primary-color);
            font-weight: 600;
            background: linear-gradient(180deg, transparent 70%, {self.add_alpha(theme.primary_color, 0.2)} 70%);
            padding: 0 4px;
            border-radius: 2px;
        }}
        
        em {{
            font-style: italic;
            color: {self.darken_color(theme.text_color, 0.2) if not is_dark else self.lighten_color(theme.text_color, 0.2)};
        }}
        
        /* 列表样式 */
        ul, ol {{
            margin: 24px 0;
            padding-left: 38px;
        }}
        
        li {{
            margin-bottom: 16px;
            font-size: var(--base-font-size);
            color: var(--text-color);
            line-height: 1.85;
            position: relative;
        }}
        
        ul li::marker {{
            color: var(--primary-color);
            font-size: calc(var(--base-font-size) + 2px);
        }}
        
        ol li::marker {{
            color: var(--primary-color);
            font-weight: 600;
        }}
        
        /* 引用样式 */
        blockquote {{
            border-left: 4px solid var(--primary-color);
            margin: 28px 0;
            padding: 20px 28px;
            background: {self.add_alpha(theme.primary_color, 0.05) if not is_dark else self.add_alpha(theme.primary_color, 0.1)};
            border-radius: 10px;
            position: relative;
            box-shadow: 0 4px 15px {self.add_alpha(theme.primary_color, 0.1)};
        }}
        
        blockquote::before {{
            content: '"';
            position: absolute;
            top: -10px;
            left: 24px;
            font-size: 48px;
            color: {self.add_alpha(theme.primary_color, 0.3)};
            font-family: Georgia, serif;
            font-weight: bold;
        }}
        
        blockquote p {{
            color: {self.darken_color(theme.text_color, 0.1) if not is_dark else self.lighten_color(theme.text_color, 0.1)};
            font-style: italic;
            margin-bottom: 0;
            font-size: calc(var(--base-font-size) - 1px);
        }}
        
        /* 行内代码 */
        code {{
            background: {self.add_alpha(theme.primary_color, 0.1)};
            padding: 4px 10px;
            border-radius: 6px;
            font-family: var(--code-font);
            font-size: calc(var(--base-font-size) - 2px);
            color: {theme.primary_color if not is_dark else theme.accent_color};
            font-weight: 500;
            border: 1px solid {self.add_alpha(theme.primary_color, 0.2)};
        }}
        
        /* 代码块 */
        pre {{
            background: {('#1e1e1e' if not is_dark else '#0a0a0f')};
            color: #d4d4d4;
            padding: 26px;
            border-radius: 12px;
            overflow-x: auto;
            margin: 28px 0;
            box-shadow: 0 8px 24px {self.add_alpha('#000000', 0.15)};
            position: relative;
            border: 1px solid {self.add_alpha(theme.primary_color, 0.2)};
        }}
        
        pre::before {{
            content: "CODE";
            position: absolute;
            top: 12px;
            right: 16px;
            font-size: 11px;
            color: {self.add_alpha(theme.text_color, 0.5)};
            font-weight: 600;
            letter-spacing: 1px;
            font-family: var(--font-family);
        }}
        
        pre code {{
            background: none;
            color: #d4d4d4;
            padding: 0;
            font-size: calc(var(--base-font-size) - 3px);
            line-height: 1.7;
            border: none;
        }}
        
        /* 表格样式 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 28px 0;
            font-size: calc(var(--base-font-size) - 1px);
            box-shadow: 0 4px 15px {self.add_alpha(theme.primary_color, 0.08)};
            border-radius: 10px;
            overflow: hidden;
        }}
        
        th {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 15px 20px;
            text-align: left;
            font-weight: 600;
            font-size: calc(var(--base-font-size) - 1px);
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 15px 20px;
            border-bottom: 1px solid {self.add_alpha(theme.text_color, 0.1)};
            color: var(--text-color);
        }}
        
        tr:nth-child(even) {{
            background: {self.add_alpha(theme.primary_color, 0.03)};
        }}
        
        tr:hover {{
            background: {self.add_alpha(theme.primary_color, 0.08)};
            transition: background 0.3s ease;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        /* 分隔线 */
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, 
                transparent, 
                {self.add_alpha(theme.primary_color, 0.3)} 20%, 
                {self.add_alpha(theme.primary_color, 0.3)} 80%, 
                transparent);
            margin: 38px 0;
            position: relative;
        }}
        
        hr::after {{
            content: "✦";
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background: {theme.background.split('(')[0] + '(180deg, #FFFFFF 0%, #FFFFFF 100%)' if 'gradient' in theme.background else '#FFFFFF'};
            color: var(--primary-color);
            padding: 0 10px;
            font-size: 20px;
        }}
        
        /* 链接样式 */
        a {{
            color: var(--link-color);
            text-decoration: none;
            border-bottom: 2px solid {self.add_alpha(theme.link_color or theme.primary_color, 0.3)};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            padding-bottom: 1px;
            position: relative;
        }}
        
        a:hover {{
            color: var(--secondary-color);
            border-bottom-color: var(--secondary-color);
            background: {self.add_alpha(theme.primary_color, 0.08)};
            padding: 2px 6px;
            margin: -2px -6px;
            border-radius: 4px;
        }}
        
        /* 动画效果 */
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .content > * {{
            animation: fadeIn 0.5s ease-out backwards;
        }}
        
        .content > *:nth-child(1) {{ animation-delay: 0.05s; }}
        .content > *:nth-child(2) {{ animation-delay: 0.1s; }}
        .content > *:nth-child(3) {{ animation-delay: 0.15s; }}
        .content > *:nth-child(4) {{ animation-delay: 0.2s; }}
        .content > *:nth-child(5) {{ animation-delay: 0.25s; }}
        
        /* 自定义滚动条 */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {self.add_alpha(theme.text_color, 0.05)};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, var(--secondary-color), var(--primary-color));
        }}
        """
    
    def get_export_settings(self, theme_name: str = None) -> Dict[str, Any]:
        """获取导出设置"""
        theme = self.get_theme(theme_name)
        
        return {
            "theme_name": theme.name,
            "page_width": 1080,
            "page_height": 1440,
            "padding": {
                "top": 45,
                "bottom": 45,
                "left": 40,
                "right": 40
            },
            "font_size": 16,
            "line_height": 1.8,
            "paragraph_spacing": 20,
            "image_quality": 100,
            "format": "PNG",
            "colors": {
                "primary": theme.primary_color,
                "secondary": theme.secondary_color,
                "text": theme.text_color,
                "background": theme.background
            }
        }
    
    def apply_custom_styles(self, styles: Dict[str, str]):
        """应用自定义样式"""
        self.custom_styles.update(styles)
    
    def get_combined_css(self, theme_name: str = None, font_size: int = 18) -> str:
        """获取组合的CSS（主题 + 自定义）"""
        base_css = self.generate_css(theme_name, font_size)
        
        if self.custom_styles:
            custom_css = "\n/* 自定义样式 */\n"
            for selector, rules in self.custom_styles.items():
                custom_css += f"{selector} {{\n{rules}\n}}\n"
            return base_css + custom_css
        
        return base_css html_generator.py->text/plain-># ============================================
# src/core/html_generator.py
# ============================================
from pathlib import Path
from typing import Optional
from src.utils.style_manager import StyleManager

class HTMLGenerator:
    def __init__(self, font_size: int = 18, page_size: str = "medium", theme: str = "xiaohongshu"):
        self.resource_path = Path(__file__).parent.parent / "resources"
        self.base_font_size = font_size  # 基础字体大小，默认18px
        
        # 页面尺寸配置
        self.page_sizes = {
            "small": {"width": 720, "height": 960},
            "medium": {"width": 1080, "height": 1440},
            "large": {"width": 1440, "height": 1920}
        }
        self.current_size = page_size
        self.page_width = self.page_sizes[page_size]["width"]
        self.page_height = self.page_sizes[page_size]["height"]
        
        # 样式管理器
        self.style_manager = StyleManager(theme)
        self.current_theme = theme
        
    def set_page_size(self, size: str):
        """设置页面尺寸"""
        if size in self.page_sizes:
            self.current_size = size
            self.page_width = self.page_sizes[size]["width"]
            self.page_height = self.page_sizes[size]["height"]
    
    def set_theme(self, theme: str):
        """设置主题"""
        self.current_theme = theme
        self.style_manager.set_theme(theme)
    
    def set_font_size(self, size: int):
        """设置基础字体大小"""
        self.base_font_size = size
        
    def generate(self, content: str, page_num: int = 0, total_pages: int = 0) -> str:
        """
        生成完整的 HTML 页面
        
        Args:
            content: HTML内容
            page_num: 当前页码（0表示不显示）
            total_pages: 总页数
        """
        # 生成主题CSS
        theme_css = self.style_manager.generate_css(self.current_theme, self.base_font_size)
        
        # 生成页面特定CSS
        page_css = self.get_page_css()
        
        # 获取JavaScript
        js = self.get_js()
        
        # 生成页码信息（如果需要）
        page_info = ""
        if page_num > 0 and total_pages > 1:
            page_info = f"""
            <div class="page-info">
                <span class="page-number">{page_num}</span>
                <span class="page-separator">/</span>
                <span class="page-total">{total_pages}</span>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小红书卡片 - {self.style_manager.get_theme().name}</title>
    <style>
        {theme_css}
        {page_css}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="content" id="content">
                {content}
            </div>
            {page_info}
        </div>
    </div>
    <script>{js}</script>
</body>
</html>
"""
        return html
    
    def get_page_css(self) -> str:
        """获取页面布局CSS"""
        theme = self.style_manager.get_theme()
        
        # 检查是否为深色主题
        is_dark = self.current_theme in ["dark_mode", "midnight", "douyin"]
        
        return f"""
        /* 页面布局 */
        html, body {{
            width: {self.page_width}px;
            height: {self.page_height}px;
            overflow: hidden !important;
            margin: 0;
            padding: 0;
        }}
        
        .container {{
            width: {self.page_width}px;
            height: {self.page_height}px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 0;
        }}
        
        .card {{
            width: 100%;
            height: 100%;
            background: {'rgba(255, 255, 255, 0.98)' if not is_dark else 'rgba(20, 20, 35, 0.98)'};
            border-radius: 20px;
            box-shadow: 0 20px 60px {self.style_manager.add_alpha(theme.primary_color, 0.15)},
                        0 10px 30px {self.style_manager.add_alpha('#000000', 0.1)};
            overflow: hidden;
            position: relative;
        }}
        
        .content {{
            padding: 50px 45px 70px 45px;
            color: var(--text-color);
            line-height: 1.85;
            height: 100%;
            overflow: hidden !important;
            position: relative;
        }}
        
        /* 页码信息 */
        .page-info {{
            position: absolute;
            bottom: 20px;
            right: 30px;
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 8px 16px;
            background: {self.style_manager.add_alpha(theme.primary_color, 0.1)};
            border-radius: 20px;
            border: 1px solid {self.style_manager.add_alpha(theme.primary_color, 0.2)};
        }}
        
        .page-number {{
            font-weight: 700;
            color: var(--primary-color);
            font-size: 14px;
        }}
        
        .page-separator {{
            color: {self.style_manager.add_alpha(theme.text_color, 0.4)};
            font-size: 12px;
        }}
        
        .page-total {{
            color: {self.style_manager.add_alpha(theme.text_color, 0.6)};
            font-size: 14px;
        }}
        
        /* 装饰元素 */
        .card::before {{
            content: "";
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, {self.style_manager.add_alpha(theme.primary_color, 0.1)} 0%, transparent 70%);
            pointer-events: none;
        }}
        
        .card::after {{
            content: "";
            position: absolute;
            bottom: -50%;
            left: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, {self.style_manager.add_alpha(theme.secondary_color, 0.1)} 0%, transparent 70%);
            pointer-events: none;
        }}
        
        /* 响应式图片 */
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            margin: 20px 0;
            box-shadow: 0 8px 24px {self.style_manager.add_alpha('#000000', 0.1)};
        }}
        
        /* 隐藏滚动条 */
        ::-webkit-scrollbar {{
            display: none !important;
        }}
        
        * {{
            scrollbar-width: none !important;
            -ms-overflow-style: none !important;
        }}
        
        /* 打印样式 */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                max-width: 100%;
            }}
            
            .card {{
                box-shadow: none;
                border-radius: 0;
                page-break-inside: avoid;
            }}
            
            .card::before,
            .card::after {{
                display: none;
            }}
        }}

        /* 完全隐藏分页标记 */
        .pagebreak-marker {{
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            visibility: hidden !important;
        }}
        """
    
    def get_js(self) -> str:
        """获取JavaScript代码"""
        return """
        // 页面加载完成后的处理
        document.addEventListener('DOMContentLoaded', function() {
            // 添加淡入动画
            const content = document.getElementById('content');
            if (content) {
                content.style.opacity = '0';
                content.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                setTimeout(() => {
                    content.style.opacity = '1';
                }, 100);
            }
            
            // 图片延迟加载和动画
            const images = document.querySelectorAll('img');
            images.forEach((img, index) => {
                img.loading = 'lazy';
                img.style.opacity = '0';
                img.style.transform = 'translateY(20px)';
                img.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                
                // 图片加载完成后显示
                if (img.complete) {
                    setTimeout(() => {
                        img.style.opacity = '1';
                        img.style.transform = 'translateY(0)';
                    }, 100 * (index + 1));
                } else {
                    img.addEventListener('load', () => {
                        setTimeout(() => {
                            img.style.opacity = '1';
                            img.style.transform = 'translateY(0)';
                        }, 100);
                    });
                }
            });
            
            // 代码块增强
            const codeBlocks = document.querySelectorAll('pre');
            codeBlocks.forEach(block => {
                // 添加语言标识
                const code = block.querySelector('code');
                if (code && code.className) {
                    const lang = code.className.replace('language-', '');
                    if (lang) {
                        block.setAttribute('data-language', lang.toUpperCase());
                    }
                }
            });
            
            // 表格增强
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                // 添加响应式包装
                const wrapper = document.createElement('div');
                wrapper.style.overflowX = 'auto';
                wrapper.style.marginBottom = '20px';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            });
            
            // 确保内容不超出
            function ensureContentFit() {
                const card = document.querySelector('.card');
                const content = document.querySelector('.content');
                if (card && content) {
                    content.style.maxHeight = '100%';
                    content.style.overflow = 'hidden';
                }
            }
            
            ensureContentFit();
            window.addEventListener('resize', ensureContentFit);
        });
        
        // 禁用所有滚动
        window.addEventListener('scroll', function(e) {
            e.preventDefault();
            window.scrollTo(0, 0);
        }, { passive: false });
        
        window.addEventListener('wheel', function(e) {
            e.preventDefault();
        }, { passive: false });
        
        window.addEventListener('touchmove', function(e) {
            e.preventDefault();
        }, { passive: false });
        """ markdown_processor.py->text/plain-># ============================================
# src/core/markdown_processor.py
# ============================================
import markdown
from markdown.extensions import fenced_code, tables
import re
import uuid

class MarkdownProcessor:
    def __init__(self):
        # 只使用必要且稳定的扩展
        self.extensions = [
            'markdown.extensions.fenced_code',  # 代码块
            'markdown.extensions.tables',       # 表格
            'markdown.extensions.nl2br',        # 换行转<br>
            'markdown.extensions.attr_list',    # 属性列表
            'markdown.extensions.def_list',     # 定义列表
            'markdown.extensions.footnotes',    # 脚注
            'markdown.extensions.toc',          # 目录
            'markdown.extensions.sane_lists',   # 改进的列表
            'markdown.extensions.smarty',       # 智能标点
        ]
        
        # 配置扩展
        self.extension_configs = {}
        
    def parse(self, text: str) -> str:
        """解析 Markdown 文本为 HTML"""
        try:
            # 1. 首先处理分页标记，将其转换为特殊的 HTML 标记
            # 这样可以避免 Markdown 解析器干扰
            text = self._process_pagebreaks_before_markdown(text)
            
            # 2. 创建新的 Markdown 实例（避免状态污染）
            md = markdown.Markdown(
                extensions=self.extensions,
                extension_configs=self.extension_configs
            )
            
            # 3. 转换 Markdown 为 HTML
            html = md.convert(text)
            
            # 4. 后处理：添加小红书特色 emoji 支持
            html = self._process_emojis(html)
            
            return html
            
        except Exception as e:
            print(f"Markdown 解析错误: {e}")
            return f"<p style='color: red;'>解析错误: {str(e)}</p>"
    
    def _process_pagebreaks_before_markdown(self, text: str) -> str:
        """
        在 Markdown 解析之前处理分页标记
        直接将 <!-- pagebreak --> 替换为特殊的 HTML div
        """
        # 匹配 HTML 注释形式的分页标记（支持大小写和空格变化）
        pattern = r'<!--\s*pagebreak\s*-->'
        
        # 直接替换为 HTML div（这个 div 不会被 Markdown 解析器改变）
        # 使用一个特殊的类名，确保 paginator.py 能识别
        replacement = '\n\n<div class="pagebreak-marker" data-pagebreak="true"></div>\n\n'
        
        # 执行替换
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _process_emojis(self, html: str) -> str:
        """处理 emoji 表情"""
        # 保持 emoji 原样显示
        return html style_manager.py->text/plain->
### 系统:
我来帮你美化UI界面。我建议采用现代化的**毛玻璃风格（Glassmorphism）+ 极光渐变**设计，这种风格在2024-2025年非常流行，视觉效果出色。

由于UI美化涉及多个文件的样式调整，变动较大，我会给你提供完整的修改代码。

## 主要美化方向：
1. **毛玻璃效果** - 半透明模糊背景，层次感强
2. **极光渐变** - 动态渐变背景，视觉冲击力强  
3. **霓虹光效** - 按钮和边框发光效果
4. **动画效果** - 平滑过渡和悬浮动画
5. **暗色主题** - 护眼且高级

让我为你重新设计主要的UI文件： 代码
```python
# ============================================
# src/ui/main_window.py - 极光毛玻璃风格
# ============================================
from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QToolBar, QSplitter, QPushButton,
                               QFileDialog, QMessageBox, QStatusBar, QLabel,
                               QGraphicsDropShadowEffect, QComboBox, QFrame)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QAction, QIcon, QColor, QLinearGradient, QPainter, QBrush
from src.ui.editor_widget import EditorWidget
from src.ui.preview_widget import PreviewWidget
from src.utils.style_manager import StyleManager

class AuroraBackground(QWidget):
    """极光渐变背景组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_offset = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_gradient)
        self.animation_timer.start(50)  # 20fps动画
        
    def update_gradient(self):
        self.gradient_offset = (self.gradient_offset + 1) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 创建动态极光渐变
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        
        # 基于时间偏移的动态颜色
        hue1 = (180 + self.gradient_offset) % 360
        hue2 = (280 + self.gradient_offset) % 360
        hue3 = (320 + self.gradient_offset) % 360
        
        color1 = QColor.fromHsv(hue1, 180, 60)
        color2 = QColor.fromHsv(hue2, 200, 80)
        color3 = QColor.fromHsv(hue3, 160, 70)
        
        gradient.setColorAt(0, color1)
        gradient.setColorAt(0.3, color2)
        gradient.setColorAt(0.6, QColor(25, 25, 60))
        gradient.setColorAt(1, color3)
        
        painter.fillRect(self.rect(), gradient)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 先创建自动更新计时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_preview)
        self.update_timer.setInterval(300)  # 300ms延迟
        
        # 初始化样式管理器
        self.style_manager = StyleManager()
        
        # 然后初始化UI
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✨ 小红书 Markdown 编辑器 - Aurora Edition")
        self.setGeometry(100, 100, 1700, 950)
        
        # 设置窗口无边框（可选）
        # self.setWindowFlags(Qt.FramelessWindowHint)
        
        # 创建主容器
        main_container = QWidget()
        self.setCentralWidget(main_container)
        
        # 创建极光背景
        self.aurora_bg = AuroraBackground(main_container)
        
        # 主布局
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 应用全局样式
        self.setStyleSheet(self.get_global_styles())
        
        # 创建顶部工具栏
        toolbar_container = self.create_toolbar()
        main_layout.addWidget(toolbar_container)
        
        # 创建内容区域
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.setObjectName("mainSplitter")
        
        # 创建编辑器和预览组件
        self.editor = EditorWidget()
        self.preview = PreviewWidget()
        
        # 为组件添加玻璃容器
        editor_container = self.create_glass_container(self.editor, "📝 Markdown Editor")
        preview_container = self.create_glass_container(self.preview, "👀 Live Preview")
        
        # 添加到分割器
        splitter.addWidget(editor_container)
        splitter.addWidget(preview_container)
        splitter.setSizes([850, 850])
        
        content_layout.addWidget(splitter)
        main_layout.addWidget(content_area, 1)
        
        # 创建底部状态栏
        self.create_status_bar()
        
        # 初始更新
        self.update_preview()
        self.update_char_count()
        
        # 确保背景在最底层
        self.aurora_bg.lower()
        
    def create_glass_container(self, widget, title):
        """创建毛玻璃容器"""
        container = QFrame()
        container.setObjectName("glassContainer")
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题栏
        title_bar = QFrame()
        title_bar.setObjectName("glassTitleBar")
        title_bar.setFixedHeight(45)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 20, 0)
        
        title_label = QLabel(title)
        title_label.setObjectName("glassTitle")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # 添加组件
        layout.addWidget(title_bar)
        layout.addWidget(widget, 1)
        
        # 添加发光效果
        self.add_glow_effect(container)
        
        return container
        
    def create_toolbar(self):
        """创建毛玻璃工具栏"""
        toolbar_container = QFrame()
        toolbar_container.setObjectName("toolbarContainer")
        toolbar_container.setFixedHeight(70)
        
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(25, 15, 25, 15)
        toolbar_layout.setSpacing(15)
        
        # Logo 和标题
        logo_label = QLabel("✨")
        logo_label.setObjectName("logoLabel")
        toolbar_layout.addWidget(logo_label)
        
        app_title = QLabel("Aurora Markdown Editor")
        app_title.setObjectName("appTitle")
        toolbar_layout.addWidget(app_title)
        
        toolbar_layout.addSpacing(40)
        
        # 功能按钮
        self.export_btn = self.create_neon_button("📸 Export", "#00ff88")
        self.export_btn.clicked.connect(self.export_images)
        toolbar_layout.addWidget(self.export_btn)
        
        self.clear_btn = self.create_neon_button("🗑️ Clear", "#ff6b6b")
        self.clear_btn.clicked.connect(self.clear_content)
        toolbar_layout.addWidget(self.clear_btn)
        
        toolbar_layout.addSpacing(20)
        
        # 主题选择器
        theme_label = QLabel("Theme:")
        theme_label.setObjectName("themeLabel")
        toolbar_layout.addWidget(theme_label)
        
        self.theme_selector = QComboBox()
        self.theme_selector.setObjectName("themeSelector")
        self.theme_selector.setFixedWidth(180)
        
        themes = self.style_manager.get_theme_display_names()
        for key, name in themes.items():
            self.theme_selector.addItem(name, key)
        
        self.theme_selector.setCurrentText("小红书经典")
        toolbar_layout.addWidget(self.theme_selector)
        
        toolbar_layout.addStretch()
        
        # 最小化和关闭按钮（如果使用无边框窗口）
        # min_btn = self.create_window_button("－")
        # max_btn = self.create_window_button("□")
        # close_btn = self.create_window_button("✕")
        # toolbar_layout.addWidget(min_btn)
        # toolbar_layout.addWidget(max_btn)
        # toolbar_layout.addWidget(close_btn)
        
        return toolbar_container
        
    def create_neon_button(self, text, color):
        """创建霓虹发光按钮"""
        btn = QPushButton(text)
        btn.setObjectName("neonButton")
        btn.setProperty("neonColor", color)
        
        # 添加发光效果
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setOffset(0, 0)
        glow.setColor(QColor(color))
        btn.setGraphicsEffect(glow)
        
        # 悬浮动画
        btn.enterEvent = lambda e: self.animate_button_hover(btn, True)
        btn.leaveEvent = lambda e: self.animate_button_hover(btn, False)
        
        return btn
        
    def animate_button_hover(self, button, hover):
        """按钮悬浮动画"""
        effect = button.graphicsEffect()
        if effect:
            if hover:
                effect.setBlurRadius(30)
            else:
                effect.setBlurRadius(20)
                
    def create_status_bar(self):
        """创建毛玻璃状态栏"""
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("glassStatusBar")
        self.status_bar.setFixedHeight(40)
        self.setStatusBar(self.status_bar)
        
        # 字数统计
        self.char_count_label = QLabel("Words: 0")
        self.char_count_label.setObjectName("statusLabel")
        
        # 主题信息
        self.theme_info_label = QLabel("Theme: 小红书经典")
        self.theme_info_label.setObjectName("statusLabel")
        
        self.status_bar.addPermanentWidget(self.theme_info_label)
        self.status_bar.addPermanentWidget(self.char_count_label)
        
    def add_glow_effect(self, widget):
        """添加发光效果"""
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setOffset(0, 0)
        glow.setColor(QColor(0, 224, 255, 80))
        widget.setGraphicsEffect(glow)
        
    def get_global_styles(self):
        """获取全局样式表"""
        return """
        /* 全局字体 */
        * {
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
        }
        
        /* 内容区域 */
        #contentArea {
            background: transparent;
        }
        
        /* 毛玻璃容器 */
        #glassContainer {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        #glassTitleBar {
            background: linear-gradient(90deg, 
                rgba(255, 255, 255, 0.1) 0%, 
                rgba(255, 255, 255, 0.05) 100%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        }
        
        #glassTitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 1px;
        }
        
        /* 工具栏 */
        #toolbarContainer {
            background: rgba(20, 20, 40, 0.8);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        #logoLabel {
            font-size: 28px;
        }
        
        #appTitle {
            color: rgba(255, 255, 255, 0.95);
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 2px;
            background: linear-gradient(90deg, #00ff88, #00ffff, #ff00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        #themeLabel {
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            font-weight: 500;
        }
        
        /* 霓虹按钮 */
        #neonButton {
            background: rgba(255, 255, 255, 0.05);
            border: 2px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 10px 25px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 1px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        #neonButton:hover {
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.4);
            transform: translateY(-2px);
        }
        
        #neonButton:pressed {
            transform: translateY(0);
        }
        
        /* 主题选择器 */
        #themeSelector {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 8px 15px;
            border-radius: 15px;
            font-size: 13px;
            font-weight: 500;
        }
        
        #themeSelector:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        #themeSelector::drop-down {
            border: none;
            width: 30px;
        }
        
        #themeSelector::down-arrow {
            image: none;
            border-style: solid;
            border-width: 5px 5px 0 5px;
            border-color: white transparent transparent transparent;
            margin-right: 8px;
        }
        
        #themeSelector QAbstractItemView {
            background: rgba(30, 30, 50, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            selection-background-color: rgba(0, 255, 136, 0.3);
            border-radius: 10px;
            padding: 5px;
        }
        
        #themeSelector QAbstractItemView::item {
            min-height: 35px;
            padding: 8px;
            border-radius: 5px;
        }
        
        #themeSelector QAbstractItemView::item:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        /* 分割器 */
        #mainSplitter::handle {
            background: linear-gradient(180deg,
                rgba(255, 255, 255, 0) 0%,
                rgba(255, 255, 255, 0.2) 50%,
                rgba(255, 255, 255, 0) 100%);
            width: 3px;
        }
        
        #mainSplitter::handle:hover {
            background: linear-gradient(180deg,
                rgba(0, 255, 255, 0) 0%,
                rgba(0, 255, 255, 0.5) 50%,
                rgba(0, 255, 255, 0) 100%);
        }
        
        /* 状态栏 */
        #glassStatusBar {
            background: rgba(20, 20, 40, 0.8);
            backdrop-filter: blur(20px);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.7);
        }
        
        #statusLabel {
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            font-weight: 500;
            padding: 5px 15px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            margin: 0 5px;
        }
        
        /* 滚动条美化 */
        QScrollBar:vertical {
            background: rgba(255, 255, 255, 0.03);
            width: 12px;
            border-radius: 6px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical {
            background: linear-gradient(180deg,
                rgba(0, 255, 255, 0.3) 0%,
                rgba(255, 0, 255, 0.3) 100%);
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: linear-gradient(180deg,
                rgba(0, 255, 255, 0.5) 0%,
                rgba(255, 0, 255, 0.5) 100%);
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            background: rgba(255, 255, 255, 0.03);
            height: 12px;
            border-radius: 6px;
            margin: 2px;
        }
        
        QScrollBar::handle:horizontal {
            background: linear-gradient(90deg,
                rgba(0, 255, 255, 0.3) 0%,
                rgba(255, 0, 255, 0.3) 100%);
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: linear-gradient(90deg,
                rgba(0, 255, 255, 0.5) 0%,
                rgba(255, 0, 255, 0.5) 100%);
        }
        
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        """
        
    def resizeEvent(self, event):
        """窗口大小改变时调整背景"""
        super().resizeEvent(event)
        if hasattr(self, 'aurora_bg'):
            self.aurora_bg.resize(self.size())
            
    def setup_connections(self):
        """设置信号连接"""
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.scrollChanged.connect(self.preview.handle_scroll)
        self.preview.pageChanged.connect(self.on_page_changed)
        self.theme_selector.currentIndexChanged.connect(self.on_theme_changed)
        
        if hasattr(self.preview, 'sizeChanged'):
            self.preview.sizeChanged.connect(self.on_size_changed)
    
    def on_text_changed(self):
        """文本改变时启动计时器"""
        self.update_timer.stop()
        self.update_timer.start()
        self.update_char_count()
        
    def update_preview(self):
        """更新预览"""
        self.update_timer.stop()
        markdown_text = self.editor.get_text()
        self.preview.update_content(markdown_text)
        
    def update_char_count(self):
        """更新字数统计"""
        text = self.editor.get_text()
        char_count = len(text.replace(" ", "").replace("\n", ""))
        self.char_count_label.setText(f"Words: {char_count}")
        
    def on_page_changed(self, current, total):
        """页码改变时更新状态栏"""
        if total > 1:
            self.status_bar.showMessage(f"Page: {current}/{total}", 2000)
            
    def on_theme_changed(self, index):
        """处理主题改变"""
        theme_key = self.theme_selector.currentData()
        if theme_key:
            self.preview.change_theme(theme_key)
            theme_name = self.theme_selector.currentText()
            self.theme_info_label.setText(f"Theme: {theme_name}")
            self.status_bar.showMessage(f"Switched to: {theme_name}", 3000)
            
    def on_size_changed(self, size):
        """处理尺寸改变"""
        size_display = {
            "small": "Small (720×960)",
            "medium": "Medium (1080×1440)",
            "large": "Large (1440×1920)"
        }
        display_name = size_display.get(size, size)
        self.status_bar.showMessage(f"Size: {display_name}", 3000)
        
    def clear_content(self):
        """清空内容"""
        reply = QMessageBox.question(
            self, "Clear Content",
            "Are you sure you want to clear all content?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.editor.editor.clear()
            self.status_bar.showMessage("Content cleared", 2000)
            
    def export_images(self):
        """导出图片"""
        if not self.editor.get_text().strip():
            QMessageBox.warning(
                self, "Warning",
                "No content to export. Please enter some text first.",
                QMessageBox.Ok
            )
            return
        
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Export Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            try:
                theme_name = self.theme_selector.currentText()
                self.status_bar.showMessage(f"Exporting images (Theme: {theme_name})...", 0)
                self.preview.export_pages(folder)
                
                QMessageBox.information(
                    self, "Export Successful",
                    f"Images exported successfully to:\n{folder}\n\nTheme: {theme_name}",
                    QMessageBox.Ok
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self, "Export Failed",
                    f"Error during export:\n{str(e)}",
                    QMessageBox.Ok
                )
                self.status_bar.showMessage("Export failed", 3000)
```
 代码
```python
# ============================================
# src/ui/editor_widget.py - 毛玻璃风格编辑器
# ============================================
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLabel, QFrame, QHBoxLayout
from PySide6.QtGui import QFont, QTextOption, QPalette, QColor, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtCore import Signal, Qt, QRegularExpression

class MarkdownHighlighter(QSyntaxHighlighter):
    """Markdown 语法高亮器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        # 标题
        heading_format = QTextCharFormat()
        heading_format.setForeground(QColor(0, 255, 136))
        heading_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegularExpression(r'^#{1,6}\s.*'), heading_format))
        
        # 粗体
        bold_format = QTextCharFormat()
        bold_format.setForeground(QColor(255, 179, 71))
        bold_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegularExpression(r'\*\*[^\*]+\*\*'), bold_format))
        
        # 斜体
        italic_format = QTextCharFormat()
        italic_format.setForeground(QColor(255, 179, 71))
        italic_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r'\*[^\*]+\*'), italic_format))
        
        # 代码块
        code_format = QTextCharFormat()
        code_format.setForeground(QColor(139, 233, 253))
        code_format.setFontFamily("Cascadia Code, Consolas, monospace")
        self.highlighting_rules.append((QRegularExpression(r'`[^`]+`'), code_format))
        
        # 链接
        link_format = QTextCharFormat()
        link_format.setForeground(QColor(189, 147, 249))
        link_format.setFontUnderline(True)
        self.highlighting_rules.append((QRegularExpression(r'\[([^\]]+)\]\(([^\)]+)\)'), link_format))
        
        # 列表
        list_format = QTextCharFormat()
        list_format.setForeground(QColor(255, 121, 198))
        self.highlighting_rules.append((QRegularExpression(r'^\s*[\*\-\+]\s'), list_format))
        self.highlighting_rules.append((QRegularExpression(r'^\s*\d+\.\s'), list_format))
        
        # 引用
        quote_format = QTextCharFormat()
        quote_format.setForeground(QColor(98, 114, 164))
        quote_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r'^>\s.*'), quote_format))
        
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class EditorWidget(QWidget):
    textChanged = Signal()
    scrollChanged = Signal(float)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 编辑器容器
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(1, 1, 1, 1)
        container_layout.setSpacing(0)
        
        # 创建编辑器
        self.editor = QTextEdit()
        self.setup_editor()
        
        # 添加
```

### 用户:
Continue
### 系统:
代码
```python
# ============================================
# src/ui/preview_widget.py - 毛玻璃风格预览（样式修改部分）
# ============================================

# 注意：这里只展示需要修改的样式相关方法
# 其他功能代码保持不变

def get_button_style(self) -> str:
    """获取按钮样式 - 毛玻璃风格"""
    return """
        QPushButton {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 0.95);
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 13px;
            letter-spacing: 0.5px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        QPushButton:hover {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.5);
            color: #00ff88;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
        }
        
        QPushButton:pressed {
            background: rgba(0, 255, 136, 0.2);
            transform: translateY(0);
        }
        
        QPushButton:disabled {
            background: rgba(255, 255, 255, 0.02);
            border-color: rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.3);
        }
    """

def get_combobox_style(self) -> str:
    """获取下拉框样式 - 毛玻璃风格"""
    return """
        QComboBox {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 0.95);
            padding: 8px 15px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
            letter-spacing: 0.3px;
        }
        
        QComboBox:hover {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.3);
        }
        
        QComboBox::drop-down {
            border: none;
            width: 25px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-style: solid;
            border-width: 5px 5px 0 5px;
            border-color: rgba(255, 255, 255, 0.7) transparent transparent transparent;
            margin-right: 5px;
        }
        
        QComboBox QAbstractItemView {
            background: rgba(30, 30, 50, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            selection-background-color: rgba(0, 255, 136, 0.3);
            outline: none;
            padding: 5px;
            border-radius: 10px;
        }
        
        QComboBox QAbstractItemView::item {
            min-height: 35px;
            padding: 8px 12px;
            border-radius: 5px;
            margin: 2px 4px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        QComboBox QAbstractItemView::item:selected {
            background: rgba(0, 255, 136, 0.3);
            color: white;
        }
    """

def get_radio_style(self) -> str:
    """获取单选按钮样式 - 毛玻璃风格"""
    return """
        QRadioButton {
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            spacing: 8px;
            padding: 5px;
        }
        
        QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.05);
        }
        
        QRadioButton::indicator:hover {
            border-color: rgba(0, 255, 136, 0.5);
            background: rgba(0, 255, 136, 0.1);
        }
        
        QRadioButton::indicator:checked {
            background: qradialgradient(
                cx: 0.5, cy: 0.5, radius: 0.5,
                fx: 0.5, fy: 0.5,
                stop: 0 #00ff88,
                stop: 0.6 #00ff88,
                stop: 0.7 transparent
            );
            border-color: #00ff88;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
        }
        
        QRadioButton:checked {
            color: #00ff88;
        }
    """

def create_title_bar(self):
    """创建标题栏 - 毛玻璃风格"""
    title_bar = QFrame()
    title_bar.setFixedHeight(50)
    title_bar.setStyleSheet("""
        QFrame {
            background: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
    """)
    
    title_layout = QHBoxLayout(title_bar)
    title_layout.setContentsMargins(20, 5, 20, 5)
    title_layout.setSpacing(15)
    
    # 标题
    title = QLabel("👀 Live Preview")
    title.setStyleSheet("""
        QLabel {
            color: rgba(255, 255, 255, 0.95);
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 1px;
            background: transparent;
        }
    """)
    
    # 尺寸选择标签
    size_label = QLabel("Size:")
    size_label.setStyleSheet("""
        QLabel {
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
            background: transparent;
        }
    """)
    
    # 尺寸选择下拉框
    self.size_selector = QComboBox()
    self.size_selector.addItems(["Small (720×960)", "Medium (1080×1440)", "Large (1440×1920)"])
    self.size_selector.setCurrentIndex(1)
    self.size_selector.setFixedWidth(150)
    self.size_selector.setStyleSheet(self.get_combobox_style())
    
    # 预览模式选择
    mode_label = QLabel("Mode:")
    mode_label.setStyleSheet("""
        QLabel {
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
            background: transparent;
        }
    """)
    
    # 预览模式按钮组
    self.mode_group = QButtonGroup()
    
    self.fit_mode_btn = QRadioButton("Fit Window")
    self.fit_mode_btn.setChecked(True)
    self.fit_mode_btn.setStyleSheet(self.get_radio_style())
    
    self.actual_mode_btn = QRadioButton("Actual Size")
    self.actual_mode_btn.setStyleSheet(self.get_radio_style())
    
    self.mode_group.addButton(self.fit_mode_btn, 0)
    self.mode_group.addButton(self.actual_mode_btn, 1)
    
    # 组装标题栏
    title_layout.addWidget(title)
    title_layout.addSpacing(20)
    title_layout.addWidget(size_label)
    title_layout.addWidget(self.size_selector)
    title_layout.addSpacing(15)
    title_layout.addWidget(mode_label)
    title_layout.addWidget(self.fit_mode_btn)
    title_layout.addWidget(self.actual_mode_btn)
    title_layout.addStretch()
    
    return title_bar

def create_control_bar(self):
    """创建控制栏 - 毛玻璃风格"""
    control_bar = QFrame()
    control_bar.setFixedHeight(60)
    control_bar.setStyleSheet("""
        QFrame {
            background: rgba(20, 20, 40, 0.6);
            backdrop-filter: blur(10px);
            border-bottom-left-radius: 20px;
            border-bottom-right-radius: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
    """)
    
    control_layout = QHBoxLayout(control_bar)
    control_layout.setContentsMargins(20, 12, 20, 12)
    control_layout.setSpacing(15)
    
    # 创建中心控制区容器
    center_controls = QWidget()
    center_layout = QHBoxLayout(center_controls)
    center_layout.setContentsMargins(0, 0, 0, 0)
    center_layout.setSpacing(15)
    
    # 上一页按钮
    self.prev_btn = QPushButton("⬅ Previous")
    self.prev_btn.setFixedSize(110, 36)
    self.prev_btn.setStyleSheet(self.get_button_style())
    
    # 页面信息标签
    self.page_info_label = QLabel("")
    self.page_info_label.setStyleSheet("""
        QLabel {
            color: #00ff88;
            font-size: 14px;
            font-weight: 600;
            padding: 8px 20px;
            background: rgba(0, 255, 136, 0.1);
            border: 1px solid rgba(0, 255, 136, 0.3);
            border-radius: 18px;
            min-width: 100px;
            text-align: center;
        }
    """)
    self.page_info_label.setAlignment(Qt.AlignCenter)
    
    # 下一页按钮
    self.next_btn = QPushButton("Next ➡")
    self.next_btn.setFixedSize(110, 36)
    self.next_btn.setStyleSheet(self.get_button_style())
    
    # 组装中心控制区
    center_layout.addWidget(self.prev_btn)
    center_layout.addWidget(self.page_info_label)
    center_layout.addWidget(self.next_btn)
    
    # 快捷提示
    tips_label = QLabel("💡 Tip: Scroll to navigate • Shift+Scroll for horizontal")
    tips_label.setStyleSheet("""
        QLabel {
            color: rgba(255, 255, 255, 0.5);
            font-size: 11px;
            font-style: italic;
            background: transparent;
        }
    """)
    
    # 组装控制栏
    control_layout.addStretch()
    control_layout.addWidget(center_controls)
    control_layout.addStretch()
    control_layout.addWidget(tips_label)
    
    return control_bar

def create_web_view_container(self):
    """创建WebView容器 - 毛玻璃风格"""
    self.web_container = CustomScrollArea()
    self.web_container.preview_widget = self
    
    self.web_container.setStyleSheet("""
        QScrollArea {
            border: none;
            background: rgba(20, 20, 40, 0.4);
            border-radius: 20px;
        }
        
        QScrollBar:vertical {
            background: rgba(255, 255, 255, 0.03);
            width: 12px;
            border-radius: 6px;
            margin: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: linear-gradient(180deg,
                rgba(0, 255, 255, 0.3) 0%,
                rgba(255, 0, 255, 0.3) 100%);
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: linear-gradient(180deg,
                rgba(0, 255, 255, 0.5) 0%,
                rgba(255, 0, 255, 0.5) 100%);
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            background: rgba(255, 255, 255, 0.03);
            height: 12px;
            border-radius: 6px;
            margin: 4px;
        }
        
        QScrollBar::handle:horizontal {
            background: linear-gradient(90deg,
                rgba(0, 255, 255, 0.3) 0%,
                rgba(255, 0, 255, 0.3) 100%);
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: linear-gradient(90deg,
                rgba(0, 255, 255, 0.5) 0%,
                rgba(255, 0, 255, 0.5) 100%);
        }
        
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """)
    
    # 创建WebView
    self.web_view = QWebEngineView()
    self.web_view.setStyleSheet("""
        QWebEngineView {
            border: none;
            background: transparent;
        }
    """)
    
    # 其他设置保持不变...
    self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, False)
    self.web_view.setFocusPolicy(Qt.StrongFocus)
    
    self.web_container.setWidget(self.web_view)
    self.web_container.setWidgetResizable(True)
    self.web_container.setAlignment(Qt.AlignCenter)
    
    self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
```
 ## 总结

我为你的小红书 Markdown 编辑器设计了一个**极光毛玻璃风格（Aurora Glassmorphism）**的全新UI，主要改进包括：

### 🎨 视觉升级
1. **动态极光背景** - 渐变色彩会缓慢流动，营造科技感
2. **毛玻璃效果** - 半透明模糊背景，层次分明
3. **霓虹发光** - 按钮和边框有柔和的发光效果
4. **语法高亮** - 编辑器支持 Markdown 语法着色

### ✨ 交互优化
1. **悬浮动画** - 鼠标悬停时按钮会上浮并增强发光
2. **平滑过渡** - 所有状态变化都有流畅的动画
3. **视觉反馈** - 操作时有明确的视觉响应

### 🎯 设计特点
- **暗色主题** - 护眼且专业，适合长时间使用
- **极简风格** - 去除冗余装饰，专注内容
- **现代美学** - 符合2024-2025年流行趋势

### 📦 使用方法
1. 替换 `main_window.py` 为新版本
2. 替换 `editor_widget.py` 为新版本  
3. 在 `preview_widget.py` 中更新样式相关方法（get_button_style、get_combobox_style等）

### 🔧 可选调整
如果你想要进一步定制：
- **背景动画速度**：修改 `AuroraBackground` 中的 timer 间隔
- **毛玻璃模糊度**：调整 `backdrop-filter: blur()` 的值
- **发光强度**：修改 `QGraphicsDropShadowEffect` 的 `blurRadius`
- **配色方案**：调整渐变色的 HSV 值

这个设计将让你的编辑器看起来更加专业和现代化，给用户带来愉悦的使用体验！
 preview_widget.py->text/plain-># ============================================
# src/ui/preview_widget.py - 滚轮滚动修复版本
# ============================================
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                               QPushButton, QHBoxLayout, QProgressDialog,
                               QMessageBox, QComboBox, QButtonGroup, QRadioButton,
                               QScrollArea)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Signal, Qt, QSize, QEvent
from PySide6.QtGui import QWheelEvent
from pathlib import Path
from src.core.markdown_processor import MarkdownProcessor
from src.core.html_generator import HTMLGenerator
from src.utils.paginator import SmartPaginator
from src.utils.exporter import ImageExporter

class CustomScrollArea(QScrollArea):
    """自定义滚动区域，处理滚轮事件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.preview_widget = None  # 将在PreviewWidget中设置
        
    def wheelEvent(self, event: QWheelEvent):
        """重写滚轮事件"""
        if self.preview_widget:
            # 适应窗口模式：滚轮翻页
            if self.preview_widget.preview_mode == "fit":
                if event.angleDelta().y() > 0:
                    self.preview_widget.prev_page()
                else:
                    self.preview_widget.next_page()
                event.accept()
                return
            
            # 实际大小模式：检查是否按住Shift进行横向滚动
            elif self.preview_widget.preview_mode == "actual":
                # 如果按住Shift键，实现横向滚动
                if event.modifiers() == Qt.ShiftModifier:
                    # 获取滚动距离
                    delta = event.angleDelta().y()
                    # 横向滚动
                    h_scrollbar = self.horizontalScrollBar()
                    h_scrollbar.setValue(h_scrollbar.value() - delta)
                    event.accept()
                    return
                else:
                    # 正常的垂直滚动
                    super().wheelEvent(event)
                    return
        
        # 默认处理
        super().wheelEvent(event)

class PreviewWidget(QWidget):
    pageChanged = Signal(int, int)  # 当前页，总页数
    sizeChanged = Signal(str)  # 尺寸改变信号
    
    def __init__(self):
        super().__init__()
        self.current_pages = []  # 存储分页后的HTML内容
        self.current_page = 1
        self.total_pages = 1
        self.markdown_text = ""  # 保存原始markdown文本
        self.current_size = "medium"  # 当前页面尺寸
        self.preview_mode = "fit"  # 预览模式: fit(适应窗口) 或 actual(实际大小)
        
        # 初始化处理器
        self.markdown_processor = MarkdownProcessor()
        self.html_generator = HTMLGenerator(page_size="medium")
        self.paginator = SmartPaginator(page_size="medium")
        
        # 初始化UI
        self.init_ui()
        
        # 设置导出器
        self.setup_exporter()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 创建容器框架
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: rgba(25, 25, 40, 0.95);
                border: 1px solid rgba(0, 224, 255, 0.2);
                border-radius: 16px;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # 创建标题栏
        title_bar = self.create_title_bar()
        
        # 创建WebView容器
        self.create_web_view_container()
        
        # 创建控制栏
        control_bar = self.create_control_bar()
        
        # 组装布局
        container_layout.addWidget(title_bar)
        container_layout.addWidget(self.web_container, 1)
        container_layout.addWidget(control_bar)
        
        layout.addWidget(container)
        
        # 连接信号
        self.connect_signals()
        
        # 初始化按钮状态
        self.update_buttons()
    
    def create_title_bar(self):
        """创建标题栏 - 毛玻璃风格"""
        title_bar = QFrame()
        title_bar.setFixedHeight(50)
        title_bar.setStyleSheet("""
            QFrame {
                background: transparent;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 5, 20, 5)
        title_layout.setSpacing(15)
        
        # 标题
        title = QLabel("👀 Live Preview")
        title.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 1px;
                background: transparent;
            }
        """)
        
        # 尺寸选择标签
        size_label = QLabel("Size:")
        size_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                background: transparent;
            }
        """)
        
        # 尺寸选择下拉框
        self.size_selector = QComboBox()
        self.size_selector.addItems(["Small (720×960)", "Medium (1080×1440)", "Large (1440×1920)"])
        self.size_selector.setCurrentIndex(1)
        self.size_selector.setFixedWidth(150)
        self.size_selector.setStyleSheet(self.get_combobox_style())
        
        # 预览模式选择
        mode_label = QLabel("Mode:")
        mode_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
                background: transparent;
            }
        """)
        
        # 预览模式按钮组
        self.mode_group = QButtonGroup()
        
        self.fit_mode_btn = QRadioButton("Fit Window")
        self.fit_mode_btn.setChecked(True)
        self.fit_mode_btn.setStyleSheet(self.get_radio_style())
        
        self.actual_mode_btn = QRadioButton("Actual Size")
        self.actual_mode_btn.setStyleSheet(self.get_radio_style())
        
        self.mode_group.addButton(self.fit_mode_btn, 0)
        self.mode_group.addButton(self.actual_mode_btn, 1)
        
        # 组装标题栏
        title_layout.addWidget(title)
        title_layout.addSpacing(20)
        title_layout.addWidget(size_label)
        title_layout.addWidget(self.size_selector)
        title_layout.addSpacing(15)
        title_layout.addWidget(mode_label)
        title_layout.addWidget(self.fit_mode_btn)
        title_layout.addWidget(self.actual_mode_btn)
        title_layout.addStretch()
        
        return title_bar

    
    def create_web_view_container(self):
        """创建WebView容器 - 毛玻璃风格"""
        self.web_container = CustomScrollArea()
        self.web_container.preview_widget = self
        
        self.web_container.setStyleSheet("""
            QScrollArea {
                border: none;
                background: rgba(20, 20, 40, 0.4);
                border-radius: 20px;
            }
            
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.03);
                width: 12px;
                border-radius: 6px;
                margin: 4px;
            }
            
            QScrollBar::handle:vertical {
                background: linear-gradient(180deg,
                    rgba(0, 255, 255, 0.3) 0%,
                    rgba(255, 0, 255, 0.3) 100%);
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: linear-gradient(180deg,
                    rgba(0, 255, 255, 0.5) 0%,
                    rgba(255, 0, 255, 0.5) 100%);
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                background: rgba(255, 255, 255, 0.03);
                height: 12px;
                border-radius: 6px;
                margin: 4px;
            }
            
            QScrollBar::handle:horizontal {
                background: linear-gradient(90deg,
                    rgba(0, 255, 255, 0.3) 0%,
                    rgba(255, 0, 255, 0.3) 100%);
                border-radius: 6px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: linear-gradient(90deg,
                    rgba(0, 255, 255, 0.5) 0%,
                    rgba(255, 0, 255, 0.5) 100%);
            }
            
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # 创建WebView
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("""
            QWebEngineView {
                border: none;
                background: transparent;
            }
        """)
    
    def create_control_bar(self):
        """创建控制栏 - 毛玻璃风格"""
        control_bar = QFrame()
        control_bar.setFixedHeight(60)
        control_bar.setStyleSheet("""
            QFrame {
                background: rgba(20, 20, 40, 0.6);
                backdrop-filter: blur(10px);
                border-bottom-left-radius: 20px;
                border-bottom-right-radius: 20px;
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        control_layout = QHBoxLayout(control_bar)
        control_layout.setContentsMargins(20, 12, 20, 12)
        control_layout.setSpacing(15)
        
        # 创建中心控制区容器
        center_controls = QWidget()
        center_layout = QHBoxLayout(center_controls)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(15)
        
        # 上一页按钮
        self.prev_btn = QPushButton("⬅ Previous")
        self.prev_btn.setFixedSize(110, 36)
        self.prev_btn.setStyleSheet(self.get_button_style())
        
        # 页面信息标签
        self.page_info_label = QLabel("")
        self.page_info_label.setStyleSheet("""
            QLabel {
                color: #00ff88;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 20px;
                background: rgba(0, 255, 136, 0.1);
                border: 1px solid rgba(0, 255, 136, 0.3);
                border-radius: 18px;
                min-width: 100px;
                text-align: center;
            }
        """)
        self.page_info_label.setAlignment(Qt.AlignCenter)
        
        # 下一页按钮
        self.next_btn = QPushButton("Next ➡")
        self.next_btn.setFixedSize(110, 36)
        self.next_btn.setStyleSheet(self.get_button_style())
        
        # 组装中心控制区
        center_layout.addWidget(self.prev_btn)
        center_layout.addWidget(self.page_info_label)
        center_layout.addWidget(self.next_btn)
        
        # 快捷提示
        tips_label = QLabel("💡 Tip: Scroll to navigate • Shift+Scroll for horizontal")
        tips_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 11px;
                font-style: italic;
                background: transparent;
            }
        """)
        
        # 组装控制栏
        control_layout.addStretch()
        control_layout.addWidget(center_controls)
        control_layout.addStretch()
        control_layout.addWidget(tips_label)
        
        return control_bar
    
    def connect_signals(self):
        """连接信号"""
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.size_selector.currentIndexChanged.connect(self.on_size_changed)
        self.mode_group.buttonClicked.connect(self.on_mode_changed)
    
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() == Qt.Key_PageUp:
            self.prev_page()
        elif event.key() == Qt.Key_PageDown:
            self.next_page()
        elif event.key() == Qt.Key_Home:
            self.go_to_page(1)
        elif event.key() == Qt.Key_End:
            self.go_to_page(self.total_pages)
        else:
            super().keyPressEvent(event)
    
    def on_mode_changed(self):
        """处理预览模式改变"""
        if self.fit_mode_btn.isChecked():
            self.preview_mode = "fit"
            # 适应窗口模式：隐藏滚动条，启用自适应
            self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.web_container.setWidgetResizable(True)
            
            # 清除 WebView 的固定尺寸限制
            self.web_view.setMinimumSize(0, 0)
            self.web_view.setMaximumSize(16777215, 16777215)
            
            # 在适应模式下，WebView不需要处理鼠标事件
            self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            
        else:
            self.preview_mode = "actual"
            # 实际大小模式：显示滚动条
            self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.web_container.setWidgetResizable(False)
            
            # 在实际大小模式下，让WebView透明于鼠标滚轮事件
            # 这样滚轮事件会直接传递给ScrollArea
            self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        # 重新渲染当前页面
        self.display_current_page()
    
    def on_size_changed(self, index):
        """处理尺寸改变"""
        size_map = {0: "small", 1: "medium", 2: "large"}
        new_size = size_map.get(index, "medium")
        
        if new_size != self.current_size:
            self.current_size = new_size
            
            # 更新各组件的尺寸设置
            self.html_generator = HTMLGenerator(page_size=new_size)
            self.paginator.set_page_size(new_size)
            
            # 重新处理内容
            if self.markdown_text:
                self.update_content(self.markdown_text)
            
            # 发送尺寸改变信号
            self.sizeChanged.emit(new_size)
    
    def update_content(self, markdown_text: str):
        """更新预览内容"""
        try:
            self.markdown_text = markdown_text
            
            # 处理 Markdown
            html_content = self.markdown_processor.parse(markdown_text)
            
            # 使用智能分页器进行分页
            self.current_pages = self.paginator.paginate(html_content)
            
            # 优化分页结果
            self.current_pages = self.paginator.optimize_pages(self.current_pages)
            
            self.total_pages = len(self.current_pages)
            self.current_page = 1
            
            # 显示第一页
            self.display_current_page()
            
            # 更新按钮和信息
            self.update_buttons()
            self.update_page_info()
            
        except Exception as e:
            self.show_error(f"预览错误: {str(e)}")
    
    def display_current_page(self):
        """显示当前页"""
        if not self.current_pages:
            return
            
        if 1 <= self.current_page <= len(self.current_pages):
            page_content = self.current_pages[self.current_page - 1]
            
            # 获取目标尺寸
            size_config = {
                "small": (720, 960),
                "medium": (1080, 1440),
                "large": (1440, 1920)
            }
            target_width, target_height = size_config.get(self.current_size, (1080, 1440))
            
            # 根据预览模式生成不同的HTML
            if self.preview_mode == "fit":
                # 适应窗口模式
                full_html = self.generate_fit_html(page_content, target_width, target_height)
                self.web_view.setMinimumSize(0, 0)
                self.web_view.setMaximumSize(16777215, 16777215)
                self.web_container.setWidgetResizable(True)
                
            else:
                # 实际大小模式：添加禁用内部滚动的CSS
                full_html = self.generate_actual_html(page_content, target_width, target_height)
                # 设置WebView为实际尺寸
                self.web_view.setFixedSize(target_width, target_height)
                self.web_container.setWidgetResizable(False)
            
            # 加载到WebView
            self.web_view.setHtml(full_html, QUrl("file:///"))
    
    def generate_actual_html(self, content: str, target_width: int, target_height: int) -> str:
        """生成实际大小模式的HTML（禁用内部滚动）"""
        base_html = self.html_generator.generate(content)
        
        # 添加禁用滚动的CSS和JavaScript
        disable_scroll = """
        <style>
            /* 禁用所有内部滚动 */
            html, body {
                overflow: hidden !important;
                position: fixed !important;
                width: 100% !important;
                height: 100% !important;
                touch-action: none !important;
                user-select: none !important;
                -webkit-user-select: none !important;
                -ms-overflow-style: none !important;
                scrollbar-width: none !important;
            }
            
            html::-webkit-scrollbar,
            body::-webkit-scrollbar {
                display: none !important;
            }
            
            * {
                -ms-overflow-style: none !important;
                scrollbar-width: none !important;
            }
            
            *::-webkit-scrollbar {
                display: none !important;
            }
        </style>
        
        <script>
            // 禁用滚动事件
            document.addEventListener('DOMContentLoaded', function() {
                // 禁用滚轮事件
                document.addEventListener('wheel', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, { passive: false, capture: true });
                
                // 禁用触摸滚动
                document.addEventListener('touchmove', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    return false;
                }, { passive: false, capture: true });
                
                // 禁用键盘滚动
                document.addEventListener('keydown', function(e) {
                    const scrollKeys = [32, 33, 34, 35, 36, 37, 38, 39, 40];
                    if (scrollKeys.includes(e.keyCode)) {
                        e.preventDefault();
                        return false;
                    }
                }, false);
                
                // 固定body位置
                document.body.style.position = 'fixed';
                document.body.style.top = '0';
                document.body.style.left = '0';
                document.body.style.width = '100%';
                document.body.style.height = '100%';
                document.body.style.overflow = 'hidden';
            });
        </script>
        """
        
        # 插入到head标签结束前
        full_html = base_html.replace('</head>', disable_scroll + '</head>')
        
        return full_html
    
    def generate_fit_html(self, content: str, target_width: int, target_height: int) -> str:
        """生成适应窗口的HTML"""
        base_html = self.html_generator.generate(content)
        
        scale_script = f"""
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            html, body {{
                width: 100%;
                height: 100%;
                overflow: hidden;
                background: #1a1a2e;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            
            #viewport-container {{
                position: relative;
                width: 100vw;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
            }}
            
            #content-wrapper {{
                position: relative;
                width: {target_width}px;
                height: {target_height}px;
                transform-origin: center center;
                transition: transform 0.3s ease;
                flex-shrink: 0;
            }}
        </style>
        
        <script>
            document.addEventListener('DOMContentLoaded', function() {{
                if (!document.getElementById('viewport-container')) {{
                    const viewportContainer = document.createElement('div');
                    viewportContainer.id = 'viewport-container';
                    
                    const contentWrapper = document.createElement('div');
                    contentWrapper.id = 'content-wrapper';
                    
                    while (document.body.firstChild) {{
                        contentWrapper.appendChild(document.body.firstChild);
                    }}
                    
                    viewportContainer.appendChild(contentWrapper);
                    document.body.appendChild(viewportContainer);
                }}
                
                function adjustScale() {{
                    const wrapper = document.getElementById('content-wrapper');
                    const container = document.getElementById('viewport-container');
                    
                    if (!wrapper || !container) return;
                    
                    const availableWidth = container.clientWidth;
                    const availableHeight = container.clientHeight;
                    
                    const targetWidth = {target_width};
                    const targetHeight = {target_height};
                    
                    const padding = 40;
                    const scaleX = (availableWidth - padding) / targetWidth;
                    const scaleY = (availableHeight - padding) / targetHeight;
                    
                    const scale = Math.min(scaleX, scaleY, 1.0);
                    
                    wrapper.style.transform = `scale(${{scale}})`;
                }}
                
                setTimeout(adjustScale, 100);
                window.addEventListener('resize', adjustScale);
                
                const observer = new ResizeObserver(adjustScale);
                observer.observe(document.getElementById('viewport-container'));
            }});
        </script>
        """
        
        full_html = base_html.replace('</head>', scale_script + '</head>')
        return full_html
    
    # ... 其余方法保持不变 ...
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.go_to_page(self.current_page - 1)
    
    def next_page(self):
        """下一页"""
        if self.current_page < self.total_pages:
            self.go_to_page(self.current_page + 1)
    
    def go_to_page(self, page_num: int):
        """跳转到指定页"""
        if 1 <= page_num <= self.total_pages:
            self.current_page = page_num
            self.display_current_page()
            self.update_buttons()
            self.update_page_info()
    
    def update_buttons(self):
        """更新按钮状态"""
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)
        self.pageChanged.emit(self.current_page, self.total_pages)
    
    def update_page_info(self):
        """更新页面信息显示"""
        if self.total_pages > 1:
            self.page_info_label.setText(f"第 {self.current_page} / {self.total_pages} 页")
        else:
            self.page_info_label.setText("第 1 页")
    
    def get_button_style(self) -> str:
        """获取按钮样式 - 毛玻璃风格"""
        return """
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: rgba(255, 255, 255, 0.95);
                padding: 10px 20px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 13px;
                letter-spacing: 0.5px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(0, 255, 136, 0.5);
                color: #00ff88;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 255, 136, 0.3);
            }
            
            QPushButton:pressed {
                background: rgba(0, 255, 136, 0.2);
                transform: translateY(0);
            }
            
            QPushButton:disabled {
                background: rgba(255, 255, 255, 0.02);
                border-color: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }
        """
    
    def get_combobox_style(self) -> str:
        """获取下拉框样式 - 毛玻璃风格"""
        return """
            QComboBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: rgba(255, 255, 255, 0.95);
                padding: 8px 15px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.3px;
            }
            
            QComboBox:hover {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 5px 5px 0 5px;
                border-color: rgba(255, 255, 255, 0.7) transparent transparent transparent;
                margin-right: 5px;
            }
            
            QComboBox QAbstractItemView {
                background: rgba(30, 30, 50, 0.95);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                selection-background-color: rgba(0, 255, 136, 0.3);
                outline: none;
                padding: 5px;
                border-radius: 10px;
            }
            
            QComboBox QAbstractItemView::item {
                min-height: 35px;
                padding: 8px 12px;
                border-radius: 5px;
                margin: 2px 4px;
            }
            
            QComboBox QAbstractItemView::item:hover {
                background: rgba(255, 255, 255, 0.1);
            }
            
            QComboBox QAbstractItemView::item:selected {
                background: rgba(0, 255, 136, 0.3);
                color: white;
            }
        """
    
    def get_radio_style(self) -> str:
        """获取单选按钮样式 - 毛玻璃风格"""
        return """
            QRadioButton {
                color: rgba(255, 255, 255, 0.8);
                font-size: 12px;
                spacing: 8px;
                padding: 5px;
            }
            
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.05);
            }
            
            QRadioButton::indicator:hover {
                border-color: rgba(0, 255, 136, 0.5);
                background: rgba(0, 255, 136, 0.1);
            }
            
            QRadioButton::indicator:checked {
                background: qradialgradient(
                    cx: 0.5, cy: 0.5, radius: 0.5,
                    fx: 0.5, fy: 0.5,
                    stop: 0 #00ff88,
                    stop: 0.6 #00ff88,
                    stop: 0.7 transparent
                );
                border-color: #00ff88;
                box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
            }
            
            QRadioButton:checked {
                color: #00ff88;
            }
        """
    
    def setup_exporter(self):
        """设置导出器"""
        self.exporter = ImageExporter(self.web_view)
        self.exporter.progress.connect(self.on_export_progress)
        self.exporter.finished.connect(self.on_export_finished)
        self.exporter.page_exported.connect(self.on_page_exported)
    
    def export_pages(self, folder: str):
        """导出所有页面为图片"""
        if not self.current_pages:
            QMessageBox.warning(self, "提示", "没有可导出的内容")
            return
        
        # 创建进度对话框
        self.progress_dialog = QProgressDialog(
            "正在导出图片...", 
            "取消", 
            0, 
            self.total_pages, 
            self
        )
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        self.progress_dialog.canceled.connect(self.on_export_canceled)
        
        # 开始导出（始终以实际大小导出）
        self.exporter.export_pages(
            self.current_pages,
            folder,
            self.html_generator,
            format="PNG",
            quality=100
        )
    
    def on_export_progress(self, current: int, total: int):
        """处理导出进度"""
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.setValue(current)
            self.progress_dialog.setLabelText(f"正在导出第 {current}/{total} 页...")
    
    def on_export_finished(self, success: bool, message: str):
        """处理导出完成"""
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            try:
                self.progress_dialog.canceled.disconnect()
                self.progress_dialog.close()
                self.progress_dialog.deleteLater()
            except:
                pass
            finally:
                self.progress_dialog = None
        
        if success:
            size_info = f"({self.current_size}: {self.get_actual_size()}px)"
            QMessageBox.information(self, "导出成功", f"{message}\n尺寸: {size_info}")
        else:
            QMessageBox.warning(self, "导出失败", message)
    
    def on_page_exported(self, page_num: int, file_path: str):
        """处理单页导出完成"""
        print(f"已导出第 {page_num} 页: {file_path}")
    
    def on_export_canceled(self):
        """处理导出取消"""
        self.exporter.cancel_export()
    
    def get_actual_size(self) -> str:
        """获取实际尺寸"""
        size_config = {
            "small": "720×960",
            "medium": "1080×1440",
            "large": "1440×1920"
        }
        return size_config.get(self.current_size, "1080×1440")
    
    def handle_scroll(self, percentage: float):
        """处理编辑器滚动同步（保留接口兼容性）"""
        pass
    
    def show_error(self, message: str):
        """显示错误信息"""
        error_html = f"""
        <html>
        <body style="padding: 20px; font-family: sans-serif; background: #1a1a2e; color: #e0e6ed;">
            <h3 style="color: #ff4757;">错误</h3>
            <p style="color: #8a92a6;">{message}</p>
        </body>
        </html>
        """
        self.web_view.setHtml(error_html)
    
    def change_theme(self, theme: str):
        """切换主题"""
        self.html_generator.set_theme(theme)
        if self.current_pages:
            self.display_current_page()
    
    def resizeEvent(self, event):
        """处理窗口大小改变事件"""
        super().resizeEvent(event)
        # 在适应窗口模式下，重新渲染以适应新尺寸
        if self.preview_mode == "fit" and self.current_pages:
            # 延迟执行以避免频繁重绘
            if hasattr(self, 'resize_timer'):
                self.resize_timer.stop()
            else:
                self.resize_timer = QTimer()
                self.resize_timer.timeout.connect(self.on_resize_finished)
                self.resize_timer.setSingleShot(True)
            self.resize_timer.start(300)
    
    def on_resize_finished(self):
        """窗口大小调整完成后的处理"""
        if self.preview_mode == "fit":
            self.display_current_page()
### 系统:
我仔细检查了你的代码和之前的聊天记录。代码整体结构良好，但我发现了几个需要修复的问题：

## 主要问题：

1. **`editor_widget.py` 不完整** - 缺少关键的语法高亮器设置和样式代码
2. **`preview_widget.py` 中的 `create_web_view_container` 方法不完整** - 缺少关键的WebView设置代码
3. **主窗口缺少部分方法实现**

让我为你提供完整的修复代码： 代码
```python
# ============================================
# src/ui/editor_widget.py - 毛玻璃风格编辑器（完整版）
# ============================================
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLabel, QFrame, QHBoxLayout
from PySide6.QtGui import QFont, QTextOption, QPalette, QColor, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtCore import Signal, Qt, QRegularExpression

class MarkdownHighlighter(QSyntaxHighlighter):
    """Markdown 语法高亮器"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        
        # 标题
        heading_format = QTextCharFormat()
        heading_format.setForeground(QColor(0, 255, 136))
        heading_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegularExpression(r'^#{1,6}\s.*'), heading_format))
        
        # 粗体
        bold_format = QTextCharFormat()
        bold_format.setForeground(QColor(255, 179, 71))
        bold_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegularExpression(r'\*\*[^\*]+\*\*'), bold_format))
        
        # 斜体
        italic_format = QTextCharFormat()
        italic_format.setForeground(QColor(255, 179, 71))
        italic_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r'\*[^\*]+\*'), italic_format))
        
        # 代码块
        code_format = QTextCharFormat()
        code_format.setForeground(QColor(139, 233, 253))
        code_format.setFontFamily("Cascadia Code, Consolas, monospace")
        self.highlighting_rules.append((QRegularExpression(r'`[^`]+`'), code_format))
        
        # 链接
        link_format = QTextCharFormat()
        link_format.setForeground(QColor(189, 147, 249))
        link_format.setFontUnderline(True)
        self.highlighting_rules.append((QRegularExpression(r'\[([^\]]+)\]\(([^\)]+)\)'), link_format))
        
        # 列表
        list_format = QTextCharFormat()
        list_format.setForeground(QColor(255, 121, 198))
        self.highlighting_rules.append((QRegularExpression(r'^\s*[\*\-\+]\s'), list_format))
        self.highlighting_rules.append((QRegularExpression(r'^\s*\d+\.\s'), list_format))
        
        # 引用
        quote_format = QTextCharFormat()
        quote_format.setForeground(QColor(98, 114, 164))
        quote_format.setFontItalic(True)
        self.highlighting_rules.append((QRegularExpression(r'^>\s.*'), quote_format))
        
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class EditorWidget(QWidget):
    textChanged = Signal()
    scrollChanged = Signal(float)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 编辑器容器
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(1, 1, 1, 1)
        container_layout.setSpacing(0)
        
        # 创建编辑器
        self.editor = QTextEdit()
        self.setup_editor()
        
        # 添加到容器
        container_layout.addWidget(self.editor)
        layout.addWidget(container)
        
    def setup_editor(self):
        """设置编辑器"""
        # 设置字体
        font = QFont("Cascadia Code, Consolas, Monaco, monospace", 13)
        font.setStyleHint(QFont.Monospace)
        self.editor.setFont(font)
        
        # 设置换行模式
        self.editor.setLineWrapMode(QTextEdit.WidgetWidth)
        self.editor.setWordWrapMode(QTextOption.WordWrap)
        
        # 设置tab宽度
        self.editor.setTabStopDistance(40)
        
        # 应用语法高亮
        self.highlighter = MarkdownHighlighter(self.editor.document())
        
        # 设置编辑器样式
        self.editor.setStyleSheet("""
            QTextEdit {
                background: rgba(20, 20, 40, 0.4);
                backdrop-filter: blur(10px);
                border: none;
                border-radius: 20px;
                padding: 25px;
                color: rgba(255, 255, 255, 0.95);
                selection-background-color: rgba(0, 255, 136, 0.3);
                selection-color: white;
                font-size: 14px;
                line-height: 1.6;
            }
            
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.03);
                width: 12px;
                border-radius: 6px;
                margin: 4px;
            }
            
            QScrollBar::handle:vertical {
                background: linear-gradient(180deg,
                    rgba(0, 255, 255, 0.3) 0%,
                    rgba(255, 0, 255, 0.3) 100%);
                border-radius: 6px;
                min-height: 30px;
            }
            
            QScrollBar::handle:vertical:hover {
                background: linear-gradient(180deg,
                    rgba(0, 255, 255, 0.5) 0%,
                    rgba(255, 0, 255, 0.5) 100%);
            }
            
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            
            QScrollBar:horizontal {
                background: rgba(255, 255, 255, 0.03);
                height: 12px;
                border-radius: 6px;
                margin: 4px;
            }
            
            QScrollBar::handle:horizontal {
                background: linear-gradient(90deg,
                    rgba(0, 255, 255, 0.3) 0%,
                    rgba(255, 0, 255, 0.3) 100%);
                border-radius: 6px;
                min-width: 30px;
            }
            
            QScrollBar::handle:horizontal:hover {
                background: linear-gradient(90deg,
                    rgba(0, 255, 255, 0.5) 0%,
                    rgba(255, 0, 255, 0.5) 100%);
            }
            
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # 设置默认文本
        self.editor.setPlainText("""# 🌸 小红书笔记标题

## 今日分享

大家好呀～今天给大家分享一个超实用的 **Markdown 编辑器**！

### ✨ 主要功能

1. **实时预览** - 左边写，右边看
2. **智能分页** - 自动适配小红书卡片尺寸
3. **一键导出** - 批量生成精美图片

### 📝 使用方法

- 在左侧输入 Markdown 文本
- 右侧实时显示预览效果
- 点击导出按钮保存图片

> 💡 小贴士：支持所有常用的 Markdown 语法哦～

### 代码示例

```python
def hello():
    print("Hello, 小红书!")
    return "❤️"
```

### 表格示例

| 功能 | 描述 | 状态 |
|------|------|------|
| 编辑 | Markdown编辑器 | ✅ |
| 预览 | 实时渲染 | ✅ |
| 导出 | 图片生成 | ✅ |

---

喜欢的话记得 **点赞收藏** 哦～ ❤️

关注我，获取更多实用工具！""")
        
        # 连接信号
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.verticalScrollBar().valueChanged.connect(self.on_scroll)
        
    def on_text_changed(self):
        """处理文本变化"""
        self.textChanged.emit()
        
    def on_scroll(self):
        """处理滚动事件"""
        scrollbar = self.editor.verticalScrollBar()
        if scrollbar.maximum() > 0:
            percentage = scrollbar.value() / scrollbar.maximum()
            self.scrollChanged.emit(percentage)
            
    def get_text(self):
        """获取编辑器文本"""
        return self.editor.toPlainText()
    
    def set_text(self, text):
        """设置编辑器文本"""
        self.editor.setPlainText(text)
        
    def clear(self):
        """清空编辑器"""
        self.editor.clear()
```
 代码
```python
def create_web_view_container(self):
    """创建WebView容器 - 毛玻璃风格（完整版）"""
    # 使用自定义滚动区域
    self.web_container = CustomScrollArea()
    self.web_container.preview_widget = self  # 设置引用
    
    self.web_container.setStyleSheet("""
        QScrollArea {
            border: none;
            background: rgba(20, 20, 40, 0.4);
            border-radius: 20px;
        }
        
        QScrollBar:vertical {
            background: rgba(255, 255, 255, 0.03);
            width: 12px;
            border-radius: 6px;
            margin: 4px;
        }
        
        QScrollBar::handle:vertical {
            background: linear-gradient(180deg,
                rgba(0, 255, 255, 0.3) 0%,
                rgba(255, 0, 255, 0.3) 100%);
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: linear-gradient(180deg,
                rgba(0, 255, 255, 0.5) 0%,
                rgba(255, 0, 255, 0.5) 100%);
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            background: rgba(255, 255, 255, 0.03);
            height: 12px;
            border-radius: 6px;
            margin: 4px;
        }
        
        QScrollBar::handle:horizontal {
            background: linear-gradient(90deg,
                rgba(0, 255, 255, 0.3) 0%,
                rgba(255, 0, 255, 0.3) 100%);
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: linear-gradient(90deg,
                rgba(0, 255, 255, 0.5) 0%,
                rgba(255, 0, 255, 0.5) 100%);
        }
        
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0px;
        }
    """)
    
    # 创建WebView
    self.web_view = QWebEngineView()
    self.web_view.setStyleSheet("""
        QWebEngineView {
            border: none;
            background: transparent;
        }
    """)
    
    # 禁用WebView自身的滚动条和鼠标交互（在实际大小模式下）
    self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, False)
    self.web_view.setFocusPolicy(Qt.StrongFocus)
    
    # 设置滚动区域
    self.web_container.setWidget(self.web_view)
    self.web_container.setWidgetResizable(True)
    self.web_container.setAlignment(Qt.AlignCenter)
    
    # 默认设置为适应窗口模式
    self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
```
 ## 问题总结和修复说明：

### 1. **已修复的问题：**

#### `editor_widget.py`：
- ✅ 添加了完整的 `setup_editor` 方法
- ✅ 实现了语法高亮器的应用
- ✅ 添加了毛玻璃风格的完整样式
- ✅ 添加了 `set_text` 和 `clear` 方法（供主窗口调用）

#### `preview_widget.py` 的 `create_web_view_container` 方法：
- ✅ 补充了完整的WebView设置代码
- ✅ 确保了滚动条样式的一致性

### 2. **小修复位置（你可以手动修改）：**

在 `preview_widget.py` 的 `init_ui` 方法中，确保在调用 `create_web_view_container()` 后正确设置了WebView的父组件关系。

### 3. **验证清单：**

请确保以下文件都已正确导入和存在：
- ✅ `src/core/markdown_processor.py`
- ✅ `src/core/html_generator.py`
- ✅ `src/utils/paginator.py`
- ✅ `src/utils/exporter.py`
- ✅ `src/utils/style_manager.py`

### 4. **运行前检查：**

```python
# requirements.txt 应包含：
PySide6>=6.5.0
PySide6-WebEngine>=6.5.0
markdown>=3.4.0
beautifulsoup4>=4.12.0
```

### 5. **可能的优化建议：**

1. 在 `main_window.py` 中，可以考虑添加窗口最小尺寸限制：
   ```python
   self.setMinimumSize(1200, 700)
   ```

2. 如果极光背景动画消耗太多性能，可以调整动画帧率：
   ```python
   self.animation_timer.start(100)  # 从50ms改为100ms
   ```

现在你的代码应该可以正常运行了。毛玻璃风格的UI会给用户带来现代化的视觉体验！
### 用户:
运行的时候会有这种终端提示，有问题吗？ 但似乎功能没啥问题
paste.txt->txt->(card) PS E:\wayForward\projects\RedBookCards> python main.py
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property box-shadow
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property box-shadow
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property box-shadow
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property backdrop-filter
Unknown property -webkit-background-clip
Unknown property -webkit-text-fill-color
Unknown property -webkit-background-clip
Unknown property -webkit-text-fill-color
Unknown property transition
Unknown property transition
Unknown property transform
Unknown property transform
Unknown property transition
Unknown property transition
Unknown property transform
Unknown property transform
Unknown property box-shadow
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property box-shadow
Unknown property box-shadow
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property backdrop-filter
Unknown property transition
Unknown property transform
Unknown property box-shadow
Unknown property transform
(card) PS E:\wayForward\projects\RedBookCards> 
### 系统:
这些警告信息表明 Qt 的样式表解析器不识别一些现代 CSS 属性。虽然功能正常运行，但这些警告会让终端输出很混乱。让我为你提供一个兼容性更好的样式版本，去除不支持的 CSS 属性： 代码
```python
# ============================================
# src/ui/main_window.py - Qt兼容样式版本
# ============================================
from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QToolBar, QSplitter, QPushButton,
                               QFileDialog, QMessageBox, QStatusBar, QLabel,
                               QGraphicsDropShadowEffect, QComboBox, QFrame)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QAction, QIcon, QColor, QLinearGradient, QPainter, QBrush
from src.ui.editor_widget import EditorWidget
from src.ui.preview_widget import PreviewWidget
from src.utils.style_manager import StyleManager

class AuroraBackground(QWidget):
    """极光渐变背景组件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_offset = 0
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_gradient)
        self.animation_timer.start(50)  # 20fps动画
        
    def update_gradient(self):
        self.gradient_offset = (self.gradient_offset + 1) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 创建动态极光渐变
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        
        # 基于时间偏移的动态颜色
        hue1 = (180 + self.gradient_offset) % 360
        hue2 = (280 + self.gradient_offset) % 360
        hue3 = (320 + self.gradient_offset) % 360
        
        color1 = QColor.fromHsv(hue1, 180, 60)
        color2 = QColor.fromHsv(hue2, 200, 80)
        color3 = QColor.fromHsv(hue3, 160, 70)
        
        gradient.setColorAt(0, color1)
        gradient.setColorAt(0.3, color2)
        gradient.setColorAt(0.6, QColor(25, 25, 60))
        gradient.setColorAt(1, color3)
        
        painter.fillRect(self.rect(), gradient)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 先创建自动更新计时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_preview)
        self.update_timer.setInterval(300)  # 300ms延迟
        
        # 初始化样式管理器
        self.style_manager = StyleManager()
        
        # 然后初始化UI
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("✨ 小红书 Markdown 编辑器 - Aurora Edition")
        self.setGeometry(100, 100, 1700, 950)
        self.setMinimumSize(1200, 700)
        
        # 创建主容器
        main_container = QWidget()
        self.setCentralWidget(main_container)
        
        # 创建极光背景
        self.aurora_bg = AuroraBackground(main_container)
        
        # 主布局
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 应用全局样式（Qt兼容版本）
        self.setStyleSheet(self.get_global_styles_qt_compatible())
        
        # 创建顶部工具栏
        toolbar_container = self.create_toolbar()
        main_layout.addWidget(toolbar_container)
        
        # 创建内容区域
        content_area = QWidget()
        content_area.setObjectName("contentArea")
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.setObjectName("mainSplitter")
        
        # 创建编辑器和预览组件
        self.editor = EditorWidget()
        self.preview = PreviewWidget()
        
        # 为组件添加玻璃容器
        editor_container = self.create_glass_container(self.editor, "📝 Markdown Editor")
        preview_container = self.create_glass_container(self.preview, "👀 Live Preview")
        
        # 添加到分割器
        splitter.addWidget(editor_container)
        splitter.addWidget(preview_container)
        splitter.setSizes([850, 850])
        
        content_layout.addWidget(splitter)
        main_layout.addWidget(content_area, 1)
        
        # 创建底部状态栏
        self.create_status_bar()
        
        # 初始更新
        self.update_preview()
        self.update_char_count()
        
        # 确保背景在最底层
        self.aurora_bg.lower()
        
    def create_glass_container(self, widget, title):
        """创建毛玻璃容器"""
        container = QFrame()
        container.setObjectName("glassContainer")
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 标题栏
        title_bar = QFrame()
        title_bar.setObjectName("glassTitleBar")
        title_bar.setFixedHeight(45)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 0, 20, 0)
        
        title_label = QLabel(title)
        title_label.setObjectName("glassTitle")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # 添加组件
        layout.addWidget(title_bar)
        layout.addWidget(widget, 1)
        
        # 添加发光效果
        self.add_glow_effect(container)
        
        return container
        
    def create_toolbar(self):
        """创建毛玻璃工具栏"""
        toolbar_container = QFrame()
        toolbar_container.setObjectName("toolbarContainer")
        toolbar_container.setFixedHeight(70)
        
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(25, 15, 25, 15)
        toolbar_layout.setSpacing(15)
        
        # Logo 和标题
        logo_label = QLabel("✨")
        logo_label.setObjectName("logoLabel")
        toolbar_layout.addWidget(logo_label)
        
        app_title = QLabel("Aurora Markdown Editor")
        app_title.setObjectName("appTitle")
        toolbar_layout.addWidget(app_title)
        
        toolbar_layout.addSpacing(40)
        
        # 功能按钮
        self.export_btn = self.create_neon_button("📸 Export", "#00ff88")
        self.export_btn.clicked.connect(self.export_images)
        toolbar_layout.addWidget(self.export_btn)
        
        self.clear_btn = self.create_neon_button("🗑️ Clear", "#ff6b6b")
        self.clear_btn.clicked.connect(self.clear_content)
        toolbar_layout.addWidget(self.clear_btn)
        
        toolbar_layout.addSpacing(20)
        
        # 主题选择器
        theme_label = QLabel("Theme:")
        theme_label.setObjectName("themeLabel")
        toolbar_layout.addWidget(theme_label)
        
        self.theme_selector = QComboBox()
        self.theme_selector.setObjectName("themeSelector")
        self.theme_selector.setFixedWidth(180)
        
        themes = self.style_manager.get_theme_display_names()
        for key, name in themes.items():
            self.theme_selector.addItem(name, key)
        
        self.theme_selector.setCurrentText("小红书经典")
        toolbar_layout.addWidget(self.theme_selector)
        
        toolbar_layout.addStretch()
        
        return toolbar_container
        
    def create_neon_button(self, text, color):
        """创建霓虹发光按钮"""
        btn = QPushButton(text)
        btn.setObjectName("neonButton")
        btn.setProperty("neonColor", color)
        
        # 添加发光效果
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(20)
        glow.setOffset(0, 0)
        glow.setColor(QColor(color))
        btn.setGraphicsEffect(glow)
        
        # 悬浮动画
        btn.enterEvent = lambda e: self.animate_button_hover(btn, True)
        btn.leaveEvent = lambda e: self.animate_button_hover(btn, False)
        
        return btn
        
    def animate_button_hover(self, button, hover):
        """按钮悬浮动画"""
        effect = button.graphicsEffect()
        if effect:
            if hover:
                effect.setBlurRadius(30)
            else:
                effect.setBlurRadius(20)
                
    def create_status_bar(self):
        """创建毛玻璃状态栏"""
        self.status_bar = QStatusBar()
        self.status_bar.setObjectName("glassStatusBar")
        self.status_bar.setFixedHeight(40)
        self.setStatusBar(self.status_bar)
        
        # 字数统计
        self.char_count_label = QLabel("Words: 0")
        self.char_count_label.setObjectName("statusLabel")
        
        # 主题信息
        self.theme_info_label = QLabel("Theme: 小红书经典")
        self.theme_info_label.setObjectName("statusLabel")
        
        self.status_bar.addPermanentWidget(self.theme_info_label)
        self.status_bar.addPermanentWidget(self.char_count_label)
        
    def add_glow_effect(self, widget):
        """添加发光效果"""
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setOffset(0, 0)
        glow.setColor(QColor(0, 224, 255, 80))
        widget.setGraphicsEffect(glow)
        
    def get_global_styles_qt_compatible(self):
        """获取Qt兼容的全局样式表（移除不支持的CSS属性）"""
        return """
        /* 全局字体 */
        * {
            font-family: 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif;
        }
        
        /* 内容区域 */
        #contentArea {
            background: transparent;
        }
        
        /* 毛玻璃容器 - 使用半透明背景代替backdrop-filter */
        #glassContainer {
            background: rgba(30, 30, 50, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 20px;
        }
        
        #glassTitleBar {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 rgba(255, 255, 255, 0.1),
                stop: 1 rgba(255, 255, 255, 0.05));
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            border-top-left-radius: 20px;
            border-top-right-radius: 20px;
        }
        
        #glassTitle {
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            font-weight: 600;
            letter-spacing: 1px;
        }
        
        /* 工具栏 */
        #toolbarContainer {
            background: rgba(20, 20, 40, 0.9);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        #logoLabel {
            font-size: 28px;
        }
        
        #appTitle {
            color: rgba(255, 255, 255, 0.95);
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 2px;
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 #00ff88, stop: 0.5 #00ffff, stop: 1 #ff00ff);
        }
        
        #themeLabel {
            color: rgba(255, 255, 255, 0.7);
            font-size: 14px;
            font-weight: 500;
        }
        
        /* 霓虹按钮 - 简化样式 */
        #neonButton {
            background: rgba(255, 255, 255, 0.08);
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 10px 25px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 1px;
        }
        
        #neonButton:hover {
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.5);
        }
        
        #neonButton:pressed {
            background: rgba(255, 255, 255, 0.05);
        }
        
        /* 主题选择器 */
        #themeSelector {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            padding: 8px 15px;
            border-radius: 15px;
            font-size: 13px;
            font-weight: 500;
        }
        
        #themeSelector:hover {
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        #themeSelector::drop-down {
            border: none;
            width: 30px;
        }
        
        #themeSelector::down-arrow {
            image: none;
            border-style: solid;
            border-width: 5px 5px 0 5px;
            border-color: white transparent transparent transparent;
            margin-right: 8px;
        }
        
        #themeSelector QAbstractItemView {
            background: rgba(30, 30, 50, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
            selection-background-color: rgba(0, 255, 136, 0.3);
            border-radius: 10px;
            padding: 5px;
        }
        
        #themeSelector QAbstractItemView::item {
            min-height: 35px;
            padding: 8px;
            border-radius: 5px;
        }
        
        #themeSelector QAbstractItemView::item:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        /* 分割器 */
        #mainSplitter::handle {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 rgba(255, 255, 255, 0),
                stop: 0.5 rgba(255, 255, 255, 0.2),
                stop: 1 rgba(255, 255, 255, 0));
            width: 3px;
        }
        
        #mainSplitter::handle:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 rgba(0, 255, 255, 0),
                stop: 0.5 rgba(0, 255, 255, 0.5),
                stop: 1 rgba(0, 255, 255, 0));
        }
        
        /* 状态栏 */
        #glassStatusBar {
            background: rgba(20, 20, 40, 0.9);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: rgba(255, 255, 255, 0.7);
        }
        
        #statusLabel {
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            font-weight: 500;
            padding: 5px 15px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            margin: 0 5px;
        }
        
        /* 滚动条美化 */
        QScrollBar:vertical {
            background: rgba(255, 255, 255, 0.03);
            width: 12px;
            border-radius: 6px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 rgba(0, 255, 255, 0.3),
                stop: 1 rgba(255, 0, 255, 0.3));
            border-radius: 6px;
            min-height: 30px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 rgba(0, 255, 255, 0.5),
                stop: 1 rgba(255, 0, 255, 0.5));
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QScrollBar:horizontal {
            background: rgba(255, 255, 255, 0.03);
            height: 12px;
            border-radius: 6px;
            margin: 2px;
        }
        
        QScrollBar::handle:horizontal {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 rgba(0, 255, 255, 0.3),
                stop: 1 rgba(255, 0, 255, 0.3));
            border-radius: 6px;
            min-width: 30px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                stop: 0 rgba(0, 255, 255, 0.5),
                stop: 1 rgba(255, 0, 255, 0.5));
        }
        
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        """
        
    def resizeEvent(self, event):
        """窗口大小改变时调整背景"""
        super().resizeEvent(event)
        if hasattr(self, 'aurora_bg'):
            self.aurora_bg.resize(self.size())
            
    def setup_connections(self):
        """设置信号连接"""
        self.editor.textChanged.connect(self.on_text_changed)
        self.editor.scrollChanged.connect(self.preview.handle_scroll)
        self.preview.pageChanged.connect(self.on_page_changed)
        self.theme_selector.currentIndexChanged.connect(self.on_theme_changed)
        
        if hasattr(self.preview, 'sizeChanged'):
            self.preview.sizeChanged.connect(self.on_size_changed)
    
    def on_text_changed(self):
        """文本改变时启动计时器"""
        self.update_timer.stop()
        self.update_timer.start()
        self.update_char_count()
        
    def update_preview(self):
        """更新预览"""
        self.update_timer.stop()
        markdown_text = self.editor.get_text()
        self.preview.update_content(markdown_text)
        
    def update_char_count(self):
        """更新字数统计"""
        text = self.editor.get_text()
        char_count = len(text.replace(" ", "").replace("\n", ""))
        self.char_count_label.setText(f"Words: {char_count}")
        
    def on_page_changed(self, current, total):
        """页码改变时更新状态栏"""
        if total > 1:
            self.status_bar.showMessage(f"Page: {current}/{total}", 2000)
            
    def on_theme_changed(self, index):
        """处理主题改变"""
        theme_key = self.theme_selector.currentData()
        if theme_key:
            self.preview.change_theme(theme_key)
            theme_name = self.theme_selector.currentText()
            self.theme_info_label.setText(f"Theme: {theme_name}")
            self.status_bar.showMessage(f"Switched to: {theme_name}", 3000)
            
    def on_size_changed(self, size):
        """处理尺寸改变"""
        size_display = {
            "small": "Small (720×960)",
            "medium": "Medium (1080×1440)",
            "large": "Large (1440×1920)"
        }
        display_name = size_display.get(size, size)
        self.status_bar.showMessage(f"Size: {display_name}", 3000)
        
    def clear_content(self):
        """清空内容"""
        reply = QMessageBox.question(
            self, "Clear Content",
            "Are you sure you want to clear all content?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.editor.editor.clear()
            self.status_bar.showMessage("Content cleared", 2000)
            
    def export_images(self):
        """导出图片"""
        if not self.editor.get_text().strip():
            QMessageBox.warning(
                self, "Warning",
                "No content to export. Please enter some text first.",
                QMessageBox.Ok
            )
            return
        
        folder = QFileDialog.getExistingDirectory(
            self, 
            "Select Export Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            try:
                theme_name = self.theme_selector.currentText()
                self.status_bar.showMessage(f"Exporting images (Theme: {theme_name})...", 0)
                self.preview.export_pages(folder)
                
                QMessageBox.information(
                    self, "Export Successful",
                    f"Images exported successfully to:\n{folder}\n\nTheme: {theme_name}",
                    QMessageBox.Ok
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self, "Export Failed",
                    f"Error during export:\n{str(e)}",
                    QMessageBox.Ok
                )
                self.status_bar.showMessage("Export failed", 3000)
```
 ## 问题说明：

这些警告是因为 Qt 的样式表解析器不支持某些现代 CSS 属性：

### 不支持的属性：
- `backdrop-filter` - 毛玻璃效果（CSS3新特性）
- `transform` - 变换效果
- `transition` - 过渡动画
- `box-shadow` - 阴影效果（部分支持）
- `-webkit-background-clip` - Webkit前缀属性
- `-webkit-text-fill-color` - Webkit前缀属性

### 解决方案：

我已经提供了一个 **Qt兼容版本** 的样式，它：
1. ✅ 移除了所有不支持的 CSS 属性
2. ✅ 使用 Qt 支持的替代方案实现类似效果
3. ✅ 保持了视觉美观度

### 主要调整：
- 用 `rgba()` 半透明背景代替 `backdrop-filter`
- 用 `QGraphicsDropShadowEffect` 代替 CSS `box-shadow`
- 移除了 `transform` 和 `transition` 属性
- 使用 `qlineargradient` 代替渐变文字效果

### 如何应用：

1. **替换 `main_window.py`** 中的 `get_global_styles()` 方法为 `get_global_styles_qt_compatible()`

2. **同样需要更新 `editor_widget.py` 和 `preview_widget.py` 中的样式**，移除不支持的属性。

如果你想要完全消除警告，也需要更新其他组件的样式。不过，**这些警告不影响功能**，只是终端输出不够干净。

### 可选方案：

如果你不介意警告，可以通过以下方式**屏蔽警告输出**：

```python
# 在 main.py 开头添加
import warnings
import logging

# 屏蔽 Qt 样式警告
warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)
```

选择哪种方案取决于你的偏好：
- **方案1**：使用兼容样式（推荐）- 干净的终端输出
- **方案2**：保持原样式 - 更炫酷的视觉效果，但有警告
