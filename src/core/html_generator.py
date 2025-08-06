# ============================================
# src/core/html_generator.py
# ============================================
from pathlib import Path

class HTMLGenerator:
    def __init__(self):
        self.resource_path = Path(__file__).parent.parent / "resources"
        
    def generate(self, content: str) -> str:
        """生成完整的 HTML 页面"""
        css = self.get_css()
        js = self.get_js()
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小红书卡片</title>
    <style>{css}</style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="content" id="content">
                {content}
            </div>
            <div class="watermark">
                <span>📝 小红书笔记</span>
            </div>
        </div>
    </div>
    <script>{js}</script>
</body>
</html>
"""
        return html
        
    def get_css(self) -> str:
        """获取优化后的CSS样式"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", 
                        "Helvetica Neue", "Hiragino Sans GB", "Microsoft YaHei UI",
                        "Microsoft YaHei", Arial, sans-serif;
            background: linear-gradient(135deg, #ffeef8 0%, #ffe0f0 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            font-size: 16px;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .container {
            width: 100%;
            max-width: 650px;
        }
        
        .card {
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(255, 36, 66, 0.08),
                        0 2px 10px rgba(0, 0, 0, 0.06);
            overflow: hidden;
            position: relative;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 50px rgba(255, 36, 66, 0.12),
                        0 5px 15px rgba(0, 0, 0, 0.08);
        }
        
        .content {
            padding: 45px 40px;
            color: #2c3e50;
            line-height: 1.8;
            min-height: 450px;
        }
        
        /* 标题样式 */
        h1 {
            color: #FF2442;
            font-size: 30px;
            margin-bottom: 25px;
            font-weight: 700;
            letter-spacing: -0.5px;
            border-bottom: 3px solid #FFE4E4;
            padding-bottom: 15px;
        }
        
        h2 {
            color: #FF2442;
            font-size: 24px;
            margin-top: 35px;
            margin-bottom: 20px;
            font-weight: 600;
            position: relative;
            padding-left: 18px;
        }
        
        h2::before {
            content: "";
            position: absolute;
            left: 0;
            top: 50%;
            transform: translateY(-50%);
            width: 5px;
            height: 22px;
            background: linear-gradient(180deg, #FF2442, #FF6B6B);
            border-radius: 3px;
        }
        
        h3 {
            color: #34495e;
            font-size: 20px;
            margin-top: 28px;
            margin-bottom: 16px;
            font-weight: 600;
        }
        
        /* 段落样式 */
        p {
            margin-bottom: 20px;
            font-size: 16px;
            color: #4a5568;
            text-align: justify;
        }
        
        /* 强调样式 */
        strong {
            color: #FF2442;
            font-weight: 600;
            background: linear-gradient(180deg, transparent 70%, #FFE4E4 70%);
            padding: 0 3px;
        }
        
        em {
            font-style: italic;
            color: #718096;
        }
        
        /* 列表样式 */
        ul, ol {
            margin: 22px 0;
            padding-left: 35px;
        }
        
        li {
            margin-bottom: 14px;
            font-size: 16px;
            color: #4a5568;
            line-height: 1.8;
        }
        
        ul li::marker {
            color: #FF2442;
            font-size: 18px;
        }
        
        ol li::marker {
            color: #FF2442;
            font-weight: 600;
        }
        
        /* 引用样式 */
        blockquote {
            border-left: 4px solid #FF2442;
            margin: 26px 0;
            padding: 18px 26px;
            background: linear-gradient(90deg, #FFF8F8 0%, #FFFFFF 100%);
            border-radius: 10px;
            position: relative;
        }
        
        blockquote::before {
            content: '"';
            position: absolute;
            top: -8px;
            left: 22px;
            font-size: 45px;
            color: #FFE4E4;
            font-family: Georgia, serif;
        }
        
        blockquote p {
            color: #6b7280;
            font-style: italic;
            margin-bottom: 0;
        }
        
        /* 行内代码 */
        code {
            background: #FFF5F5;
            padding: 4px 10px;
            border-radius: 6px;
            font-family: "JetBrains Mono", "Cascadia Code", "Consolas", "Monaco", monospace;
            font-size: 14px;
            color: #e53e3e;
            font-weight: 500;
        }
        
        /* 代码块 */
        pre {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 24px;
            border-radius: 12px;
            overflow-x: auto;
            margin: 26px 0;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            position: relative;
        }
        
        pre::before {
            content: "CODE";
            position: absolute;
            top: 10px;
            right: 14px;
            font-size: 11px;
            color: #6b7280;
            font-weight: 600;
            letter-spacing: 1px;
            opacity: 0.5;
        }
        
        pre code {
            background: none;
            color: #d4d4d4;
            padding: 0;
            font-size: 14px;
            line-height: 1.7;
        }
        
        /* 表格样式 */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 26px 0;
            font-size: 15px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
            border-radius: 10px;
            overflow: hidden;
        }
        
        th {
            background: linear-gradient(135deg, #FF2442, #FF6B6B);
            color: white;
            padding: 14px 18px;
            text-align: left;
            font-weight: 600;
            font-size: 15px;
        }
        
        td {
            padding: 14px 18px;
            border-bottom: 1px solid #f0f0f0;
            color: #4a5568;
        }
        
        tr:nth-child(even) {
            background: #FAFAFA;
        }
        
        tr:hover {
            background: #FFF5F5;
        }
        
        tr:last-child td {
            border-bottom: none;
        }
        
        /* 分隔线 */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, #FFE4E4 20%, #FFE4E4 80%, transparent);
            margin: 35px 0;
        }
        
        /* 链接样式 */
        a {
            color: #FF2442;
            text-decoration: none;
            border-bottom: 1px solid #FFD0D7;
            transition: all 0.3s ease;
            padding-bottom: 1px;
        }
        
        a:hover {
            color: #FF6B6B;
            border-bottom-color: #FF6B6B;
            background: #FFF5F5;
            padding: 0 3px;
            margin: 0 -3px;
            border-radius: 3px;
        }
        
        /* 水印样式 */
        .watermark {
            position: absolute;
            bottom: 22px;
            right: 25px;
            font-size: 13px;
            color: #CBD5E0;
            opacity: 0.5;
            font-weight: 500;
        }
        
        /* 滚动条样式 */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f5f5f5;
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #FF6B6B, #FF2442);
            border-radius: 5px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #FF2442, #FF1030);
        }
        """
    
    def get_js(self) -> str:
        """获取JavaScript代码"""
        return """
        // 监听编辑器滚动事件（通过postMessage）
        window.addEventListener('message', function(e) {
            if (e.data.type === 'scroll') {
                const content = document.getElementById('content');
                const scrollPercentage = e.data.percentage;
                content.scrollTop = content.scrollHeight * scrollPercentage;
            }
        });
        """