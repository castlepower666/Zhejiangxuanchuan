# 浙江宣传写作客户端

基于Flask的Web界面AI写作工具，使用DeepSeek API，支持连续对话。

## 项目结构

```
zjxc-writer/
├── app.py              # Flask后端
├── templates/
│   └── index.html     # 前端页面
├── prompt/
│   └── system_prompt.md # 系统提示词
├── .env.example
└── requirements.txt
```

## 快速开始

### 1. 安装依赖

```bash
cd zjxc-writer
pip install -r requirements.txt
```

### 2. 配置API Key

```bash
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY=你的key
```

### 3. 启动

```bash
python app.py
```

浏览器打开 http://localhost:5000

## 功能

- **连续对话** - 支持多轮对话，AI记住上下文
- **生成文章** - 输入主题生成浙江宣传风格议论文
- **局部修改** - 说"第3段不好"，只修改指定段落
- **文章下载** - 每篇文章可单独下载Word
- **模板查询** - 输入"模板"查看所有主题分类
- **配置查询** - 输入"配置"查看当前API设置
- **清空功能** - 新建对话/清空历史/清空文章

## 界面说明

- 左侧：文章列表 + 下载按钮
- 右侧：对话区域（支持连续对话）
- 顶部：清空历史/清空文章按钮
- 底部：输入框

## 对话命令

- 输入"模板" - 查看主题分类
- 输入"配置" - 查看API配置
- 输入"清空"或"新对话" - 重置对话
- 输入"历史" - 查看所有文章
- 说"第X段不好" - 修改指定段落