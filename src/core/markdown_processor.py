# ============================================
# src/core/markdown_processor.py
# ============================================
import markdown
from markdown.extensions import fenced_code, tables
import re
import os
from pathlib import Path

class TaskListExtension(markdown.Extension):
    """自定义任务列表扩展"""
    
    def extendMarkdown(self, md):
        # 提高优先级到 100，确保在列表处理之前执行
        md.preprocessors.register(TaskListPreprocessor(md), 'tasklist', 100)
        md.postprocessors.register(TaskListPostprocessor(md), 'tasklist', 25)

class TaskListPreprocessor(markdown.preprocessors.Preprocessor):
    """预处理器：标记任务列表项"""
    
    TASK_PATTERN = re.compile(r'^(\s*)([-\*\+])\s+\[([ xX])\]\s+(.*)$')
    
    def run(self, lines):
        new_lines = []
        for line in lines:
            match = self.TASK_PATTERN.match(line)
            if match:
                indent, marker, checked, text = match.groups()
                # 将任务列表转换为特殊标记，避免被普通列表处理干扰
                checked_mark = 'checked' if checked.lower() == 'x' else 'unchecked'
                # 使用特殊的HTML注释包裹，确保Markdown解析器不会破坏它
                new_line = f"{indent}{marker} <!--tasklist-{checked_mark}--> {text}"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        return new_lines

class TaskListPostprocessor(markdown.postprocessors.Postprocessor):
    """后处理器：将标记转换为HTML复选框"""
    
    def run(self, text):
        # 替换已选中的任务
        text = re.sub(
            r'<li><!--tasklist-checked-->\s*(.*?)</li>',
            r'<li class="task-list-item"><input type="checkbox" class="task-list-checkbox" checked disabled> \1</li>',
            text,
            flags=re.DOTALL
        )
        
        # 替换未选中的任务
        text = re.sub(
            r'<li><!--tasklist-unchecked-->\s*(.*?)</li>',
            r'<li class="task-list-item"><input type="checkbox" class="task-list-checkbox" disabled> \1</li>',
            text,
            flags=re.DOTALL
        )
        
        # 为包含任务列表的ul/ol添加class
        text = re.sub(
            r'<(ul|ol)>(\s*<li class="task-list-item">)',
            r'<\1 class="task-list">\2',
            text
        )
        
        return text

class MarkdownProcessor:
    def __init__(self):
        # 使用必要且稳定的扩展
        self.extensions = [
            TaskListExtension(),                # 放到最前面，优先处理任务列表
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
            'markdown.extensions.attr_list',
            'markdown.extensions.def_list',
            'markdown.extensions.footnotes',
            'markdown.extensions.toc',
            'markdown.extensions.sane_lists',   # 放到任务列表扩展之后
            'markdown.extensions.smarty',
        ]
        
        # 配置扩展
        self.extension_configs = {}
        
    def parse(self, text: str) -> str:
        """解析 Markdown 文本为 HTML"""
        try:
            # 1. 先处理分页标记
            text = self._process_pagebreaks_before_markdown(text)
            
            # 2. 正常让 Markdown 解析（包括图片）
            md = markdown.Markdown(
                extensions=self.extensions,
                extension_configs=self.extension_configs
            )
            html = md.convert(text)
            
            # 3. 处理本地图片路径
            html = self._fix_local_image_paths(html)
            
            # 4. 添加任务列表样式
            html = self._add_tasklist_styles(html)
            
            return html
            
        except Exception as e:
            print(f"Markdown 解析错误: {e}")
            return f"<p style='color: red;'>解析错误: {str(e)}</p>"
    
    def _fix_local_image_paths(self, html: str) -> str:
        """修复本地图片路径，确保能在 QWebEngineView 中显示"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src:
                # 处理本地文件路径
                if not src.startswith(('http://', 'https://', 'data:', 'file:')):
                    # 处理 Windows 路径
                    if src.startswith('C:') or src.startswith('D:') or ':\\' in src or ':/' in src:
                        # 这是绝对路径
                        # 统一转换为正斜杠
                        src = src.replace('\\', '/')
                        # 如果路径以 C:/ 开头，转换为 file:///C:/
                        if not src.startswith('file:'):
                            if src[1:3] == ':/':  # 类似 C:/ 的格式
                                src = 'file:///' + src
                            else:
                                src = 'file:///' + src.replace(':', '')
                    else:
                        # 相对路径，转换为绝对路径
                        try:
                            abs_path = os.path.abspath(src).replace('\\', '/')
                            src = 'file:///' + abs_path
                        except:
                            pass
                    
                    img['src'] = src
                    
                # 添加一些默认属性以改善显示
                if not img.get('style'):
                    img['style'] = 'max-width: 100%; height: auto;'
                
                # 保护标记
                img['data-protected'] = 'true'
        
        return str(soup)
    
    def _process_pagebreaks_before_markdown(self, text: str) -> str:
        """
        在 Markdown 解析之前处理分页标记
        直接将 <!-- pagebreak --> 替换为特殊的 HTML div
        """
        # 匹配 HTML 注释形式的分页标记（支持大小写和空格变化）
        pattern = r'<!--\s*pagebreak\s*-->'
        
        # 直接替换为 HTML div（这个 div 不会被 Markdown 解析器改变）
        replacement = '\n\n<div class="pagebreak-marker" data-pagebreak="true"></div>\n\n'
        
        # 执行替换
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _add_tasklist_styles(self, html: str) -> str:
        """添加任务列表的内联样式"""
        # 如果HTML中包含任务列表，添加样式
        if 'task-list' in html:
            style = """
            <style>
                .task-list {
                    list-style-type: none;
                    padding-left: 0;
                }
                
                .task-list-item {
                    list-style-type: none;
                    margin-left: 0;
                    padding-left: 0;
                    position: relative;
                }
                
                .task-list-checkbox {
                    margin-right: 8px;
                    margin-left: 0;
                    vertical-align: middle;
                    position: relative;
                    top: -1px;
                    cursor: default;
                    width: 16px;
                    height: 16px;
                    accent-color: var(--primary-color, #FF2442);
                }
                
                .task-list-item + .task-list-item {
                    margin-top: 8px;
                }
                
                /* 美化复选框样式 */
                .task-list-checkbox:checked::before {
                    content: '✓';
                    position: absolute;
                    color: var(--primary-color, #FF2442);
                    font-weight: bold;
                    font-size: 12px;
                    left: 2px;
                    top: -2px;
                }
            </style>
            """
            # 将样式插入到HTML开头
            html = style + html
        
        return html