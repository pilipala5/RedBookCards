# ============================================
# src/ui/preview_widget.py - Qt兼容优化版（修复导出后模式问题）
# ============================================
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                               QPushButton, QHBoxLayout, QProgressDialog,
                               QMessageBox, QComboBox, QButtonGroup, QRadioButton,
                               QScrollArea)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Signal, Qt, QSize, QEvent
from PySide6.QtGui import QWheelEvent, QFont
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
        self._is_exporting = False  # 添加导出状态标志
        
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
        
        # 创建容器框架 - 移除重复的标题栏
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # 创建顶部控制栏（包含尺寸和模式选择）
        top_control_bar = self.create_top_control_bar()
        
        # 创建WebView容器
        self.create_web_view_container()
        
        # 创建底部导航控制栏
        bottom_control_bar = self.create_bottom_control_bar()
        
        # 组装布局
        container_layout.addWidget(top_control_bar)
        container_layout.addWidget(self.web_container, 1)
        container_layout.addWidget(bottom_control_bar)
        
        layout.addWidget(container)
        
        # 连接信号
        self.connect_signals()
        
        # 初始化按钮状态
        self.update_buttons()
    
    def create_top_control_bar(self):
        """创建顶部控制栏 - Qt兼容样式"""
        control_bar = QFrame()
        control_bar.setFixedHeight(50)
        control_bar.setStyleSheet("""
            QFrame {
                background: rgba(30, 30, 50, 0.8);
                border-bottom: 1px solid rgba(255, 255, 255, 0.15);
                border-top-left-radius: 16px;
                border-top-right-radius: 16px;
            }
        """)
        
        layout = QHBoxLayout(control_bar)
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(20)
        
        # 尺寸选择部分
        size_container = QWidget()
        size_layout = QHBoxLayout(size_container)
        size_layout.setContentsMargins(0, 0, 0, 0)
        size_layout.setSpacing(10)
        
        size_label = QLabel("尺寸:")
        size_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 13px;
                font-weight: 500;
            }
        """)
        
        self.size_selector = QComboBox()
        self.size_selector.addItems(["Small (720×960)", "Medium (1080×1440)", "Large (1440×1920)"])
        self.size_selector.setCurrentIndex(1)
        self.size_selector.setFixedWidth(160)
        self.size_selector.setStyleSheet(self.get_combobox_style_qt())
        
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_selector)
        
        # 预览模式部分
        mode_container = QWidget()
        mode_layout = QHBoxLayout(mode_container)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_layout.setSpacing(10)
        
        mode_label = QLabel("模式:")
        mode_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 13px;
                font-weight: 500;
            }
        """)
        
        self.mode_group = QButtonGroup()
        
        self.fit_mode_btn = QRadioButton("适应窗口")
        self.fit_mode_btn.setChecked(True)
        self.fit_mode_btn.setStyleSheet(self.get_radio_style_qt())
        
        self.actual_mode_btn = QRadioButton("实际大小")
        self.actual_mode_btn.setStyleSheet(self.get_radio_style_qt())
        
        self.mode_group.addButton(self.fit_mode_btn, 0)
        self.mode_group.addButton(self.actual_mode_btn, 1)
        
        mode_layout.addWidget(mode_label)
        mode_layout.addWidget(self.fit_mode_btn)
        mode_layout.addWidget(self.actual_mode_btn)
        
        # 组装顶部控制栏
        layout.addWidget(size_container)
        layout.addSpacing(30)
        layout.addWidget(mode_container)
        layout.addStretch()
        
        return control_bar
    
    def create_web_view_container(self):
        """创建WebView容器 - Qt兼容样式"""
        # 使用自定义滚动区域
        self.web_container = CustomScrollArea()
        self.web_container.preview_widget = self  # 设置引用
        
        self.web_container.setStyleSheet("""
            QScrollArea {
                border: none;
                background: rgba(20, 20, 40, 0.4);
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
    
    def create_bottom_control_bar(self):
        """创建底部导航控制栏 - Qt兼容样式"""
        control_bar = QFrame()
        control_bar.setFixedHeight(60)
        control_bar.setStyleSheet("""
            QFrame {
                background: rgba(20, 20, 40, 0.8);
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
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
        self.prev_btn.setStyleSheet(self.get_button_style_qt())
        
        # 页面信息标签
        self.page_info_label = QLabel("Page 1")
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
            }
        """)
        self.page_info_label.setAlignment(Qt.AlignCenter)
        
        # 下一页按钮
        self.next_btn = QPushButton("Next ➡")
        self.next_btn.setFixedSize(110, 36)
        self.next_btn.setStyleSheet(self.get_button_style_qt())
        
        # 组装中心控制区
        center_layout.addWidget(self.prev_btn)
        center_layout.addWidget(self.page_info_label)
        center_layout.addWidget(self.next_btn)
        
        # 快捷提示
        tips_label = QLabel("💡 滚轮：上下导航 • Shift+滚轮：左右滚动")
        tips_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 11px;
                font-style: italic;
                background: transparent;
            }
        """)
        tips_label.setFont(QFont("Arial", 10))
        
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
        # 如果正在导出，不允许切换模式
        if self._is_exporting:
            return
            
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
            self.show_error(f"Preview error: {str(e)}")
    
    def display_current_page(self):
        """显示当前页"""
        # 如果正在导出，不更新显示
        if self._is_exporting:
            return
            
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
            self.page_info_label.setText(f"Page {self.current_page} / {self.total_pages}")
        else:
            self.page_info_label.setText("Page 1")
    
    def get_button_style_qt(self) -> str:
        """获取按钮样式 - Qt兼容版本"""
        return """
            QPushButton {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.25);
                color: rgba(255, 255, 255, 0.95);
                padding: 10px 20px;
                border-radius: 18px;
                font-weight: 600;
                font-size: 13px;
                letter-spacing: 0.5px;
            }
            
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(0, 255, 136, 0.5);
                color: #00ff88;
            }
            
            QPushButton:pressed {
                background: rgba(0, 255, 136, 0.2);
            }
            
            QPushButton:disabled {
                background: rgba(255, 255, 255, 0.02);
                border-color: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }
        """
    
    def get_combobox_style_qt(self) -> str:
        """获取下拉框样式 - Qt兼容版本"""
        return """
            QComboBox {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: rgba(255, 255, 255, 0.95);
                padding: 8px 15px;
                border-radius: 10px;
                font-size: 12px;
                font-weight: 500;
                letter-spacing: 0.3px;
            }
            
            QComboBox:hover {
                background: rgba(255, 255, 255, 0.12);
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
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                selection-background-color: rgba(0, 255, 136, 0.3);
                outline: none;
                padding: 5px;
                border-radius: 8px;
            }
            
            QComboBox QAbstractItemView::item {
                min-height: 32px;
                padding: 8px 12px;
                border-radius: 4px;
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
    
    def get_radio_style_qt(self) -> str:
        """获取单选按钮样式 - Qt兼容版本"""
        return """
            QRadioButton {
                color: rgba(255, 255, 255, 0.85);
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
            QMessageBox.warning(self, "Warning", "No content to export")
            return
        
        # 保存当前状态
        self._is_exporting = True
        self._saved_preview_mode = self.preview_mode
        self._saved_current_page = self.current_page
        
        # 创建进度对话框
        self.progress_dialog = QProgressDialog(
            "Exporting images...", 
            "Cancel", 
            0, 
            self.total_pages, 
            self
        )
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setAutoClose(False)
        self.progress_dialog.setAutoReset(False)
        
        # 设置进度对话框样式
        self.progress_dialog.setStyleSheet("""
            QProgressDialog {
                background: rgba(30, 30, 50, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                color: white;
            }
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 rgba(0, 255, 136, 0.6),
                    stop: 1 rgba(0, 255, 255, 0.6));
                border-radius: 4px;
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
            self.progress_dialog.setLabelText(f"Exporting page {current}/{total}...")
    
    def on_export_finished(self, success: bool, message: str):
        """处理导出完成"""
        # 重置导出状态
        self._is_exporting = False
        
        # 关闭进度对话框
        if hasattr(self, 'progress_dialog') and self.progress_dialog:
            try:
                self.progress_dialog.canceled.disconnect()
                self.progress_dialog.close()
                self.progress_dialog.deleteLater()
            except:
                pass
            finally:
                self.progress_dialog = None
        
        # 恢复之前的预览模式
        if hasattr(self, '_saved_preview_mode'):
            if self._saved_preview_mode == "fit":
                self.fit_mode_btn.setChecked(True)
                self.preview_mode = "fit"
                # 恢复适应窗口模式设置
                self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.web_container.setWidgetResizable(True)
                self.web_view.setMinimumSize(0, 0)
                self.web_view.setMaximumSize(16777215, 16777215)
                self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            else:
                self.actual_mode_btn.setChecked(True)
                self.preview_mode = "actual"
                # 恢复实际大小模式设置
                self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.web_container.setWidgetResizable(False)
                self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        # 恢复到之前的页面
        if hasattr(self, '_saved_current_page'):
            self.go_to_page(self._saved_current_page)
        
        # 显示结果消息
        if success:
            size_info = f"({self.current_size}: {self.get_actual_size()}px)"
            QMessageBox.information(self, "Export Successful", f"{message}\nSize: {size_info}")
        else:
            QMessageBox.warning(self, "Export Failed", message)
    
    def on_page_exported(self, page_num: int, file_path: str):
        """处理单页导出完成"""
        print(f"Exported page {page_num}: {file_path}")
    
    def on_export_canceled(self):
        """处理导出取消"""
        self.exporter.cancel_export()
        # 重置导出状态
        self._is_exporting = False
        
        # 恢复之前的预览模式
        if hasattr(self, '_saved_preview_mode'):
            if self._saved_preview_mode == "fit":
                self.fit_mode_btn.setChecked(True)
                self.preview_mode = "fit"
                self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.web_container.setWidgetResizable(True)
                self.web_view.setMinimumSize(0, 0)
                self.web_view.setMaximumSize(16777215, 16777215)
                self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            else:
                self.actual_mode_btn.setChecked(True)
                self.preview_mode = "actual"
                self.web_container.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.web_container.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                self.web_container.setWidgetResizable(False)
                self.web_view.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        # 恢复到之前的页面
        if hasattr(self, '_saved_current_page'):
            self.go_to_page(self._saved_current_page)
    
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
            <h3 style="color: #ff4757;">Error</h3>
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