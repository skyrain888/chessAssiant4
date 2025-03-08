#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy

# 创建SQLAlchemy实例
db = SQLAlchemy()

def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    
    # 创建所有表
    with app.app_context():
        db.create_all()
        
        # 导入模型以确保它们被注册
        from .user import User
        from .chess import ChessNotation 