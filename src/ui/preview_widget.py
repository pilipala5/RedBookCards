# ============================================
# src/ui/preview_widget.py
# ============================================
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                               QPushButton, QHBoxLayout, QProgressDialog,
                               QMessageBox, QScrollArea, QSlider, QComboBox)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Signal, Qt, QSize
from pathlib import Path
from src.core.markdown_processor import MarkdownProcessor
from src.core.html_generator import HTMLGenerator
from src.utils.paginator import SmartPaginator
from src.utils.exporter import ImageExporter

class PreviewWidget(QWidget):
    pageChanged = Signal(int, int)  # 当前页，总页数
    sizeChanged = Signal(str)  # 尺寸改变信号
    
    def __init__(self):
        super().__init__()
        self.current_pages = []  # 存储分页后的HTML内容
        self.current_page = 1
        self.total_pages = 1
        self.markdown_text = ""  # 保存原始markdown文本
        self.current_zoom = 1.0  # 当前缩放比例
        self.current_size = "medium"  # 当前页面尺寸
        
        # 初始化处理器
        self.markdown_processor = MarkdownProcessor()
        self.html_generator = HTMLGenerator(page_size="medium")
        self.paginator = SmartPaginator(page_size="medium")
        
        # 初始化UI
        self.init_ui()
        
        # 设置导出器
        self.setup_exporter()
        
        # 延迟设置初始缩放，确保所有组件都已初始化
        QTimer.singleShot(500, self.zoom_to_100)
        
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
        
        # 创建滚动区域和WebView
        self.create_web_view()
        
        # 创建控制栏
        control_bar = self.create_control_bar()
        
        # 组装布局
        container_layout.addWidget(title_bar)
        container_layout.addWidget(self.scroll_area, 1)
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
        
        # 使用水平布局，设置正确的边距
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(20, 5, 20, 5)
        title_layout.setSpacing(10)
        
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
        self.size_selector.setStyleSheet("""
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
        """)
        
        # 页面信息标签
        self.page_info_label = QLabel("")
        self.page_info_label.setStyleSheet("""
            QLabel {
                color: #8a92a6;
                font-size: 12px;
                padding: 0 10px;
                background: transparent;
            }
        """)
        
        # 缩放显示标签
        self.zoom_label = QLabel("100%")
        self.zoom_label.setStyleSheet("""
            QLabel {
                color: #8a92a6;
                font-size: 12px;
                padding: 0 10px;
                background: transparent;
            }
        """)
        
        # 组装标题栏
        title_layout.addWidget(title)
        title_layout.addSpacing(20)
        title_layout.addWidget(size_label)
        title_layout.addWidget(self.size_selector)
        title_layout.addWidget(self.page_info_label)
        title_layout.addStretch()
        title_layout.addWidget(self.zoom_label)
        
        return title_bar
    
    def create_web_view(self):
        """创建WebView和滚动区域"""
        # 创建滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: #1a1a2e;
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
        
        # 创建容器widget
        self.web_container = QWidget()
        self.web_container.setStyleSheet("""
            QWidget {
                background: #1a1a2e;
            }
        """)
        
        # 创建WebView
        self.web_view = QWebEngineView(self.web_container)
        self.update_web_view_size()
        self.web_view.setStyleSheet("""
            QWebEngineView {
                border: none;
                background: white;
            }
        """)
        
        # 禁用WebView的滚动条
        self.web_view.page().settings().setAttribute(
            self.web_view.page().settings().WebAttribute.ShowScrollBars, False
        )
        
        # 设置滚动区域
        self.scroll_area.setWidget(self.web_container)
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    
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
        
        # 使用水平布局，设置边距
        control_layout = QHBoxLayout(control_bar)
        control_layout.setContentsMargins(20, 12, 20, 12)
        control_layout.setSpacing(15)
        
        # 上一页按钮
        self.prev_btn = QPushButton("⬅ 上一页")
        self.prev_btn.setFixedSize(100, 36)
        self.prev_btn.setStyleSheet(self.get_button_style())
        
        # 缩放标签
        zoom_text_label = QLabel("缩放:")
        zoom_text_label.setStyleSheet("""
            QLabel {
                color: #8a92a6;
                font-size: 13px;
                background: transparent;
            }
        """)
        
        # 缩放滑块
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(25, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(200)
        self.zoom_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(0, 224, 255, 0.2);
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                width: 18px;
                height: 18px;
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #00e0ff,
                    stop: 1 #0096ff
                );
                border-radius: 9px;
                margin: -6px 0;
            }
            QSlider::handle:horizontal:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #00f0ff,
                    stop: 1 #00a6ff
                );
            }
        """)
        
        # 缩放100%按钮
        self.zoom_100_btn = QPushButton("📐 100%")
        self.zoom_100_btn.setFixedSize(80, 36)
        self.zoom_100_btn.setStyleSheet(self.get_button_style())
        
        # 下一页按钮
        self.next_btn = QPushButton("下一页 ➡")
        self.next_btn.setFixedSize(100, 36)
        self.next_btn.setStyleSheet(self.get_button_style())
        
        # 组装控制栏 - 居中布局
        control_layout.addWidget(self.prev_btn)
        control_layout.addStretch(1)
        control_layout.addWidget(zoom_text_label)
        control_layout.addWidget(self.zoom_slider)
        control_layout.addWidget(self.zoom_100_btn)
        control_layout.addStretch(1)
        control_layout.addWidget(self.next_btn)
        
        return control_bar
    
    def connect_signals(self):
        """连接信号"""
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        self.zoom_100_btn.clicked.connect(self.zoom_to_100)
        self.size_selector.currentIndexChanged.connect(self.on_size_changed)
    
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
    
    def on_size_changed(self, index):
        """处理尺寸改变"""
        size_map = {0: "small", 1: "medium", 2: "large"}
        new_size = size_map.get(index, "medium")
        
        if new_size != self.current_size:
            self.current_size = new_size
            
            # 更新各组件的尺寸设置
            self.html_generator = HTMLGenerator(page_size=new_size)
            self.paginator.set_page_size(new_size)
            
            # 更新WebView尺寸并居中
            self.update_web_view_size()
            self.center_web_view()
            
            # 重新处理内容
            if self.markdown_text:
                self.update_content(self.markdown_text)
            
            # 发送尺寸改变信号
            self.sizeChanged.emit(new_size)
    
    def update_web_view_size(self):
        """更新WebView尺寸"""
        size_config = {
            "small": (720, 960),
            "medium": (1080, 1440),
            "large": (1440, 1920)
        }
        width, height = size_config.get(self.current_size, (1080, 1440))
        self.web_view.setFixedSize(width, height)
        
        # 更新容器大小以适应缩放后的尺寸
        self.update_container_size()
    
    def update_container_size(self):
        """更新容器大小以适应缩放后的WebView"""
        # 获取缩放后的实际大小
        scaled_width = int(self.web_view.width() * self.current_zoom)
        scaled_height = int(self.web_view.height() * self.current_zoom)
        
        # 获取滚动区域的可视大小
        viewport_size = self.scroll_area.viewport().size()
        
        # 设置容器大小，确保至少和视口一样大（用于居中）
        container_width = max(scaled_width + 40, viewport_size.width())
        container_height = max(scaled_height + 40, viewport_size.height())
        
        self.web_container.setFixedSize(container_width, container_height)
        
        # 居中WebView
        self.center_web_view()
    
    def center_web_view(self):
        """将WebView在容器中居中"""
        # 计算居中位置
        container_width = self.web_container.width()
        container_height = self.web_container.height()
        
        scaled_width = int(self.web_view.width() * self.current_zoom)
        scaled_height = int(self.web_view.height() * self.current_zoom)
        
        x = (container_width - scaled_width) // 2
        y = (container_height - scaled_height) // 2
        
        # 确保不会是负数
        x = max(0, x)
        y = max(0, y)
        
        self.web_view.move(x, y)
    
    def on_zoom_changed(self, value):
        """处理缩放滑块变化"""
        zoom = value / 100.0
        self.set_zoom(zoom)
    
    def set_zoom(self, zoom_factor):
        """设置缩放比例"""
        try:
            self.current_zoom = zoom_factor
            self.web_view.setZoomFactor(zoom_factor)
            
            # 安全更新zoom_label
            if hasattr(self, 'zoom_label') and self.zoom_label:
                self.zoom_label.setText(f"{int(zoom_factor * 100)}%")
            
            # 安全更新滑块值
            if hasattr(self, 'zoom_slider') and self.zoom_slider:
                self.zoom_slider.blockSignals(True)
                self.zoom_slider.setValue(int(zoom_factor * 100))
                self.zoom_slider.blockSignals(False)
            
            # 更新容器大小和位置
            self.update_container_size()
        except RuntimeError:
            # 如果组件已被删除，忽略错误
            pass
    
    def zoom_to_100(self):
        """恢复100%大小"""
        try:
            # 确保组件存在后再设置缩放
            if hasattr(self, 'web_view') and self.web_view:
                self.set_zoom(1.0)
        except RuntimeError:
            # 组件可能还未完全初始化，忽略错误
            pass
    
    def resizeEvent(self, event):
        """窗口大小改变时更新居中"""
        super().resizeEvent(event)
        # 延迟执行，确保布局已更新
        QTimer.singleShot(10, self.update_container_size)
    
    def setup_exporter(self):
        """设置导出器"""
        self.exporter = ImageExporter(self.web_view)
        self.exporter.progress.connect(self.on_export_progress)
        self.exporter.finished.connect(self.on_export_finished)
        self.exporter.page_exported.connect(self.on_page_exported)
    
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
            
            # 更新按钮
            self.update_buttons()
            
            # 更新页面信息
            self.update_page_info()
            
            # 保持当前缩放比例
            QTimer.singleShot(100, lambda: self.set_zoom(self.current_zoom))
            
        except Exception as e:
            self.show_error(f"预览错误: {str(e)}")
    
    def update_page_info(self):
        """更新页面信息显示"""
        if hasattr(self, 'page_info_label') and self.page_info_label:
            if self.total_pages > 1:
                self.page_info_label.setText(f"第 {self.current_page}/{self.total_pages} 页")
            else:
                self.page_info_label.setText("")
    
    def display_current_page(self):
        """显示当前页"""
        if not self.current_pages:
            return
            
        if 1 <= self.current_page <= len(self.current_pages):
            page_content = self.current_pages[self.current_page - 1]
            
            # 生成完整HTML
            full_html = self.html_generator.generate(page_content)
            
            # 加载到WebView
            self.web_view.setHtml(full_html, QUrl("file:///"))
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_current_page()
            self.update_buttons()
            self.update_page_info()
    
    def next_page(self):
        """下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.display_current_page()
            self.update_buttons()
            self.update_page_info()
    
    def update_buttons(self):
        """更新按钮状态"""
        if hasattr(self, 'prev_btn') and self.prev_btn:
            self.prev_btn.setEnabled(self.current_page > 1)
        if hasattr(self, 'next_btn') and self.next_btn:
            self.next_btn.setEnabled(self.current_page < self.total_pages)
        
        # 发送页面改变信号
        self.pageChanged.emit(self.current_page, self.total_pages)
    
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
        self.progress_dialog.canceled.connect(self.on_export_canceled)
        
        # 导出前恢复100%大小（确保导出的是原始尺寸）
        original_zoom = self.current_zoom
        self.web_view.setZoomFactor(1.0)
        
        # 开始导出
        self.exporter.export_pages(
            self.current_pages,
            folder,
            self.html_generator,
            format="PNG",
            quality=100
        )
        
        # 保存原始缩放比例，导出完成后恢复
        self._original_zoom_for_export = original_zoom
    
    def on_export_progress(self, current: int, total: int):
        """处理导出进度"""
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            self.progress_dialog.setValue(current)
            self.progress_dialog.setLabelText(f"正在导出第 {current}/{total} 页...")
    
    def on_export_finished(self, success: bool, message: str):
        """处理导出完成"""
        # 关闭进度对话框
        if hasattr(self, 'progress_dialog') and self.progress_dialog is not None:
            try:
                self.progress_dialog.close()
                self.progress_dialog.deleteLater()
            except:
                pass
            finally:
                self.progress_dialog = None
        
        # 恢复原始缩放比例
        if hasattr(self, '_original_zoom_for_export'):
            self.set_zoom(self._original_zoom_for_export)
            delattr(self, '_original_zoom_for_export')
        
        if success:
            # 添加尺寸信息到消息中
            size_info = f"({self.current_size}: {self.web_view.width()}×{self.web_view.height()}px)"
            QMessageBox.information(self, "导出成功", f"{message}\n尺寸: {size_info}")
        else:
            QMessageBox.warning(self, "导出失败", message)
    
    def on_page_exported(self, page_num: int, file_path: str):
        """处理单页导出完成"""
        print(f"已导出第 {page_num} 页: {file_path}")
    
    def on_export_canceled(self):
        """处理导出取消"""
        self.exporter.cancel_export()
        # 恢复原始缩放
        if hasattr(self, '_original_zoom_for_export'):
            self.set_zoom(self._original_zoom_for_export)
            delattr(self, '_original_zoom_for_export')
    
    def handle_scroll(self, percentage: float):
        """处理编辑器滚动同步"""
        # 固定尺寸，不需要滚动同步
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