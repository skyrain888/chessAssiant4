#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from models import db  # 导入数据库实例

# 加载环境变量
load_dotenv()

def create_app(config_name=None):
    """创建Flask应用实例"""
    app = Flask(__name__)
    
    # 配置应用
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
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
    
    # 初始化CORS，允许所有来源的请求
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    
    # 初始化JWT
    jwt = JWTManager(app)
    
    # 初始化数据库
    db.init_app(app)
    
    # 确保上传目录存在
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # 注册蓝图
    try:
        # 认证蓝图
        from api.auth import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        
        # 用户蓝图
        from api.user import user_bp
        app.register_blueprint(user_bp, url_prefix='/api/user')
        
        # 国际象棋蓝图
        from api.chess import chess_bp
        app.register_blueprint(chess_bp, url_prefix='/api/chess')
    except ImportError:
        # 如果蓝图模块不存在，创建一个简单的路由
        @app.route('/api/health')
        def health_check():
            return jsonify({"status": "ok", "message": "API服务正常运行"})
    
    # 添加CORS预检请求的响应处理
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    
    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Server error"}), 500
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    return app

# 直接运行此文件时执行
if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5001))  # 默认使用5001端口
    app.run(host='0.0.0.0', port=port, debug=True)
