import os
import base64
from pathlib import Path
from typing import List, Optional
from openai import OpenAI, APITimeoutError, RateLimitError, APIError
from config import settings
from character_manager import CharacterManager
from novel_parser import Scene
import requests
import time
import logging

# 配置日志
logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self, character_manager: CharacterManager):
        self.character_manager = character_manager
        
        if settings.qiniu_api_key:
            self.client = OpenAI(
                api_key=settings.qiniu_api_key,
                base_url=settings.qiniu_base_url
            )
            self.use_qiniu = True
        elif settings.openai_api_key:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.use_qiniu = False
        else:
            self.client = None
            self.use_qiniu = False
            
        self.output_dir = Path(settings.output_dir) / "images"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 添加默认超时参数和重试次数
        self.api_timeout = 60  # 秒
        self.max_retries = 3
        self.retry_delay = 2  # 秒
    
    def generate_scene_image(self, scene: Scene, output_filename: str) -> Optional[str]:
        if not self.client:
            print(f"⚠️ 未配置API Key，跳过图像生成")
            return None
        
        prompt = self._build_scene_prompt(scene)
        
        # 使用重试逻辑
        for attempt in range(self.max_retries):
            try:
                if self.use_qiniu:
                    response = self.client.images.generate(
                        model=settings.image_model,
                        prompt=prompt,
                        size="1024x1024",
                        n=1,
                        response_format="b64_json",
                        timeout=self.api_timeout  # 添加超时参数
                    )
                    
                    image_data = response.data[0].b64_json
                    output_path = self.output_dir / output_filename
                    self._save_base64_image(image_data, output_path)
                else:
                    response = self.client.images.generate(
                        model=settings.image_model,
                        prompt=prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                        timeout=self.api_timeout  # 添加超时参数
                    )
                    
                    image_url = response.data[0].url
                    output_path = self.output_dir / output_filename
                    self._download_image(image_url, output_path)
                
                return str(output_path)
                
            except APITimeoutError:
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    logger.warning(f"⚠️ API请求超时，{wait_time}秒后重试 (尝试 {attempt+1}/{self.max_retries})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ API请求超时，已达到最大重试次数 ({self.max_retries})")
                    return None
            except RateLimitError:
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    logger.warning(f"⚠️ API速率限制，{wait_time}秒后重试 (尝试 {attempt+1}/{self.max_retries})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ API速率限制，已达到最大重试次数 ({self.max_retries})")
                    return None
            except APIError as e:
                logger.error(f"⚠️ OpenAI API错误: {e}")
                return None
            except Exception as e:
                logger.error(f"生成图像时出错: {e}")
                return None
    
    def _build_scene_prompt(self, scene: Scene) -> str:
        character_descriptions = []
        for char_name in scene.characters:
            char_prompt = self.character_manager.get_character_prompt_for_scene(
                char_name, 
                scene.setting
            )
            if char_prompt:
                character_descriptions.append(f"{char_name}: {char_prompt}")
        
        prompt_parts = [
            "anime style scene,",
            scene.image_prompt,
            f"setting: {scene.setting}",
        ]
        
        if character_descriptions:
            prompt_parts.append("characters: " + "; ".join(character_descriptions))
        
        prompt_parts.extend([
            "high quality anime art style",
            "consistent character design",
            "detailed background",
            "cinematic composition"
        ])
        
        final_prompt = " ".join(prompt_parts)
        
        if len(final_prompt) > 1000:
            final_prompt = final_prompt[:1000]
        
        return final_prompt
    
    def _save_base64_image(self, b64_data: str, output_path: Path):
        image_bytes = base64.b64decode(b64_data)
        with open(output_path, 'wb') as f:
            f.write(image_bytes)
        print(f"✓ 图像已保存到: {output_path}")
    
    def _download_image(self, url: str, output_path: Path):
        response = requests.get(url, timeout=self.api_timeout)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ 图像已保存到: {output_path}")
    
    def generate_character_reference(self, character_name: str) -> Optional[str]:
        if not self.client:
            print(f"⚠️ 未配置API Key，跳过角色参考图生成")
            return None
        
        profile = self.character_manager.get_visual_profile(character_name)
        if not profile:
            return None
        
        # 使用重试逻辑
        for attempt in range(self.max_retries):
            try:
                output_path = self.output_dir / f"character_ref_{character_name}.png"
                
                if self.use_qiniu:
                    response = self.client.images.generate(
                        model=settings.image_model,
                        prompt=profile.reference_prompt,
                        size="1024x1024",
                        n=1,
                        response_format="b64_json",
                        timeout=self.api_timeout  # 添加超时参数
                    )
                    
                    image_data = response.data[0].b64_json
                    self._save_base64_image(image_data, output_path)
                else:
                    response = self.client.images.generate(
                        model=settings.image_model,
                        prompt=profile.reference_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                        timeout=self.api_timeout  # 添加超时参数
                    )
                    
                    image_url = response.data[0].url
                    self._download_image(image_url, output_path)
                
                return str(output_path)
                
            except APITimeoutError:
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    logger.warning(f"⚠️ API请求超时，{wait_time}秒后重试 (尝试 {attempt+1}/{self.max_retries})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ API请求超时，已达到最大重试次数 ({self.max_retries})")
                    return None
            except RateLimitError:
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    logger.warning(f"⚠️ API速率限制，{wait_time}秒后重试 (尝试 {attempt+1}/{self.max_retries})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ API速率限制，已达到最大重试次数 ({self.max_retries})")
                    return None
            except APIError as e:
                logger.error(f"⚠️ OpenAI API错误: {e}")
                return None
            except Exception as e:
                logger.error(f"生成角色参考图时出错: {e}")
                return None