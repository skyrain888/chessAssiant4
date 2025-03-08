#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from flask import current_app
import openai
import google.generativeai as genai
from anthropic import Anthropic

def parse_chess_notation(image_url, model='gpt-4-vision'):
    """
    使用AI模型解析棋谱图片
    
    Args:
        image_url: 图片URL
        model: 使用的模型，支持 'gpt-4-vision', 'gemini-pro-vision', 'claude-3-opus'
    
    Returns:
        解析后的棋谱步骤
    """
    # 获取图片完整URL
    if image_url.startswith('/'):
        # 如果是相对路径，转换为绝对路径
        image_path = os.path.join(current_app.root_path, 'uploads', image_url.lstrip('/'))
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
    else:
        # 如果是完整URL，直接使用
        image_path = image_url
    
    # 根据选择的模型调用不同的API
    if model == 'gpt-4-vision':
        return parse_with_gpt4_vision(image_path)
    elif model == 'gemini-pro-vision':
        return parse_with_gemini(image_path)
    elif model == 'claude-3-opus':
        return parse_with_claude(image_path)
    else:
        raise ValueError(f"不支持的模型: {model}")

def parse_with_gpt4_vision(image_path):
    """使用GPT-4 Vision解析棋谱"""
    # 设置API密钥
    openai.api_key = current_app.config['OPENAI_API_KEY']
    
    # 准备图片数据
    if image_path.startswith(('http://', 'https://')):
        # 如果是URL，直接使用
        image_data = {"url": image_path}
    else:
        # 如果是本地文件，读取并编码
        with open(image_path, "rb") as image_file:
            import base64
            image_data = {
                "data": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
            }
    
    # 调用API
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": "你是一个国际象棋专家，擅长解析棋谱图片。请分析图片中的棋谱，并以标准代数记号(SAN)格式返回所有步骤。只返回棋步，不要有其他解释。"
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "请解析这张棋谱图片，以标准代数记号(SAN)格式返回所有步骤。"},
                    {"type": "image", "image": image_data}
                ]
            }
        ],
        max_tokens=1000
    )
    
    # 提取结果
    moves = response.choices[0].message.content.strip()
    return moves

def parse_with_gemini(image_path):
    """使用Gemini Pro Vision解析棋谱"""
    # 设置API密钥
    genai.configure(api_key=current_app.config['GEMINI_API_KEY'])
    
    # 准备图片数据
    if image_path.startswith(('http://', 'https://')):
        # 如果是URL，下载图片
        response = requests.get(image_path)
        image_data = response.content
    else:
        # 如果是本地文件，读取
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
    
    # 创建模型
    model = genai.GenerativeModel('gemini-pro-vision')
    
    # 调用API
    response = model.generate_content([
        "请解析这张棋谱图片，以标准代数记号(SAN)格式返回所有步骤。只返回棋步，不要有其他解释。",
        image_data
    ])
    
    # 提取结果
    moves = response.text.strip()
    return moves

def parse_with_claude(image_path):
    """使用Claude 3 Opus解析棋谱"""
    # 创建客户端
    client = Anthropic(api_key=current_app.config['CLAUDE_API_KEY'])
    
    # 准备图片数据
    if image_path.startswith(('http://', 'https://')):
        # 如果是URL，直接使用
        image_url = image_path
    else:
        # 如果是本地文件，需要先上传到可访问的URL
        # 这里简化处理，实际应用中需要实现文件上传
        raise ValueError("Claude API需要公开可访问的图片URL")
    
    # 调用API
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请解析这张棋谱图片，以标准代数记号(SAN)格式返回所有步骤。只返回棋步，不要有其他解释。"
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": image_url
                        }
                    }
                ]
            }
        ]
    )
    
    # 提取结果
    moves = response.content[0].text.strip()
    return moves 