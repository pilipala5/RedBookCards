# ============================================
# src/ui/main_window.py - 增强版工具栏
# ============================================
from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QToolBar, QSplitter, QPushButton,
                               QFileDialog, QMessageBox, QStatusBar, QLabel,
                               QGraphicsDropShadowEffect, QComboBox, QFrame,
                               QToolButton, QMenu, QDialog, QTextEdit,
                               QDialogButtonBox, QSpinBox, QGridLayout, QLineEdit)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QSize
from PySide6.QtGui import QAction, QIcon, QColor, QLinearGradient, QPainter, QBrush, QKeySequence, QTextCursor
from src.ui.editor_widget import EditorWidget
from src.ui.preview_widget import PreviewWidget
from src.utils.style_manager import StyleManager
import re

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

class TableDialog(QDialog):
    """插入表格对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📊 插入表格")
        self.setFixedSize(300, 150)
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout(self)
        
        # 行数
        layout.addWidget(QLabel("行数:"), 0, 0)
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(2, 20)
        self.rows_spin.setValue(3)
        layout.addWidget(self.rows_spin, 0, 1)
        
        # 列数
        layout.addWidget(QLabel("列数:"), 1, 0)
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(2, 10)
        self.cols_spin.setValue(3)
        layout.addWidget(self.cols_spin, 1, 1)
        
        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 2, 0, 1, 2)
        
        self.setStyleSheet("""
            QDialog {
                background: rgba(30, 30, 50, 0.95);
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
            QSpinBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)

