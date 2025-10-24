import os
import json
import time
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from anime_generator import AnimeGenerator
from config import settings

app = Flask(__name__)
CORS(app)

tasks = {}


def generate_anime_task(task_id: str, novel_text: str):
    try:
        tasks[task_id]['status'] = 'processing'
        tasks[task_id]['progress'] = 10
        tasks[task_id]['message'] = '正在初始化...'
        
        generator = AnimeGenerator()
        
        tasks[task_id]['progress'] = 20
        tasks[task_id]['message'] = '正在分析小说内容...'
        
        result = generator.generate_from_novel(
            novel_text,
            generate_images=True,
            generate_audio=True
        )
        
        tasks[task_id]['progress'] = 90
        tasks[task_id]['message'] = '正在生成预览页面...'
        
        preview_path = generator.generate_preview_html()
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['progress'] = 100
        tasks[task_id]['message'] = '生成完成！'
        tasks[task_id]['result'] = {
            'preview_url': f'/output/preview.html',
            'characters_count': len(result['characters']),
            'scenes_count': result['total_scenes']
        }
        
    except Exception as e:
        tasks[task_id]['status'] = 'failed'
        tasks[task_id]['message'] = f'生成失败: {str(e)}'
        tasks[task_id]['error'] = str(e)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        novel_text = data.get('novel_text', '')
        
        if not novel_text:
            return jsonify({
                'error': '请输入小说文本'
            }), 400
        
        task_id = str(int(time.time() * 1000))
        
        tasks[task_id] = {
            'status': 'pending',
            'progress': 0,
            'message': '任务已创建，等待处理...',
            'result': None,
            'error': None
        }
        
        thread = threading.Thread(
            target=generate_anime_task,
            args=(task_id, novel_text)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'task_id': task_id,
            'message': '动漫生成任务已启动'
        })
        
    except Exception as e:
        return jsonify({
            'error': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/status/<task_id>', methods=['GET'])
def get_status(task_id):
    if task_id not in tasks:
        return jsonify({
            'error': '任务不存在'
        }), 404
    
    return jsonify(tasks[task_id])


@app.route('/output/<path:filename>')
def serve_output(filename):
    output_dir = Path(settings.output_dir).absolute()
    return send_from_directory(output_dir, filename)


@app.route('/api/example-novel', methods=['GET'])
def get_example_novel():
    try:
        with open('example_novel.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({
            'content': content
        })
    except Exception as e:
        return jsonify({
            'error': f'无法读取示例小说: {str(e)}'
        }), 500


if __name__ == '__main__':
    output_dir = Path(settings.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("🎬 动漫生成器 Web 服务")
    print("=" * 60)
    print(f"✓ 服务地址: http://{settings.web_host}:{settings.web_port}")
    print(f"✓ 输出目录: {output_dir.absolute()}")
    print("=" * 60 + "\n")
    
    app.run(
        host=settings.web_host,
        port=settings.web_port,
        debug=settings.web_debug
    )
