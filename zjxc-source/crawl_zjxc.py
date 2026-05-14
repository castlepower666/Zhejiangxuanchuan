"""
浙江宣传文章爬虫 - 修复版
有leaf属性用leaf提取，没有leaf属性的用get_text
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import os
import sys
import re
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

def get_article_list(page=1):
    if page == 1:
        url = "https://zjnews.zjol.com.cn/zjxc/"
    else:
        url = f"https://zjnews.zjol.com.cn/zjxc/index_{page}.shtml"

    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = []
        for li in soup.select('ul.listUl li.listLi'):
            a_tag = li.select_one('a')
            span = li.select_one('span.listSpan')
            if a_tag:
                title = a_tag.get_text(strip=True)
                link = a_tag.get('href', '')
                if link.startswith('//zjnews.zjol.com.cn//'):
                    link = 'https:' + link
                elif link.startswith('//'):
                    link = 'https:' + link
                date = span.get_text(strip=True) if span else ''
                articles.append({'title': title, 'link': link, 'date': date})
        return articles
    except Exception as e:
        print(f"获取列表失败: {e}")
        return []

def get_article_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        html = response.text

        # 获取标题
        title_match = re.search(r'<h1 class="artTitle">([^<]+)</h1>', html)
        title = title_match.group(1) if title_match else ''

        # 获取发布时间
        pub_time = ''
        time_match = re.search(r'<div class="info"[^>]*>.*?<span>([^<]*?)</span>', html, re.DOTALL)
        if time_match:
            pub_time = time_match.group(1).strip()
            pub_time = re.sub(r'\s*来源：.*', '', pub_time)
            pub_time = re.sub(r'\s*责任编辑：.*', '', pub_time)

        # 提取artCon内容
        artCon_match = re.search(r'<div class="artCon">(.*?)<div class="cprtip">', html, re.DOTALL)
        if not artCon_match:
            return {'title': title, 'pub_time': pub_time, 'content': ''}

        artCon_html = artCon_match.group(1)

        # 移除script, style, section
        artCon_html = re.sub(r'<script[^>]*>.*?</script>', '', artCon_html, flags=re.DOTALL)
        artCon_html = re.sub(r'<style[^>]*>.*?</style>', '', artCon_html, flags=re.DOTALL)
        artCon_html = re.sub(r'<section[^>]*>.*?</section>', '', artCon_html, flags=re.DOTALL)

        soup_content = BeautifulSoup(artCon_html, 'html.parser')

        # 获取所有段落内容（按p标签分组，用get_text保留所有文字包括数字）
        paragraphs = soup_content.find_all('p')
        result_paragraphs = []
        for p in paragraphs:
            # 获取段落中所有leaf span的文本，拼接在一起
            leafs = p.find_all('span', attrs={'leaf': ''})
            if leafs:
                texts = [leaf.get_text() for leaf in leafs if leaf.get_text()]
                para_text = ''.join(texts)
            else:
                # 没有leaf就直接获取文本
                para_text = p.get_text()

            # 清理空白字符但保留段落结构
            para_text = re.sub(r'\s+', ' ', para_text).strip()
            # 过滤版权信息和过短文本
            if para_text and len(para_text) > 5 and '版权所有' not in para_text and '未经许可' not in para_text:
                result_paragraphs.append(para_text)

        if result_paragraphs:
            return {
                'title': title,
                'pub_time': pub_time,
                'content': '\n\n'.join(result_paragraphs)
            }

        # 兜底：直接用get_text
        content = soup_content.get_text(separator='\n', strip=True)
        lines = [line.strip() for line in content.split('\n') if line.strip() and len(line.strip()) > 10]
        content = '\n\n'.join(lines)

        return {
            'title': title,
            'pub_time': pub_time,
            'content': content
        }

    except Exception as e:
        return {'title': '', 'pub_time': '', 'content': ''}

def main():
    output_dir = './浙江宣传文章'
    os.makedirs(output_dir, exist_ok=True)

    all_articles = []
    page = 1

    print("开始爬取所有文章...")
    while True:
        print(f"获取第 {page} 页列表...")
        articles = get_article_list(page)

        if not articles:
            break

        print(f"  第 {page} 页找到 {len(articles)} 篇")
        all_articles.extend(articles)

        if len(articles) < 25:
            break

        page += 1
        time.sleep(0.5)

    print(f"\n共找到 {len(all_articles)} 篇文章")
    print("开始获取文章正文...")

    total = len(all_articles)
    for i, article in enumerate(all_articles):
        if i % 50 == 0:
            print(f"\n[{i+1}/{total}]")

        safe_title = ''.join(c for c in article['title'][:30] if ord(c) > 31 or c == '\n').strip()
        print(f"  {safe_title}...")

        content_data = get_article_content(article['link'])
        all_articles[i]['title'] = content_data.get('title', article['title'])
        all_articles[i]['pub_time'] = content_data.get('pub_time', '')
        all_articles[i]['content'] = content_data.get('content', '')

        time.sleep(0.3)

        if (i + 1) % 100 == 0:
            with open(os.path.join(output_dir, 'articles.json'), 'w', encoding='utf-8') as f:
                json.dump(all_articles[:i+1], f, ensure_ascii=False, indent=2)
            print(f"  已保存 {i+1} 篇")

    # 最终保存
    with open(os.path.join(output_dir, 'articles.json'), 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    # 生成markdown
    md_file = os.path.join(output_dir, 'articles.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# 浙江宣传文章汇总\n\n")
        f.write(f"抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"文章数量: {total}\n\n")

        for i, article in enumerate(all_articles, 1):
            f.write(f"## {i}. {article['title']}\n\n")
            date_str = article.get('date', '')
            pub_time_str = article.get('pub_time', '')
            f.write(f"日期: {date_str} {pub_time_str}\n\n")
            if article.get('content'):
                f.write(article['content'])
                f.write("\n\n")
            f.write(f"链接: {article['link']}\n\n")
            f.write("---\n\n")

    # 统计
    has_content = sum(1 for a in all_articles if a.get('content', ''))
    print(f"\n完成!")
    print(f"  - 总文章数: {total}")
    print(f"  - 有内容的文章: {has_content}")
    print(f"  - 无内容的文章: {total - has_content}")

if __name__ == '__main__':
    main()