import os
import base64
import time
from pathlib import Path
from typing import Optional
import requests
from config import settings
from novel_parser import Scene


class AudioGenerator:
    def __init__(self):
        self.qiniu_api_key = settings.qiniu_api_key
        self.qiniu_base_url = settings.qiniu_base_url
        self.qiniu_backup_url = settings.qiniu_backup_url
        self.output_dir = Path(settings.output_dir) / "audio"
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_scene_narration(self, scene: Scene, output_filename: str) -> Optional[str]:
        if not self.qiniu_api_key:
            print(f"⚠️ 未配置七牛云 API Key，跳过音频生成")
            return None
        
        narration_text = self._build_narration_text(scene)
        if not narration_text or narration_text.strip() == "":
            return None
        
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
        
        parts.append(f"{scene.setting}。")
        
        for dialogue in scene.dialogue:
            text = dialogue.get("text", "")
            parts.append(text)
        
        return " ".join(parts)
    
    def generate_dialogue(self, speaker: str, text: str, output_filename: str, voice: str = "qiniu_zh_female_wwxkjx") -> Optional[str]:
        if not self.qiniu_api_key:
            print(f"⚠️ 未配置七牛云 API Key，跳过对话音频生成")
            return None
        
        if not text or text.strip() == "":
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
        
        headers = {
            "Authorization": f"Bearer {self.qiniu_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "audio": {
                "voice_type": voice_type,
                "encoding": "mp3",
                "speed_ratio": 1.0
            },
            "request": {
                "text": text
            }
        }
        
        urls_to_try = [
            (self.qiniu_base_url, "主URL"),
            (self.qiniu_backup_url, "备用URL")
        ]
        
        for base_url, url_label in urls_to_try:
            url = f"{base_url}/voice/tts"
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    response = requests.post(url, json=payload, headers=headers, timeout=30)
                    response.raise_for_status()
                    result = response.json()
                    
                    if "data" in result:
                        if attempt > 0 or url_label == "备用URL":
                            print(f"✓ TTS API调用成功 ({url_label}, 尝试 {attempt + 1}/{max_retries})")
                        return base64.b64decode(result["data"])
                    else:
                        print(f"⚠️ TTS API返回格式错误 ({url_label}): {result}")
                        break
                
                except requests.exceptions.HTTPError as e:
                    print(f"   错误响应内容: {e.response.text if e.response else 'N/A'}")
                    if e.response.status_code == 500:
                        wait_time = (2 ** attempt) * 0.5
                        print(f"⚠️ 服务器错误 (500) - {url_label}, 尝试 {attempt + 1}/{max_retries}")
                        if attempt < max_retries - 1:
                            print(f"   等待 {wait_time:.1f} 秒后重试...")
                            time.sleep(wait_time)
                        else:
                            print(f"   已达到最大重试次数，尝试下一个URL")
                    else:
                        print(f"⚠️ HTTP错误 ({e.response.status_code}) - {url_label}: {e}")
                        break
                
                except requests.exceptions.Timeout:
                    print(f"⚠️ 请求超时 - {url_label}, 尝试 {attempt + 1}/{max_retries}")
                    if attempt == max_retries - 1:
                        print(f"   已达到最大重试次数，尝试下一个URL")
                
                except Exception as e:
                    print(f"⚠️ 调用TTS API时出错 ({url_label}): {type(e).__name__}: {e}")
                    import traceback
                    print(f"   堆栈跟踪: {traceback.format_exc()}")
                    break
        
        print(f"❌ 所有TTS API端点均失败，跳过音频生成")
        return None
