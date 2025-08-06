# ============================================
# src/utils/paginator.py
# ============================================
from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from bs4 import BeautifulSoup, NavigableString, Tag
import re

@dataclass
class PageElement:
    """页面元素"""
    type: str  # 'heading', 'paragraph', 'list', 'code', 'blockquote', 'table', 'hr', 'text'
    content: str  # HTML内容
    text: str  # 纯文本内容（用于计算高度）
    level: int = 0  # 标题级别或嵌套深度
    height: int = 0  # 估算高度（像素）
    can_break: bool = True  # 是否可以在此处分页
    
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
        
    def parse_html_to_elements(self, html: str) -> List[PageElement]:
        """将HTML解析为页面元素列表，保持原始顺序"""
        elements = []
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, 'html.parser')
        
        # 遍历所有顶层元素
        for element in soup.children:
            if isinstance(element, NavigableString):
                # 处理纯文本
                text = str(element).strip()
                if text:
                    elements.append(PageElement(
                        type='text',
                        content=f'<p>{text}</p>',
                        text=text,
                        height=self._calculate_text_height(text),
                        can_break=True
                    ))
            elif isinstance(element, Tag):
                # 处理HTML标签
                parsed_element = self._parse_element(element)
                if parsed_element:
                    elements.append(parsed_element)
        
        return elements
    
    def _parse_element(self, element: Tag) -> Optional[PageElement]:
        """解析单个HTML元素"""
        tag_name = element.name.lower()
        
        # 标题元素
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag_name[1])
            text = element.get_text(strip=True)
            height = self.ELEMENT_HEIGHTS[tag_name] + self.ELEMENT_HEIGHTS['margin_bottom']
            
            return PageElement(
                type='heading',
                content=str(element),
                text=text,
                level=level,
                height=height,
                can_break=False  # 标题前不分页
            )
        
        # 段落
        elif tag_name == 'p':
            text = element.get_text(strip=True)
            if not text:
                return None
                
            height = self._calculate_paragraph_height(text)
            
            return PageElement(
                type='paragraph',
                content=str(element),
                text=text,
                height=height,
                can_break=True
            )
        
        # 列表
        elif tag_name in ['ul', 'ol']:
            items = element.find_all('li')
            text = element.get_text(strip=True)
            height = len(items) * self.ELEMENT_HEIGHTS['li'] + self.ELEMENT_HEIGHTS['margin_bottom']
            
            return PageElement(
                type='list',
                content=str(element),
                text=text,
                height=height,
                can_break=len(items) > 3  # 列表项多于3个时可以分页
            )
        
        # 代码块
        elif tag_name == 'pre':
            text = element.get_text()
            lines = text.count('\n') + 1
            height = (self.ELEMENT_HEIGHTS['code_block'] + 
                     lines * self.ELEMENT_HEIGHTS['code_line'] +
                     self.ELEMENT_HEIGHTS['margin_bottom'])
            
            return PageElement(
                type='code',
                content=str(element),
                text=text,
                height=height,
                can_break=lines > 10  # 代码超过10行可以考虑分页
            )
        
        # 引用
        elif tag_name == 'blockquote':
            text = element.get_text(strip=True)
            height = self._calculate_blockquote_height(text)
            
            return PageElement(
                type='blockquote',
                content=str(element),
                text=text,
                height=height,
                can_break=True
            )
        
        # 表格
        elif tag_name == 'table':
            rows = element.find_all('tr')
            headers = element.find_all('th')
            text = element.get_text(strip=True)
            
            height = (len(headers) * self.ELEMENT_HEIGHTS['table_header'] +
                     (len(rows) - len(headers)) * self.ELEMENT_HEIGHTS['table_row'] +
                     self.ELEMENT_HEIGHTS['margin_bottom'])
            
            return PageElement(
                type='table',
                content=str(element),
                text=text,
                height=height,
                can_break=len(rows) > 5  # 表格行数多于5行时可以分页
            )
        
        # 分隔线
        elif tag_name == 'hr':
            return PageElement(
                type='hr',
                content=str(element),
                text='',
                height=self.ELEMENT_HEIGHTS['hr'],
                can_break=True
            )
        
        # 其他块级元素
        elif tag_name in ['div', 'section', 'article']:
            # 递归处理子元素
            sub_elements = []
            for child in element.children:
                if isinstance(child, Tag):
                    parsed = self._parse_element(child)
                    if parsed:
                        sub_elements.append(parsed)
            
            # 如果有子元素，返回第一个（简化处理）
            if sub_elements:
                return sub_elements[0]
        
        return None
    
    def _calculate_text_height(self, text: str) -> int:
        """计算纯文本高度"""
        lines = self._estimate_lines(text)
        return self.ELEMENT_HEIGHTS['p_base'] + lines * self.ELEMENT_HEIGHTS['p_line']
    
    def _calculate_paragraph_height(self, text: str) -> int:
        """计算段落高度"""
        lines = self._estimate_lines(text)
        height = self.ELEMENT_HEIGHTS['p_base'] + lines * self.ELEMENT_HEIGHTS['p_line']
        return height + self.ELEMENT_HEIGHTS['margin_bottom']
    
    def _calculate_blockquote_height(self, text: str) -> int:
        """计算引用块高度"""
        lines = self._estimate_lines(text, width_reduction=100)  # 引用有缩进
        height = self.ELEMENT_HEIGHTS['blockquote'] + lines * self.ELEMENT_HEIGHTS['blockquote_line']
        return height + self.ELEMENT_HEIGHTS['margin_bottom']
    
    def _estimate_lines(self, text: str, width_reduction: int = 0) -> int:
        """估算文本行数 - 根据页面宽度动态计算"""
        if not text:
            return 1
        
        # 计算可用宽度（使用动态内容宽度）
        available_width = self.content_width - width_reduction
        
        # 粗略估算：中英文混合
        # 统计中文字符数
        chinese_chars = len(re.findall(r'[\u4e00-\u9fa5]', text))
        english_chars = len(text) - chinese_chars
        
        # 计算总宽度
        total_width = (chinese_chars * self.CHAR_WIDTH + 
                      english_chars * self.CHAR_WIDTH_EN)
        
        # 计算行数
        lines = max(1, int(total_width / available_width) + 1)
        
        # 考虑强制换行
        forced_breaks = text.count('\n')
        
        return lines + forced_breaks
    
    def paginate(self, html_content: str) -> List[str]:
        """执行智能分页"""
        # 如果内容很短，直接返回
        if not html_content or len(html_content.strip()) < 100:
            return [html_content] if html_content else ['<p>无内容</p>']
        
        # 解析HTML为元素
        elements = self.parse_html_to_elements(html_content)
        if not elements:
            return [html_content]
        
        pages = []
        current_page_elements = []
        current_height = 0
        
        for i, element in enumerate(elements):
            # 检查是否需要新页面
            need_new_page = False
            
            # 1. 基础高度检查（使用动态内容高度）
            if current_height + element.height > self.content_height:
                need_new_page = True
            
            # 2. 标题关联检查（避免标题孤立）
            if element.type == 'heading':
                # 检查标题后是否有足够空间放置内容
                remaining_height = self.content_height - current_height - element.height
                
                if remaining_height < self.HEADING_KEEP_WITH:
                    # 剩余空间不足，将标题移到下一页
                    need_new_page = True
                
                # 如果是第一个元素且不是第一页，不要分页
                if not current_page_elements and pages:
                    need_new_page = False
            
            # 3. 段落完整性检查
            if element.type == 'paragraph' and current_page_elements:
                # 如果段落太大，且当前页已有内容，考虑分页
                if element.height > self.content_height * 0.6 and current_height > self.content_height * 0.3:
                    need_new_page = True
            
            # 4. 避免页面过空（根据页面尺寸调整阈值）
            min_fill_ratio = 0.25 if self.page_size_name == "small" else 0.3
            if need_new_page and current_height < self.content_height * min_fill_ratio:
                # 如果当前页面填充不足，尽量不分页
                if element.can_break or element.height < self.content_height * 0.5:
                    need_new_page = False
            
            # 创建新页面
            if need_new_page and current_page_elements:
                page_html = ''.join([e.content for e in current_page_elements])
                pages.append(page_html)
                current_page_elements = []
                current_height = 0
            
            # 添加元素到当前页
            current_page_elements.append(element)
            current_height += element.height
        
        # 添加最后一页
        if current_page_elements:
            page_html = ''.join([e.content for e in current_page_elements])
            pages.append(page_html)
        
        # 优化分页结果
        pages = self.optimize_pages(pages)
        
        return pages if pages else [html_content]
    
    def optimize_pages(self, pages: List[str]) -> List[str]:
        """优化分页结果，合并过短的页面"""
        if len(pages) <= 1:
            return pages
        
        optimized = []
        i = 0
        
        # 根据页面尺寸调整合并阈值
        merge_threshold = 0.35 if self.page_size_name == "small" else 0.4
        
        while i < len(pages):
            current_page = pages[i]
            
            # 估算当前页面高度
            current_elements = self.parse_html_to_elements(current_page)
            current_height = sum(e.height for e in current_elements)
            
            # 如果页面过短，尝试与下一页合并
            if current_height < self.content_height * merge_threshold and i < len(pages) - 1:
                next_page = pages[i + 1]
                next_elements = self.parse_html_to_elements(next_page)
                next_height = sum(e.height for e in next_elements)
                
                # 如果合并后不超过最大高度，则合并
                if current_height + next_height <= self.content_height:
                    optimized.append(current_page + next_page)
                    i += 2  # 跳过下一页
                    continue
            
            optimized.append(current_page)
            i += 1
        
        return optimized if optimized else pages
    
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