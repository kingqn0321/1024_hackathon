# 动漫生成器 - 从小说到动漫

这是一个自动根据小说文本生成动漫的工具。它可以：
- 自动提取小说中的角色和场景
- 为每个角色生成一致的视觉形象
- 生成场景图片（图配文的形式）
- 生成场景旁白和对话的语音
- 输出HTML预览页面，展示完整的动漫内容

## 功能特点

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
- 使用DALL-E 3生成高质量动漫风格图片
- 每个场景都包含相应的角色和背景
- 支持生成角色参考图和场景图

### 🔊 音频生成
- 使用OpenAI TTS生成场景旁白
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
- `OPENAI_API_KEY`: 用于图像生成和文字转语音（必需）
- `ANTHROPIC_API_KEY`: 用于高级文本分析（可选）

## 使用方法

### 基本使用

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
├── main.py                 # 主程序入口
├── anime_generator.py      # 动漫生成器核心类
├── novel_parser.py         # 小说解析器
├── character_manager.py    # 角色管理器（保持一致性）
├── image_generator.py      # 图像生成器
├── audio_generator.py      # 音频生成器
├── config.py              # 配置管理
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量模板
└── example_novel.txt     # 示例小说
```

## 示例

项目包含一个示例小说 `example_novel.txt`，可以直接使用：

```bash
python main.py example_novel.txt
```

这个示例讲述了一个关于高中生小雪和明宇因救助小猫而成为朋友的温馨故事。

## 技术栈

- **文本分析**: OpenAI GPT-4
- **图像生成**: DALL-E 3
- **语音合成**: OpenAI TTS
- **Python库**: openai, anthropic, pillow, pydantic

## 配置说明

在 `.env` 文件中可以配置以下参数：

```env
OPENAI_API_KEY=sk-...           # OpenAI API密钥
ANTHROPIC_API_KEY=sk-ant-...    # Anthropic API密钥（可选）
IMAGE_MODEL=dall-e-3            # 图像生成模型
TTS_MODEL=tts-1                 # 语音合成模型
TEXT_MODEL=gpt-4                # 文本分析模型
OUTPUT_DIR=output               # 输出目录
```

## 工作原理

### 1. 角色提取
使用GPT-4分析小说文本，提取所有主要角色的信息：
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
- 使用DALL-E 3生成场景图片（包含一致的角色形象）
- 使用OpenAI TTS生成场景旁白和对话音频
- 记录所有元数据

### 5. 预览生成
自动生成包含所有内容的HTML页面：
- 角色介绍区域
- 场景展示区域（图片 + 文字 + 音频）
- 响应式布局

## 注意事项

1. **API费用**: 图像和音频生成会消耗OpenAI API额度，请注意使用量
2. **处理时间**: 生成过程可能需要几分钟，取决于场景数量
3. **文本长度**: 建议小说长度在1000-5000字之间，太长可能需要较长处理时间
4. **中文支持**: 完全支持中文小说和中文界面

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
