#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from flask import current_app

# 创建SQLAlchemy实例
db = SQLAlchemy()

def init_db(app):
    """初始化数据库"""
    # 初始化SQLAlchemy
    db.init_app(app)
    
    # 创建所有表
    with app.app_context():
        current_app.logger.info("初始化数据库，创建所有表")
        db.create_all()
        
        # 导入模型以确保它们被注册
        from .user import User
        from .chess import ChessNotation
        
        current_app.logger.info("数据库初始化完成") 