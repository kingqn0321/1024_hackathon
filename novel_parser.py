import re
from typing import List, Dict
from dataclasses import dataclass
from openai import OpenAI
from config import settings


@dataclass
class Character:
    name: str
    description: str
    appearance: str
    personality: str


@dataclass
class Scene:
    scene_number: int
    characters: List[str]
    setting: str
    narration: str
    dialogue: List[Dict[str, str]]
    image_prompt: str


class NovelParser:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
    
    def extract_characters(self, novel_text: str) -> List[Character]:
        if not self.client:
            return self._extract_characters_simple(novel_text)
        
        prompt = f"""分析以下小说文本，提取所有主要角色的信息。对于每个角色，提供：
1. 角色名字
2. 角色描述（背景、职业等）
3. 外貌特征（详细描述，用于图像生成）
4. 性格特点

小说文本：
{novel_text}

请以JSON格式返回，格式如下：
[
  {{
    "name": "角色名",
    "description": "角色描述",
    "appearance": "外貌特征（详细、具体，适合用于AI图像生成）",
    "personality": "性格特点"
  }}
]
"""
        
        response = self.client.chat.completions.create(
            model=settings.text_model,
            messages=[
                {"role": "system", "content": "你是一个专业的小说分析助手。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        import json
        characters_data = json.loads(response.choices[0].message.content)
        return [Character(**char) for char in characters_data]
    
    def _extract_characters_simple(self, novel_text: str) -> List[Character]:
        return [
            Character(
                name="示例角色",
                description="这是一个示例角色",
                appearance="年轻女性，长黑发，穿着校服，大眼睛",
                personality="开朗活泼，善良友好"
            )
        ]
    
    def split_into_scenes(self, novel_text: str, characters: List[Character]) -> List[Scene]:
        if not self.client:
            return self._split_scenes_simple(novel_text, characters)
        
        character_names = [c.name for c in characters]
        
        prompt = f"""将以下小说分解成多个场景，每个场景应该：
1. 包含明确的时间和地点
2. 列出场景中出现的角色
3. 提供场景描述和旁白
4. 提取对话
5. 生成适合用于AI图像生成的详细视觉提示词

已知角色：{', '.join(character_names)}

小说文本：
{novel_text}

请以JSON格式返回，格式如下：
[
  {{
    "scene_number": 1,
    "characters": ["角色1", "角色2"],
    "setting": "场景地点和时间",
    "narration": "场景旁白描述",
    "dialogue": [
      {{"speaker": "角色1", "text": "对话内容"}},
      {{"speaker": "角色2", "text": "对话内容"}}
    ],
    "image_prompt": "详细的英文图像生成提示词，描述场景、角色位置、动作、氛围等"
  }}
]
"""
        
        response = self.client.chat.completions.create(
            model=settings.text_model,
            messages=[
                {"role": "system", "content": "你是一个专业的小说场景分析师。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        import json
        scenes_data = json.loads(response.choices[0].message.content)
        return [Scene(**scene) for scene in scenes_data]
    
    def _split_scenes_simple(self, novel_text: str, characters: List[Character]) -> List[Scene]:
        paragraphs = [p.strip() for p in novel_text.split('\n\n') if p.strip()]
        scenes = []
        
        for i, para in enumerate(paragraphs[:5]):
            scenes.append(Scene(
                scene_number=i + 1,
                characters=[characters[0].name] if characters else [],
                setting="场景设置",
                narration=para[:200],
                dialogue=[],
                image_prompt=f"anime style scene {i+1}, character in a setting"
            ))
        
        return scenes
