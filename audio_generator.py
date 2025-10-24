import os
import base64
from pathlib import Path
from typing import Optional
import requests
from config import settings
from novel_parser import Scene


class AudioGenerator:
    def __init__(self):
        self.qiniu_api_key = settings.qiniu_api_key
        self.qiniu_base_url = settings.qiniu_base_url
        self.output_dir = Path(settings.output_dir) / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_scene_narration(self, scene: Scene, output_filename: str) -> Optional[str]:
        if not self.qiniu_api_key:
            print(f"⚠️ 未配置七牛云 API Key，跳过音频生成")
            return None
        
        narration_text = self._build_narration_text(scene)
        
        try:
            audio_data = self._call_qiniu_tts(narration_text)
            if not audio_data:
                return None
            
            output_path = self.output_dir / output_filename
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
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
    
    def generate_dialogue(self, speaker: str, text: str, output_filename: str, voice: str = "qiniu_zh_female_wwxkjx") -> Optional[str]:
        if not self.qiniu_api_key:
            print(f"⚠️ 未配置七牛云 API Key，跳过对话音频生成")
            return None
        
        try:
            audio_data = self._call_qiniu_tts(text, voice)
            if not audio_data:
                return None
            
            output_path = self.output_dir / output_filename
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            
            print(f"✓ 对话音频已保存到: {output_path}")
            return str(output_path)
        
        except Exception as e:
            print(f"生成对话音频时出错: {e}")
            return None
    
    def _call_qiniu_tts(self, text: str, voice_type: str = None) -> Optional[bytes]:
        if voice_type is None:
            voice_type = settings.tts_voice_type
        
        url = f"{self.qiniu_base_url}/voice/tts"
        headers = {
            "Authorization": f"Bearer {self.qiniu_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "text": text
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            if "data" in result:
                return base64.b64decode(result["data"])
            else:
                print(f"TTS API返回格式错误: {result}")
                return None
        
        except Exception as e:
            print(f"调用七牛云TTS API时出错: {e}")
            return None
