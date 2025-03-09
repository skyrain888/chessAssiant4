#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity
from dotenv import load_dotenv
from models.db import db, init_db  # 导入数据库实例和初始化函数

# 加载环境变量
load_dotenv()

def create_app(config_name=None):
    """创建Flask应用实例"""
    app = Flask(__name__)
    
    # 配置应用
    if config_name is None:
        # 使用 FLASK_DEBUG 代替已弃用的 FLASK_ENV
        debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
        config_name = 'development' if debug_mode else 'production'
    
    # 从config模块导入配置
    try:
        from config.config import config
        app.config.from_object(config[config_name])
    except (ImportError, KeyError):
        # 如果配置模块不存在，使用基本配置
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')
        app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt_dev_key')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///parent_assistant.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
    
    # 配置日志
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    app.logger.setLevel(log_level)
    app.logger.info(f"应用启动，环境: {config_name}, 日志级别: {logging.getLevelName(log_level)}")
    
    # 初始化CORS，允许所有来源的请求
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # 配置JWT
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
    
    # JWT加载回调
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        app.logger.debug(f"JWT用户查找回调: {jwt_data}")
        return jwt_data["sub"]
    
    # JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.warning(f"JWT令牌已过期: {jwt_payload}")
        return jsonify({"code": 401, "message": "令牌已过期，请重新登录"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        app.logger.warning(f"无效的JWT令牌: {error_string}")
        return jsonify({"code": 401, "message": "无效的令牌"}), 401
    
    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        app.logger.warning(f"未授权的请求: {error_string}")
        return jsonify({"code": 401, "message": "缺少令牌"}), 401
    
    @jwt.token_verification_failed_loader
    def verification_failed_callback():
        app.logger.warning("令牌验证失败")
        return jsonify({"code": 401, "message": "令牌验证失败"}), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        app.logger.warning(f"已撤销的令牌: {jwt_payload}")
        return jsonify({"code": 401, "message": "令牌已被撤销"}), 401
    
    # 初始化数据库
    init_db(app)
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 注册蓝图
    try:
        # 认证蓝图
        from api.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        
        # 国际象棋蓝图
        from api.chess import chess_bp
        app.register_blueprint(chess_bp, url_prefix='/api/chess')
        
        # 用户蓝图
        from api.user import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/user')
        
    except ImportError as e:
        # 如果蓝图模块不存在，创建一个简单的路由
        app.logger.error(f"注册蓝图失败: {str(e)}")
        @app.route('/api/health')
        def health_check():
            return jsonify({"status": "ok", "message": "API服务正常运行"})
    
    # 添加请求日志中间件
    @app.before_request
    def log_request_info():
        app.logger.debug('请求头: %s', request.headers)
        app.logger.debug('请求方法: %s, 路径: %s', request.method, request.path)
        if request.is_json:
            app.logger.debug('请求JSON: %s', request.json)
    
    # 添加CORS预检请求的响应处理
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        app.logger.debug('响应状态: %s', response.status)
        app.logger.debug('响应头: %s', response.headers)
        return response
    
    # 注册错误处理器
    register_error_handlers(app)
    
    return app

def register_error_handlers(app):
    """注册错误处理器"""
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'code': 404,
            'message': '请求的资源不存在'
        }), 404
    
    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'code': 500,
            'message': '服务器内部错误'
        }), 500

# 直接运行此文件时执行
if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5001))  # 默认使用5001端口
    app.run(host='0.0.0.0', port=port, debug=True)
