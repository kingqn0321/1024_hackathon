import os
from pathlib import Path
from typing import Optional
from openai import OpenAI
from config import settings
from novel_parser import Scene


class AudioGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.output_dir = Path(settings.output_dir) / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_scene_narration(self, scene: Scene, output_filename: str) -> Optional[str]:
        if not self.client:
            print(f"⚠️ 未配置OpenAI API Key，跳过音频生成")
            return None
        
        narration_text = self._build_narration_text(scene)
        
        try:
            response = self.client.audio.speech.create(
                model=settings.tts_model,
                voice="alloy",
                input=narration_text
            )
            
            output_path = self.output_dir / output_filename
            
            response.stream_to_file(output_path)
            
            print(f"✓ 音频已保存到: {output_path}")
            return str(output_path)
        
        except Exception as e:
            print(f"生成音频时出错: {e}")
            return None
    
    def _build_narration_text(self, scene: Scene) -> str:
        parts = []
        
        parts.append(f"场景{scene.scene_number}。{scene.setting}。")
        
        parts.append(scene.narration)
        
        for dialogue in scene.dialogue:
            speaker = dialogue.get("speaker", "")
            text = dialogue.get("text", "")
            parts.append(f"{speaker}说：{text}")
        
        return " ".join(parts)
    
    def generate_dialogue(self, speaker: str, text: str, output_filename: str, voice: str = "nova") -> Optional[str]:
        if not self.client:
            print(f"⚠️ 未配置OpenAI API Key，跳过对话音频生成")
            return None
        
        try:
            response = self.client.audio.speech.create(
                model=settings.tts_model,
                voice=voice,
                input=text
            )
            
            output_path = self.output_dir / output_filename
            response.stream_to_file(output_path)
            
            print(f"✓ 对话音频已保存到: {output_path}")
            return str(output_path)
        
        except Exception as e:
            print(f"生成对话音频时出错: {e}")
            return None
