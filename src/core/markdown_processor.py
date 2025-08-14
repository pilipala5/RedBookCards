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
    """预处理任务列表语法"""
    
    def run(self, lines):
        new_lines = []
        in_list = False
        
        for line in lines:
            stripped = line.strip()
            
            # 识别任务列表项
            if stripped.startswith('- [ ] ') or stripped.startswith('- [x] ') or \
               stripped.startswith('* [ ] ') or stripped.startswith('* [x] '):
                # 将任务列表标记转换为 HTML 注释，避免被 Markdown 再次处理
                if stripped.startswith('- [x] ') or stripped.startswith('* [x] '):
                    new_line = line.replace('[x] ', '<!--tasklist-checked--> ', 1)
                else:
                    new_line = line.replace('[ ] ', '<!--tasklist-unchecked--> ', 1)
                
                new_lines.append(new_line)
                in_list = True
            else:
                # 如果从任务列表切换到普通文本，插入一个空行保证 Markdown 正常渲染
                if in_list and stripped and not stripped.startswith(('-', '*')):
                    new_lines.append('')
                    in_list = False
                
                new_lines.append(line)
        
        return new_lines

class TaskListPostprocessor(markdown.postprocessors.Postprocessor):
    """后处理：将占位注释替换为真正的复选框"""
    
    def run(self, text):
        # 将任务列表标记转换为带有 checkbox 的 li
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
        
        return text

class MarkdownProcessor:
    def __init__(self):
        # 初始化 Markdown 扩展
        self.extensions = [
            TaskListExtension(),                # 放到最前面，优先处理任务列表
            'meta',
            'toc',
            'abbr',
            'attr_list',
            'def_list',
            'admonition',
            'codehilite',
            'fenced_code',
            'footnotes',
            'md_in_html',
            'sane_lists',
            'smarty',
            'tables',
            'wikilinks'
        ]
        
        self.extension_configs = {
            'codehilite': {
                'css_class': 'highlight',
                'guess_lang': False,
                'pygments_style': 'default'
            },
            'toc': {
                'permalink': True
            }
        }
    
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
        """修复本地图片路径，确保能在 QWebEngineView 中显示（兼容任意盘符）"""
        from bs4 import BeautifulSoup
        import re
        soup = BeautifulSoup(html, 'html.parser')
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if not src:
                continue
            # 已是可用的 URL / data URI 直接跳过
            if src.startswith(('http://', 'https://', 'data:', 'file:')):
                img['data-protected'] = 'true'
                if not img.get('style'):
                    img['style'] = 'max-width: 100%; height: auto;'
                continue
            # Windows 绝对路径：任意盘符，如 E:\ 或 E:/ 开头
            if re.match(r'^[A-Za-z]:[\\/]', src):
                src = src.replace('\\', '/')
                if not src.startswith('file:'):
                    src = 'file:///' + src
            else:
                # 相对路径 -> 绝对路径
                try:
                    abs_path = os.path.abspath(src).replace('\\', '/')
                    src = 'file:///' + abs_path
                except Exception:
                    pass
            # 应用修正
            img['src'] = src
            # 默认样式
            if not img.get('style'):
                img['style'] = 'max-width: 100%; height: auto;'
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
        """为任务列表添加样式"""
        if '<input type="checkbox" class="task-list-checkbox"' in html:
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
                    width: 16px;
                    height: 16px;
                    vertical-align: middle;
                    position: relative;
                    top: -1px;
                    border: 1px solid var(--border-color, #ddd);
                    border-radius: 3px;
                    background: var(--bg-color, #fff);
                    appearance: none;
                }
                
                .task-list-checkbox:checked {
                    background: var(--checkbox-bg, #ffeef0);
                    border-color: var(--primary-color, #FF2442);
                }
                
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
