#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid
import json
from datetime import datetime

from models.chess import ChessNotation
from models.db import db
from utils.response import make_response
from utils.ai import parse_chess_notation

# 创建蓝图
chess_bp = Blueprint('chess', __name__)

# 路由：上传棋谱图片
@chess_bp.route('/upload', methods=['POST'])
# 暂时注释掉JWT认证要求，用于测试

def upload_chess_image():
    # 如果有JWT认证，则获取用户ID，否则使用默认值
    try:
        user_id = get_jwt_identity()
    except:
        user_id = 1  # 使用默认用户ID
    
    # 打印请求信息
    print("=" * 50)
    print("请求方法:", request.method)
    print("请求内容类型:", request.content_type)
    print("请求头:", dict(request.headers))
    print("表单数据:", request.form.to_dict() if request.form else "无表单数据")
    print("请求文件:", [f.filename for f in request.files.values()] if request.files else "无文件")
    print("请求体:", request.get_data(as_text=True)[:200] + "..." if len(request.get_data(as_text=True)) > 200 else request.get_data(as_text=True))
    print("=" * 50)
    
    # 检查请求中的文件
    if not request.files:
        print("请求中没有文件")
        return make_response(None, "未找到文件", 400)
    
    if 'file' not in request.files:
        print("未找到'file'字段，但有其他文件字段:", list(request.files.keys()))
        
        # 如果只有一个文件，尝试使用它
        if len(request.files) == 1:
            key = list(request.files.keys())[0]
            file = request.files[key]
            print(f"使用唯一的文件字段 '{key}' 代替 'file'")
        else:
            return make_response(None, "未找到文件", 400)
    else:
        file = request.files['file']
    
    print("文件名:", file.filename)
    print("文件类型:", file.content_type)
    
    if file.filename == '':
        return make_response(None, "未选择文件", 400)
    
    # 验证文件类型
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return make_response(None, "不支持的文件类型", 400)
    
    # 验证文件大小
    file_content = file.read()
    file.seek(0)  # 重置文件指针
    
    print("文件大小:", len(file_content), "字节")
    
    if len(file_content) > current_app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024):
        max_size_mb = current_app.config.get('MAX_CONTENT_LENGTH', 5 * 1024 * 1024) / (1024 * 1024)
        return make_response(None, f"文件大小不能超过{max_size_mb}MB", 400)
    
    if file:
        # 确保上传目录存在
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # 生成安全的文件名
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        file_path = os.path.join(upload_folder, filename)
        
        print("保存路径:", file_path)
        
        file.save(file_path)
        
        # 构建图片URL
        image_url = f"/uploads/{filename}"
        
        print("图片URL:", image_url)
        
        # 尝试调用AI解析棋谱
        moves = ""
        try:
            # 获取默认模型
            default_model = current_app.config.get('AI_MODEL', 'gpt-4-vision')
            # 调用AI解析棋谱
            moves = parse_chess_notation(file_path, default_model, is_file_path=True)
            print("AI解析结果:", moves)
        except Exception as e:
            print("AI解析失败:", str(e))
            # 解析失败不影响上传，只是返回空的moves
            moves = ""
        
        return make_response({
            "image_url": image_url,
            "moves": moves
        })

# 路由：解析棋谱
@chess_bp.route('/parse', methods=['POST'])
@jwt_required()
def parse_notation():
    # 获取用户ID
    user_id = get_jwt_identity()
    current_app.logger.info(f"解析棋谱请求，用户ID: {user_id}")
    
    # 检查请求中的文件
    if 'file' not in request.files:
        current_app.logger.error("解析棋谱请求中未找到文件")
        return make_response(None, "未找到文件", 400)
    
    file = request.files['file']
    
    if file.filename == '':
        current_app.logger.error("解析棋谱请求中未选择文件")
        return make_response(None, "未选择文件", 400)
    
    # 获取模型参数
    model = request.form.get('model', 'gpt-4-vision')
    current_app.logger.info(f"使用模型: {model}, 文件名: {file.filename}")
    
    try:
        # 保存上传的文件到临时目录
        filename = secure_filename(file.filename)
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_path)
        current_app.logger.info(f"文件已保存到临时路径: {temp_path}")
        
        # 调用AI解析棋谱，传入文件路径而不是URL
        moves = parse_chess_notation(temp_path, model, is_file_path=True)
        current_app.logger.info(f"棋谱解析成功，步骤数: {len(moves.split()) if moves else 0}")
        
        # 解析完成后删除临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)
            current_app.logger.info(f"临时文件已删除: {temp_path}")
            
        return make_response({
            "moves": moves
        })
    except Exception as e:
        current_app.logger.error(f"解析棋谱失败: {str(e)}")
        # 确保临时文件被删除
        try:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.remove(temp_path)
                current_app.logger.info(f"异常处理中删除临时文件: {temp_path}")
        except Exception as cleanup_error:
            current_app.logger.error(f"删除临时文件失败: {str(cleanup_error)}")
        
        # 返回更详细的错误信息
        error_message = str(e)
        error_code = 500
        
        # 根据错误类型返回不同的状态码
        if "权限不足" in error_message or "未授权" in error_message:
            error_code = 403
        elif "验证失败" in error_message:
            error_code = 422
        elif "未找到" in error_message:
            error_code = 404
        
        return make_response(None, f"解析棋谱失败: {error_message}", error_code)

