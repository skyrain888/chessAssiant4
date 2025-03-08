# 家长助手应用

家长助手是一个面向学生家长的工具集合平台，提供多种实用工具，帮助家长更好地辅导孩子学习。目前已实现国际象棋工具模块，支持棋谱上传、识别、查看和练习功能。

## 技术栈

### 前端
- Vue.js 3 + TypeScript
- Arco Design Vue 组件库
- Pinia 状态管理
- Vue Router 路由管理
- Axios HTTP请求
- Tailwind CSS 样式

### 后端
- Python + Flask
- SQLAlchemy ORM
- JWT 认证
- OpenAI/Gemini/Claude API 集成

## 功能特点

1. **用户管理**
   - 用户注册、登录、个人信息管理
   - JWT认证和授权

2. **国际象棋工具**
   - 棋谱上传与AI识别
   - 棋谱列表管理
   - 棋谱查看与分析
   - 棋谱练习与进度跟踪

## 快速开始

### 环境要求
- Node.js 16+
- Python 3.8+
- npm 或 yarn

### 安装依赖

1. 克隆仓库
```bash
git clone https://github.com/yourusername/parent-assistant.git
cd parent-assistant
```

2. 安装所有依赖
```bash
npm run install:all
```

### 配置环境变量

1. 前端配置
```bash
cp frontend/.env.example frontend/.env.local
```

2. 后端配置
```bash
cp backend/.env.example backend/.env
```

根据需要修改环境变量文件中的配置。

### 使用启停脚本

项目提供了一系列启停脚本，方便开发和部署：

#### 根目录脚本

1. 启动所有服务
```bash
./start.sh
```

2. 只启动前端
```bash
./start.sh frontend
```

3. 只启动后端
```bash
./start.sh backend
```

4. 停止所有服务
```bash
./stop.sh
```

#### 前端脚本

1. 启动开发服务器
```bash
cd frontend
./start.sh dev
```

2. 构建生产版本
```bash
cd frontend
./start.sh build
```

3. 预览生产版本
```bash
cd frontend
./start.sh preview
```

4. 停止前端服务
```bash
cd frontend
./stop.sh
```

#### 后端脚本

1. 启动开发服务器
```bash
cd backend
./start.sh dev
```

2. 启动生产服务器
```bash
cd backend
./start.sh prod
```

3. 运行测试
```bash
cd backend
./start.sh pytest
```

4. 停止后端服务
```bash
cd backend
./stop.sh
```

### 使用npm脚本

您也可以使用package.json中定义的npm脚本：

1. 启动前端和后端
```bash
npm run dev
```

2. 仅启动前端
```bash
npm run frontend:dev
```

3. 仅启动后端
```bash
npm run backend:dev
```

### 构建生产版本

```bash
npm run frontend:build
```

## 项目结构

```
parent-assistant/
├── frontend/                # 前端代码
│   ├── public/              # 静态资源
│   ├── src/                 # 源代码
│   │   ├── assets/          # 资源文件
│   │   ├── components/      # 组件
│   │   ├── composables/     # 组合式API
│   │   ├── config/          # 配置
│   │   ├── layouts/         # 布局组件
│   │   ├── router/          # 路由
│   │   ├── stores/          # 状态管理
│   │   ├── types/           # 类型定义
│   │   ├── utils/           # 工具函数
│   │   └── views/           # 页面
│   ├── .env.example         # 环境变量示例
│   └── package.json         # 前端依赖
│
├── backend/                 # 后端代码
│   ├── api/                 # API蓝图
│   ├── config/              # 配置
│   ├── models/              # 数据模型
│   ├── utils/               # 工具函数
│   ├── uploads/             # 上传文件目录
│   ├── app.py               # 应用入口
│   ├── .env.example         # 环境变量示例
│   └── requirements.txt     # 后端依赖
│
├── package.json             # 项目脚本
└── README.md                # 项目说明
```

## 开发指南

### 添加新工具

1. 在 `frontend/src/views/tools/` 目录下创建新工具的页面组件
2. 在 `frontend/src/router/index.ts` 中添加新工具的路由
3. 在 `backend/api/` 目录下创建新工具的API蓝图
4. 在 `backend/app.py` 中注册新工具的蓝图

## 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT 

## 启停脚本总结

为了方便项目的开发和部署，我们创建了一系列启停脚本：

### 根目录脚本

1. **start.sh**：
   - 启动前端和后端服务
   - 支持单独启动前端或后端
   - 自动检查环境变量文件，如果不存在则从示例文件创建
   - 记录进程ID，方便后续停止

2. **stop.sh**：
   - 停止前端和后端服务
   - 支持单独停止前端或后端
   - 通过进程ID文件或进程名查找并终止进程

### 前端脚本

1. **frontend/start.sh**：
   - 启动开发服务器（默认）
   - 构建生产版本
   - 预览生产版本
   - 自动检查环境变量文件和依赖
   - 提供帮助信息

2. **frontend/stop.sh**：
   - 停止开发服务器
   - 停止预览服务器
   - 停止所有前端相关进程
   - 提供帮助信息

### 后端脚本

1. **backend/start.sh**：
   - 启动开发服务器（默认）
   - 启动生产服务器（使用Gunicorn）
   - 启动测试服务器
   - 运行测试
   - 自动检查环境变量文件、虚拟环境、依赖和上传目录
   - 提供帮助信息

2. **backend/stop.sh**：
   - 停止开发服务器
   - 停止生产服务器（包括Gunicorn主进程和工作进程）
   - 停止所有后端相关进程
   - 提供帮助信息

### 脚本特点

1. **彩色输出**：
   - 使用ANSI颜色代码使输出更加友好
   - 不同类型的消息使用不同颜色（成功、警告、错误等）

2. **自动检查**：
   - 检查环境变量文件，如果不存在则自动创建
   - 检查依赖是否安装
   - 检查必要的目录是否存在

3. **灵活的命令行参数**：
   - 支持不同的启动模式（开发、生产、测试等）
   - 提供帮助信息

4. **进程管理**：
   - 记录进程ID，方便后续停止
   - 多种方式查找进程（PID文件、进程名） 