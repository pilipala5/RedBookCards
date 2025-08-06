# ============================================
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
            event.accept()