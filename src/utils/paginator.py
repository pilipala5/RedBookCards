# ============================================
# src/utils/paginator.py - 优化完整版
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
    can_break: bool = True  # 是否允许在元素内部分页
    metadata: dict = None  # 额外信息

class SmartPaginator:
    """智能分页器 - 支持多尺寸"""

    # 元素高度估算（像素）
    ELEMENT_HEIGHTS = {
        'h1': 85,        # 大标题 + 底部边框
        'h2': 68,        # 二级标题
        'h3': 58,        # 三级标题
        'h4': 48,        # 四级标题
        'h5': 43,        # 五级标题
        'h6': 38,        # 六级标题
        'p_base': 20,    # 段落基础高度
        'p_line': 26,    # 段落每行高度（考虑行高1.8）
        'li': 32,        # 列表项
        'code_block': 35,  # 代码块基础高度
        'code_line': 22,   # 代码每行高度
        'blockquote': 55,  # 引用块基础高度
        'blockquote_line': 26,  # 引用每行高度
        'table_header': 42,  # 表格头
        'table_row': 38,     # 表格行
        'hr': 30,           # 分隔线
        'margin_bottom': 18,  # 元素底部间距
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
            "width": 1024,
            "height": 1365,
            "padding_top": 50,
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
    MIN_ORPHAN_LINES = 2  # 孤行控制
    MIN_WIDOW_LINES = 2  # 寡行控制
    HEADING_KEEP_WITH = 120  # 标题后至少保留的内容高度

    # 字符宽度估算（像素）
    CHAR_WIDTH = 15  # 中文字符平均宽度（稍微调小）
    CHAR_WIDTH_EN = 8  # 英文字符平均宽度

    def __init__(self, page_size: str = "medium"):
        """初始化分页器"""
        self.elements: List[PageElement] = []
        self.set_page_size(page_size)
        self.forced_break_pages = set()

    def set_page_size(self, size: str):
        """设置页面尺寸"""
        if size not in self.PAGE_SIZES:
            size = "medium"
        cfg = self.PAGE_SIZES[size]
        self.page_size_name = size
        self.page_width = cfg["width"]
        self.page_height = cfg["height"]
        self.padding_top = cfg["padding_top"]
        self.padding_bottom = cfg["padding_bottom"]
        self.padding_sides = cfg["padding_sides"]
        self.content_height = self.page_height - self.padding_top - self.padding_bottom
        self.content_width = self.page_width - self.padding_sides * 2

    def get_page_info(self) -> Dict[str, int]:
        """获取当前页面信息"""
        return {
            "page_width": self.page_width,
            "page_height": self.page_height,
            "content_width": self.content_width,
            "content_height": self.content_height,
            "padding_top": self.padding_top,
            "padding_bottom": self.padding_bottom,
            "padding_sides": self.padding_sides
        }

    def paginate(self, html_content: str) -> List[str]:
        """
        核心分页方法

        Args:
            html_content: HTML内容

        Returns:
            分页后的HTML内容列表
        """
        # 重置状态
        self.forced_break_pages = set()

        # 1. 解析HTML为元素列表
        elements = self.parse_html_to_elements(html_content)

        if not elements:
            return [html_content] if html_content else []

        # 2. 执行分页
        pages = []
        current_page_elements = []
        current_height = 0

        i = 0
        while i < len(elements):
            element = elements[i]

            # 处理强制分页标记
            if element.type == 'pagebreak':
                if current_page_elements:
                    pages.append(self._elements_to_html(current_page_elements))
                    current_page_elements = []
                    current_height = 0
                    self.forced_break_pages.add(len(pages) - 1)
                else:
                    # 当前页为空，插入一个空页以表示强制分页
                    pages.append('')
                    self.forced_break_pages.add(len(pages) - 1)
                i += 1
                continue

            # 如果当前元素能放下
            if current_height + element.height <= self.content_height:
                current_page_elements.append(element)
                current_height += element.height
                i += 1
                continue

            # 放不下，尝试分割（仅对段落支持）
            if element.can_break and element.type in ('paragraph', 'paragraph_with_images', 'text', 'blockquote', 'code'):
                # 可用高度
                available = self.content_height - current_height

                # 仅对“纯文本段落”尝试分割；图文段落/代码/引用通常不分割
                if element.type == 'paragraph' and element.text:
                    split_result = self._try_split_paragraph(element, available)
                    if split_result:
                        part1, part2 = split_result
                        current_page_elements.append(part1)
                        pages.append(self._elements_to_html(current_page_elements))
                        current_page_elements = [part2]
                        current_height = part2.height
                        i += 1
                        continue

            # 如果无法分割或分割失败，则换页
            if current_page_elements:
                pages.append(self._elements_to_html(current_page_elements))
                current_page_elements = []
                current_height = 0
                # 不前进i，下一轮再尝试放element
                continue
            else:
                # 如果当前页为空也放不下，就强制放进去（避免死循环）
                current_page_elements.append(element)
                pages.append(self._elements_to_html(current_page_elements))
                current_page_elements = []
                current_height = 0
                i += 1

        # 3. 收尾：最后一页
        if current_page_elements:
            pages.append(self._elements_to_html(current_page_elements))

        # 4. 合并过短页（避免出现很多内容特别少的页面）
        pages = self.optimize_pages(pages)

        return pages

    def _elements_to_html(self, elements: List[PageElement]) -> str:
        """将元素列表转换回HTML字符串"""
        html_parts = []
        for element in elements:
            if element.type != 'pagebreak':
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
        # 如果剩余空间太小，不分割
        if available_height < self.ELEMENT_HEIGHTS['p_base'] + 2 * self.ELEMENT_HEIGHTS['p_line']:
            return None

        text = element.text
        if not text:
            return None

        # 估算可以放入的字符数
        chars_per_line = self.content_width // self.CHAR_WIDTH
        min_lines = 2
        max_lines = max(min_lines, (available_height - self.ELEMENT_HEIGHTS['p_base'] - self.ELEMENT_HEIGHTS['margin_bottom']) // self.ELEMENT_HEIGHTS['p_line'])
        if max_lines < min_lines:
            return None

        max_chars = chars_per_line * max_lines
        if max_chars <= 0 or max_chars >= len(text):
            return None

        # 在空白处切分（尽量不拆词）
        split_index = max_chars
        # 尝试往前找到一个空格或标点
        match = re.search(r'[\s，。；；、,.!?)]', text[:max_chars][::-1])
        if match:
            split_index = max_chars - match.start()

        part1_text = text[:split_index].rstrip()
        part2_text = text[split_index:].lstrip()

        # 重新估算高度
        def para_height(t: str) -> int:
            if not t:
                return self.ELEMENT_HEIGHTS['p_base'] + self.ELEMENT_HEIGHTS['margin_bottom']
            total_width = 0
            for ch in t:
                total_width += self.CHAR_WIDTH if ord(ch) > 127 else self.CHAR_WIDTH_EN
            lines = max(1, int(total_width / self.content_width) + 1)
            return self.ELEMENT_HEIGHTS['p_base'] + lines * self.ELEMENT_HEIGHTS['p_line'] + self.ELEMENT_HEIGHTS['margin_bottom']

        part1 = PageElement(
            type='paragraph',
            content=f"<p>{part1_text}</p>",
            text=part1_text,
            height=para_height(part1_text),
            can_break=True
        )
        part2 = PageElement(
            type='paragraph',
            content=f"<p>{part2_text}</p>",
            text=part2_text,
            height=para_height(part2_text),
            can_break=True
        )
        return part1, part2

    # ----------------------
    # 高度估算辅助方法
    # ----------------------
    def _calculate_text_height(self, text: str) -> int:
        """计算纯文本高度"""
        if not text:
            return self.ELEMENT_HEIGHTS['p_base'] + self.ELEMENT_HEIGHTS['margin_bottom']

        total_width = 0
        for ch in text:
            total_width += self.CHAR_WIDTH if ord(ch) > 127 else self.CHAR_WIDTH_EN
        lines = max(1, int(total_width / self.content_width) + 1)

        return self.ELEMENT_HEIGHTS['p_base'] + lines * self.ELEMENT_HEIGHTS['p_line'] + self.ELEMENT_HEIGHTS['margin_bottom']

    def _calculate_paragraph_height(self, text: str) -> int:
        """计算段落高度"""
        if not text:
            return self.ELEMENT_HEIGHTS['p_base'] + self.ELEMENT_HEIGHTS['margin_bottom']

        # 更精确的计算（中英文混排）
        total_width = 0
        for ch in text:
            total_width += self.CHAR_WIDTH if ord(ch) > 127 else self.CHAR_WIDTH_EN
        lines = max(1, int(total_width / self.content_width) + 1)

        return self.ELEMENT_HEIGHTS['p_base'] + lines * self.ELEMENT_HEIGHTS['p_line'] + self.ELEMENT_HEIGHTS['margin_bottom']

    def _calculate_blockquote_height(self, text: str) -> int:
        """计算引用块高度"""
        if not text:
            return self.ELEMENT_HEIGHTS['blockquote']

        # 引用块内容宽度更窄
        effective_width = self.content_width - 60
        chars_per_line = max(1, effective_width // self.CHAR_WIDTH)
        lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)

        return self.ELEMENT_HEIGHTS['blockquote'] + lines * self.ELEMENT_HEIGHTS['blockquote_line'] + self.ELEMENT_HEIGHTS['margin_bottom']

    def parse_html_to_elements(self, html: str) -> List[PageElement]:
        """
        将HTML解析为页面元素列表
        """
        if not html or not html.strip():
            return []

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, 'html.parser')

        # 收集所有元素
        elements = []

        # 如果soup本身就是一个标签，处理它
        if isinstance(soup, Tag):
            nodes = list(soup.children)
        else:
            nodes = list(soup.children)

        # 遍历顶层节点
        for node in nodes:
            if isinstance(node, Comment):
                continue
            if isinstance(node, NavigableString):
                text = str(node).strip()
                if text:
                    height = self._calculate_text_height(text)
                    elements.append(PageElement(
                        type='text',
                        content=str(node),
                        text=text,
                        height=height,
                        can_break=True
                    ))
                continue
            if not isinstance(node, Tag):
                continue

            # 处理分页标记
            if self._is_pagebreak_marker(node):
                elements.append(PageElement(
                    type='pagebreak',
                    content=str(node),
                    text='',
                    height=self.ELEMENT_HEIGHTS['hr'],
                    can_break=False
                ))
                continue

            # 分发处理
            child_elements = self._process_node(node)
            elements.extend(child_elements)

        return elements

    def _process_node(self, node) -> List[PageElement]:
        """递归处理节点"""
        elements = []

        if isinstance(node, NavigableString):
            text = str(node).strip()
            if text:
                height = self._calculate_text_height(text)
                elements.append(PageElement(
                    type='text',
                    content=text,
                    text=text,
                    height=height,
                    can_break=True
                ))
            return elements

        if not isinstance(node, Tag):
            return elements

        # 强制分页标记
        if self._is_pagebreak_marker(node):
            elements.append(PageElement(
                type='pagebreak',
                content=str(node),
                text='',
                height=self.ELEMENT_HEIGHTS['hr'],
                can_break=False
            ))
            return elements

        tag_name = node.name.lower()

        # 先检查内部是否有分页标记
        has_pagebreak = any(self._is_pagebreak_marker(child) for child in node.find_all() if isinstance(child, Tag))

        if has_pagebreak:
            # 递归处理包含分页标记的段落
            for child in node.children:
                elements.extend(self._process_node(child))
        else:
            # 处理具体的元素类型
            if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # 标题
                text = node.get_text(strip=True)
                if text:
                    level = int(tag_name[1])
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
                # 普通段落
                text = node.get_text(strip=True)
                imgs = node.find_all('img')
                if text:
                    if imgs:
                        # 包含图片的段落（图文）
                        text_height = self._calculate_paragraph_height(text)
                        img_height = len(imgs) * 300
                        total_height = text_height + img_height
                        elements.append(PageElement(
                            type='paragraph_with_images',
                            content=str(node),
                            text=text,
                            height=total_height,
                            can_break=False
                        ))
                    else:
                        # 纯文本段落
                        height = self._calculate_paragraph_height(text)
                        elements.append(PageElement(
                            type='paragraph',
                            content=str(node),
                            text=text,
                            height=height,
                            can_break=True
                        ))
                else:
                    # 没有文本内容
                    if imgs:
                        # 纯图片段落（如 <p><img/></p>）
                        total_height = len(imgs) * 300 + self.ELEMENT_HEIGHTS['margin_bottom']
                        elements.append(PageElement(
                            type='paragraph_with_images',
                            content=str(node),
                            text='',
                            height=total_height,
                            can_break=False
                        ))
                    else:
                        # 空段落，给最小基础高度，避免被完全忽略
                        height = self.ELEMENT_HEIGHTS['p_base']
                        elements.append(PageElement(
                            type='paragraph',
                            content=str(node),
                            text='',
                            height=height,
                            can_break=True
                        ))

            elif tag_name == 'img':
                # 图片
                alt = node.get('alt', '图片')
                elements.append(PageElement(
                    type='image',
                    content=str(node),
                    text=alt,
                    height=300 + self.ELEMENT_HEIGHTS['margin_bottom'],
                    can_break=False
                ))

            elif tag_name in ['ul', 'ol']:
                # 列表
                items = node.find_all('li', recursive=False)
                imgs = node.find_all('img')
                list_height = len(items) * self.ELEMENT_HEIGHTS['li']
                img_height = len(imgs) * 300
                total_height = list_height + img_height + self.ELEMENT_HEIGHTS['margin_bottom']
                elements.append(PageElement(
                    type='list',
                    content=str(node),
                    text=node.get_text(strip=True),
                    height=total_height,
                    can_break=True
                ))

            elif tag_name == 'pre':
                # 代码块
                code_elem = node.find('code')
                code_text = code_elem.get_text() if code_elem else node.get_text()
                lines = max(1, len(code_text.splitlines()))
                height = (self.ELEMENT_HEIGHTS['code_block'] +
                          lines * self.ELEMENT_HEIGHTS['code_line'] +
                          self.ELEMENT_HEIGHTS['margin_bottom'])
                elements.append(PageElement(
                    type='code',
                    content=str(node),
                    text=code_text,
                    height=height,
                    can_break=lines > 10
                ))

            elif tag_name == 'blockquote':
                # 引用块
                text = node.get_text(strip=True)
                imgs = node.find_all('img')
                if text:
                    text_height = self._calculate_blockquote_height(text)
                    img_height = len(imgs) * 300
                    total_height = text_height + img_height
                    elements.append(PageElement(
                        type='blockquote',
                        content=str(node),
                        text=text,
                        height=total_height,
                        can_break=True
                    ))
                else:
                    if imgs:
                        total_height = len(imgs) * 300 + self.ELEMENT_HEIGHTS['margin_bottom']
                        elements.append(PageElement(
                            type='blockquote',
                            content=str(node),
                            text='',
                            height=total_height,
                            can_break=False
                        ))
                    else:
                        # 空引用块，给基础高度
                        height = self.ELEMENT_HEIGHTS['blockquote'] + self.ELEMENT_HEIGHTS['margin_bottom']
                        elements.append(PageElement(
                            type='blockquote',
                            content=str(node),
                            text='',
                            height=height,
                            can_break=True
                        ))

            elif tag_name == 'table':
                # 表格
                rows = node.find_all('tr')
                if rows:
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
                        can_break=True
                    ))
                else:
                    elements.append(PageElement(
                        type='table',
                        content=str(node),
                        text='',
                        height=self.ELEMENT_HEIGHTS['table_row'] + self.ELEMENT_HEIGHTS['margin_bottom'],
                        can_break=True
                    ))

            elif tag_name == 'hr':
                # 分隔线
                elements.append(PageElement(
                    type='hr',
                    content=str(node),
                    text='',
                    height=self.ELEMENT_HEIGHTS['hr'],
                    can_break=False
                ))

            elif tag_name in ['div', 'section', 'article', 'main']:
                # 容器：递归处理子元素
                for child in node.children:
                    child_elements = self._process_node(child)
                    elements.extend(child_elements)

            else:
                # 其他元素
                text = node.get_text(strip=True)
                if text:
                    # 如果包含子标签，递归处理子节点
                    if node.find_all():
                        for child in node.children:
                            child_elements = self._process_node(child)
                            elements.extend(child_elements)
                    else:
                        # 纯文本内容
                        elements.append(PageElement(
                            type='unknown',
                            content=str(node),
                            text=text,
                            height=self._calculate_text_height(text),
                            can_break=True
                        ))

        return elements

    def _is_pagebreak_marker(self, element: Tag) -> bool:
        """
        检查元素是否是分页标记
        """
        if not isinstance(element, Tag):
            return False

        # 1) class 名称中包含 pagebreak-marker
        classes = element.get('class', [])
        if isinstance(classes, list):
            if 'pagebreak-marker' in classes:
                return True

        # 2) data 属性标记
        if element.get('data-pagebreak') == 'true':
            return True

        return False

    def optimize_pages(self, pages: List[str]) -> List[str]:
        """
        优化分页结果，合并过短的页面
        """
        if len(pages) <= 1:
            return pages

        optimized = []
        i = 0

        # 根据页面尺寸调整合并阈值
        merge_threshold = 0.3 if self.page_size_name == "small" else 0.35

        while i < len(pages):
            current_page = pages[i]
            if not current_page or not current_page.strip():
                i += 1
                continue

            # 估算当前页面高度
            current_elements = self.parse_html_to_elements(current_page)
            current_height = sum(e.height for e in current_elements)

            # 如果页面过短，尝试与下一页合并
            if current_height < self.content_height * merge_threshold and i < len(pages) - 1:
                next_page_index = i + 1
                # 不合并强制分页的页面
                if next_page_index not in self.forced_break_pages:
                    next_page = pages[next_page_index]
                    if next_page and next_page.strip():
                        next_elements = self.parse_html_to_elements(next_page)
                        next_height = sum(e.height for e in next_elements)

                        # 如果合并后不超过最大高度，则合并
                        if current_height + next_height <= self.content_height * 0.95:  # 留5%余量
                            optimized.append(current_page + '\n' + next_page)
                            i += 2
                            continue

            optimized.append(current_page)
            i += 1

        return optimized if optimized else pages

    def debug_pagination(self, html_content: str) -> List[dict]:
        """
        调试用：返回每一页的高度明细
        """
        pages = self.paginate(html_content)
        pages_info = []

        for i, page in enumerate(pages, start=1):
            page_elements = self.parse_html_to_elements(page)
            total_height = sum(e.height for e in page_elements)

            pages_info.append({
                'page_index': i,
                'elements_count': len(page_elements),
                'total_height': total_height,
                'max_height': self.content_height,
                'fill_rate': f"{(total_height / self.content_height * 100):.1f}%",
                'is_forced_break': (i-1) in self.forced_break_pages,
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
