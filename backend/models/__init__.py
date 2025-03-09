# 模型包初始化文件

# 导入数据库实例，使其可以从models包直接导入
from .db import db, init_db

# 导入模型，使它们对ORM可见
from .user import User
from .chess import ChessNotation 