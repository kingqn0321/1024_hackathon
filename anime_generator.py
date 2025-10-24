import json
from pathlib import Path
from typing import List, Dict
from dataclasses import asdict
from novel_parser import NovelParser, Scene, Character
from character_manager import CharacterManager
from image_generator import ImageGenerator
from audio_generator import AudioGenerator
from video_generator import VideoGenerator
from config import settings


class AnimeGenerator:
    def __init__(self):
        self.parser = NovelParser()
        self.character_manager = None
        self.image_generator = None
        self.audio_generator = AudioGenerator()
        self.video_generator = VideoGenerator()
        self.output_dir = Path(settings.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_from_novel(self, novel_text: str, generate_images: bool = True, generate_audio: bool = True, generate_video: bool = True) -> Dict:
        print("=" * 50)
        print("开始生成动漫...")
        print("=" * 50)
        
        print("\n步骤 1/6: 提取角色...")
        characters = self.parser.extract_characters(novel_text)
        print(f"✓ 提取到 {len(characters)} 个角色")
        for char in characters:
            print(f"  - {char.name}: {char.description}")
        
        print("\n步骤 2/6: 初始化角色管理器...")
        self.character_manager = CharacterManager(characters)
        self.image_generator = ImageGenerator(self.character_manager)
        print("✓ 角色管理器初始化完成")
        
        print("\n步骤 3/6: 分解场景...")
        scenes = self.parser.split_into_scenes(novel_text, characters)
        print(f"✓ 分解为 {len(scenes)} 个场景")
        
        print("\n步骤 4/6: 生成角色参考图...")
        character_refs = {}
        if generate_images:
            for char in characters:
                print(f"  正在生成 {char.name} 的参考图...")
                ref_path = self.image_generator.generate_character_reference(char.name)
                if ref_path:
                    character_refs[char.name] = ref_path
        else:
            print("  ⊘ 跳过图像生成")
        
        print("\n步骤 5/6: 生成场景内容...")
        scene_outputs = []
        
        for scene in scenes:
            print(f"\n  场景 {scene.scene_number}: {scene.setting}")
            
            scene_data = {
                "scene_number": scene.scene_number,
                "setting": scene.setting,
                "narration": scene.narration,
                "characters": scene.characters,
                "dialogue": scene.dialogue,
                "image_path": None,
                "audio_path": None
            }
            
            if generate_images:
                print(f"    - 生成场景图像...")
                image_filename = f"scene_{scene.scene_number:03d}.png"
                image_path = self.image_generator.generate_scene_image(scene, image_filename)
                scene_data["image_path"] = image_path
            
            if generate_audio:
                print(f"    - 生成场景音频...")
                audio_filename = f"scene_{scene.scene_number:03d}.mp3"
                audio_path = self.audio_generator.generate_scene_narration(scene, audio_filename)
                scene_data["audio_path"] = audio_path
            
            scene_outputs.append(scene_data)
        
        result = {
            "characters": [asdict(char) for char in characters],
            "character_references": character_refs,
            "scenes": scene_outputs,
            "total_scenes": len(scenes)
        }
        
        metadata_path = self.output_dir / "anime_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        if generate_video and (generate_images or scene_outputs):
            print("\n步骤 6/6: 生成视频...")
            video_filename = "anime_output.mp4"
            video_path = self.video_generator.generate_video_from_scenes(
                scene_outputs,
                output_filename=video_filename,
                fps=1,
                audio_enabled=generate_audio
            )
            if video_path:
                result["video_path"] = video_path
        
        print("\n" + "=" * 50)
        print("✓ 动漫生成完成！")
        print(f"✓ 元数据已保存到: {metadata_path}")
        if result.get("video_path"):
            print(f"✓ 视频已保存到: {result['video_path']}")
        print("=" * 50)
        
        return result
    
    def generate_preview_html(self, metadata_path: str = None):
        if metadata_path is None:
            metadata_path = self.output_dir / "anime_metadata.json"
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        html_content = self._build_html(metadata)
        
        html_path = self.output_dir / "preview.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ 预览页面已生成: {html_path}")
        return str(html_path)
    
    def _build_html(self, metadata: Dict) -> str:
        html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>动漫预览</title>
    <style>
        body {
            font-family: "Microsoft YaHei", Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 { color: #333; text-align: center; }
        .characters {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-bottom: 40px;
        }
        .character-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            flex: 1;
            min-width: 250px;
        }
        .character-card h3 { margin-top: 0; color: #2c3e50; }
        .character-card img {
            max-width: 100%;
            border-radius: 4px;
        }
        .scene {
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .scene h2 { color: #2c3e50; margin-top: 0; }
        .scene img {
            max-width: 100%;
            border-radius: 4px;
            margin: 15px 0;
        }
        .scene-setting {
            background: #ecf0f1;
            padding: 10px;
            border-left: 4px solid #3498db;
            margin: 10px 0;
        }
        .narration {
            line-height: 1.8;
            color: #555;
            margin: 15px 0;
        }
        .dialogue {
            margin: 10px 0;
            padding: 10px;
            background: #fff9e6;
            border-left: 3px solid #f39c12;
        }
        .dialogue strong { color: #e67e22; }
        audio {
            width: 100%;
            margin: 10px 0;
        }
        .video-container {
            background: white;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .video-container video {
            max-width: 100%;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>🎬 动漫预览</h1>
"""
        
        # 在开头添加视频显示
        if metadata.get("video_path"):
            relative_video_path = self._convert_to_relative_path(metadata["video_path"])
            html += f"""
    <div class="video-container">
        <h2>🎥 完整视频</h2>
        <video controls>
            <source src="{relative_video_path}" type="video/mp4">
            您的浏览器不支持视频播放。
        </video>
    </div>
"""
        
        html += """
    <h2>角色介绍</h2>
    <div class="characters">
"""
        
        for char in metadata.get("characters", []):
            char_name = char["name"]
            ref_path = metadata.get("character_references", {}).get(char_name, "")
            
            html += f"""
        <div class="character-card">
            <h3>{char_name}</h3>
            <p><strong>描述：</strong>{char["description"]}</p>
            <p><strong>外貌：</strong>{char["appearance"]}</p>
            <p><strong>性格：</strong>{char["personality"]}</p>
"""
            if ref_path:
                relative_path = self._convert_to_relative_path(ref_path)
                html += f'            <img src="{relative_path}" alt="{char_name}">\n'
            
            html += "        </div>\n"
        
        html += """    </div>
    
    <h2>场景</h2>
"""
        
        for scene in metadata.get("scenes", []):
            html += f"""
    <div class="scene">
        <h2>场景 {scene["scene_number"]}</h2>
        <div class="scene-setting">
            <strong>场景：</strong>{scene["setting"]}
        </div>
"""
            
            if scene.get("image_path"):
                relative_path = self._convert_to_relative_path(scene["image_path"])
                html += f'        <img src="{relative_path}" alt="场景 {scene["scene_number"]}">\n'
            
            html += f"""
        <div class="narration">
            {scene["narration"]}
        </div>
"""
            
            if scene.get("audio_path"):
                relative_audio_path = self._convert_to_relative_path(scene["audio_path"])
                html += f"""
        <audio controls>
            <source src="{relative_audio_path}" type="audio/mpeg">
            您的浏览器不支持音频播放。
        </audio>
"""
            
            if scene.get("dialogue"):
                html += "        <div class=\"dialogues\">\n"
                for d in scene["dialogue"]:
                    html += f"""            <div class="dialogue">
                <strong>{d.get("speaker", "")}：</strong>{d.get("text", "")}
            </div>
"""
                html += "        </div>\n"
            
            html += "    </div>\n"
        
        html += """
</body>
</html>
"""
        return html
    
    def _convert_to_relative_path(self, file_path: str) -> str:
        if not file_path:
            return ""
        
        path_obj = Path(file_path)
        
        try:
            relative_path = path_obj.relative_to(self.output_dir)
            return str(relative_path)
        except ValueError:
            return file_path
