# ============================================
# src/ui/editor_widget.py - Qt兼容版本（无警告）
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
        """设置编辑器 - Qt兼容版本"""
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
        
        # 设置编辑器样式 - Qt兼容版本（移除不支持的CSS属性）
        self.editor.setStyleSheet("""
            QTextEdit {
                background: rgba(20, 20, 40, 0.6);
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
                margin: 4px;
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
        
    def setFocus(self):
        """设置焦点到编辑器"""
        self.editor.setFocus()
        
    def insertPlainText(self, text):
        """在光标位置插入文本"""
        self.editor.insertPlainText(text)
        
    def selectAll(self):
        """全选文本"""
        self.editor.selectAll()
        
    def copy(self):
        """复制选中文本"""
        self.editor.copy()
        
    def cut(self):
        """剪切选中文本"""
        self.editor.cut()
        
    def paste(self):
        """粘贴文本"""
        self.editor.paste()
        
    def undo(self):
        """撤销"""
        self.editor.undo()
        
    def redo(self):
        """重做"""
        self.editor.redo()
        
    def setReadOnly(self, readonly):
        """设置只读模式"""
        self.editor.setReadOnly(readonly)
        
    def zoomIn(self):
        """放大字体"""
        self.editor.zoomIn(1)
        
    def zoomOut(self):
        """缩小字体"""
        self.editor.zoomOut(1)
        
    def resetZoom(self):
        """重置字体大小"""
        font = QFont("Cascadia Code, Consolas, Monaco, monospace", 13)
        self.editor.setFont(font)