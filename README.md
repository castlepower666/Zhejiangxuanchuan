# 浙江宣传文风技能

本项目用于爬取浙江宣传文章、分析文风、制作文风技能并练习写作。

## 目录结构

```
├── crawl_zjxc.py              # 爬虫脚本
├── md_to_epub.py              # Markdown转ePub脚本
├── zjxc-style/                # zjxc-style技能原始文件
│   ├── SKILL.md
│   └── reference/articles.md
└── .claude/
    ├── settings.local.json
    └── skills/zjxc-style/    # 已激活的zjxc-style技能
```

## 使用方法

### 爬取文章
```bash
python crawl_zjxc.py
```

### 转换为ePub
```bash
python md_to_epub.py
```

### 使用文风技能
在Claude Code中输入 `/zjxc-style`，描述文章主题即可生成浙江宣传风格的议论文。

## 数据统计

- 爬取文章：970篇
- 有正文：947篇
- 无内容：23篇（微信外链/旧版页面）
- 最早：2023年
- 最新：2026年5月