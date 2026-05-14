# 浙江宣传文风写作工具

基于浙江宣传文风的AI写作客户端。

## 项目结构

```
├── zjxc-source/      # 原始素材（爬虫、数据、技能）
└── zjxc-writer/      # Chainlit写作客户端
```

## 开始使用

### 1. 进入客户端目录
```bash
cd zjxc-writer
```

### 2. 安装依赖
```bash
pip install chainlit anthropic
```

### 3. 配置API Key
```bash
export ANTHROPIC_API_KEY=your_api_key
```

### 4. 启动
```bash
chainlit run app.py
```

然后访问 http://localhost:8000