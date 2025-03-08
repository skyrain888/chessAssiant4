#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from . import db

class ChessNotation(db.Model):
    """国际象棋棋谱模型"""
    __tablename__ = 'chess_notations'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    moves = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(256))
    difficulty = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    tags = db.Column(db.JSON, default=list)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, title, moves, description=None, image_url=None, difficulty='beginner', tags=None, user_id=None):
        self.title = title
        self.moves = moves
        self.description = description
        self.image_url = image_url
        self.difficulty = difficulty
        self.tags = tags or []
        self.user_id = user_id
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'moves': self.moves,
            'image_url': self.image_url,
            'difficulty': self.difficulty,
            'tags': self.tags,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<ChessNotation {self.title}>' 