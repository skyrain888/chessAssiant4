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
# @jwt_required()
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
        
        # 这里可以调用大模型API解析棋谱，但为简化处理，返回空moves
        return make_response({
            "image_url": image_url,
            "moves": ""
        })

# 路由：解析棋谱
@chess_bp.route('/parse', methods=['POST'])
@jwt_required()
def parse_notation():
    user_id = get_jwt_identity()
    data = request.json
    
    image_url = data.get('image_url')
    model = data.get('model', 'gpt-4-vision')
    
    if not image_url:
        return make_response(None, "图片URL不能为空", 400)
    
    try:
        # 调用AI解析棋谱
        moves = parse_chess_notation(image_url, model)
        return make_response({
            "moves": moves
        })
    except Exception as e:
        current_app.logger.error(f"解析棋谱失败: {str(e)}")
        return make_response(None, f"解析棋谱失败: {str(e)}", 500)

# 路由：创建棋谱
@chess_bp.route('/notations', methods=['POST'])
@jwt_required()
def create_chess_notation():
    user_id = get_jwt_identity()
    data = request.json
    
    title = data.get('title')
    description = data.get('description', '')
    moves = data.get('moves')
    image_url = data.get('image_url', '')
    difficulty = data.get('difficulty', 'medium')
    tags = data.get('tags', [])
    
    if not title or not moves:
        return make_response(None, "标题和棋谱步骤不能为空", 400)
    
    try:
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
        
        return make_response(notation.to_dict())
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