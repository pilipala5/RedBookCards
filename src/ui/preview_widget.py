# ============================================
# src/ui/preview_widget.py
# ============================================
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QHBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Signal, Qt
from PySide6.QtGui import QImage, QPainter
import os
from pathlib import Path
from src.core.markdown_processor import MarkdownProcessor
from src.core.html_generator import HTMLGenerator

class PreviewWidget(QWidget):
    pageChanged = Signal(int, int)  # 当前页，总页数
    
    def __init__(self):
        super().__init__()
        self.current_pages = []
        self.current_page = 1
        self.total_pages = 1
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
        title_layout = QHBoxLayout(title_bar)
        
        title = QLabel("👀 实时预览")
        title.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.5px;
            }
        """)
        
        # 页码显示
        self.page_label = QLabel("第 1/1 页")
        self.page_label.setStyleSheet("""
            QLabel {
                color: #00e0ff;
                font-size: 13px;
                font-weight: 500;
                padding: 5px 15px;
                background: rgba(0, 224, 255, 0.1);
                border: 1px solid rgba(0, 224, 255, 0.3);
                border-radius: 15px;
            }
        """)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(self.page_label)
        
        # Web视图
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("""
            QWebEngineView {
                border: none;
                background: rgba(15, 15, 25, 0.6);
            }
        """)
        
        # 翻页控制栏
        control_bar = QFrame()
        control_bar.setFixedHeight(60)
        control_bar.setStyleSheet("""
            QFrame {
                background: rgba(20, 20, 35, 0.8);
                padding: 10px 20px;
                border-bottom-left-radius: 16px;
                border-bottom-right-radius: 16px;
                border-top: 1px solid rgba(0, 224, 255, 0.1);
            }
        """)
        control_layout = QHBoxLayout(control_bar)
        
        self.prev_btn = QPushButton("⬅ 上一页")
        self.prev_btn.setFixedSize(120, 36)
        self.prev_btn.setStyleSheet("""
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
        """)
        
        self.next_btn = QPushButton("下一页 ➡")
        self.next_btn.setFixedSize(120, 36)
        self.next_btn.setStyleSheet("""
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
        """)
        
        control_layout.addWidget(self.prev_btn)
        control_layout.addStretch()
        control_layout.addWidget(self.next_btn)
        
        # 组装布局
        container_layout.addWidget(title_bar)
        container_layout.addWidget(self.web_view, 1)
        container_layout.addWidget(control_bar)
        
        layout.addWidget(container)
        
        # 处理器
        self.markdown_processor = MarkdownProcessor()
        self.html_generator = HTMLGenerator()
        
        # 连接信号
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        
        # 初始化按钮状态
        self.update_buttons()
        
    def update_content(self, markdown_text: str):
        """更新预览内容"""
        try:
            # 处理 Markdown
            html_content = self.markdown_processor.parse(markdown_text)
            
            # 生成完整HTML
            full_html = self.html_generator.generate(html_content)
            
            # 加载到WebView
            self.web_view.setHtml(full_html, QUrl("file:///"))
            
            # 保存当前页面（用于导出）
            self.current_html = full_html
            
            # 更新页码显示
            self.update_page_info()
            
        except Exception as e:
            error_html = f"""
            <html>
            <body style="padding: 20px; font-family: sans-serif; background: #1a1a2e; color: #e0e6ed;">
                <h3 style="color: #ff4757;">预览错误</h3>
                <p style="color: #8a92a6;">{str(e)}</p>
            </body>
            </html>
            """
            self.web_view.setHtml(error_html)
    
    def prev_page(self):
        """上一页"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_page_display()
            self.update_buttons()
    
    def next_page(self):
        """下一页"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_page_display()
            self.update_buttons()
    
    def update_page_display(self):
        """更新页面显示（预留接口）"""
        # 这里可以实现真正的分页逻辑
        pass
    
    def update_buttons(self):
        """更新按钮状态"""
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)
    
    def update_page_info(self):
        """更新页码信息"""
        self.page_label.setText(f"第 {self.current_page}/{self.total_pages} 页")
        self.pageChanged.emit(self.current_page, self.total_pages)
    
    def export_pages(self, folder: str):
        """导出页面为图片"""
        page = self.web_view.page()
        
        # 设置页面大小为小红书卡片尺寸（1080x1440）
        page.setViewportSize(page.contentsSize().toSize())
        
        # 创建保存路径
        save_path = Path(folder) / f"card_{self.current_page:02d}.png"
        
        # 截图并保存
        def save_screenshot(pixmap):
            # 创建小红书尺寸的图片
            target_image = QImage(1080, 1440, QImage.Format_ARGB32)
            target_image.fill(Qt.white)
            
            # 绘制内容
            painter = QPainter(target_image)
            scaled_pixmap = pixmap.scaled(
                1080, 1440,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            # 居中绘制
            x = (1080 - scaled_pixmap.width()) // 2
            y = (1440 - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
            painter.end()
            
            # 保存
            target_image.save(str(save_path), "PNG", 100)
            
        page.grabToImage(save_screenshot)
    
    def handle_scroll(self, percentage: float):
        """处理编辑器滚动同步"""
        # 通过JavaScript同步滚动
        script = f"""
        var content = document.getElementById('content');
        if (content) {{
            content.scrollTop = content.scrollHeight * {percentage};
        }}
        """
        self.web_view.page().runJavaScript(script)