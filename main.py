#!/usr/bin/env python3

import sys
from pathlib import Path
from anime_generator import AnimeGenerator


def main():
    if len(sys.argv) < 2:
        print("使用方法: python main.py <小说文本文件路径> [--no-images] [--no-audio] [--no-video]")
        print("\n示例:")
        print("  python main.py novel.txt")
        print("  python main.py novel.txt --no-images")
        print("  python main.py novel.txt --no-audio")
        print("  python main.py novel.txt --no-video")
        sys.exit(1)
    
    novel_file = sys.argv[1]
    generate_images = "--no-images" not in sys.argv
    generate_audio = "--no-audio" not in sys.argv
    generate_video = "--no-video" not in sys.argv
    
    if not Path(novel_file).exists():
        print(f"错误：文件 '{novel_file}' 不存在")
        sys.exit(1)
    
    with open(novel_file, 'r', encoding='utf-8') as f:
        novel_text = f.read()
    
    if not novel_text.strip():
        print("错误：小说文件为空")
        sys.exit(1)
    
    generator = AnimeGenerator()
    
    result = generator.generate_from_novel(
        novel_text,
        generate_images=generate_images,
        generate_audio=generate_audio,
        generate_video=generate_video
    )
    
    generator.generate_preview_html()
    
    print("\n📊 生成统计:")
    print(f"  - 角色数量: {len(result['characters'])}")
    print(f"  - 场景数量: {result['total_scenes']}")
    if generate_images:
        print(f"  - 角色参考图: {len(result['character_references'])}")
    if generate_video and result.get('video_path'):
        print(f"  - 视频: {result['video_path']}")
    print(f"\n💡 提示: 打开 output/preview.html 查看生成的动漫")


if __name__ == "__main__":
    main()
