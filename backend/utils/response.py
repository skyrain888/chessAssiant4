#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify

def make_response(data=None, message="操作成功", code=200):
    """
    统一响应格式
    
    Args:
        data: 响应数据
        message: 响应消息
        code: 响应状态码
    
    Returns:
        JSON响应
    """
    return jsonify({
        "code": code,
        "message": message,
        "data": data
    }), code 