# ============================================
# src/utils/exporter.py
# ============================================
from PySide6.QtCore import QObject, Signal, QTimer, QEventLoop, QSize, Qt, QPoint
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
        QTimer.singleShot(1000, lambda: self._capture_page(page_num))
    
    def _capture_page(self, page_num: int):
        """捕获当前页面为图片"""
        if not self._is_exporting:
            return
            
        # 构建输出文件名
        extension = self.export_format.lower()
        filename = f"card_{page_num:02d}.{extension}"
        output_path = self.output_folder / filename
        
        # 使用render方法捕获页面
        self._render_to_image(output_path, page_num)
    
    def _render_to_image(self, output_path: Path, page_num: int):
        """使用render方法渲染页面到图片"""
        try:
            # 创建目标尺寸的图片（小红书卡片尺寸）
            image = QImage(1080, 1440, QImage.Format_ARGB32)
            image.fill(Qt.white)
            
            # 获取WebView的尺寸
            view_size = self.web_view.size()
            
            # 创建临时图片来捕获WebView内容
            temp_image = QImage(view_size, QImage.Format_ARGB32)
            temp_image.fill(Qt.white)
            
            # 创建QPainter并渲染WebView到临时图片
            painter = QPainter(temp_image)
            
            # 修复：正确使用 RenderFlag 枚举
            # 检查 Qt 版本并使用正确的枚举
            if isinstance(self.web_view, QWidget):
                # PySide6 中 QWidget 的 render 方法
                self.web_view.render(
                    painter,                    # painter参数
                    QPoint(0, 0),              # targetOffset参数
                    QRegion(),                 # sourceRegion参数（默认为整个widget）
                    QWidget.RenderFlag.DrawWindowBackground | QWidget.RenderFlag.DrawChildren
                )
            else:
                # 备用方案
                self.web_view.render(painter)
            
            painter.end()
            
            # 创建最终图片的painter
            final_painter = QPainter(image)
            # 修复：使用 Qt.SmoothTransformation 而不是 QPainter.SmoothPixmapTransformation
            final_painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            final_painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            
            # 计算缩放比例以适应目标尺寸
            scale_x = 1080.0 / view_size.width()
            scale_y = 1440.0 / view_size.height()
            scale = min(scale_x, scale_y)
            
            # 计算居中位置
            scaled_width = int(view_size.width() * scale)
            scaled_height = int(view_size.height() * scale)
            x = (1080 - scaled_width) // 2
            y = (1440 - scaled_height) // 2
            
            # 绘制缩放后的图片
            # 修复：使用 Qt 命名空间下的枚举值
            final_painter.drawImage(
                x, y, 
                temp_image.scaled(
                    scaled_width, scaled_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
            
            # 添加水印（可选）
            self._add_watermark(final_painter, page_num)
            
            final_painter.end()
            
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
    
    def _add_watermark(self, painter: QPainter, page_num: int):
        """添加水印（可选）"""
        # 设置水印字体和颜色
        font = QFont("Arial", 10)
        painter.setFont(font)
        painter.setPen(QColor(200, 200, 200, 100))
        
        # 在右下角添加生成时间
        timestamp = time.strftime("%Y-%m-%d %H:%M")
        painter.drawText(
            950, 1410,
            timestamp
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
            printer.setPageSize(QPageSize(QSize(1080, 1440), QPageSize.Unit.Point))
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
            
            # 添加页面内容
            combined_content += f'<div class="page">{page}</div>'
        
        # 生成完整HTML
        return html_generator.generate(combined_content)
    
    def cancel_export(self):
        """取消导出"""
        self._is_exporting = False
        self.pages_to_export = []
        self.finished.emit(False, "导出已取消")