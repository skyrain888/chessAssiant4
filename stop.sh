#!/bin/bash

# 家长助手应用停止脚本
# 用于停止前端和后端服务

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

# 停止前端
stop_frontend() {
  print_message "正在停止前端服务..." "${BLUE}"
  
  if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    if ps -p $FRONTEND_PID > /dev/null; then
      kill $FRONTEND_PID
      print_message "前端服务已停止，PID: $FRONTEND_PID" "${GREEN}"
    else
      print_message "前端服务未运行" "${YELLOW}"
    fi
    rm .frontend.pid
  else
    print_message "找不到前端服务PID文件" "${YELLOW}"
    # 尝试查找并杀死Vite进程
    VITE_PID=$(ps aux | grep "vite" | grep -v grep | awk '{print $2}')
    if [ ! -z "$VITE_PID" ]; then
      kill $VITE_PID
      print_message "已停止Vite进程，PID: $VITE_PID" "${GREEN}"
    fi
  fi
}

# 停止后端
stop_backend() {
  print_message "正在停止后端服务..." "${BLUE}"
  
  if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    if ps -p $BACKEND_PID > /dev/null; then
      kill $BACKEND_PID
      print_message "后端服务已停止，PID: $BACKEND_PID" "${GREEN}"
    else
      print_message "后端服务未运行" "${YELLOW}"
    fi
    rm .backend.pid
  else
    print_message "找不到后端服务PID文件" "${YELLOW}"
    # 尝试查找并杀死Python Flask进程
    FLASK_PID=$(ps aux | grep "python app.py" | grep -v grep | awk '{print $2}')
    if [ ! -z "$FLASK_PID" ]; then
      kill $FLASK_PID
      print_message "已停止Flask进程，PID: $FLASK_PID" "${GREEN}"
    fi
  fi
}

# 主函数
main() {
  print_message "===== 家长助手应用停止脚本 =====" "${GREEN}"
  
  # 检查命令行参数
  if [ "$1" == "frontend" ]; then
    stop_frontend
  elif [ "$1" == "backend" ]; then
    stop_backend
  else
    # 停止前端和后端
    stop_frontend
    stop_backend
    
    print_message "===== 所有服务已停止 =====" "${GREEN}"
  fi
}

# 执行主函数
main "$@" 