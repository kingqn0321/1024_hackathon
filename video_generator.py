import subprocess
import json
from pathlib import Path
from typing import List, Optional, Dict
from config import settings


class VideoGenerator:
    def __init__(self):
        self.output_dir = Path(settings.output_dir) / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self._check_ffmpeg()
    
    def _check_ffmpeg(self):
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ 未检测到 ffmpeg，请安装 ffmpeg 以使用视频生成功能")
            print("   安装方法：")
            print("   - Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("   - macOS: brew install ffmpeg")
            print("   - Windows: 从 https://ffmpeg.org/download.html 下载")
    
    def generate_video_from_scenes(
        self,
        scenes: List[Dict],
        output_filename: str = "output.mp4",
        fps: int = 1,
        audio_enabled: bool = True
    ) -> Optional[str]:
        if not scenes:
            print("⚠️ 没有场景数据，无法生成视频")
            return None
        
        scenes_with_images = [s for s in scenes if s.get("image_path")]
        if not scenes_with_images:
            print("⚠️ 没有找到场景图片，无法生成视频")
            return None
        
        output_path = self.output_dir / output_filename
        
        try:
            if audio_enabled and any(s.get("audio_path") for s in scenes):
                return self._generate_video_with_audio(scenes_with_images, output_path)
            else:
                return self._generate_video_without_audio(scenes_with_images, output_path, fps)
        
        except Exception as e:
            print(f"生成视频时出错: {e}")
            import traceback
            print(f"堆栈跟踪: {traceback.format_exc()}")
            return None
    
    def _generate_video_without_audio(
        self,
        scenes: List[Dict],
        output_path: Path,
        fps: int = 1
    ) -> Optional[str]:
        concat_file = self.output_dir / "concat_list.txt"
        
        with open(concat_file, 'w', encoding='utf-8') as f:
            for scene in scenes:
                image_path = scene.get("image_path")
                if image_path and Path(image_path).exists():
                    duration = 1.0 / fps
                    f.write(f"file '{Path(image_path).absolute()}'\n")
                    f.write(f"duration {duration}\n")
            
            last_image = scenes[-1].get("image_path")
            if last_image and Path(last_image).exists():
                f.write(f"file '{Path(last_image).absolute()}'\n")
        
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-vf", "scale=1024:1024:force_original_aspect_ratio=decrease,pad=1024:1024:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ FFmpeg 错误: {result.stderr}")
            return None
        
        print(f"✓ 视频已保存到: {output_path}")
        return str(output_path)
    
    def _generate_video_with_audio(
        self,
        scenes: List[Dict],
        output_path: Path
    ) -> Optional[str]:
        temp_dir = self.output_dir / "temp"
        temp_dir.mkdir(exist_ok=True)
        
        segment_files = []
        
        for idx, scene in enumerate(scenes):
            image_path = scene.get("image_path")
            audio_path = scene.get("audio_path")
            
            if not image_path or not Path(image_path).exists():
                continue
            
            segment_output = temp_dir / f"segment_{idx:03d}.mp4"
            
            if audio_path and Path(audio_path).exists():
                cmd = [
                    "ffmpeg",
                    "-loop", "1",
                    "-i", str(Path(image_path).absolute()),
                    "-i", str(Path(audio_path).absolute()),
                    "-vf", "scale=1024:1024:force_original_aspect_ratio=decrease,pad=1024:1024:(ow-iw)/2:(oh-ih)/2",
                    "-c:v", "libx264",
                    "-tune", "stillimage",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-pix_fmt", "yuv420p",
                    "-shortest",
                    "-y",
                    str(segment_output)
                ]
            else:
                cmd = [
                    "ffmpeg",
                    "-loop", "1",
                    "-i", str(Path(image_path).absolute()),
                    "-t", "3",
                    "-vf", "scale=1024:1024:force_original_aspect_ratio=decrease,pad=1024:1024:(ow-iw)/2:(oh-ih)/2",
                    "-c:v", "libx264",
                    "-tune", "stillimage",
                    "-pix_fmt", "yuv420p",
                    "-y",
                    str(segment_output)
                ]
            
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if result.returncode == 0:
                segment_files.append(segment_output)
            else:
                print(f"⚠️ 场景 {idx} 视频段生成失败: {result.stderr}")
        
        if not segment_files:
            print("❌ 没有成功生成任何视频段")
            return None
        
        concat_file = temp_dir / "segments_concat.txt"
        with open(concat_file, 'w', encoding='utf-8') as f:
            for segment in segment_files:
                f.write(f"file '{segment.absolute()}'\n")
        
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.returncode != 0:
            print(f"❌ 视频合并失败: {result.stderr}")
            return None
        
        for segment in segment_files:
            try:
                segment.unlink()
            except:
                pass
        
        print(f"✓ 视频已保存到: {output_path}")
        return str(output_path)
