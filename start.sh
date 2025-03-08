#!/bin/bash

# 家长助手应用启动脚本
# 用于启动前端和后端服务

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_message() {
  echo -e "${2}${1}${NC}"
}

# 检查环境变量文件
check_env_files() {
  if [ ! -f "frontend/.env.local" ]; then
    print_message "前端环境变量文件不存在，将从示例文件创建..." "${YELLOW}"
    cp frontend/.env.example frontend/.env.local
    print_message "已创建前端环境变量文件: frontend/.env.local" "${GREEN}"
  fi

  if [ ! -f "backend/.env" ]; then
    print_message "后端环境变量文件不存在，将从示例文件创建..." "${YELLOW}"
    cp backend/.env.example backend/.env
    print_message "已创建后端环境变量文件: backend/.env" "${GREEN}"
    print_message "请记得更新环境变量文件中的配置！" "${RED}"
  fi
}

# 启动前端
start_frontend() {
  print_message "正在启动前端服务..." "${BLUE}"
  cd frontend && npm run dev &
  FRONTEND_PID=$!
  echo $FRONTEND_PID > .frontend.pid
  print_message "前端服务已启动，PID: $FRONTEND_PID" "${GREEN}"
  cd ..
}

# 启动后端
start_backend() {
  print_message "正在启动后端服务..." "${BLUE}"
  
  # 检查是否存在Python虚拟环境
  if [ -d "backend/venv" ]; then
    print_message "使用Python虚拟环境..." "${BLUE}"
    if [ -f "backend/venv/bin/activate" ]; then
      source backend/venv/bin/activate
    elif [ -f "backend/venv/Scripts/activate" ]; then
      source backend/venv/Scripts/activate
    fi
  fi
  
  cd backend && python app.py &
  BACKEND_PID=$!
  echo $BACKEND_PID > .backend.pid
  print_message "后端服务已启动，PID: $BACKEND_PID" "${GREEN}"
  cd ..
}

# 主函数
main() {
  print_message "===== 家长助手应用启动脚本 =====" "${GREEN}"
  
  # 检查环境变量文件
  check_env_files
  
  # 检查命令行参数
  if [ "$1" == "frontend" ]; then
    start_frontend
  elif [ "$1" == "backend" ]; then
    start_backend
  else
    # 启动前端和后端
    start_backend
    start_frontend
    
    print_message "===== 所有服务已启动 =====" "${GREEN}"
    print_message "前端地址: http://localhost:5173" "${BLUE}"
    print_message "后端地址: http://localhost:5001" "${BLUE}"
    print_message "使用 ./stop.sh 停止所有服务" "${YELLOW}"
  fi
}

# 执行主函数
main "$@" 