# ============================================
# src/ui/editor_widget.py
# ============================================
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget, QLabel, QFrame
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
                padding: 12px 20px;
            }
        """)
        title_layout = QVBoxLayout(title_bar)
        
        title = QLabel("✍️ Markdown 编辑器")
        title.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
        """)
        title_layout.addWidget(title)
        
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
            self.scrollChanged.emit(percentage)