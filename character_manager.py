from typing import Dict, List
from dataclasses import dataclass
from novel_parser import Character


@dataclass
class CharacterVisualProfile:
    name: str
    base_appearance: str
    reference_prompt: str
    seed: int


class CharacterManager:
    def __init__(self, characters: List[Character]):
        self.characters = {c.name: c for c in characters}
        self.visual_profiles: Dict[str, CharacterVisualProfile] = {}
        self._initialize_visual_profiles()
    
    def _initialize_visual_profiles(self):
        for name, character in self.characters.items():
            seed = hash(name) % 1000000
            
            reference_prompt = self._create_reference_prompt(character)
            
            self.visual_profiles[name] = CharacterVisualProfile(
                name=name,
                base_appearance=character.appearance,
                reference_prompt=reference_prompt,
                seed=seed
            )
    
    def _create_reference_prompt(self, character: Character) -> str:
        prompt = f"""anime style character portrait, {character.appearance}, 
consistent character design, detailed features, professional anime art style, 
full body reference sheet, character turnaround"""
        return prompt.strip()
    
    def get_character_prompt_for_scene(self, character_name: str, scene_context: str = "") -> str:
        if character_name not in self.visual_profiles:
            return ""
        
        profile = self.visual_profiles[character_name]
        base = self.characters[character_name]
        
        prompt = f"""{base.appearance}, anime style, {scene_context}, 
consistent with character design, detailed and expressive"""
        
        return prompt.strip()
    
    def get_visual_profile(self, character_name: str) -> CharacterVisualProfile:
        return self.visual_profiles.get(character_name)
