# 模型包初始化文件

from flask_sqlalchemy import SQLAlchemy

# 创建SQLAlchemy实例
db = SQLAlchemy()

# 导入模型，使它们对ORM可见
from .user import User
from .chess import ChessNotation 