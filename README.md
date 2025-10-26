# 动漫生成器 - 从小说到动漫

这是一个自动根据小说文本生成动漫的Web应用。它可以：
- 🌐 **Web界面**：用户友好的网页界面，可在本地或服务器部署
- 🤖 **七牛云AI**：使用七牛云大模型API进行图像生成和文本分析
- 🎭 **角色一致性**：自动提取小说中的角色并保持视觉一致性
- 🎨 **动漫风格**：生成高质量动漫风格场景图片
- 🔊 **语音合成**：生成场景旁白和对话的语音
- 📱 **实时预览**：自动生成HTML预览页面展示完整动漫

## 功能特点

### 🌐 Web应用界面
- 现代化的响应式Web界面
- 支持本地部署或服务器部署
- 实时进度显示
- 异步任务处理

### 🎭 角色一致性
- 自动提取小说中的所有主要角色
- 为每个角色创建详细的视觉描述档案
- 使用一致的角色特征生成所有场景图片
- 生成角色参考图，确保整个动漫中角色外观统一

### 📖 场景分解
- 智能分析小说，自动分解为多个场景
- 提取每个场景的时间、地点、角色和对话
- 生成适合AI图像生成的详细场景描述

### 🎨 图像生成
- 使用七牛云Gemini 2.5 Flash Image模型生成高质量动漫风格图片
- 每个场景都包含相应的角色和背景
- 支持生成角色参考图和场景图
- Base64格式直接接收，无需下载

### 🔊 音频生成
- 使用七牛云TTS生成场景旁白
- 支持为对话生成语音
- 自动合成完整的场景音频

### 📱 预览界面
- 自动生成HTML预览页面
- 展示所有角色介绍和参考图
- 按顺序展示每个场景的图片、文字和音频
- 响应式设计，支持各种设备

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/kingqn0321/1024_hackathon.git
cd 1024_hackathon
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置API密钥：
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

需要配置的API密钥：
- `QINIU_API_KEY`: 七牛云大模型API密钥（必需，用于图像生成、文本分析和TTS语音合成）

⚠️ **重要提示**：请勿在代码中硬编码API密钥，务必使用 `.env` 文件进行配置

## 使用方法

### Web应用模式（推荐）

1. 启动Web服务器：
```bash
python app.py
```

2. 打开浏览器访问：
```
http://localhost:8088
```
或如果部署在服务器上：
```
http://服务器IP:8088
```

3. 在网页文本框中输入小说内容

4. 点击"生成动漫"按钮

5. 等待生成完成后，点击"查看生成的动漫"即可预览

### 命令行模式

```bash
python main.py example_novel.txt
```

这将：
1. 分析小说文本
2. 提取角色和场景
3. 生成所有图片和音频
4. 创建预览HTML页面

### 命令行选项

```bash
python main.py <小说文件> [选项]
```

选项：
- `--no-images`: 跳过图像生成（仅分析文本）
- `--no-audio`: 跳过音频生成

示例：
```bash
python main.py novel.txt --no-audio
```

### 输出结构

生成的内容保存在 `output/` 目录：

```
output/
├── anime_metadata.json    # 元数据（角色、场景信息）
├── preview.html           # 预览页面
├── images/                # 生成的图片
│   ├── character_ref_*.png    # 角色参考图
│   └── scene_*.png            # 场景图片
└── audio/                 # 生成的音频
    └── scene_*.mp3            # 场景音频
```

### 查看结果

在浏览器中打开 `output/preview.html` 即可查看生成的动漫。

## 项目结构

```
.
├── app.py                  # Flask Web应用（主入口）
├── main.py                 # 命令行程序入口
├── anime_generator.py      # 动漫生成器核心类
├── novel_parser.py         # 小说解析器
├── character_manager.py    # 角色管理器（保持一致性）
├── image_generator.py      # 图像生成器（七牛云API）
├── audio_generator.py      # 音频生成器
├── config.py              # 配置管理
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量模板
├── templates/            # Flask模板目录
│   └── index.html       # Web界面
└── example_novel.txt     # 示例小说
```

## 示例

项目包含一个示例小说 `example_novel.txt`，可以直接使用：

```bash
python main.py example_novel.txt
```

或在Web界面中点击"点击加载示例小说"快速体验。

这个示例讲述了一个关于高中生小雪和明宇因救助小猫而成为朋友的温馨故事。

### 动漫成果物示例

我们提供了完整的动漫生成成果物示例，您可以查看：

📹 [动漫视频示例](output/videos/anime_output.mp4) - 完整的动漫视频输出示例

该示例展示了从小说文本到最终动漫视频的完整生成效果，包括：
- 角色设定和一致性呈现
- 场景图像生成
- 语音合成和配音
- 视频自动合成

## 技术栈

- **Web框架**: Flask（提供Web服务和API）
- **AI服务**: 七牛云大模型平台
  - 图像生成：Gemini 2.5 Flash Image
  - 文本分析：Qwen3-Max模型（通过七牛云API）
  - 语音合成：七牛云TTS API
