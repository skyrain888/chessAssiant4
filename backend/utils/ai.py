#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
from flask import current_app
import openai
import google.generativeai as genai
from anthropic import Anthropic
import re

def parse_chess_notation(image_url, model='gpt-4-vision', is_file_path=False):
    """
    使用AI模型解析棋谱图片
    
    Args:
        image_url: 图片URL或文件路径
        model: 使用的模型，支持 'gpt-4-vision', 'gemini-pro-vision', 'claude-3-opus'
        is_file_path: 是否直接传入文件路径
    
    Returns:
        解析后的棋谱步骤
    """
    # 获取图片完整路径
    if is_file_path:
        # 如果直接传入文件路径，直接使用
        image_path = image_url
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
    elif image_url.startswith('/'):
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
    elif model == 'claude-3':
        return parse_with_claude(image_path)
    else:
        raise ValueError(f"不支持的模型: {model}")

def normalize_chess_notation(moves):
    """
    规范化棋谱格式，确保每步棋都包含白方和黑方的走法在同一行
    
    Args:
        moves: 原始棋谱文本
        
    Returns:
        规范化后的棋谱文本
    """
    # 如果输入为空，直接返回
    if not moves:
        return moves
    
    # 分割成行
    lines = moves.strip().split('\n')
    normalized_lines = []
    current_move = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检查是否是新的一步（白方）
        if re.match(r'^\d+\.', line):
            # 如果是完整的一步（包含白方和黑方），直接添加
            if ' ' in line and not line.endswith('.'):
                normalized_lines.append(line)
                current_move = None
            else:
                # 如果只有白方，保存当前步骤
                current_move = line
        # 检查是否是黑方的走法
        elif current_move and (line.startswith('...') or not re.match(r'^\d+\.', line)):
            # 去掉可能的"..."前缀
            black_move = re.sub(r'^\d+\.\.\.', '', line).strip()
            # 合并白方和黑方的走法
            normalized_lines.append(f"{current_move} {black_move}")
            current_move = None
        else:
            # 其他情况，直接添加
            normalized_lines.append(line)
    
    # 如果最后还有未处理的当前步骤，添加它
    if current_move:
        normalized_lines.append(current_move)
    
    return '\n'.join(normalized_lines)

def parse_with_gpt4_vision(image_path):
    """使用GPT-4 Vision解析棋谱"""
    # 设置API密钥
    api_key = current_app.config.get('OPENAI_API_KEY')
    if not api_key:
        current_app.logger.warning("未找到 OPENAI_API_KEY 配置，使用模拟数据进行测试")
        # 返回模拟数据用于测试
        return "1.e4 e5 2.Nf3 Nc6 3.Bb5 a6 4.Ba4 Nf6 5.O-O Be7 6.Re1 b5 7.Bb3 d6 8.c3 O-O 9.h3 Nb8 10.d4 Nbd7"
    
    try:
        # 临时清除环境变量中的代理设置，避免影响OpenAI客户端
        original_http_proxy = os.environ.pop('HTTP_PROXY', None)
        original_https_proxy = os.environ.pop('HTTPS_PROXY', None)
        
        openai.api_key = api_key
        
        # 打印调试信息
        current_app.logger.info(f"解析图片路径: {image_path}")
        current_app.logger.info(f"使用模型: gpt-4-vision-preview")
        
        # 准备图片数据
        if image_path.startswith(('http://', 'https://')):
            # 如果是URL，直接使用
            image_data = {"url": image_path}
            current_app.logger.info(f"使用URL图片: {image_path}")
        else:
            # 如果是本地文件，读取并编码
            try:
                with open(image_path, "rb") as image_file:
                    import base64
                    image_bytes = image_file.read()
                    current_app.logger.info(f"读取本地图片成功，大小: {len(image_bytes)} 字节")
                    image_data = {
                        "data": f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                    }
            except Exception as e:
                current_app.logger.error(f"读取图片文件失败: {str(e)}")
                raise FileNotFoundError(f"无法读取图片文件: {str(e)}")
        
        try:
            # 调用API
            current_app.logger.info("开始调用 OpenAI API...")
            response = openai.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个国际象棋专家，擅长解析棋谱图片。请分析图片中的棋谱，并以标准代数记号(SAN)格式返回所有步骤。请确保格式正确，每步棋必须包含白方和黑方的走法在同一行，例如：'1. e4 e5'，而不是分开显示。如果某一步只有一方的走法，也要保持格式一致。只返回棋步，不要有其他解释。"
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "请解析这张棋谱图片，以标准代数记号(SAN)格式返回所有步骤。确保每步棋都包含白方和黑方的走法在同一行，例如：'1. e4 e5'，'2. Nf3 Nc6'等。"},
                            {"type": "image", "image": image_data}
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            # 提取结果
            moves = response.choices[0].message.content.strip()
            current_app.logger.info(f"API调用成功，解析结果: {moves[:100]}...")
            
            # 规范化棋谱格式
            normalized_moves = normalize_chess_notation(moves)
            current_app.logger.info(f"规范化后的结果: {normalized_moves[:100]}...")
            
            return normalized_moves
        except Exception as e:
            current_app.logger.error(f"调用 OpenAI API 失败: {str(e)}")
            raise RuntimeError(f"调用 OpenAI API 失败: {str(e)}")
    finally:
        # 恢复环境变量中的代理设置
        if original_http_proxy:
            os.environ['HTTP_PROXY'] = original_http_proxy
        if original_https_proxy:
            os.environ['HTTPS_PROXY'] = original_https_proxy

