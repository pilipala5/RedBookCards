# ============================================
# src/utils/style_manager.py
# ============================================
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class ThemeConfig:
    """主题配置"""
    name: str
    primary_color: str
    secondary_color: str
    text_color: str
    background: str
    font_family: str
    heading_font: str
    code_font: str
    
class StyleManager:
    """样式管理器"""
    
    # 预设主题
    THEMES = {
        "xiaohongshu": ThemeConfig(
            name="小红书",
            primary_color="#FF2442",
            secondary_color="#FF6B6B",
            text_color="#2c3e50",
            background="linear-gradient(135deg, #ffeef8 0%, #ffe0f0 100%)",
            font_family='-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Helvetica Neue", sans-serif',
            code_font='"JetBrains Mono", "Cascadia Code", "Consolas", monospace'
        ),
        "instagram": ThemeConfig(
            name="Instagram",
            primary_color="#E4405F",
            secondary_color="#BC2A8D",
            text_color="#262626",
            background="linear-gradient(45deg, #F9ED69 0%, #EE2A7B 50%, #6228D7 100%)",
            font_family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
            heading_font='"Segoe UI", Roboto, sans-serif',
            code_font='"Monaco", "Courier New", monospace'
        ),
        "wechat": ThemeConfig(
            name="微信",
            primary_color="#07C160",
            secondary_color="#4CAF50",
            text_color="#353535",
            background="linear-gradient(180deg, #F7F7F7 0%, #FFFFFF 100%)",
            font_family='"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Microsoft YaHei", sans-serif',
            code_font='"SF Mono", "Monaco", "Inconsolata", monospace'
        ),
        "zhihu": ThemeConfig(
            name="知乎",
            primary_color="#0084FF",
            secondary_color="#1890FF",
            text_color="#1A1A1A",
            background="linear-gradient(180deg, #FFFFFF 0%, #F6F6F6 100%)",
            font_family='"PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Helvetica Neue", sans-serif',
            code_font='"Source Code Pro", "Consolas", monospace'
        ),
        "dark": ThemeConfig(
            name="深色模式",
            primary_color="#00E0FF",
            secondary_color="#0096FF",
            text_color="#E0E6ED",
            background="linear-gradient(135deg, #0F0F1E 0%, #1A1A2E 50%, #16213E 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Fira Code", "JetBrains Mono", monospace'
        )
    }
    
    def __init__(self, theme: str = "xiaohongshu"):
        self.current_theme = theme
        self.custom_styles = {}
        
    def get_theme(self, theme_name: str = None) -> ThemeConfig:
        """获取主题配置"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.THEMES.get(theme_name, self.THEMES["xiaohongshu"])
    
    def set_theme(self, theme_name: str):
        """设置当前主题"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
    
    def generate_css(self, theme_name: str = None) -> str:
        """生成主题CSS"""
        theme = self.get_theme(theme_name)
        
        return f"""
        /* 主题: {theme.name} */
        :root {{
            --primary-color: {theme.primary_color};
            --secondary-color: {theme.secondary_color};
            --text-color: {theme.text_color};
            --font-family: {theme.font_family};
            --heading-font: {theme.heading_font};
            --code-font: {theme.code_font};
        }}
        
        body {{
            font-family: var(--font-family);
            background: {theme.background};
            color: var(--text-color);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--heading-font);
            color: var(--primary-color);
        }}
        
        h1 {{
            border-bottom-color: {self._lighten_color(theme.primary_color, 0.7)};
        }}
        
        h2::before {{
            background: linear-gradient(180deg, {theme.primary_color}, {theme.secondary_color});
        }}
        
        strong {{
            color: var(--primary-color);
            background: linear-gradient(180deg, transparent 70%, {self._lighten_color(theme.primary_color, 0.8)} 70%);
        }}
        
        ul li::marker, ol li::marker {{
            color: var(--primary-color);
        }}
        
        blockquote {{
            border-left-color: var(--primary-color);
            background: linear-gradient(90deg, {self._lighten_color(theme.primary_color, 0.95)} 0%, #FFFFFF 100%);
        }}
        
        code {{
            font-family: var(--code-font);
            background: {self._lighten_color(theme.primary_color, 0.95)};
            color: {self._darken_color(theme.primary_color, 0.2)};
        }}
        
        pre {{
            font-family: var(--code-font);
        }}
        
        th {{
            background: linear-gradient(135deg, {theme.primary_color}, {theme.secondary_color});
        }}
        
        a {{
            color: var(--primary-color);
            border-bottom-color: {self._lighten_color(theme.primary_color, 0.5)};
        }}
        
        a:hover {{
            color: var(--secondary-color);
            border-bottom-color: var(--secondary-color);
            background: {self._lighten_color(theme.primary_color, 0.95)};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {theme.secondary_color}, {theme.primary_color});
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, {theme.primary_color}, {self._darken_color(theme.primary_color, 0.2)});
        }}
        """
    
    def _lighten_color(self, color: str, amount: float) -> str:
        """使颜色变浅"""
        # 简化实现，实际应该进行RGB计算
        if amount >= 0.9:
            return f"{color}10"  # 添加透明度
        elif amount >= 0.7:
            return f"{color}30"
        else:
            return f"{color}50"
    
    def _darken_color(self, color: str, amount: float) -> str:
        """使颜色变深"""
        # 简化实现
        return color
    
    def get_export_settings(self, theme_name: str = None) -> Dict[str, Any]:
        """获取导出设置"""
        theme = self.get_theme(theme_name)
        
        return {
            "page_width": 1080,
            "page_height": 1440,
            "padding": {
                "top": 45,
                "bottom": 45,
                "left": 40,
                "right": 40
            },
            "font_size": 16,
            "line_height": 1.8,
            "paragraph_spacing": 20,
            "image_quality": 100,
            "format": "PNG"
        }
    
    def apply_custom_styles(self, styles: Dict[str, str]):
        """应用自定义样式"""
        self.custom_styles.update(styles)
    
    def get_combined_css(self, theme_name: str = None) -> str:
        """获取组合的CSS（主题 + 自定义）"""
        base_css = self.generate_css(theme_name)
        
        if self.custom_styles:
            custom_css = "\n/* 自定义样式 */\n"
            for selector, rules in self.custom_styles.items():
                custom_css += f"{selector} {{\n{rules}\n}}\n"
            return base_css + custom_css
        
        return base_css