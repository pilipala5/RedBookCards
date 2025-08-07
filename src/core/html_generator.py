# ============================================
# src/core/html_generator.py
# ============================================
from pathlib import Path
from typing import Optional
from src.utils.style_manager import StyleManager

class HTMLGenerator:
    def __init__(self, font_size: int = 18, page_size: str = "medium", theme: str = "xiaohongshu"):
        self.resource_path = Path(__file__).parent.parent / "resources"
        self.base_font_size = font_size  # 基础字体大小，默认18px
        
        # 页面尺寸配置
        self.page_sizes = {
            "small": {"width": 720, "height": 960},
            "medium": {"width": 1080, "height": 1440},
            "large": {"width": 1440, "height": 1920}
        }
        self.current_size = page_size
        self.page_width = self.page_sizes[page_size]["width"]
        self.page_height = self.page_sizes[page_size]["height"]
        
        # 样式管理器
        self.style_manager = StyleManager(theme)
        self.current_theme = theme
        
    def set_page_size(self, size: str):
        """设置页面尺寸"""
        if size in self.page_sizes:
            self.current_size = size
            self.page_width = self.page_sizes[size]["width"]
            self.page_height = self.page_sizes[size]["height"]
    
    def set_theme(self, theme: str):
        """设置主题"""
        self.current_theme = theme
        self.style_manager.set_theme(theme)
    
    def set_font_size(self, size: int):
        """设置基础字体大小"""
        self.base_font_size = size
        
    def generate(self, content: str, page_num: int = 0, total_pages: int = 0) -> str:
        """
        生成完整的 HTML 页面
        
        Args:
            content: HTML内容
            page_num: 当前页码（0表示不显示）
            total_pages: 总页数
        """
        # 生成主题CSS
        theme_css = self.style_manager.generate_css(self.current_theme, self.base_font_size)
        
        # 生成页面特定CSS
        page_css = self.get_page_css()
        
        # 获取JavaScript
        js = self.get_js()
        
        # 生成页码信息（如果需要）
        page_info = ""
        if page_num > 0 and total_pages > 1:
            page_info = f"""
            <div class="page-info">
                <span class="page-number">{page_num}</span>
                <span class="page-separator">/</span>
                <span class="page-total">{total_pages}</span>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小红书卡片 - {self.style_manager.get_theme().name}</title>
    <style>
        {theme_css}
        {page_css}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="content" id="content">
                {content}
            </div>
            {page_info}
        </div>
    </div>
    <script>{js}</script>
</body>
</html>
"""
        return html
    
    def get_page_css(self) -> str:
        """获取页面布局CSS"""
        theme = self.style_manager.get_theme()
        
        # 检查是否为深色主题
        is_dark = self.current_theme in ["dark_mode", "midnight", "douyin"]
        
        return f"""
        /* 页面布局 */
        html, body {{
            width: {self.page_width}px;
            height: {self.page_height}px;
            overflow: hidden !important;
            margin: 0;
            padding: 0;
        }}
        
        .container {{
            width: {self.page_width}px;
            height: {self.page_height}px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 0;
        }}
        
        .card {{
            width: 100%;
            height: 100%;
            background: {'rgba(255, 255, 255, 0.98)' if not is_dark else 'rgba(20, 20, 35, 0.98)'};
            border-radius: 20px;
            box-shadow: 0 20px 60px {self.style_manager.add_alpha(theme.primary_color, 0.15)},
                        0 10px 30px {self.style_manager.add_alpha('#000000', 0.1)};
            overflow: hidden;
            position: relative;
        }}
        
        .content {{
            padding: 50px 45px 70px 45px;
            color: var(--text-color);
            line-height: 1.85;
            height: 100%;
            overflow: hidden !important;
            position: relative;
        }}
        
        /* 页码信息 */
        .page-info {{
            position: absolute;
            bottom: 20px;
            right: 30px;
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 8px 16px;
            background: {self.style_manager.add_alpha(theme.primary_color, 0.1)};
            border-radius: 20px;
            border: 1px solid {self.style_manager.add_alpha(theme.primary_color, 0.2)};
        }}
        
        .page-number {{
            font-weight: 700;
            color: var(--primary-color);
            font-size: 14px;
        }}
        
        .page-separator {{
            color: {self.style_manager.add_alpha(theme.text_color, 0.4)};
            font-size: 12px;
        }}
        
        .page-total {{
            color: {self.style_manager.add_alpha(theme.text_color, 0.6)};
            font-size: 14px;
        }}
        
        /* 装饰元素 */
        .card::before {{
            content: "";
            position: absolute;
            top: -50%;
            right: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, {self.style_manager.add_alpha(theme.primary_color, 0.1)} 0%, transparent 70%);
            pointer-events: none;
        }}
        
        .card::after {{
            content: "";
            position: absolute;
            bottom: -50%;
            left: -50%;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle, {self.style_manager.add_alpha(theme.secondary_color, 0.1)} 0%, transparent 70%);
            pointer-events: none;
        }}
        
        /* 响应式图片 */
        img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            margin: 20px 0;
            box-shadow: 0 8px 24px {self.style_manager.add_alpha('#000000', 0.1)};
        }}
        
        /* 隐藏滚动条 */
        ::-webkit-scrollbar {{
            display: none !important;
        }}
        
        * {{
            scrollbar-width: none !important;
            -ms-overflow-style: none !important;
        }}
        
        /* 打印样式 */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                max-width: 100%;
            }}
            
            .card {{
                box-shadow: none;
                border-radius: 0;
                page-break-inside: avoid;
            }}
            
            .card::before,
            .card::after {{
                display: none;
            }}
        }}

        /* 完全隐藏分页标记 */
        .pagebreak-marker {{
            display: none !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            visibility: hidden !important;
        }}
        """
    
    def get_js(self) -> str:
        """获取JavaScript代码"""
        return """
        // 页面加载完成后的处理
        document.addEventListener('DOMContentLoaded', function() {
            // 添加淡入动画
            const content = document.getElementById('content');
            if (content) {
                content.style.opacity = '0';
                content.style.transition = 'opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                setTimeout(() => {
                    content.style.opacity = '1';
                }, 100);
            }
            
            // 图片延迟加载和动画
            const images = document.querySelectorAll('img');
            images.forEach((img, index) => {
                img.loading = 'lazy';
                img.style.opacity = '0';
                img.style.transform = 'translateY(20px)';
                img.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                
                // 图片加载完成后显示
                if (img.complete) {
                    setTimeout(() => {
                        img.style.opacity = '1';
                        img.style.transform = 'translateY(0)';
                    }, 100 * (index + 1));
                } else {
                    img.addEventListener('load', () => {
                        setTimeout(() => {
                            img.style.opacity = '1';
                            img.style.transform = 'translateY(0)';
                        }, 100);
                    });
                }
            });
            
            // 代码块增强
            const codeBlocks = document.querySelectorAll('pre');
            codeBlocks.forEach(block => {
                // 添加语言标识
                const code = block.querySelector('code');
                if (code && code.className) {
                    const lang = code.className.replace('language-', '');
                    if (lang) {
                        block.setAttribute('data-language', lang.toUpperCase());
                    }
                }
            });
            
            // 表格增强
            const tables = document.querySelectorAll('table');
            tables.forEach(table => {
                // 添加响应式包装
                const wrapper = document.createElement('div');
                wrapper.style.overflowX = 'auto';
                wrapper.style.marginBottom = '20px';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            });
            
            // 确保内容不超出
            function ensureContentFit() {
                const card = document.querySelector('.card');
                const content = document.querySelector('.content');
                if (card && content) {
                    content.style.maxHeight = '100%';
                    content.style.overflow = 'hidden';
                }
            }
            
            ensureContentFit();
            window.addEventListener('resize', ensureContentFit);
        });
        
        // 禁用所有滚动
        window.addEventListener('scroll', function(e) {
            e.preventDefault();
            window.scrollTo(0, 0);
        }, { passive: false });
        
        window.addEventListener('wheel', function(e) {
            e.preventDefault();
        }, { passive: false });
        
        window.addEventListener('touchmove', function(e) {
            e.preventDefault();
        }, { passive: false });
        """