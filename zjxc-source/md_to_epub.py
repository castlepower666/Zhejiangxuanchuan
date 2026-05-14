"""
将浙江宣传文章的Markdown文件转换为ePub格式电子书
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from ebooklib import epub
import re

def md_to_html(md_text):
    """简单的Markdown转HTML"""
    html = md_text
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    paragraphs = []
    for para in html.split('\n'):
        para = para.strip()
        if para and not para.startswith('<h'):
            paragraphs.append(f'<p>{para}</p>')
        elif para:
            paragraphs.append(para)
    return '\n'.join(paragraphs)

def create_epub():
    with open('浙江宣传文章/articles.md', 'r', encoding='utf-8') as f:
        md_content = f.read()

    book = epub.EpubBook()
    book.set_identifier('zjxc-articles')
    book.set_title('浙江宣传文章汇总')
    book.set_language('zh-CN')

    # 用 ## N. 标题 来匹配文章
    # 每篇文章结构: ## N. 标题\n\n日期: ...\n\n正文...\n\n链接: ...\n---(下篇文章开始)
    article_pattern = r'## (\d+)\.\s+(.+?)\n\n日期:'
    matches = list(re.finditer(article_pattern, md_content, re.DOTALL))

    chapters = []
    for i, match in enumerate(matches):
        num = match.group(1)
        title = match.group(2).strip()

        # 获取这篇文章的完整内容
        start = match.start()
        end = matches[i+1].start() if i+1 < len(matches) else len(md_content)
        article_text = md_content[start:end]

        # 提取日期
        date_match = re.search(r'日期:\s*(.+)', article_text)
        date_str = date_match.group(1).strip() if date_match else ''

        # 提取链接
        link_match = re.search(r'链接:\s*(.+)', article_text)
        link = link_match.group(1).strip() if link_match else ''

        # 提取正文（去掉标题和元信息）
        content = re.sub(r'^##?\s*\d+\.\s*.+\n\n日期:.+\n\n', '', article_text, count=1)
        content = re.sub(r'日期:.+\n', '', content)
        content = re.sub(r'链接:.+', '', content)
        content = re.sub(r'\n---\n.*', '', content)
        content = content.strip()

        if not content:
            continue

        html_content = md_to_html(content)

        chapter = epub.EpubHtml(title=title, file_name=f'chapter_{num}.xhtml', lang='zh-CN')
        chapter.content = f'''<html xmlns="http://www.w3.org/1999/xhtml" lang="zh-CN">
<head><title>{title}</title></head>
<body>
<h2>{title}</h2>
<p style="color:gray;font-size:0.9em">{date_str}</p>
{html_content}
<p style="color:gray;font-size:0.8em">原文链接: <a href="{link}">{link}</a></p>
</body>
</html>'''
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = tuple(chapters)
    book.spine = ['nav'] + chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    output_path = '浙江宣传文章/articles.epub'
    epub.write_epub(output_path, book)
    print(f'已生成: {output_path}')
    print(f'共 {len(chapters)} 篇文章')

if __name__ == '__main__':
    create_epub()