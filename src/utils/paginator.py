# ============================================
# src/utils/paginator.py
# ============================================
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import re

@dataclass
class PageElement:
    """页面元素"""
    type: str  # 'heading', 'paragraph', 'list', 'code', 'blockquote', 'table', 'hr', 'text', 'pagebreak'
    content: str  # HTML内容
    text: str  # 纯文本内容（用于计算高度）
    level: int = 0  # 标题级别或嵌套深度
    height: int = 0  # 估算高度（像素）
    can_break: bool = True  # 是否可以在此处分页
    is_forced_break: bool = False  # 是否是强制分页（用于标记用户添加的分页符）
    
class SmartPaginator:
    """智能分页器 - 支持多尺寸"""
    
    # 元素高度估算（像素）- 调整为更准确的值
    ELEMENT_HEIGHTS = {
        'h1': 90,        # 大标题 + 底部边框
        'h2': 70,        # 二级标题
        'h3': 60,        # 三级标题
        'h4': 50,        # 四级标题
        'h5': 45,        # 五级标题
        'h6': 40,        # 六级标题
        'p_base': 25,    # 段落基础高度
        'p_line': 28,    # 段落每行高度（考虑行高1.8）
        'li': 35,        # 列表项
        'code_block': 40,  # 代码块基础高度
        'code_line': 24,   # 代码每行高度
        'blockquote': 60,  # 引用块基础高度
        'blockquote_line': 28,  # 引用每行高度
        'table_header': 45,  # 表格头
        'table_row': 40,     # 表格行
        'hr': 35,           # 分隔线
        'margin_bottom': 20,  # 元素底部间距
    }
    
    # 页面尺寸配置
    PAGE_SIZES = {
        "small": {
            "width": 720,
            "height": 960,
            "padding_top": 35,
            "padding_bottom": 50,
            "padding_sides": 30
        },
        "medium": {
            "width": 1080,
            "height": 1440,
            "padding_top": 45,
            "padding_bottom": 70,
            "padding_sides": 40
        },
        "large": {
            "width": 1440,
            "height": 1920,
            "padding_top": 55,
            "padding_bottom": 90,
            "padding_sides": 50
        }
    }
    
    # 分页策略参数
    MIN_ORPHAN_LINES = 2  # 孤行控制：段落末尾最少保留行数
    MIN_WIDOW_LINES = 2   # 寡行控制：段落开头最少保留行数
    HEADING_KEEP_WITH = 150  # 标题后至少保留的内容高度
    
    # 字符宽度估算（像素）
    CHAR_WIDTH = 16  # 中文字符平均宽度
    CHAR_WIDTH_EN = 9  # 英文字符平均宽度
    
    def __init__(self, page_size: str = "medium"):
        """
        初始化分页器
        
        Args:
            page_size: 页面尺寸 ("small", "medium", "large")
        """
        self.elements: List[PageElement] = []
        self.set_page_size(page_size)
        self.forced_break_pages = set()  # 记录哪些页面是通过分页符创建的
        
    def set_page_size(self, size: str):
        """设置页面尺寸"""
        if size not in self.PAGE_SIZES:
            size = "medium"
        
        config = self.PAGE_SIZES[size]
        self.page_size_name = size
        self.page_width = config["width"]
        self.page_height = config["height"]
        self.padding_top = config["padding_top"]
        self.padding_bottom = config["padding_bottom"]
        self.padding_sides = config["padding_sides"]
        
        # 计算内容区域
        self.content_width = self.page_width - (self.padding_sides * 2)
        self.content_height = self.page_height - self.padding_top - self.padding_bottom
        
        # 根据尺寸调整分页策略
        if size == "small":
            self.HEADING_KEEP_WITH = 100  # 小尺寸页面，标题后保留空间可以更少
        elif size == "large":
            self.HEADING_KEEP_WITH = 200  # 大尺寸页面，标题后保留更多空间
        else:
            self.HEADING_KEEP_WITH = 150
    
    def get_page_info(self) -> Dict:
        """获取当前页面配置信息"""
        return {
            "size_name": self.page_size_name,
            "width": self.page_width,
            "height": self.page_height,
            "content_width": self.content_width,
            "content_height": self.content_height,
            "padding": {
                "top": self.padding_top,
                "bottom": self.padding_bottom,
                "sides": self.padding_sides
            }
        }
    
    def paginate(self, html_content: str) -> List[str]:
        """
        核心分页方法
        
        Args:
            html_content: HTML内容
            
        Returns:
            分页后的HTML内容列表
        """
        # 重置强制分页记录
        self.forced_break_pages = set()
        
        # 1. 解析HTML为元素列表
        elements = self.parse_html_to_elements(html_content)
        
        if not elements:
            return [html_content] if html_content else []
        
        # 2. 执行分页
        pages = []
        current_page_elements = []
        current_height = 0
        consecutive_breaks = 0  # 追踪连续的分页符数量
        
        i = 0
        while i < len(elements):
            element = elements[i]
            
            # 处理强制分页标记
            if element.type == 'pagebreak':
                consecutive_breaks += 1
                
                # 保存当前页（如果有内容）
                if current_page_elements:
                    pages.append(self._elements_to_html(current_page_elements))
                    self.forced_break_pages.add(len(pages) - 1)  # 记录这是强制分页
                    current_page_elements = []
                    current_height = 0
                elif consecutive_breaks > 1:
                    # 如果是连续的分页符，创建空页
                    pages.append("")
                    self.forced_break_pages.add(len(pages) - 1)  # 记录这是强制分页创建的空页
                
                i += 1
                continue
            
            # 非分页符元素，重置连续分页符计数
            consecutive_breaks = 0
            
            # 检查是否需要分页
            element_height = element.height
            
            # 特殊处理：标题元素
            if element.type == 'heading':
                # 检查标题后是否有足够空间放置内容
                if current_height + element_height + self.HEADING_KEEP_WITH > self.content_height:
                    # 需要分页，标题放到下一页
                    if current_page_elements:
                        pages.append(self._elements_to_html(current_page_elements))
                        current_page_elements = []
                        current_height = 0
            
            # 检查当前元素是否超出页面高度
            if current_height + element_height > self.content_height:
                # 检查是否可以分割元素
                if element.type == 'paragraph' and element_height > self.content_height * 0.3:
                    # 长段落可以尝试分割
                    split_result = self._try_split_paragraph(element, self.content_height - current_height)
                    if split_result:
                        first_part, second_part = split_result
                        if first_part:
                            current_page_elements.append(first_part)
                        pages.append(self._elements_to_html(current_page_elements))
                        current_page_elements = [second_part] if second_part else []
                        current_height = second_part.height if second_part else 0
                    else:
                        # 无法分割，整个元素放到下一页
                        if current_page_elements:
                            pages.append(self._elements_to_html(current_page_elements))
                        current_page_elements = [element]
                        current_height = element_height
                else:
                    # 不可分割的元素或不需要分割，放到下一页
                    if current_page_elements:
                        pages.append(self._elements_to_html(current_page_elements))
                    current_page_elements = [element]
                    current_height = element_height
            else:
                # 当前元素可以放入当前页
                current_page_elements.append(element)
                current_height += element_height
            
            i += 1
        
        # 3. 保存最后一页
        if current_page_elements:
            pages.append(self._elements_to_html(current_page_elements))
        
        # 4. 如果没有生成任何页面，返回原始内容
        if not pages:
            return [html_content]
        
        return pages
    
    def _elements_to_html(self, elements: List[PageElement]) -> str:
        """将元素列表转换回HTML字符串"""
        html_parts = []
        for element in elements:
            if element.type != 'pagebreak':  # 跳过分页标记
                html_parts.append(element.content)
        return '\n'.join(html_parts)
    
    def _try_split_paragraph(self, element: PageElement, available_height: int) -> Optional[Tuple[PageElement, PageElement]]:
        """
        尝试分割段落
        
        Args:
            element: 要分割的段落元素
            available_height: 当前页剩余高度
            
        Returns:
            分割后的两个元素，如果无法分割则返回None
        """
        # 简单实现：暂不分割段落，保持段落完整性
        # 未来可以实现更复杂的分割逻辑
        return None
    
    def _calculate_text_height(self, text: str) -> int:
        """计算纯文本高度"""
        if not text:
            return 0
        
        # 估算文本行数
        chars_per_line = self.content_width // self.CHAR_WIDTH
        total_chars = len(text)
        estimated_lines = max(1, (total_chars + chars_per_line - 1) // chars_per_line)
        
        return self.ELEMENT_HEIGHTS['p_base'] + estimated_lines * self.ELEMENT_HEIGHTS['p_line']
    
    def _calculate_paragraph_height(self, text: str) -> int:
        """计算段落高度"""
        if not text:
            return self.ELEMENT_HEIGHTS['p_base']
        
        # 考虑中英文混合
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
        english_chars = len(text) - chinese_chars
        
        # 计算平均每行字符数
        avg_char_width = (chinese_chars * self.CHAR_WIDTH + english_chars * self.CHAR_WIDTH_EN) / max(1, len(text))
        chars_per_line = self.content_width / avg_char_width
        
        # 计算行数
        lines = max(1, int(len(text) / chars_per_line) + 1)
        
        return self.ELEMENT_HEIGHTS['p_base'] + lines * self.ELEMENT_HEIGHTS['p_line'] + self.ELEMENT_HEIGHTS['margin_bottom']
    
    def _calculate_blockquote_height(self, text: str) -> int:
        """计算引用块高度"""
        if not text:
            return self.ELEMENT_HEIGHTS['blockquote']
        
        # 引用块内容宽度更窄
        effective_width = self.content_width - 60  # 减去左边框和内边距
        chars_per_line = effective_width // self.CHAR_WIDTH
        lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)
        
        return self.ELEMENT_HEIGHTS['blockquote'] + lines * self.ELEMENT_HEIGHTS['blockquote_line'] + self.ELEMENT_HEIGHTS['margin_bottom']
    
    def parse_html_to_elements(self, html: str) -> List[PageElement]:
        """
        将HTML解析为页面元素列表，保持原始顺序
        改进版：使用深度优先遍历，确保所有分页标记都被识别
        """
        elements = []
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # 深度优先遍历所有元素，扁平化处理
        elements = self._flatten_parse(soup)
        
        return elements
    
    def _flatten_parse(self, node) -> List[PageElement]:
        """
        扁平化解析所有节点，确保分页标记被正确识别
        这个方法会遍历整个DOM树，将所有内容扁平化为元素列表
        
        修复版本：专门处理图片标签，避免图片丢失
        """
        elements = []
        
        # 如果是文本节点
        if isinstance(node, NavigableString):
            # 跳过注释和空白文本
            if not isinstance(node, Comment):
                text = str(node).strip()
                if text:
                    elements.append(PageElement(
                        type='text',
                        content=f'<p>{text}</p>',
                        text=text,
                        height=self._calculate_text_height(text),
                        can_break=True
                    ))
            return elements
        
        # 如果不是Tag，返回空列表
        if not isinstance(node, Tag):
            return elements
        
        # 首先检查是否是分页标记
        if self._is_pagebreak_marker(node):
            elements.append(PageElement(
                type='pagebreak',
                content='',
                text='',
                height=0,
                can_break=True,
                level=999,
                is_forced_break=True
            ))
            return elements
        
        # 处理具体的元素类型
        tag_name = node.name.lower()
        
        # ===== 新增：专门处理图片标签 =====
        if tag_name == 'img':
            # 保持img标签完整，不要丢失
            src = node.get('src', '')
            alt = node.get('alt', '图片')
            
            # 估算图片高度
            img_height = 350  # 默认图片高度
            if 'width' in node.attrs and 'height' in node.attrs:
                try:
                    # 如果有指定尺寸，按比例计算
                    width = int(node['width'])
                    height = int(node['height'])
                    # 限制最大宽度为内容宽度
                    if width > self.content_width:
                        ratio = self.content_width / width
                        img_height = int(height * ratio)
                    else:
                        img_height = height
                except:
                    pass
            
            elements.append(PageElement(
                type='image',
                content=str(node),  # 保留完整的img标签HTML
                text=alt,
                height=img_height + self.ELEMENT_HEIGHTS['margin_bottom'],
                can_break=False  # 图片不可分割
            ))
            return elements
        
        # 处理块级元素
        elif tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            # 标题元素
            level = int(tag_name[1])
            text = node.get_text(strip=True)
            height = self.ELEMENT_HEIGHTS[tag_name] + self.ELEMENT_HEIGHTS['margin_bottom']
            
            elements.append(PageElement(
                type='heading',
                content=str(node),
                text=text,
                level=level,
                height=height,
                can_break=False
            ))
            
        elif tag_name == 'p':
            # ===== 修改：段落元素需要检查是否包含图片 =====
            imgs = node.find_all('img')
            
            if imgs:
                # 如果段落包含图片，特殊处理
                text = node.get_text(strip=True)
                # 计算高度：文本高度 + 所有图片高度
                text_height = self._calculate_paragraph_height(text)
                img_heights = len(imgs) * 350  # 每个图片估算350px
                total_height = text_height + img_heights
                
                elements.append(PageElement(
                    type='paragraph_with_images',
                    content=str(node),  # 保留完整HTML，包括img标签
                    text=text,
                    height=total_height,
                    can_break=False  # 包含图片的段落不分割
                ))
            else:
                # 普通段落，检查是否有分页标记
                has_pagebreak = False
                sub_elements = []
                
                # 检查段落内部的所有子节点
                for child in node.children:
                    if isinstance(child, Tag) and self._is_pagebreak_marker(child):
                        has_pagebreak = True
                        # 如果段落内有分页标记，需要特殊处理
                        # 先保存分页标记前的内容
                        text_before = ''.join(str(c) for c in list(node.children)[:list(node.children).index(child)])
                        if text_before.strip():
                            sub_elements.append(PageElement(
                                type='paragraph',
                                content=f'<p>{text_before}</p>',
                                text=text_before,
                                height=self._calculate_paragraph_height(text_before),
                                can_break=True
                            ))
                        # 添加分页标记
                        sub_elements.append(PageElement(
                            type='pagebreak',
                            content='',
                            text='',
                            height=0,
                            can_break=True,
                            level=999,
                            is_forced_break=True
                        ))
                
                if has_pagebreak:
                    elements.extend(sub_elements)
                else:
                    # 正常的段落
                    text = node.get_text(strip=True)
                    if text:
                        height = self._calculate_paragraph_height(text)
                        elements.append(PageElement(
                            type='paragraph',
                            content=str(node),
                            text=text,
                            height=height,
                            can_break=True
                        ))
                        
        elif tag_name in ['ul', 'ol']:
            # ===== 修改：列表元素也要检查是否包含图片 =====
            items = node.find_all('li')
            imgs = node.find_all('img')
            text = node.get_text(strip=True)
            
            # 计算高度
            list_height = len(items) * self.ELEMENT_HEIGHTS['li']
            img_height = len(imgs) * 350
            total_height = list_height + img_height + self.ELEMENT_HEIGHTS['margin_bottom']
            
            elements.append(PageElement(
                type='list',
                content=str(node),  # 保留完整HTML
                text=text,
                height=total_height,
                can_break=len(items) > 3 and len(imgs) == 0  # 有图片就不分割
            ))
            
        elif tag_name == 'pre':
            # 代码块
            text = node.get_text()
            lines = text.count('\n') + 1
            height = (self.ELEMENT_HEIGHTS['code_block'] + 
                    lines * self.ELEMENT_HEIGHTS['code_line'] +
                    self.ELEMENT_HEIGHTS['margin_bottom'])
            
            elements.append(PageElement(
                type='code',
                content=str(node),
                text=text,
                height=height,
                can_break=lines > 10
            ))
            
        elif tag_name == 'blockquote':
            # ===== 修改：引用块也要检查图片 =====
            imgs = node.find_all('img')
            text = node.get_text(strip=True)
            
            text_height = self._calculate_blockquote_height(text)
            img_height = len(imgs) * 350
            total_height = text_height + img_height
            
            elements.append(PageElement(
                type='blockquote',
                content=str(node),  # 保留完整HTML
                text=text,
                height=total_height,
                can_break=len(imgs) == 0  # 有图片就不分割
            ))
            
        elif tag_name == 'table':
            # 表格
            rows = node.find_all('tr')
            headers = node.find_all('th')
            text = node.get_text(strip=True)
            
            height = (len(headers) * self.ELEMENT_HEIGHTS['table_header'] +
                    (len(rows) - len(headers)) * self.ELEMENT_HEIGHTS['table_row'] +
                    self.ELEMENT_HEIGHTS['margin_bottom'])
            
            elements.append(PageElement(
                type='table',
                content=str(node),
                text=text,
                height=height,
                can_break=len(rows) > 5
            ))
            
        elif tag_name == 'hr':
            # 分隔线
            elements.append(PageElement(
                type='hr',
                content=str(node),
                text='',
                height=self.ELEMENT_HEIGHTS['hr'],
                can_break=True
            ))
            
        elif tag_name in ['div', 'section', 'article', 'main', 'aside', 'nav', 'header', 'footer']:
            # ===== 修改：容器元素要递归处理，但要检查是否包含图片 =====
            # 先检查是否直接包含图片
            direct_imgs = []
            for child in node.children:
                if isinstance(child, Tag) and child.name.lower() == 'img':
                    direct_imgs.append(child)
            
            # 如果容器直接包含图片，整体处理
            if direct_imgs:
                text = node.get_text(strip=True)
                img_height = len(direct_imgs) * 350
                text_height = self._calculate_text_height(text) if text else 0
                
                elements.append(PageElement(
                    type='container_with_images',
                    content=str(node),  # 保留完整HTML
                    text=text,
                    height=text_height + img_height,
                    can_break=False
                ))
            else:
                # 递归处理子元素
                for child in node.children:
                    elements.extend(self._flatten_parse(child))
                    
        else:
            # ===== 修改：其他元素的处理 =====
            # 首先检查是否包含图片
            imgs = node.find_all('img') if hasattr(node, 'find_all') else []
            
            if imgs:
                # 如果包含图片，保留完整HTML
                text = node.get_text(strip=True)
                img_height = len(imgs) * 350
                text_height = self._calculate_text_height(text) if text else 0
                
                elements.append(PageElement(
                    type='mixed_with_images',
                    content=str(node),  # 重要：保留完整HTML，不要用get_text
                    text=text,
                    height=text_height + img_height,
                    can_break=False
                ))
            else:
                # 不包含图片的其他元素
                text = node.get_text(strip=True)
                if text:
                    # 检查子元素
                    has_content = False
                    for child in node.children:
                        child_elements = self._flatten_parse(child)
                        if child_elements:
                            elements.extend(child_elements)
                            has_content = True
                    
                    # 如果没有子元素被解析，则将整个元素作为文本处理
                    if not has_content:
                        elements.append(PageElement(
                            type='text',
                            content=str(node),
                            text=text,
                            height=self._calculate_text_height(text),
                            can_break=True
                        ))
                else:
                    # 递归处理子元素
                    for child in node.children:
                        elements.extend(self._flatten_parse(child))
        
        return elements
    
    def _is_pagebreak_marker(self, element: Tag) -> bool:
        """
        检查元素是否是分页标记
        支持多种识别方式
        """
        if not isinstance(element, Tag):
            return False
            
        # 检查是否是带有特定class的div
        if element.name.lower() == 'div':
            classes = element.get('class', [])
            if isinstance(classes, str):
                classes = classes.split()
            
            # 检查class名
            if 'pagebreak-marker' in classes:
                return True
            
            # 检查data属性
            if element.get('data-pagebreak') == 'true':
                return True
        
        return False
    
    def optimize_pages(self, pages: List[str]) -> List[str]:
        """
        优化分页结果，合并过短的页面
        修改：保留通过分页符创建的页面，即使是空页
        """
        if len(pages) <= 1:
            return pages
        
        optimized = []
        i = 0
        
        # 根据页面尺寸调整合并阈值
        merge_threshold = 0.35 if self.page_size_name == "small" else 0.4
        
        while i < len(pages):
            current_page = pages[i]
            
            # 检查当前页是否是通过分页符创建的
            is_forced_page = i in self.forced_break_pages
            
            # 如果是强制分页创建的页面，直接保留（即使是空页）
            if is_forced_page:
                optimized.append(current_page)
                i += 1
                continue
            
            # 非强制分页的页面，进行常规优化
            # 过滤掉完全空的页面
            if not current_page or not current_page.strip():
                i += 1
                continue
            
            # 估算当前页面高度
            current_elements = self.parse_html_to_elements(current_page)
            current_height = sum(e.height for e in current_elements)
            
            # 如果页面过短，尝试与下一页合并（但不合并强制分页的页面）
            if current_height < self.content_height * merge_threshold and i < len(pages) - 1:
                next_page_index = i + 1
                # 检查下一页是否是强制分页
                if next_page_index not in self.forced_break_pages:
                    next_page = pages[next_page_index]
                    if next_page and next_page.strip():  # 确保下一页有内容
                        next_elements = self.parse_html_to_elements(next_page)
                        next_height = sum(e.height for e in next_elements)
                        
                        # 如果合并后不超过最大高度，则合并
                        if current_height + next_height <= self.content_height:
                            optimized.append(current_page + next_page)
                            i += 2  # 跳过下一页
                            continue
            
            optimized.append(current_page)
            i += 1
        
        # 如果优化后没有页面，至少返回一个页面
        return optimized if optimized else ['']
    
    def debug_pagination(self, html_content: str) -> List[dict]:
        """调试分页，返回详细信息"""
        elements = self.parse_html_to_elements(html_content)
        pages_info = []
        
        pages = self.paginate(html_content)
        for i, page in enumerate(pages, 1):
            page_elements = self.parse_html_to_elements(page)
            total_height = sum(e.height for e in page_elements)
            
            pages_info.append({
                'page_num': i,
                'page_size': self.page_size_name,
                'content_dimensions': f"{self.content_width}×{self.content_height}px",
                'elements_count': len(page_elements),
                'total_height': total_height,
                'max_height': self.content_height,
                'fill_rate': f"{(total_height / self.content_height * 100):.1f}%",
                'is_forced_break': (i-1) in self.forced_break_pages,  # 标记是否是强制分页
                'elements': [
                    {
                        'type': e.type,
                        'height': e.height,
                        'text_preview': e.text[:50] + '...' if len(e.text) > 50 else e.text
                    }
                    for e in page_elements
                ]
            })
        
        return pages_info