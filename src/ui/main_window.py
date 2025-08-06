# ============================================
# src/ui/main_window.py
# ============================================
from PySide6.QtWidgets import (QMainWindow, QHBoxLayout, QVBoxLayout, 
                               QWidget, QToolBar, QSplitter, QPushButton,
                               QFileDialog, QMessageBox, QStatusBar, QLabel,
                               QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QIcon, QColor
from src.ui.editor_widget import EditorWidget
from src.ui.preview_widget import PreviewWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 先创建自动更新计时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_preview)
        self.update_timer.setInterval(300)  # 300ms延迟
        
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
        self.status_bar.showMessage(f"页面: {current}/{total}", 2000)
        
    def clear_content(self):
        """清空内容"""
        reply = QMessageBox.question(
            self, "确认清空",
            "确定要清空所有内容吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.editor.editor.clear()
            
    def export_images(self):
        """导出图片"""
        folder = QFileDialog.getExistingDirectory(self, "选择导出文件夹")
        if folder:
            try:
                self.preview.export_pages(folder)
                QMessageBox.information(
                    self, "导出成功",
                    f"图片已成功导出到:\n{folder}",
                    QMessageBox.Ok
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "导出失败",
                    f"导出过程中出现错误:\n{str(e)}",
                    QMessageBox.Ok
                )