# ============================================
# create_icon.py - 生成应用图标
# ============================================
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

def create_app_icon():
    """创建小红书风格的应用图标"""
    
    # 创建图标目录
    icon_dir = Path("resources/icons")
    icon_dir.mkdir(parents=True, exist_ok=True)
    
    # 定义所需的图标尺寸
    sizes = [16, 32, 48, 64, 128, 256, 512]
    
    # 创建最大尺寸的图标作为基础
    base_size = 512
    img = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制背景渐变（模拟小红书风格）
    for y in range(base_size):
        # 从粉色到红色的渐变
        ratio = y / base_size
        r = int(255 - ratio * 20)
        g = int(36 + ratio * 40)
        b = int(66 + ratio * 20)
        draw.rectangle([(0, y), (base_size, y + 1)], fill=(r, g, b, 255))
    
    # 添加圆角效果
    mask = Image.new('L', (base_size, base_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    corner_radius = 100
    mask_draw.rounded_rectangle([(0, 0), (base_size, base_size)], 
                                radius=corner_radius, fill=255)
    
    # 应用遮罩
    output = Image.new('RGBA', (base_size, base_size), (0, 0, 0, 0))
    output.paste(img, (0, 0))
    output.putalpha(mask)
    img = output
    draw = ImageDraw.Draw(img)
    
    # 绘制中心的 "M" 标记（代表 Markdown）
    try:
        # 尝试使用系统字体
        font_size = 280
        try:
            # Windows
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                # 尝试其他常见字体
                font = ImageFont.truetype("Arial.ttf", font_size)
            except:
                # 使用默认字体
                font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # 绘制白色的 "M" 字母
    text = "M"
    # 获取文本边界框
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # 计算居中位置
    x = (base_size - text_width) // 2
    y = (base_size - text_height) // 2 - 20  # 稍微上移
    
    # 添加阴影效果
    shadow_offset = 8
    draw.text((x + shadow_offset, y + shadow_offset), text, 
             fill=(0, 0, 0, 100), font=font)
    
    # 绘制主文字
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # 添加小的装饰元素 - 小红书风格的笔记本线条
    line_color = (255, 255, 255, 80)
    line_width = 3
    line_spacing = 40
    
    # 底部装饰线
    for i in range(3):
        y_pos = base_size - 80 - (i * line_spacing)
        draw.rectangle([(60, y_pos), (base_size - 60, y_pos + line_width)], 
                      fill=line_color)
    
    # 生成不同尺寸的图标
    icons = {}
    for size in sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        icon_path = icon_dir / f"icon_{size}x{size}.png"
        resized.save(icon_path, 'PNG')
        icons[size] = icon_path
        print(f"Created: {icon_path}")
    
    # 生成 ICO 文件（Windows需要）
    ico_path = icon_dir / "app.ico"
    img.save(ico_path, format='ICO', sizes=[(s, s) for s in [16, 32, 48, 64, 128, 256]])
    print(f"Created: {ico_path}")
    
    # 保存原始大图标
    original_path = icon_dir / "icon_original.png"
    img.save(original_path, 'PNG')
    print(f"Created: {original_path}")
    
    return ico_path

def create_simple_icon_alternative():
    """创建简化版图标（如果没有PIL库）"""
    import tkinter as tk
    from tkinter import Canvas
    import base64
    
    # 创建图标目录
    icon_dir = Path("resources/icons")
    icon_dir.mkdir(parents=True, exist_ok=True)
    
    # 使用tkinter创建简单图标
    root = tk.Tk()
    root.withdraw()
    
    size = 256
    canvas = Canvas(root, width=size, height=size)
    
    # 绘制渐变背景（简化版）
    for i in range(size):
        color_val = int(255 - (i / size) * 50)
        color = f'#{color_val:02x}{int(36 + (i/size)*40):02x}{int(66 + (i/size)*20):02x}'
        canvas.create_line(0, i, size, i, fill=color)
    
    # 绘制 M 字母
    canvas.create_text(size//2, size//2, text="M", 
                       font=("Arial", 120, "bold"), 
                       fill="white")
    
    # 保存为PostScript然后转换
    ps_file = icon_dir / "temp.ps"
    canvas.postscript(file=str(ps_file))
    
    print("Simple icon created (requires manual conversion from PS to ICO)")
    return None

if __name__ == "__main__":
    try:
        # 尝试使用PIL创建高质量图标
        from PIL import Image, ImageDraw, ImageFont
        ico_path = create_app_icon()
        print(f"\n✅ 应用图标创建成功！")
        print(f"ICO文件位置: {ico_path}")
    except ImportError:
        print("⚠️ 需要安装 Pillow 库来生成图标")
        print("请运行: pip install Pillow")
        print("\n尝试创建简化版图标...")
        create_simple_icon_alternative()