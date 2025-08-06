# ============================================
# src/utils/style_manager.py
# ============================================
from typing import Dict, Any, Tuple
from dataclasses import dataclass
import colorsys

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
    accent_color: str = ""  # 强调色
    link_color: str = ""    # 链接色
    
class StyleManager:
    """样式管理器 - 扩展版"""
    
    # 预设主题 - 12种风格
    THEMES = {
        # 社交媒体风格
        "xiaohongshu": ThemeConfig(
            name="小红书经典",
            primary_color="#FF2442",
            secondary_color="#FF6B6B",
            text_color="#2c3e50",
            background="linear-gradient(135deg, #ffeef8 0%, #ffe0f0 100%)",
            font_family='-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Helvetica Neue", sans-serif',
            code_font='"JetBrains Mono", "Cascadia Code", "Consolas", monospace',
            accent_color="#FFB6C1",
            link_color="#FF69B4"
        ),
        
        "instagram": ThemeConfig(
            name="Instagram渐变",
            primary_color="#E4405F",
            secondary_color="#BC2A8D",
            text_color="#262626",
            background="linear-gradient(45deg, #F9ED69 0%, #EE2A7B 50%, #6228D7 100%)",
            font_family='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
            heading_font='"Segoe UI", Roboto, sans-serif',
            code_font='"Monaco", "Courier New", monospace',
            accent_color="#FCAF45",
            link_color="#833AB4"
        ),
        
        "wechat": ThemeConfig(
            name="微信简约",
            primary_color="#07C160",
            secondary_color="#4CAF50",
            text_color="#353535",
            background="linear-gradient(180deg, #F7F7F7 0%, #FFFFFF 100%)",
            font_family='"PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Microsoft YaHei", sans-serif',
            code_font='"SF Mono", "Monaco", "Inconsolata", monospace',
            accent_color="#95EC69",
            link_color="#576B95"
        ),
        
        "douyin": ThemeConfig(
            name="抖音酷黑",
            primary_color="#FE2C55",
            secondary_color="#25F4EE",
            text_color="#FFFFFF",
            background="linear-gradient(135deg, #000000 0%, #161823 100%)",
            font_family='"PingFang SC", "Helvetica Neue", Arial, sans-serif',
            heading_font='"PingFang SC", "Helvetica Neue", sans-serif',
            code_font='"Fira Code", "Source Code Pro", monospace',
            accent_color="#00F2EA",
            link_color="#FE2C55"
        ),
        
        # 知识平台风格
        "zhihu": ThemeConfig(
            name="知乎蓝",
            primary_color="#0084FF",
            secondary_color="#1890FF",
            text_color="#1A1A1A",
            background="linear-gradient(180deg, #FFFFFF 0%, #F6F6F6 100%)",
            font_family='"PingFang SC", "Helvetica Neue", "Microsoft YaHei", sans-serif',
            heading_font='"PingFang SC", "Helvetica Neue", sans-serif',
            code_font='"Source Code Pro", "Consolas", monospace',
            accent_color="#5BBCFF",
            link_color="#175199"
        ),
        
        "notion": ThemeConfig(
            name="Notion极简",
            primary_color="#000000",
            secondary_color="#2F3437",
            text_color="#37352F",
            background="linear-gradient(180deg, #FFFFFF 0%, #FAFAFA 100%)",
            font_family='"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
            heading_font='"Inter", -apple-system, sans-serif',
            code_font='"SFMono-Regular", "Consolas", "Liberation Mono", monospace',
            accent_color="#EB5757",
            link_color="#0070F3"
        ),
        
        # 优雅风格
        "elegant_purple": ThemeConfig(
            name="优雅紫",
            primary_color="#6B46C1",
            secondary_color="#9333EA",
            text_color="#1F2937",
            background="linear-gradient(135deg, #F9FAFB 0%, #F3E8FF 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Playfair Display", "PingFang SC", serif',
            code_font='"JetBrains Mono", "Cascadia Code", monospace',
            accent_color="#A78BFA",
            link_color="#7C3AED"
        ),
        
        "ocean_blue": ThemeConfig(
            name="海洋蓝",
            primary_color="#0EA5E9",
            secondary_color="#06B6D4",
            text_color="#0F172A",
            background="linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 50%, #BAE6FD 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Fira Code", "Consolas", monospace',
            accent_color="#38BDF8",
            link_color="#0284C7"
        ),
        
        "sunset_orange": ThemeConfig(
            name="日落橙",
            primary_color="#F97316",
            secondary_color="#FB923C",
            text_color="#1C1917",
            background="linear-gradient(135deg, #FFF7ED 0%, #FED7AA 50%, #FDBA74 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Source Code Pro", "Monaco", monospace',
            accent_color="#FCD34D",
            link_color="#EA580C"
        ),
        
        "forest_green": ThemeConfig(
            name="森林绿",
            primary_color="#059669",
            secondary_color="#10B981",
            text_color="#064E3B",
            background="linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 50%, #A7F3D0 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"JetBrains Mono", monospace',
            accent_color="#34D399",
            link_color="#047857"
        ),
        
        # 深色主题
        "dark_mode": ThemeConfig(
            name="深色模式",
            primary_color="#00E0FF",
            secondary_color="#0096FF",
            text_color="#E0E6ED",
            background="linear-gradient(135deg, #0F0F1E 0%, #1A1A2E 50%, #16213E 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Fira Code", "JetBrains Mono", monospace',
            accent_color="#00F0FF",
            link_color="#00B8D4"
        ),
        
        "midnight": ThemeConfig(
            name="午夜紫",
            primary_color="#B794F4",
            secondary_color="#9F7AEA",
            text_color="#E9D8FD",
            background="linear-gradient(135deg, #1A202C 0%, #2D3748 50%, #4A5568 100%)",
            font_family='"Inter", "PingFang SC", "Microsoft YaHei", sans-serif',
            heading_font='"Inter", "PingFang SC", sans-serif',
            code_font='"Cascadia Code", "Fira Code", monospace',
            accent_color="#D6BCFA",
            link_color="#B794F4"
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
    
    def get_theme_list(self) -> list:
        """获取所有主题列表"""
        return list(self.THEMES.keys())
    
    def get_theme_display_names(self) -> Dict[str, str]:
        """获取主题显示名称"""
        return {key: theme.name for key, theme in self.THEMES.items()}
    
    def set_theme(self, theme_name: str):
        """设置当前主题"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """十六进制颜色转RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """RGB转十六进制"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def lighten_color(self, hex_color: str, amount: float) -> str:
        """使颜色变浅（amount: 0-1）"""
        r, g, b = self.hex_to_rgb(hex_color)
        # 转换为HSL
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        # 增加亮度
        l = min(1.0, l + (1 - l) * amount)
        # 转回RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return self.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def darken_color(self, hex_color: str, amount: float) -> str:
        """使颜色变深（amount: 0-1）"""
        r, g, b = self.hex_to_rgb(hex_color)
        # 转换为HSL
        h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
        # 降低亮度
        l = max(0.0, l * (1 - amount))
        # 转回RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return self.rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def add_alpha(self, hex_color: str, alpha: float) -> str:
        """添加透明度（返回rgba格式）"""
        r, g, b = self.hex_to_rgb(hex_color)
        return f"rgba({r}, {g}, {b}, {alpha})"
    
    def generate_css(self, theme_name: str = None, font_size: int = 18) -> str:
        """生成主题CSS"""
        theme = self.get_theme(theme_name)
        
        # 生成派生颜色
        primary_light = self.lighten_color(theme.primary_color, 0.9)
        primary_dark = self.darken_color(theme.primary_color, 0.2)
        secondary_light = self.lighten_color(theme.secondary_color, 0.9)
        
        # 检查是否为深色主题
        is_dark = theme_name in ["dark_mode", "midnight", "douyin"]
        
        return f"""
        /* 主题: {theme.name} */
        :root {{
            --primary-color: {theme.primary_color};
            --secondary-color: {theme.secondary_color};
            --accent-color: {theme.accent_color or theme.secondary_color};
            --text-color: {theme.text_color};
            --link-color: {theme.link_color or theme.primary_color};
            --font-family: {theme.font_family};
            --heading-font: {theme.heading_font};
            --code-font: {theme.code_font};
            --primary-light: {primary_light};
            --primary-dark: {primary_dark};
            --secondary-light: {secondary_light};
            --base-font-size: {font_size}px;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: var(--font-family);
            background: {theme.background};
            color: var(--text-color);
            font-size: var(--base-font-size);
            line-height: 1.85;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        /* 标题样式 */
        h1, h2, h3, h4, h5, h6 {{
            font-family: var(--heading-font);
            color: var(--primary-color);
            font-weight: 700;
            letter-spacing: -0.02em;
        }}
        
        h1 {{
            font-size: calc(var(--base-font-size) + 16px);
            margin-bottom: 28px;
            padding-bottom: 16px;
            border-bottom: 3px solid {self.add_alpha(theme.primary_color, 0.2)};
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        h2 {{
            font-size: calc(var(--base-font-size) + 10px);
            margin-top: 38px;
            margin-bottom: 22px;
            position: relative;
            padding-left: 20px;
        }}
        
        h2::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 5px;
            height: 24px;
            background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
            border-radius: 3px;
            box-shadow: 0 2px 8px {self.add_alpha(theme.primary_color, 0.3)};
        }}
        
        h3 {{
            font-size: calc(var(--base-font-size) + 5px);
            margin-top: 30px;
            margin-bottom: 18px;
            color: {theme.text_color if not is_dark else theme.secondary_color};
        }}
        
        /* 段落样式 */
        p {{
            margin-bottom: 22px;
            font-size: var(--base-font-size);
            color: var(--text-color);
            text-align: justify;
            line-height: 1.85;
        }}
        
        /* 强调样式 */
        strong {{
            color: var(--primary-color);
            font-weight: 600;
            background: linear-gradient(180deg, transparent 70%, {self.add_alpha(theme.primary_color, 0.2)} 70%);
            padding: 0 4px;
            border-radius: 2px;
        }}
        
        em {{
            font-style: italic;
            color: {self.darken_color(theme.text_color, 0.2) if not is_dark else self.lighten_color(theme.text_color, 0.2)};
        }}
        
        /* 列表样式 */
        ul, ol {{
            margin: 24px 0;
            padding-left: 38px;
        }}
        
        li {{
            margin-bottom: 16px;
            font-size: var(--base-font-size);
            color: var(--text-color);
            line-height: 1.85;
            position: relative;
        }}
        
        ul li::marker {{
            color: var(--primary-color);
            font-size: calc(var(--base-font-size) + 2px);
        }}
        
        ol li::marker {{
            color: var(--primary-color);
            font-weight: 600;
        }}
        
        /* 引用样式 */
        blockquote {{
            border-left: 4px solid var(--primary-color);
            margin: 28px 0;
            padding: 20px 28px;
            background: {self.add_alpha(theme.primary_color, 0.05) if not is_dark else self.add_alpha(theme.primary_color, 0.1)};
            border-radius: 10px;
            position: relative;
            box-shadow: 0 4px 15px {self.add_alpha(theme.primary_color, 0.1)};
        }}
        
        blockquote::before {{
            content: '"';
            position: absolute;
            top: -10px;
            left: 24px;
            font-size: 48px;
            color: {self.add_alpha(theme.primary_color, 0.3)};
            font-family: Georgia, serif;
            font-weight: bold;
        }}
        
        blockquote p {{
            color: {self.darken_color(theme.text_color, 0.1) if not is_dark else self.lighten_color(theme.text_color, 0.1)};
            font-style: italic;
            margin-bottom: 0;
            font-size: calc(var(--base-font-size) - 1px);
        }}
        
        /* 行内代码 */
        code {{
            background: {self.add_alpha(theme.primary_color, 0.1)};
            padding: 4px 10px;
            border-radius: 6px;
            font-family: var(--code-font);
            font-size: calc(var(--base-font-size) - 2px);
            color: {theme.primary_color if not is_dark else theme.accent_color};
            font-weight: 500;
            border: 1px solid {self.add_alpha(theme.primary_color, 0.2)};
        }}
        
        /* 代码块 */
        pre {{
            background: {('#1e1e1e' if not is_dark else '#0a0a0f')};
            color: #d4d4d4;
            padding: 26px;
            border-radius: 12px;
            overflow-x: auto;
            margin: 28px 0;
            box-shadow: 0 8px 24px {self.add_alpha('#000000', 0.15)};
            position: relative;
            border: 1px solid {self.add_alpha(theme.primary_color, 0.2)};
        }}
        
        pre::before {{
            content: "CODE";
            position: absolute;
            top: 12px;
            right: 16px;
            font-size: 11px;
            color: {self.add_alpha(theme.text_color, 0.5)};
            font-weight: 600;
            letter-spacing: 1px;
            font-family: var(--font-family);
        }}
        
        pre code {{
            background: none;
            color: #d4d4d4;
            padding: 0;
            font-size: calc(var(--base-font-size) - 3px);
            line-height: 1.7;
            border: none;
        }}
        
        /* 表格样式 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 28px 0;
            font-size: calc(var(--base-font-size) - 1px);
            box-shadow: 0 4px 15px {self.add_alpha(theme.primary_color, 0.08)};
            border-radius: 10px;
            overflow: hidden;
        }}
        
        th {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 15px 20px;
            text-align: left;
            font-weight: 600;
            font-size: calc(var(--base-font-size) - 1px);
            letter-spacing: 0.5px;
        }}
        
        td {{
            padding: 15px 20px;
            border-bottom: 1px solid {self.add_alpha(theme.text_color, 0.1)};
            color: var(--text-color);
        }}
        
        tr:nth-child(even) {{
            background: {self.add_alpha(theme.primary_color, 0.03)};
        }}
        
        tr:hover {{
            background: {self.add_alpha(theme.primary_color, 0.08)};
            transition: background 0.3s ease;
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        /* 分隔线 */
        hr {{
            border: none;
            height: 2px;
            background: linear-gradient(90deg, 
                transparent, 
                {self.add_alpha(theme.primary_color, 0.3)} 20%, 
                {self.add_alpha(theme.primary_color, 0.3)} 80%, 
                transparent);
            margin: 38px 0;
            position: relative;
        }}
        
        hr::after {{
            content: "✦";
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            background: {theme.background.split('(')[0] + '(180deg, #FFFFFF 0%, #FFFFFF 100%)' if 'gradient' in theme.background else '#FFFFFF'};
            color: var(--primary-color);
            padding: 0 10px;
            font-size: 20px;
        }}
        
        /* 链接样式 */
        a {{
            color: var(--link-color);
            text-decoration: none;
            border-bottom: 2px solid {self.add_alpha(theme.link_color or theme.primary_color, 0.3)};
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            padding-bottom: 1px;
            position: relative;
        }}
        
        a:hover {{
            color: var(--secondary-color);
            border-bottom-color: var(--secondary-color);
            background: {self.add_alpha(theme.primary_color, 0.08)};
            padding: 2px 6px;
            margin: -2px -6px;
            border-radius: 4px;
        }}
        
        /* 动画效果 */
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .content > * {{
            animation: fadeIn 0.5s ease-out backwards;
        }}
        
        .content > *:nth-child(1) {{ animation-delay: 0.05s; }}
        .content > *:nth-child(2) {{ animation-delay: 0.1s; }}
        .content > *:nth-child(3) {{ animation-delay: 0.15s; }}
        .content > *:nth-child(4) {{ animation-delay: 0.2s; }}
        .content > *:nth-child(5) {{ animation-delay: 0.25s; }}
        
        /* 自定义滚动条 */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {self.add_alpha(theme.text_color, 0.05)};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, var(--secondary-color), var(--primary-color));
        }}
        """
    
    def get_export_settings(self, theme_name: str = None) -> Dict[str, Any]:
        """获取导出设置"""
        theme = self.get_theme(theme_name)
        
        return {
            "theme_name": theme.name,
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
            "format": "PNG",
            "colors": {
                "primary": theme.primary_color,
                "secondary": theme.secondary_color,
                "text": theme.text_color,
                "background": theme.background
            }
        }
    
    def apply_custom_styles(self, styles: Dict[str, str]):
        """应用自定义样式"""
        self.custom_styles.update(styles)
    
    def get_combined_css(self, theme_name: str = None, font_size: int = 18) -> str:
        """获取组合的CSS（主题 + 自定义）"""
        base_css = self.generate_css(theme_name, font_size)
        
        if self.custom_styles:
            custom_css = "\n/* 自定义样式 */\n"
            for selector, rules in self.custom_styles.items():
                custom_css += f"{selector} {{\n{rules}\n}}\n"
            return base_css + custom_css
        
        return base_css