class LinkDialog(QDialog):
    """插入链接对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔗 插入链接")
        self.setFixedSize(400, 180)
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout(self)
        
        # 链接文字
        layout.addWidget(QLabel("链接文字:"), 0, 0)
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText("输入显示的文字")
        layout.addWidget(self.text_edit, 0, 1)
        
        # 链接地址
        layout.addWidget(QLabel("链接地址:"), 1, 0)
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://example.com")
        layout.addWidget(self.url_edit, 1, 1)
        
        # 按钮
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons, 2, 0, 1, 2)
        
        self.setStyleSheet("""
            QDialog {
                background: rgba(30, 30, 50, 0.95);
            }
            QLabel {
                color: white;
                font-size: 13px;
            }
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px;
                border-radius: 5px;
            }
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)

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
        self.setWindowTitle("✨ 小红书 Markdown 编辑器")
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
        
        # 应用全局样式
        self.setStyleSheet(self.get_global_styles_qt_compatible())
        
        # 创建编辑器和预览组件
        self.editor = EditorWidget()
        self.preview = PreviewWidget()
        
        # 创建增强版工具栏
        toolbar_container = self.create_enhanced_toolbar()
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
        
        # 为组件添加玻璃容器
        editor_container = self.create_glass_container(self.editor, "📝 Markdown 编辑器")
        preview_container = self.create_glass_container(self.preview, "👀 实时预览")
        
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
        
    def create_enhanced_toolbar(self):
        """创建增强版单行工具栏"""
        toolbar_container = QFrame()
        toolbar_container.setObjectName("toolbarContainer")
        toolbar_container.setFixedHeight(55)
        
        main_layout = QHBoxLayout(toolbar_container)
        main_layout.setContentsMargins(15, 8, 15, 8)
        main_layout.setSpacing(15)
        
        # 左侧：基础格式化按钮组
        format_group = QFrame()
        format_group.setObjectName("buttonGroup")
        format_layout = QHBoxLayout(format_group)
        format_layout.setContentsMargins(8, 3, 8, 3)
        format_layout.setSpacing(5)
        
        # 基础格式化按钮
        basic_buttons = [
            ("B", "加粗 (Ctrl+B)", self.insert_bold, True, False),
            ("I", "斜体 (Ctrl+I)", self.insert_italic, False, True),
            ("S", "删除线", self.insert_strikethrough, False, False),
            ("`", "行内代码", self.insert_inline_code, False, False),
            ("⟨⟩", "代码块", self.insert_code_block, False, False),
        ]
        
        for text, tooltip, callback, is_bold, is_italic in basic_buttons:
            btn = QToolButton()
            btn.setText(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setFixedSize(35, 35)
            
            # 设置字体样式
            font = btn.font()
            if is_bold:
                font.setBold(True)
            if is_italic:
                font.setItalic(True)
            btn.setFont(font)
            
            btn.setStyleSheet(self.get_tool_button_style())
            format_layout.addWidget(btn)
        
        main_layout.addWidget(format_group)
        
        # 添加分隔线
        separator1 = self.create_separator()
        main_layout.addWidget(separator1)
        
        # 中间左：标题选择器
        heading_group = QFrame()
        heading_layout = QHBoxLayout(heading_group)
        heading_layout.setContentsMargins(0, 0, 0, 0)
        heading_layout.setSpacing(8)
        
        heading_label = QLabel("标题:")
        heading_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 12px;")
        heading_layout.addWidget(heading_label)
        
        self.heading_selector = QComboBox()
        self.heading_selector.setFixedWidth(100)
        self.heading_selector.addItems([
            "正文",
            "H1 一级标题",
            "H2 二级标题", 
            "H3 三级标题",
            "H4 四级标题",
            "H5 五级标题",
            "H6 六级标题"
        ])
        self.heading_selector.setCurrentIndex(0)
        self.heading_selector.setStyleSheet(self.get_mini_combobox_style())
        heading_layout.addWidget(self.heading_selector)
        
        main_layout.addWidget(heading_group)
        
        # 中间右：列表和链接按钮组
        list_group = QFrame()
        list_group.setObjectName("buttonGroup")
        list_layout = QHBoxLayout(list_group)
        list_layout.setContentsMargins(8, 3, 8, 3)
        list_layout.setSpacing(5)
        
        # 列表和链接按钮
        list_buttons = [
            ("◉", "无序列表", self.insert_unordered_list),
            ("①", "有序列表", self.insert_ordered_list),
            ("🔗", "插入链接", self.insert_link),
            ("🖼", "插入图片", self.insert_image),
            ("📊", "插入表格", self.insert_table),
            (">", "引用", self.insert_quote),
            ("—", "分隔线", self.insert_divider),
        ]
        
        for text, tooltip, callback in list_buttons:
            btn = QToolButton()
            btn.setText(text)
            btn.setToolTip(tooltip)
            btn.clicked.connect(callback)
            btn.setFixedSize(35, 35)
            btn.setStyleSheet(self.get_tool_button_style())
            list_layout.addWidget(btn)
        
        main_layout.addWidget(list_group)
        
        # 添加分隔线
        separator2 = self.create_separator()
        main_layout.addWidget(separator2)
        
        # 操作按钮组
        action_group = QFrame()
        action_group.setObjectName("buttonGroup")
        action_layout = QHBoxLayout(action_group)
        action_layout.setContentsMargins(8, 3, 8, 3)
        action_layout.setSpacing(8)
        
        # 撤销/重做
        undo_btn = QPushButton("↶")
        undo_btn.setToolTip("撤销 (Ctrl+Z)")
        undo_btn.clicked.connect(self.editor.undo)
        undo_btn.setFixedSize(35, 35)
        undo_btn.setStyleSheet(self.get_action_button_style())
        action_layout.addWidget(undo_btn)

        redo_btn = QPushButton("↷")
        redo_btn.setToolTip("重做 (Ctrl+Y)")
        redo_btn.clicked.connect(self.editor.redo)
        redo_btn.setFixedSize(35, 35)
        redo_btn.setStyleSheet(self.get_action_button_style())
        action_layout.addWidget(redo_btn)

        # 清空
        clear_btn = QPushButton("🗑")
        clear_btn.setToolTip("清空所有内容")
        clear_btn.clicked.connect(self.clear_content)
        clear_btn.setFixedSize(35, 35)
        clear_btn.setStyleSheet(self.get_action_button_style())
        action_layout.addWidget(clear_btn)
        
        main_layout.addWidget(action_group)
        
        # 添加弹性空间
        main_layout.addStretch()
        
        # 右侧：主题选择和导出
        right_group = QFrame()
        right_layout = QHBoxLayout(right_group)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(15)
        
        # 主题选择器
        theme_label = QLabel("主题:")
        theme_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 13px;")
        right_layout.addWidget(theme_label)
        
        self.theme_selector = QComboBox()
        self.theme_selector.setFixedWidth(130)
        themes = self.style_manager.get_theme_display_names()
        for key, name in themes.items():
            self.theme_selector.addItem(name, key)
        self.theme_selector.setCurrentText("小红书经典")
        self.theme_selector.setStyleSheet(self.get_combobox_style())
        right_layout.addWidget(self.theme_selector)
        
        # 导出按钮
        self.export_btn = QPushButton("📸 导出图片")
        self.export_btn.clicked.connect(self.export_images)
        self.export_btn.setStyleSheet(self.get_export_button_style())
        right_layout.addWidget(self.export_btn)
        
        main_layout.addWidget(right_group)
        
        # 连接标题选择器信号
        self.heading_selector.currentIndexChanged.connect(self.on_heading_changed)
        
        return toolbar_container
    
    def create_separator(self):
        """创建分隔线"""
        separator = QFrame()
        separator.setFrameStyle(QFrame.VLine | QFrame.Sunken)
        separator.setStyleSheet("background: rgba(255, 255, 255, 0.1);")
        separator.setFixedWidth(1)
        return separator
    
    def get_tool_button_style(self):
        """工具按钮样式"""
        return """
            QToolButton {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                padding: 2px;
            }
            QToolButton:hover {
                background: rgba(0, 255, 136, 0.15);
                border-color: rgba(0, 255, 136, 0.4);
                color: #00ff88;
            }
            QToolButton:pressed {
                background: rgba(0, 255, 136, 0.25);
            }
        """
    
    def get_action_button_style(self):
        """操作按钮样式（更小的尺寸）"""
        return """
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.12);
                border-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.18);
            }
        """
    
    def get_mini_combobox_style(self):
        """迷你下拉框样式"""
        return """
            QComboBox {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 8px;
                border-radius: 6px;
                font-size: 12px;
            }
            QComboBox:hover {
                background: rgba(255, 255, 255, 0.12);
            }
            QComboBox::drop-down {
                border: none;
                width: 16px;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 3px 3px 0 3px;
                border-color: white transparent transparent transparent;
            }
            QComboBox QAbstractItemView {
                background: rgba(30, 30, 50, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                selection-background-color: rgba(0, 255, 136, 0.3);
                padding: 5px;
            }
        """
    
    def get_export_button_style(self):
        """导出按钮样式"""
        return """
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 255, 136, 0.3),
                    stop: 1 rgba(0, 255, 200, 0.3));
                border: 2px solid #00ff88;
                color: #00ff88;
                padding: 8px 20px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 255, 136, 0.4),
                    stop: 1 rgba(0, 255, 200, 0.4));
            }
            QPushButton:pressed {
                background: rgba(0, 255, 136, 0.5);
            }
        """
    
    def get_combobox_style(self):
        """下拉框样式"""
        return """
            QComboBox {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 10px;
                border-radius: 8px;
                font-size: 13px;
            }
            QComboBox:hover {
                background: rgba(255, 255, 255, 0.12);
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-style: solid;
                border-width: 4px 4px 0 4px;
                border-color: white transparent transparent transparent;
            }
            QComboBox QAbstractItemView {
                background: rgba(30, 30, 50, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                selection-background-color: rgba(0, 255, 136, 0.3);
                padding: 5px;
            }
        """
    
    # ===== 编辑器操作方法 =====
    
    def on_heading_changed(self, index):
        """处理标题选择改变"""
        cursor = self.editor.editor.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        
        # 获取当前行文本
        cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
        line_text = cursor.selectedText()
        
        # 移除已有的标题标记
        cleaned_text = line_text.lstrip('#').lstrip()
        
        # 根据选择添加新的标题标记
        if index == 0:  # 正文
            cursor.insertText(cleaned_text)
        else:  # H1-H6
            heading_level = '#' * index
            cursor.insertText(f"{heading_level} {cleaned_text}")
    
    def insert_bold(self):
        """插入粗体标记"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"**{text}**")
        else:
            cursor.insertText("****")
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 2)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_italic(self):
        """插入斜体标记"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"*{text}*")
        else:
            cursor.insertText("**")
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_strikethrough(self):
        """插入删除线标记"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"~~{text}~~")
        else:
            cursor.insertText("~~~~")
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 2)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_inline_code(self):
        """插入行内代码标记"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"`{text}`")
        else:
            cursor.insertText("``")
            cursor.movePosition(QTextCursor.Left, QTextCursor.MoveAnchor, 1)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_code_block(self):
        """插入代码块"""
        cursor = self.editor.editor.textCursor()
        if cursor.hasSelection():
            text = cursor.selectedText()
            cursor.insertText(f"```\n{text}\n```")
        else:
            cursor.insertText("```python\n\n```")
            cursor.movePosition(QTextCursor.Up, QTextCursor.MoveAnchor, 1)
            self.editor.editor.setTextCursor(cursor)
    
    def insert_unordered_list(self):
        """插入无序列表 - 支持多行转换"""
        cursor = self.editor.editor.textCursor()
        
        # 检查是否有选中文本
        if cursor.hasSelection():
            # 获取选中的文本
            selected_text = cursor.selectedText()
            
            # 将段落分隔符转换为换行符（Qt使用特殊字符表示段落）
            lines = selected_text.replace('\u2029', '\n').split('\n')
            
            # 转换每一行为列表项
            list_lines = []
            for line in lines:
                line = line.strip()
                if line:  # 忽略空行
                    # 检查是否已经是列表项
                    if line.startswith('- '):
                        list_lines.append(line)  # 已经是无序列表
                    elif line.startswith('* ') or line.startswith('+ '):
                        # 其他无序列表标记，统一为 -
                        list_lines.append('- ' + line[2:])
                    elif re.match(r'^\d+\.\s', line):
                        # 有序列表，转换为无序
                        list_lines.append('- ' + re.sub(r'^\d+\.\s+', '', line))
                    elif line.startswith('- [ ] ') or line.startswith('- [x] '):
                        # 任务列表，保留内容但改为普通无序列表
                        content = line[6:] if line.startswith('- [ ] ') else line[6:]
                        list_lines.append('- ' + content)
                    else:
                        # 普通文本，添加列表标记
                        list_lines.append('- ' + line)
            
            # 替换选中的文本
            if list_lines:
                cursor.insertText('\n'.join(list_lines))
        else:
            # 没有选中文本，只在当前行添加列表标记
            cursor.movePosition(QTextCursor.StartOfLine)
            
            # 获取当前行文本
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText().strip()
            
            # 检查并转换当前行
            if line_text:
                if not line_text.startswith('- '):
                    # 移除其他列表标记
                    if line_text.startswith('* ') or line_text.startswith('+ '):
                        cursor.insertText('- ' + line_text[2:])
                    elif re.match(r'^\d+\.\s', line_text):
                        cursor.insertText('- ' + re.sub(r'^\d+\.\s+', '', line_text))
                    elif line_text.startswith('- [ ] ') or line_text.startswith('- [x] '):
                        content = line_text[6:]
                        cursor.insertText('- ' + content)
                    else:
                        cursor.insertText('- ' + line_text)
                else:
                    # 已经是无序列表，保持不变
                    cursor.insertText(line_text)
            else:
                # 空行，直接添加列表标记
                cursor.insertText('- ')
    
    def insert_ordered_list(self):
        """插入有序列表 - 支持多行转换"""
        cursor = self.editor.editor.textCursor()
        
        # 检查是否有选中文本
        if cursor.hasSelection():
            # 获取选中的文本
            selected_text = cursor.selectedText()
            
            # 将段落分隔符转换为换行符
            lines = selected_text.replace('\u2029', '\n').split('\n')
            
            # 转换每一行为列表项
            list_lines = []
            list_number = 1
            for line in lines:
                line = line.strip()
                if line:  # 忽略空行
                    # 检查是否已经是列表项
                    if re.match(r'^\d+\.\s', line):
                        # 已经是有序列表，重新编号
                        content = re.sub(r'^\d+\.\s+', '', line)
                        list_lines.append(f"{list_number}. {content}")
                        list_number += 1
                    elif line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
                        # 无序列表，转换为有序
                        list_lines.append(f"{list_number}. {line[2:]}")
                        list_number += 1
                    elif line.startswith('- [ ] ') or line.startswith('- [x] '):
                        # 任务列表，转换为有序列表
                        content = line[6:]
                        list_lines.append(f"{list_number}. {content}")
                        list_number += 1
                    else:
                        # 普通文本，添加列表编号
                        list_lines.append(f"{list_number}. {line}")
                        list_number += 1
            
            # 替换选中的文本
            if list_lines:
                cursor.insertText('\n'.join(list_lines))
        else:
            # 没有选中文本，只在当前行添加列表标记
            cursor.movePosition(QTextCursor.StartOfLine)
            
            # 获取当前行文本
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText().strip()
            
            # 检查并转换当前行
            if line_text:
                if not re.match(r'^\d+\.\s', line_text):
                    # 移除其他列表标记
                    if line_text.startswith('- ') or line_text.startswith('* ') or line_text.startswith('+ '):
                        cursor.insertText('1. ' + line_text[2:])
                    elif line_text.startswith('- [ ] ') or line_text.startswith('- [x] '):
                        content = line_text[6:]
                        cursor.insertText('1. ' + content)
                    else:
                        cursor.insertText('1. ' + line_text)
                else:
                    # 已经是有序列表，保持不变
                    cursor.insertText(line_text)
            else:
                # 空行，直接添加列表标记
                cursor.insertText('1. ')
    
    def insert_task_list(self):
        """插入任务列表 - 支持多行转换"""
        cursor = self.editor.editor.textCursor()
        
        # 检查是否有选中文本
        if cursor.hasSelection():
            # 获取选中的文本
            selected_text = cursor.selectedText()
            
            # 将段落分隔符转换为换行符
            lines = selected_text.replace('\u2029', '\n').split('\n')
            
            # 转换每一行为任务列表项
            list_lines = []
            for line in lines:
                line = line.strip()
                if line:  # 忽略空行
                    # 检查是否已经是任务列表
                    if line.startswith('- [ ] ') or line.startswith('- [x] ') or line.startswith('- [X] '):
                        list_lines.append(line)  # 已经是任务列表，保持不变
                    elif line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
                        # 普通无序列表，转换为任务列表
                        list_lines.append('- [ ] ' + line[2:])
                    elif re.match(r'^\d+\.\s', line):
                        # 有序列表，转换为任务列表
                        content = re.sub(r'^\d+\.\s+', '', line)
                        list_lines.append('- [ ] ' + content)
                    else:
                        # 普通文本，添加任务列表标记
                        list_lines.append('- [ ] ' + line)
            
            # 替换选中的文本
            if list_lines:
                cursor.insertText('\n'.join(list_lines))
        else:
            # 没有选中文本，只在当前行添加任务列表标记
            cursor.movePosition(QTextCursor.StartOfLine)
            
            # 获取当前行文本
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line_text = cursor.selectedText().strip()
            
            # 检查并转换当前行
            if line_text:
                if not (line_text.startswith('- [ ] ') or line_text.startswith('- [x] ')):
                    # 移除其他列表标记
                    if line_text.startswith('- ') or line_text.startswith('* ') or line_text.startswith('+ '):
                        cursor.insertText('- [ ] ' + line_text[2:])
                    elif re.match(r'^\d+\.\s', line_text):
                        content = re.sub(r'^\d+\.\s+', '', line_text)
                        cursor.insertText('- [ ] ' + content)
                    else:
                        cursor.insertText('- [ ] ' + line_text)
                else:
                    # 已经是任务列表，切换选中状态
                    if line_text.startswith('- [ ] '):
                        cursor.insertText('- [x] ' + line_text[6:])
                    else:
                        cursor.insertText('- [ ] ' + line_text[6:])
            else:
                # 空行，直接添加任务列表标记
                cursor.insertText('- [ ] ')
    
    def insert_quote(self):
        """插入引用"""
        cursor = self.editor.editor.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine)
        cursor.insertText("> ")
    
    def insert_divider(self):
        """插入分隔线"""
        self.editor.insertPlainText("\n---\n")
    
    def insert_link(self):
        """插入链接（带对话框）"""
        dialog = LinkDialog(self)
        if dialog.exec():
            text = dialog.text_edit.text() or "链接文字"
            url = dialog.url_edit.text() or "https://example.com"
            self.editor.insertPlainText(f"[{text}]({url})")
    
    def insert_image(self):
        """插入图片"""
        # 弹出文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp *.svg);;All Files (*)"
        )
        
        if file_path:
            # 获取文件名作为替代文本
            import os
            file_name = os.path.basename(file_path)
            
            # 插入图片语法
            cursor = self.editor.editor.textCursor()
            cursor.insertText(f"![{file_name}]({file_path})")
            
            # 提示用户
            self.status_bar.showMessage(f"已插入图片: {file_name}", 3000)
    
    def insert_table(self):
        """插入表格"""
        dialog = TableDialog(self)
        if dialog.exec():
            rows = dialog.rows_spin.value()
            cols = dialog.cols_spin.value()
            
            # 生成表格
            table = []
            
            # 表头
            header = "|"
            for i in range(cols):
                header += f" 列{i+1} |"
            table.append(header)
            
            # 分隔线
            separator = "|"
            for _ in range(cols):
                separator += " --- |"
            table.append(separator)
            
            # 数据行
            for r in range(rows - 1):
                row = "|"
                for c in range(cols):
                    row += f" 数据 |"
                table.append(row)
            
            # 插入表格
            self.editor.insertPlainText("\n" + "\n".join(table) + "\n")
    
    # ===== 其他方法保持不变 =====
    
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
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setOffset(0, 0)
        glow.setColor(QColor(0, 224, 255, 80))
        widget.setGraphicsEffect(glow)
        
        return container
    
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
    
    def get_global_styles_qt_compatible(self):
        """获取Qt兼容的全局样式表"""
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
        
        /* 工具栏容器 */
        #toolbarContainer {
            background: rgba(20, 20, 40, 0.95);
            border-bottom: 2px solid rgba(255, 255, 255, 0.1);
        }
        
        #buttonGroup {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
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
        
        /* 工具提示 */
        QToolTip {
            background: rgba(30, 30, 50, 0.95);
            border: 1px solid rgba(0, 255, 136, 0.5);
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 12px;
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
        # 添加更新锁，防止并发
        if hasattr(self, '_updating') and self._updating:
            return
        
        self.update_timer.stop()
        self.update_timer.start()
        self.update_char_count()
    
    def update_preview(self):
        """更新预览"""
        self._updating = True  # 加锁
        try:
            self.update_timer.stop()
            markdown_text = self.editor.get_text()
            
            # 添加图片检测日志
            img_count = markdown_text.count('![')
            print(f"检测到 {img_count} 个图片标记")
            
            self.preview.update_content(markdown_text)
        finally:
            self._updating = False  # 解锁
    
    def update_char_count(self):
        """更新字数统计"""
        text = self.editor.get_text()
        char_count = len(text.replace(" ", "").replace("\n", ""))
        word_count = len(text.split())
        self.char_count_label.setText(f"字符: {char_count} | 单词: {word_count}")
    
    def on_page_changed(self, current, total):
        """页码改变时更新状态栏"""
        if total > 1:
            self.status_bar.showMessage(f"第 {current}/{total} 页", 2000)
    
    def on_theme_changed(self, index):
        """处理主题改变"""
        theme_key = self.theme_selector.currentData()
        if theme_key:
            self.preview.change_theme(theme_key)
            theme_name = self.theme_selector.currentText()
            self.theme_info_label.setText(f"主题: {theme_name}")
            self.status_bar.showMessage(f"已切换到: {theme_name}", 3000)
    
    def on_size_changed(self, size):
        """处理尺寸改变"""
        size_display = {
            "small": "小 (720×960)",
            "medium": "中 (1080×1440)",
            "large": "大 (1440×1920)"
        }
        display_name = size_display.get(size, size)
        self.status_bar.showMessage(f"尺寸: {display_name}", 3000)
    
    def clear_content(self):
        """清空内容"""
        reply = QMessageBox.question(
            self, "清空内容",
            "确定要清空所有内容吗？\n此操作无法撤销。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.editor.editor.clear()
            self.status_bar.showMessage("✅ 内容已清空", 2000)
    
    def export_images(self):
        """导出图片"""
        if not self.editor.get_text().strip():
            QMessageBox.warning(
                self, "提示",
                "没有内容可导出。请先输入一些文本。",
                QMessageBox.Ok
            )
            return
        
        folder = QFileDialog.getExistingDirectory(
            self, 
            "选择导出文件夹",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        
        if folder:
            try:
                theme_name = self.theme_selector.currentText()
                self.status_bar.showMessage(f"正在导出图片 (主题: {theme_name})...", 0)
                self.preview.export_pages(folder)
                
                QMessageBox.information(
                    self, "导出成功",
                    f"图片已成功导出到:\n{folder}\n\n主题: {theme_name}",
                    QMessageBox.Ok
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self, "导出失败",
                    f"导出过程中出错:\n{str(e)}",
                    QMessageBox.Ok
                )
                self.status_bar.showMessage("❌ 导出失败", 3000)