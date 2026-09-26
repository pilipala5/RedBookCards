# ============================================
# src/core/markdown_processor.py
# ============================================
import os
import re

import markdown
from bs4 import BeautifulSoup
from latex2mathml.converter import convert as latex_to_mathml


class TaskListExtension(markdown.Extension):
    """自定义任务列表扩展"""

    def extendMarkdown(self, md):
        md.preprocessors.register(TaskListPreprocessor(md), "tasklist", 100)
        md.postprocessors.register(TaskListPostprocessor(md), "tasklist", 25)


class TaskListPreprocessor(markdown.preprocessors.Preprocessor):
    """预处理任务列表语法，且不修改代码块中的字面量。"""

    FENCE_RE = re.compile(r"^\s*(\`{3,}|~{3,})(.*)$")

    def run(self, lines):
        new_lines = []
        in_list = False
        fence_char = None
        fence_len = 0

        for line in lines:
            fence_match = self.FENCE_RE.match(line)
            if fence_match:
                token = fence_match.group(1)
                suffix = fence_match.group(2).strip()

                if fence_char is None:
                    fence_char = token[0]
                    fence_len = len(token)
                elif token[0] == fence_char and len(token) >= fence_len and not suffix:
                    fence_char = None
                    fence_len = 0

                new_lines.append(line)
                continue

            if fence_char is not None:
                new_lines.append(line)
                continue

            stripped = line.strip()

            if (
                stripped.startswith("- [ ] ")
                or stripped.startswith("- [x] ")
                or stripped.startswith("* [ ] ")
                or stripped.startswith("* [x] ")
            ):
                if stripped.startswith("- [x] ") or stripped.startswith("* [x] "):
                    new_line = line.replace("[x] ", "<!--tasklist-checked--> ", 1)
                else:
                    new_line = line.replace("[ ] ", "<!--tasklist-unchecked--> ", 1)

                new_lines.append(new_line)
                in_list = True
            else:
                if in_list and stripped and not stripped.startswith(("-", "*")):
                    new_lines.append("")
                    in_list = False
                new_lines.append(line)

        return new_lines


class TaskListPostprocessor(markdown.postprocessors.Postprocessor):
    """后处理：将占位注释替换为真正的复选框。"""

    def run(self, text):
        text = re.sub(
            r'<li><!--tasklist-checked-->\s*(.*?)</li>',
            r'<li class="task-list-item"><input type="checkbox" class="task-list-checkbox" checked disabled> \1</li>',
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r'<li><!--tasklist-unchecked-->\s*(.*?)</li>',
            r'<li class="task-list-item"><input type="checkbox" class="task-list-checkbox" disabled> \1</li>',
            text,
            flags=re.DOTALL,
        )
        return text


class MarkdownProcessor:
    def __init__(self):
        self.extensions = [
            TaskListExtension(),
            "meta",
            "toc",
            "abbr",
            "attr_list",
            "def_list",
            "admonition",
            "pymdownx.highlight",
            "pymdownx.superfences",
            "pymdownx.arithmatex",
            "footnotes",
            "md_in_html",
            "sane_lists",
            "smarty",
            "tables",
            "wikilinks",
        ]

        self.extension_configs = {
            "pymdownx.highlight": {
                "css_class": "highlight",
                "guess_lang": False,
                "pygments_style": "default",
            },
            "pymdownx.arithmatex": {
                "generic": True,
                "smart_dollar": True,
            },
            "toc": {"permalink": True},
        }

    def parse(self, text: str) -> str:
        """解析 Markdown 文本为 HTML。"""
        try:
            text = self._process_pagebreaks_before_markdown(text)

            md = markdown.Markdown(
                extensions=self.extensions,
                extension_configs=self.extension_configs,
            )
            html = md.convert(text)

            html = self._render_mathml(html)
            html = self._fix_local_image_paths(html)
            html = self._add_tasklist_styles(html)
            return html

        except Exception as exc:
            print(f"Markdown 解析错误: {exc}")
            return f"<p style='color: red;'>解析错误: {str(exc)}</p>"

    def _render_mathml(self, html: str) -> str:
        """将 Arithmatex generic 输出转换为原生 MathML。"""
        soup = BeautifulSoup(html, "html.parser")

        for node in soup.select(".arithmatex"):
            raw = node.get_text("", strip=False).strip()
            display = "block" if node.name == "div" else "inline"
            latex = raw

            if raw.startswith(r"\(") and raw.endswith(r"\)"):
                latex = raw[2:-2]
                display = "inline"
            elif raw.startswith(r"\[") and raw.endswith(r"\]"):
                latex = raw[2:-2]
                display = "block"

            try:
                mathml = latex_to_mathml(latex.strip(), display=display)
                fragment = BeautifulSoup(mathml, "html.parser")
                math_tag = fragment.find("math")
                if math_tag is None:
                    continue

                classes = list(math_tag.get("class", []))
                if "mathml-formula" not in classes:
                    classes.append("mathml-formula")
                math_tag["class"] = classes
                node.replace_with(math_tag)
            except Exception as exc:
                classes = list(node.get("class", []))
                if "math-error" not in classes:
                    classes.append("math-error")
                node["class"] = classes
                node["title"] = f"公式渲染失败: {exc}"

        return str(soup)

    def _fix_local_image_paths(self, html: str) -> str:
        """修复本地图片路径，兼容 Windows/macOS/Linux。"""
        soup = BeautifulSoup(html, "html.parser")

        for img in soup.find_all("img"):
            src = img.get("src", "")
            if not src:
                continue

            if src.startswith(("http://", "https://", "data:", "file:")):
                img["data-protected"] = "true"
                if not img.get("style"):
                    img["style"] = "max-width: 100%; height: auto;"
                continue

            if re.match(r"^[A-Za-z]:[\\/]", src):
                src = src.replace("\\", "/")
                if not src.startswith("file:"):
                    src = "file:///" + src
            else:
                try:
                    src = "file:///" + os.path.abspath(src).replace("\\", "/")
                except Exception:
                    pass

            img["src"] = src
            if not img.get("style"):
                img["style"] = "max-width: 100%; height: auto;"
            img["data-protected"] = "true"

        return str(soup)

    def _process_pagebreaks_before_markdown(self, text: str) -> str:
        """在 Markdown 解析前将手动分页注释替换成稳定的 HTML 标记。"""
        pattern = r"<!--\s*pagebreak\s*-->"
        replacement = '\n\n<div class="pagebreak-marker" data-pagebreak="true"></div>\n\n'
        return re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    def _add_tasklist_styles(self, html: str) -> str:
        """为任务列表添加样式。"""
        if '<input type="checkbox" class="task-list-checkbox"' not in html:
            return html

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
        return style + html
