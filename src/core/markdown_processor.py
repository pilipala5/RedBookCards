# ============================================
# src/core/markdown_processor.py
# ============================================
import markdown
from markdown.extensions import fenced_code, tables

class MarkdownProcessor:
    def __init__(self):
        # 只使用必要且稳定的扩展
        self.extensions = [
            'markdown.extensions.fenced_code',  # 代码块
            'markdown.extensions.tables',       # 表格
            'markdown.extensions.nl2br',        # 换行转<br>
            'markdown.extensions.attr_list',    # 属性列表
            'markdown.extensions.def_list',     # 定义列表
            'markdown.extensions.footnotes',    # 脚注
            'markdown.extensions.toc',          # 目录
            'markdown.extensions.sane_lists',   # 改进的列表
            'markdown.extensions.smarty',       # 智能标点
        ]
        
        # 配置扩展（移除不支持的 css_class 参数）
        self.extension_configs = {}
        
    def parse(self, text: str) -> str:
        """解析 Markdown 文本为 HTML"""
        try:
            # 创建新的 Markdown 实例（避免状态污染）
            md = markdown.Markdown(
                extensions=self.extensions,
                extension_configs=self.extension_configs
            )
            
            # 转换 Markdown 为 HTML
            html = md.convert(text)
            
            # 后处理：添加小红书特色 emoji 支持
            html = self._process_emojis(html)
            
            return html
            
        except Exception as e:
            print(f"Markdown 解析错误: {e}")
            return f"<p style='color: red;'>解析错误: {str(e)}</p>"
    
    def _process_emojis(self, html: str) -> str:
        """处理 emoji 表情"""
        # 保持 emoji 原样显示
        return html