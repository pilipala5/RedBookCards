import unittest

from bs4 import BeautifulSoup

from src.core.markdown_processor import MarkdownProcessor
from src.utils.paginator import SmartPaginator


class MarkdownRegressionTests(unittest.TestCase):
    def setUp(self):
        self.processor = MarkdownProcessor()

    def test_nested_fenced_code_in_lists(self):
        source = """### test

- aaaa

    ```
    test
    ```

- bbbb

    ```
    test
    ```

    ```
    ❯ git merge master
    Auto-merging hello.txt
    CONFLICT (content): Merge conflict in hello.txt
    ```

    ```
    ❯ cat hello.txt
    <<<<<<< HEAD
    Banana
    =======
    Apple
    >>>>>>> master
    ```
"""
        html = self.processor.parse(source)
        soup = BeautifulSoup(html, "html.parser")
        self.assertEqual(len(soup.find_all("pre")), 4)
        self.assertEqual(len(soup.find_all("li", recursive=True)), 2)

    def test_inline_and_block_formula_render_to_mathml(self):
        source = r"""Inline: $E=mc^2$.

$$
\frac{a}{b} = c
$$
"""
        html = self.processor.parse(source)
        soup = BeautifulSoup(html, "html.parser")
        maths = soup.find_all("math")
        self.assertGreaterEqual(len(maths), 2, html)
        self.assertTrue(any(m.get("display") == "block" for m in maths))
        self.assertTrue(any(m.get("display") == "inline" for m in maths))

    def test_task_marker_inside_code_is_not_rewritten(self):
        html = self.processor.parse("""```
- [ ] literal code
```
""")
        self.assertIn("- [ ] literal code", BeautifulSoup(html, "html.parser").get_text())


class PaginationRegressionTests(unittest.TestCase):
    def test_page_dimensions_match_renderer(self):
        expected = {
            "small": (720, 960),
            "medium": (1080, 1440),
            "large": (1440, 1920),
        }
        for size, dimensions in expected.items():
            paginator = SmartPaginator(size)
            self.assertEqual((paginator.page_width, paginator.page_height), dimensions)

    def test_pages_respect_estimated_content_height(self):
        html = "".join(
            f"<p>第{i}段：这是用于分页回归测试的一段中文文本，确保页面底部不会吞掉内容。</p>"
            for i in range(60)
        )
        paginator = SmartPaginator("medium")
        pages = paginator.paginate(html)
        self.assertGreater(len(pages), 1)
        for page in pages:
            height = sum(e.height for e in paginator.parse_html_to_elements(page))
            self.assertLessEqual(height, paginator.content_height)


if __name__ == "__main__":
    unittest.main()