# 路由：创建棋谱
@chess_bp.route('/notations', methods=['POST'])
@jwt_required()
def create_chess_notation():
    """创建新的棋谱"""
    # 获取用户ID，确保是字符串形式
    current_user_id = get_jwt_identity()
    current_app.logger.info(f"创建棋谱请求，用户ID: {current_user_id}, 类型: {type(current_user_id)}")
    
    # 获取请求数据
    data = request.json
    current_app.logger.debug(f"请求数据: {data}")
    
    # 提取字段
    title = data.get('title')
    description = data.get('description', '')
    moves = data.get('moves')
    image_url = data.get('image_url', '')
    difficulty = data.get('difficulty', 'medium')
    tags = data.get('tags', [])
    
    # 验证必填字段
    if not title or not moves:
        current_app.logger.warning("标题或棋谱步骤为空")
        return make_response(None, "标题和棋谱步骤不能为空", 400)
    
    try:
        # 确保用户ID是整数
        user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        
        # 创建新棋谱
        notation = ChessNotation(
            title=title,
            description=description,
            moves=moves,
            image_url=image_url,
            difficulty=difficulty,
            tags=tags,
            user_id=user_id
        )
        
        # 保存到数据库
        db.session.add(notation)
        db.session.commit()
        
        current_app.logger.info(f"棋谱创建成功，ID: {notation.id}, 标题: {notation.title}")
        return make_response(notation.to_dict())
    except ValueError as e:
        current_app.logger.error(f"用户ID格式错误: {current_user_id}, 错误: {str(e)}")
        return make_response(None, f"用户ID格式错误", 400)
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"创建棋谱失败: {str(e)}")
        return make_response(None, f"创建棋谱失败: {str(e)}", 500)

# 路由：获取棋谱列表
@chess_bp.route('/notations', methods=['GET'])
@jwt_required()
def get_chess_notations():
    user_id = get_jwt_identity()
    
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))
    keyword = request.args.get('keyword', '')
    difficulty = request.args.get('difficulty', '')
    tags = request.args.getlist('tags')
    
    # 构建查询
    query = ChessNotation.query.filter_by(user_id=user_id)
    
    # 应用筛选条件
    if keyword:
        query = query.filter(
            (ChessNotation.title.ilike(f'%{keyword}%')) | 
            (ChessNotation.description.ilike(f'%{keyword}%'))
        )
    
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    if tags:
        for tag in tags:
            query = query.filter(ChessNotation.tags.contains([tag]))
    
    # 获取总数
    total = query.count()
    
    # 分页
    notations = query.order_by(ChessNotation.created_at.desc()).paginate(
        page=page, per_page=size, error_out=False
    )
    
    # 转换为字典列表
    notation_list = [notation.to_dict() for notation in notations.items]
    
    return make_response({
        "data": notation_list,
        "total": total,
        "page": page,
        "size": size
    })

# 路由：获取棋谱详情
@chess_bp.route('/notations/<int:notation_id>', methods=['GET'])
@jwt_required()
def get_chess_notation(notation_id):
    user_id = get_jwt_identity()
    
    notation = ChessNotation.query.filter_by(id=notation_id, user_id=user_id).first()
    
    if not notation:
        return make_response(None, "棋谱不存在或无权访问", 404)
    
    return make_response(notation.to_dict())

# 路由：更新棋谱
@chess_bp.route('/notations/<int:notation_id>', methods=['PUT'])
@jwt_required()
def update_chess_notation(notation_id):
    user_id = get_jwt_identity()
    data = request.json
    
    notation = ChessNotation.query.filter_by(id=notation_id, user_id=user_id).first()
    
    if not notation:
        return make_response(None, "棋谱不存在或无权访问", 404)
    
    try:
        # 更新字段
        if 'title' in data:
            notation.title = data['title']
        
        if 'description' in data:
            notation.description = data['description']
        
        if 'moves' in data:
            notation.moves = data['moves']
        
        if 'image_url' in data:
            notation.image_url = data['image_url']
        
        if 'difficulty' in data:
            notation.difficulty = data['difficulty']
        
        if 'tags' in data:
            notation.tags = data['tags']
        
        # 更新时间
        notation.updated_at = datetime.utcnow()
        
        # 保存到数据库
        db.session.commit()
        
        return make_response(notation.to_dict())
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"更新棋谱失败: {str(e)}")
        return make_response(None, f"更新棋谱失败: {str(e)}", 500)

# 路由：删除棋谱
@chess_bp.route('/notations/<int:notation_id>', methods=['DELETE'])
@jwt_required()
def delete_chess_notation(notation_id):
    user_id = get_jwt_identity()
    
    notation = ChessNotation.query.filter_by(id=notation_id, user_id=user_id).first()
    
    if not notation:
        return make_response(None, "棋谱不存在或无权访问", 404)
    
    try:
        db.session.delete(notation)
        db.session.commit()
        return make_response(None, "删除成功")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"删除棋谱失败: {str(e)}")
        return make_response(None, f"删除棋谱失败: {str(e)}", 500) 