- **Python库**: flask, pillow, pydantic, requests

## 配置说明

在 `.env` 文件中可以配置以下参数：

```env
# 七牛云API配置（必需）
QINIU_API_KEY=your_qiniu_api_key_here    # 请填入您的七牛云API密钥
QINIU_BASE_URL=https://openai.qiniu.com/v1
QINIU_BACKUP_URL=https://api.qnaigc.com/v1

# 模型配置
IMAGE_MODEL=gemini-2.5-flash-image       # 七牛云图像生成模型
TTS_VOICE_TYPE=qiniu_zh_female_wwxkjx    # 七牛云TTS语音类型
TEXT_MODEL=qwen3-max                      # 文本分析模型

# Web服务配置
WEB_HOST=0.0.0.0                         # Web服务监听地址
WEB_PORT=8088                            # Web服务端口

# 输出目录
OUTPUT_DIR=output                        # 生成内容保存目录
```

## 工作原理

### 1. 角色提取
使用Qwen3-Max模型（通过七牛云API）分析小说文本，提取所有主要角色的信息：
- 角色名字
- 背景描述
- 外貌特征（详细描述，用于保持一致性）
- 性格特点

### 2. 角色一致性管理
为每个角色创建视觉档案：
- 生成标准化的角色描述
- 创建角色参考图
- 在所有场景中使用相同的角色特征

### 3. 场景分解
将小说分解为多个场景，每个场景包含：
- 场景编号
- 出现的角色
- 时间和地点
- 场景描述和旁白
- 对话内容
- 图像生成提示词

### 4. 内容生成
对每个场景：
- 使用七牛云Gemini 2.5 Flash Image生成场景图片（包含一致的角色形象）
- 使用七牛云TTS生成场景旁白和对话音频
- 记录所有元数据

### 5. 预览生成
自动生成包含所有内容的HTML页面：
- 角色介绍区域
- 场景展示区域（图片 + 文字 + 音频）
- 响应式布局

## 部署说明

### 本地部署

```bash
python app.py
```

访问 `http://localhost:8088`

### 服务器部署

1. 修改 `.env` 文件中的 `WEB_HOST` 和 `WEB_PORT`：
```env
WEB_HOST=0.0.0.0
WEB_PORT=8088
```

2. 启动服务：
```bash
python app.py
```

3. 通过服务器IP访问：
```
http://服务器IP:8088
```

### 生产环境部署（推荐使用Gunicorn）

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8088 app:app
```

### 安全建议

1. **API密钥安全**：
   - 切勿在代码中硬编码API密钥
   - 使用 `.env` 文件存储敏感信息
   - 确保 `.env` 文件在 `.gitignore` 中
   - 不要将真实的API密钥提交到版本控制系统

2. **生产环境**：
   - 使用环境变量或密钥管理服务
   - 定期轮换API密钥
   - 限制API密钥的访问权限

## API文档

### POST /api/generate
生成动漫

**请求体**：
```json
{
  "novel_text": "小说文本内容..."
}
```

**响应**：
```json
{
  "task_id": "1234567890",
  "message": "动漫生成任务已启动"
}
```

### GET /api/status/<task_id>
查询生成状态

**响应**：
```json
{
  "status": "processing",
  "progress": 50,
  "message": "正在生成场景图像...",
  "result": null
}
```

完成时：
```json
{
  "status": "completed",
  "progress": 100,
  "message": "生成完成！",
  "result": {
    "preview_url": "/output/preview.html",
    "characters_count": 3,
    "scenes_count": 5
  }
}
```

## 注意事项

1. **API配置**: 必须配置七牛云API密钥才能使用图像生成功能
2. **API费用**: 图像生成会消耗七牛云API额度，请注意使用量
3. **处理时间**: 生成过程可能需要几分钟，取决于场景数量
4. **文本长度**: 建议小说长度在1000-5000字之间，太长可能需要较长处理时间
5. **中文支持**: 完全支持中文小说和中文界面
6. **并发处理**: Web应用支持多个任务同时处理

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 团队分工

本项目由以下成员共同完成：

- **kingqn0321** - 项目负责人，核心功能开发
  - 动漫生成器核心架构设计
  - Web应用开发
  - 七牛云API集成
  - 项目管理和版本发布

- **XiaoJihuaQiniu** - 功能开发
  - 视频合成功能实现
  - 语音生成优化
  - 功能测试和优化

感谢所有贡献者对本项目的支持！

## 更新日志

### v2.0.0
- ✨ 添加Web应用界面
- 🤖 集成七牛云大模型API
- 📊 实时进度显示
- 🚀 支持服务器部署
- 💫 异步任务处理

### v1.0.3 (当前版本)
- 📝 更新README文档，增加团队分工说明
- 📹 添加动漫成果物示例链接
- 🔧 语音生成优化，移除场景前缀
- 🎬 视频合成功能完善

### v1.0.0
- 🎉 初始版本发布
- 📝 命令行模式实现
- 🎨 基于OpenAI API的图像生成
