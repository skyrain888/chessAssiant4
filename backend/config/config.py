#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from datetime import timedelta

# 获取项目根目录
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class Config:
    """基础配置类"""
    # 应用配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_key')
    DEBUG = False
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///' + os.path.join(basedir, 'parent_assistant.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_dev_key')
    print(f"JWT_SECRET_KEY: {JWT_SECRET_KEY}")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 86400)))  # 默认24小时
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000)))  # 默认30天
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # 上传配置
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(basedir, 'uploads'))
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    
    # AI模型配置
    AI_MODEL = os.getenv('AI_MODEL', 'openai')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL_NAME = os.getenv('GEMINI_MODEL_NAME', 'gemini-pro-vision')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    
    # 国际象棋工具配置
    CHESS_IMAGE_FORMATS = os.getenv('CHESS_IMAGE_FORMATS', 'jpg,jpeg,png').split(',')
    CHESS_MAX_UPLOAD_SIZE = int(os.getenv('CHESS_MAX_UPLOAD_SIZE', 5 * 1024 * 1024))  # 5MB

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    
    # 在生产环境中，应该使用环境变量设置敏感信息
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    
    # 生产环境可以使用更强大的数据库
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

# 配置映射
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    
    # 默认配置
    'default': DevelopmentConfig
}
