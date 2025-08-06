# ============================================
# src/ui/preview_widget.py
# ============================================
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, 
                               QPushButton, QHBoxLayout, QProgressDialog,
                               QMessageBox)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, QTimer, Signal, Qt
from pathlib import Path
from src.core.markdown_processor import MarkdownProcessor
from src.core.html_generator import HTMLGenerator
from src.utils.paginator import SmartPaginator
from src.utils.exporter import ImageExporter

class PreviewWidget(QWidget):
    pageChanged = Signal(int, int)  # 当前页，总页数
    
    def __init__(self):
        super().__init__()
        self.current_pages = []  # 存储分页后的HTML内容
        self.current_page = 1
        self.total_pages = 1
        self.markdown_text = ""  # 保存原始markdown文本
        self.init_ui()
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
        self.prev_btn.setStyleSheet(self.get_button_style())
        
        self.next_btn = QPushButton("下一页 ➡")
        self.next_btn.setFixedSize(120, 36)
        self.next_btn.setStyleSheet(self.get_button_style())
        
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
        self.paginator = SmartPaginator()
        
        # 连接信号
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)
        
        # 初始化按钮状态
        self.update_buttons()
    
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
            
            # 更新按钮和页码
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
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < self.total_pages)
    
    def update_page_info(self):
        """更新页码信息"""
        self.page_label.setText(f"第 {self.current_page}/{self.total_pages} 页")
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
        
        # 开始导出
        self.exporter.export_pages(
            self.current_pages,
            folder,
            self.html_generator,
            format="PNG",
            quality=100
        )
    
    def on_export_progress(self, current: int, total: int):
        """处理导出进度"""
        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.setValue(current)
            self.progress_dialog.setLabelText(f"正在导出第 {current}/{total} 页...")
    
    def on_export_finished(self, success: bool, message: str):
        """处理导出完成"""
        # 安全地关闭和删除进度对话框
        if hasattr(self, 'progress_dialog') and self.progress_dialog is not None:
            try:
                self.progress_dialog.close()
                self.progress_dialog.deleteLater()
            except:
                pass
            finally:
                self.progress_dialog = None
        
        if success:
            QMessageBox.information(self, "导出成功", message)
        else:
            QMessageBox.warning(self, "导出失败", message)
    
    def on_page_exported(self, page_num: int, file_path: str):
        """处理单页导出完成"""
        print(f"已导出第 {page_num} 页: {file_path}")
    
    def on_export_canceled(self):
        """处理导出取消"""
        self.exporter.cancel_export()
    
    def handle_scroll(self, percentage: float):
        """处理编辑器滚动同步"""
        # 通过JavaScript同步滚动
        script = f"""
        (function() {{
            var content = document.getElementById('content');
            if (content) {{
                content.scrollTop = content.scrollHeight * {percentage};
            }}
        }})();
        """
        self.web_view.page().runJavaScript(script)
    
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