#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, get_jwt
)
from datetime import timedelta
from werkzeug.security import check_password_hash

from models import db
from models.user import User
from utils.response import make_response

# 创建蓝图
auth_bp = Blueprint('auth', __name__)

# 导入模型
try:
    from models.user import User
except ImportError:
    # 如果模型不存在，创建一个简单的用户字典用于演示
    USERS = {
        'admin@example.com': {
            'id': 1,
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'pbkdf2:sha256:260000$rqT0bWnTKz1Qs$627f77c4940d0f2ce9fb7439b9f486c6429e9927d456d9cad6b4e8254d3a3f5b',  # 'password'
            'name': '管理员',
            'avatar': None,
            'created_at': timedelta(days=1),
            'updated_at': timedelta(days=1)
        }
    }

# 路由：用户注册
@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    if not data:
        return jsonify({'message': '无效的请求数据'}), 400
    
    # 验证必填字段
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'缺少必填字段: {field}'}), 400
    
    try:
        # 检查用户名和邮箱是否已存在
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': '用户名已存在'}), 409
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': '邮箱已存在'}), 409
        
        # 创建新用户
        new_user = User(
            username=data['username'],
            email=data['email'],
            name=data.get('name', data['username']),
            avatar=data.get('avatar')
        )
        new_user.set_password(data['password'])
        
        # 保存到数据库
        db.session.add(new_user)
        db.session.commit()
        
        # 创建令牌
        access_token = create_access_token(identity=new_user.id)
        refresh_token = create_refresh_token(identity=new_user.id)
        
        return jsonify({
            'message': '注册成功',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'name': new_user.name,
                'avatar': new_user.avatar
            }
        }), 201
    except (NameError, AttributeError):
        # 如果模型不存在，返回演示消息
        return jsonify({'message': '注册功能暂未实现'}), 501

# 路由：用户登录
@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': '请提供邮箱和密码'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    try:
        # 查询用户
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'message': '邮箱或密码错误'}), 401
        
        # 创建访问令牌和刷新令牌，确保将用户ID转换为字符串
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        current_app.logger.info(f"用户登录成功，用户ID: {user.id}, 邮箱: {user.email}")
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.name,
                'avatar': user.avatar
            }
        }), 200
    except (NameError, AttributeError):
        # 如果模型不存在，使用演示用户
        if email in USERS and check_password_hash(USERS[email]['password'], password):
            user = USERS[email]
            # 确保将用户ID转换为字符串
            access_token = create_access_token(identity=str(user['id']))
            refresh_token = create_refresh_token(identity=str(user['id']))
            
            current_app.logger.info(f"演示用户登录成功，用户ID: {user['id']}, 邮箱: {user['email']}")
            
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'name': user['name'],
                    'avatar': user['avatar']
                }
            }), 200
        else:
            return jsonify({'message': '邮箱或密码错误'}), 401

# 路由：刷新令牌
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新访问令牌"""
    current_user_id = get_jwt_identity()
    current_app.logger.info(f"刷新令牌请求，用户ID: {current_user_id}")
    
    # 记录请求头和请求体
    auth_header = request.headers.get('Authorization', '')
    current_app.logger.debug(f"Authorization头: {auth_header}")
    current_app.logger.debug(f"请求体: {request.get_json()}")
    
    try:
        # 创建新的访问令牌，确保用户ID是字符串
        # 如果current_user_id已经是字符串，这一步不会有变化
        # 如果是数字，则会转换为字符串
        access_token = create_access_token(identity=str(current_user_id))
        current_app.logger.info(f"访问令牌刷新成功，用户ID: {current_user_id}")
        
        # 返回新的访问令牌
        response_data = {
            'access_token': access_token
        }
        current_app.logger.debug(f"响应数据: {response_data}")
        
        return make_response(response_data)
    except Exception as e:
        current_app.logger.error(f"刷新令牌失败: {str(e)}")
        return make_response(None, f"刷新令牌失败: {str(e)}", 500)

# 路由：获取当前用户信息
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    current_app.logger.info(f"获取当前用户信息，用户ID: {current_user_id}, 类型: {type(current_user_id)}")
    
    try:
        # 确保用户ID是整数
        user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        user = User.query.get(user_id)
        
        if not user:
            current_app.logger.warning(f"用户不存在，ID: {current_user_id}")
            return make_response(None, "用户不存在", 404)
        
        current_app.logger.info(f"成功获取当前用户信息，用户ID: {current_user_id}")
        return make_response(user.to_dict())
    except ValueError as e:
        current_app.logger.error(f"用户ID格式错误: {current_user_id}, 错误: {str(e)}")
        return make_response(None, f"用户ID格式错误", 400)
    except Exception as e:
        current_app.logger.error(f"获取当前用户信息失败: {str(e)}")
        return make_response(None, f"获取当前用户信息失败: {str(e)}", 500)

# 路由：修改密码
@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    current_app.logger.info(f"修改密码请求，用户ID: {current_user_id}, 类型: {type(current_user_id)}")
    
    try:
        # 确保用户ID是整数
        user_id = int(current_user_id) if isinstance(current_user_id, str) else current_user_id
        user = User.query.get(user_id)
        
        if not user:
            current_app.logger.warning(f"用户不存在，ID: {current_user_id}")
            return make_response(None, "用户不存在", 404)
        
        data = request.json
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not old_password or not new_password:
            current_app.logger.warning("旧密码或新密码为空")
            return make_response(None, "旧密码和新密码不能为空", 400)
        
        # 验证旧密码
        if not user.verify_password(old_password):
            current_app.logger.warning(f"旧密码验证失败，用户ID: {current_user_id}")
            return make_response(None, "旧密码错误", 401)
        
        try:
            # 更新密码
            user.password = new_password
            db.session.commit()
            current_app.logger.info(f"密码修改成功，用户ID: {current_user_id}")
            
            return make_response(None, "密码修改成功")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"修改密码失败: {str(e)}")
            return make_response(None, f"修改密码失败: {str(e)}", 500)
    except ValueError as e:
        current_app.logger.error(f"用户ID格式错误: {current_user_id}, 错误: {str(e)}")
        return make_response(None, f"用户ID格式错误", 400)
    except Exception as e:
        current_app.logger.error(f"修改密码请求处理失败: {str(e)}")
        return make_response(None, f"修改密码失败: {str(e)}", 500)

# 路由：忘记密码（发送重置邮件）
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """忘记密码"""
    data = request.get_json()
    
    if not data or not data.get('email'):
        return jsonify({'message': '请提供邮箱地址'}), 400
    
    # 在实际应用中，应该发送重置密码的邮件
    return jsonify({'message': '如果邮箱存在，重置密码的链接已发送'}), 200

# 路由：重置密码
@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """重置密码"""
    data = request.get_json()
    
    if not data or not data.get('token') or not data.get('password'):
        return jsonify({'message': '请提供重置令牌和新密码'}), 400
    
    # 在实际应用中，应该验证令牌并更新密码
    return jsonify({'message': '密码重置成功'}), 200

# 路由：注销
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """用户注销"""
    current_user_id = get_jwt_identity()
    current_app.logger.info(f"用户注销请求，用户ID: {current_user_id}, 类型: {type(current_user_id)}")
    
    # 这里可以添加令牌到黑名单的逻辑
    # 例如：jti = get_jwt()['jti']
    # 将jti添加到黑名单数据库中
    
    return make_response(None, "注销成功") 