def parse_with_gemini(image_path):
    """使用Gemini Pro Vision解析棋谱"""
    # 设置API密钥
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        current_app.logger.warning("未找到 GEMINI_API_KEY 配置，使用模拟数据进行测试")
        # 返回模拟数据用于测试
        return "1.d4 Nf6 2.c4 e6 3.Nc3 Bb4 4.e3 O-O 5.Bd3 d5 6.Nf3 c5 7.O-O Nc6 8.a3 Ba5 9.Ne5 Nxe5 10.dxe5 Nd7"
    

    # 配置Gemini API
    genai.configure(api_key=api_key)
    
    # 从配置文件获取模型名称
    model_name = current_app.config.get('GEMINI_MODEL_NAME', 'gemini-pro-vision')
    current_app.logger.info(f"使用Gemini模型: {model_name}")
    
    current_app.logger.info(f"解析图片路径: {image_path}")
    
    try:
        # 导入必要的库
        import base64
        import pathlib
        
        # 读取图片文件为base64
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            current_app.logger.info(f"读取本地图片成功，大小: {len(image_bytes)} 字节")
        
        # 确定图片MIME类型
        file_extension = pathlib.Path(image_path).suffix.lower()
        if file_extension in ['.jpg', '.jpeg']:
            mime_type = 'image/jpeg'
        elif file_extension == '.png':
            mime_type = 'image/png'
        else:
            mime_type = 'image/jpeg'  # 默认使用jpeg
        
        current_app.logger.info(f"图片MIME类型: {mime_type}")
        
        # 创建模型配置
        generation_config = {
            "temperature": 0,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 1024,
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        # 创建模型实例
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
        
        current_app.logger.info(f"开始调用 Gemini API，模型: {model_name}...")
        
        # 将图片转换为base64字符串
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # 创建请求内容
        contents = [
            {
                "role": "user",
                "parts": [
                    {"text": "你是一个国际象棋专家，擅长解析棋谱图片。请分析图片中的棋谱，并以标准代数记号(SAN)格式返回所有步骤。请确保格式正确，每步棋必须包含白方和黑方的走法在同一行，例如：'1. e4 e5'，'2. Nf3 Nc6'等，而不是分开显示。如果某一步只有一方的走法，也要保持格式一致。只返回棋步，不要有其他解释。"},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
        
        # 调用API
        current_app.logger.info("发送请求到Gemini API...")
        response = model.generate_content(contents)
        
        # 提取结果
        moves = response.text.strip()
        current_app.logger.info(f"API调用成功，解析结果: {moves[:100]}...")
        
        # 规范化棋谱格式
        normalized_moves = normalize_chess_notation(moves)
        current_app.logger.info(f"规范化后的结果: {normalized_moves[:100]}...")
        
        return normalized_moves
    except Exception as e:
        current_app.logger.error(f"调用 Gemini API 失败: {str(e)}")
        # 打印更详细的错误信息
        import traceback
        current_app.logger.error(f"详细错误: {traceback.format_exc()}")
        raise RuntimeError(f"调用 Gemini API 失败: {str(e)}")

def parse_with_claude(image_path):
    """使用Claude 3解析棋谱"""
    # 设置API密钥
    api_key = current_app.config.get('ANTHROPIC_API_KEY')
    if not api_key:
        current_app.logger.warning("未找到 ANTHROPIC_API_KEY 配置，使用模拟数据进行测试")
        # 返回模拟数据用于测试
        return "1.e4 c5 2.Nf3 d6 3.d4 cxd4 4.Nxd4 Nf6 5.Nc3 a6 6.Be3 e5 7.Nb3 Be6 8.f3 Be7 9.Qd2 O-O 10.O-O-O Nbd7"
    
    try:
        # 临时清除环境变量中的代理设置，避免影响Anthropic客户端
        original_http_proxy = os.environ.pop('HTTP_PROXY', None)
        original_https_proxy = os.environ.pop('HTTPS_PROXY', None)
        
        # 创建Anthropic客户端，只传入必要的参数
        client = Anthropic(api_key=api_key)
        
        current_app.logger.info(f"解析图片路径: {image_path}")
        current_app.logger.info(f"使用模型: claude-3-opus-20240229")
        
        # 准备图片数据
        try:
            # 读取图片文件并进行base64编码
            with open(image_path, "rb") as image_file:
                import base64
                image_bytes = image_file.read()
                current_app.logger.info(f"读取本地图片成功，大小: {len(image_bytes)} 字节")
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                
                # 构建媒体类型
                file_extension = os.path.splitext(image_path)[1].lower()
                if file_extension in ['.jpg', '.jpeg']:
                    media_type = 'image/jpeg'
                elif file_extension == '.png':
                    media_type = 'image/png'
                else:
                    media_type = 'image/jpeg'  # 默认使用jpeg
        except Exception as e:
            current_app.logger.error(f"读取图片文件失败: {str(e)}")
            raise FileNotFoundError(f"无法读取图片文件: {str(e)}")
        
        current_app.logger.info("开始调用 Claude API...")
        
        # 调用Claude API
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "你是一个国际象棋专家，擅长解析棋谱图片。请分析图片中的棋谱，并以标准代数记号(SAN)格式返回所有步骤。请确保格式正确，每步棋必须包含白方和黑方的走法在同一行，例如：'1. e4 e5'，'2. Nf3 Nc6'等，而不是分开显示。如果某一步只有一方的走法，也要保持格式一致。只返回棋步，不要有其他解释。"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_base64
                            }
                        }
                    ]
                }
            ]
        )
        
        # 提取结果
        moves = response.content[0].text.strip()
        current_app.logger.info(f"API调用成功，解析结果: {moves[:100]}...")
        
        # 规范化棋谱格式
        normalized_moves = normalize_chess_notation(moves)
        current_app.logger.info(f"规范化后的结果: {normalized_moves[:100]}...")
        
        return normalized_moves
    except Exception as e:
        current_app.logger.error(f"调用 Claude API 失败: {str(e)}")
        raise RuntimeError(f"调用 Claude API 失败: {str(e)}")
    finally:
        # 恢复环境变量中的代理设置
        if original_http_proxy:
            os.environ['HTTP_PROXY'] = original_http_proxy
        if original_https_proxy:
            os.environ['HTTPS_PROXY'] = original_https_proxy 