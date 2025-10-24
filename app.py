# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify, send_from_directory
from pathlib import Path
import threading
import time
from anime_generator import AnimeGenerator
from config import settings
import json
import os

app = Flask(__name__)

generation_status = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_anime():
    data = request.json
    novel_text = data.get('novel_text', '')
    
    if not novel_text or not novel_text.strip():
        return jsonify({'error': '小说文本不能为空'}), 400
    
    task_id = str(int(time.time() * 1000))
    
    generation_status[task_id] = {
        'status': 'processing',
        'progress': 0,
        'message': '开始处理...',
        'result': None
    }
    
    thread = threading.Thread(
        target=run_generation,
        args=(task_id, novel_text)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'task_id': task_id,
        'message': '动漫生成任务已启动'
    })


@app.route('/api/status/<task_id>')
def get_status(task_id):
    if task_id not in generation_status:
        return jsonify({'error': '任务不存在'}), 404
    
    return jsonify(generation_status[task_id])


@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory(settings.output_dir, filename)


def run_generation(task_id, novel_text):
    try:
        generation_status[task_id]['message'] = '正在初始化生成器...'
        generation_status[task_id]['progress'] = 10
        
        generator = AnimeGenerator()
        
        generation_status[task_id]['message'] = '正在生成动漫...'
        generation_status[task_id]['progress'] = 20
        
        result = generator.generate_from_novel(
            novel_text,
            generate_images=True,
            generate_audio=True
        )
        
        generation_status[task_id]['message'] = '正在生成预览页面...'
        generation_status[task_id]['progress'] = 90
        
        preview_html = generator.generate_preview_html()
        
        relative_preview_path = os.path.relpath(preview_html, settings.output_dir)
        
        generation_status[task_id]['status'] = 'completed'
        generation_status[task_id]['progress'] = 100
        generation_status[task_id]['message'] = '生成完成！'
        generation_status[task_id]['result'] = {
            'preview_url': '/output/{}'.format(relative_preview_path),
            'characters_count': len(result['characters']),
            'scenes_count': result['total_scenes']
        }
        
    except Exception as e:
        generation_status[task_id]['status'] = 'error'
        generation_status[task_id]['message'] = '生成失败: {}'.format(str(e))
        generation_status[task_id]['progress'] = 0


if __name__ == '__main__':
    app.run(
        host=settings.web_host,
        port=settings.web_port,
        debug=True
    )
