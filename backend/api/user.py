#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid

from models.user import User
from models.db import db
from utils.response import make_response

# 创建蓝图
user_bp = Blueprint('user', __name__)

# 导入模型
try:
    from models import db
    from models.user import User
except ImportError:
    # 如果模型不存在，创建一个简单的用户字典用于演示
    USERS = {
        1: {
            'id': 1,
            'username': 'admin',
            'email': 'admin@example.com',
            'name': '管理员',
            'avatar': None
        }
    }

# 路由：获取用户信息
@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取当前用户的个人资料"""
    current_user_id = get_jwt_identity()
    current_app.logger.info(f"获取用户资料请求，用户ID: {current_user_id}, 类型: {type(current_user_id)}")
    
    try:
        # 查询用户，确保用户ID是整数
        # 如果current_user_id是字符串形式的数字，需要转换为整数
        user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        user = User.query.get(user_id)
        
        if not user:
            current_app.logger.warning(f"用户不存在，ID: {current_user_id}")
            return make_response(None, "用户不存在", 404)
        
        current_app.logger.info(f"成功获取用户资料，用户ID: {current_user_id}")
        return make_response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'avatar': user.avatar,
            'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None
        })
    except ValueError as e:
        current_app.logger.error(f"用户ID格式错误: {current_user_id}, 错误: {str(e)}")
        return make_response(None, f"用户ID格式错误", 400)
    except Exception as e:
        current_app.logger.error(f"获取用户资料失败: {str(e)}")
        return make_response(None, f"获取用户资料失败: {str(e)}", 500)

# 路由：更新用户信息
@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新当前用户的个人资料"""
    current_user_id = get_jwt_identity()
    current_app.logger.info(f"更新用户资料请求，用户ID: {current_user_id}, 类型: {type(current_user_id)}")
    
    # 获取请求数据
    try:
        data = request.get_json()
    except Exception as e:
        current_app.logger.error(f"解析请求数据失败: {str(e)}")
        return make_response(None, "无效的请求数据格式，请确保发送的是JSON格式", 400)
    
    if not data:
        current_app.logger.warning("请求数据为空")
        return make_response(None, "请求数据不能为空", 400)
    
    try:
        # 查询用户，确保用户ID是整数
        user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        user = User.query.get(user_id)
        
        if not user:
            current_app.logger.warning(f"用户不存在，ID: {current_user_id}")
            return make_response(None, "用户不存在", 404)
        
        # 更新用户信息
        if 'name' in data:
            user.name = data['name']
            current_app.logger.debug(f"更新用户名称: {data['name']}")
        
        if 'avatar' in data:
            user.avatar = data['avatar']
            current_app.logger.debug(f"更新用户头像: {data['avatar']}")
        
        # 保存到数据库
        db.session.commit()
        current_app.logger.info(f"用户资料更新成功，用户ID: {current_user_id}")
        
        return make_response({
            'message': '个人资料更新成功',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.name,
                'avatar': user.avatar
            }
        })
    except ValueError as e:
        current_app.logger.error(f"用户ID格式错误: {current_user_id}, 错误: {str(e)}")
        return make_response(None, f"用户ID格式错误", 400)
    except Exception as e:
        current_app.logger.error(f"更新用户资料失败: {str(e)}")
        # 回滚数据库事务
        db.session.rollback()
        return make_response(None, f"更新用户资料失败: {str(e)}", 500)

@user_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """修改当前用户的密码"""
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('old_password') or not data.get('new_password'):
        return jsonify({'message': '请提供旧密码和新密码'}), 400
    
    try:
        # 查询用户
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        # 验证旧密码
        if not user.verify_password(data['old_password']):
            return jsonify({'message': '旧密码错误'}), 401
        
        # 更新密码
        user.set_password(data['new_password'])
        
        # 保存到数据库
        db.session.commit()
        
        return jsonify({'message': '密码修改成功'}), 200
    except (NameError, AttributeError):
        # 如果模型不存在，返回演示消息
        return jsonify({'message': '密码修改功能暂未实现'}), 501

# 路由：上传头像
@user_bp.route('/avatar', methods=['POST'])
@jwt_required()
def upload_avatar():
    """上传用户头像"""
    current_user_id = get_jwt_identity()
    
    if 'avatar' not in request.files:
        return jsonify({'message': '没有上传文件'}), 400
    
    file = request.files['avatar']
    
    if file.filename == '':
        return jsonify({'message': '没有选择文件'}), 400
    
    try:
        # 查询用户
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'message': '用户不存在'}), 404
        
        # 保存文件
        filename = f"avatar_{current_user_id}_{os.path.basename(file.filename)}"
        upload_folder = os.path.join(os.getcwd(), 'uploads', 'avatars')
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # 更新用户头像
        user.avatar = f"/uploads/avatars/{filename}"
        
        # 保存到数据库
        db.session.commit()
        
        return jsonify({
            'message': '头像上传成功',
            'avatar': user.avatar
        }), 200
    except (NameError, AttributeError):
        # 如果模型不存在，返回演示消息
        return jsonify({'message': '头像上传功能暂未实现'}), 501 