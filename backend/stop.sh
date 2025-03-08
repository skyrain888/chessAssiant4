#!/bin/bash

# 后端停止脚本
# 用于停止Flask后端应用

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

# 停止开发服务器
stop_dev_server() {
  print_message "正在停止开发服务器..." "${BLUE}"
  
  # 查找Python进程
  FLASK_PID=$(ps aux | grep "python app.py" | grep -v grep | awk '{print $2}')
  
  if [ ! -z "$FLASK_PID" ]; then
    kill $FLASK_PID
    print_message "已停止Flask进程，PID: $FLASK_PID" "${GREEN}"
  else
    print_message "未找到运行中的Flask进程" "${YELLOW}"
  fi
}

# 停止生产服务器
stop_prod_server() {
  print_message "正在停止生产服务器..." "${BLUE}"
  
  # 查找Gunicorn进程
  GUNICORN_PID=$(ps aux | grep "gunicorn.*app:create_app" | grep -v grep | awk '{print $2}')
  
  if [ ! -z "$GUNICORN_PID" ]; then
    kill $GUNICORN_PID
    print_message "已停止Gunicorn主进程，PID: $GUNICORN_PID" "${GREEN}"
    
    # 查找Gunicorn工作进程
    WORKER_PIDS=$(ps aux | grep "gunicorn: worker" | grep -v grep | awk '{print $2}')
    
    if [ ! -z "$WORKER_PIDS" ]; then
      for pid in $WORKER_PIDS; do
        kill $pid
        print_message "已停止Gunicorn工作进程，PID: $pid" "${GREEN}"
      done
    fi
  else
    print_message "未找到运行中的Gunicorn进程" "${YELLOW}"
  fi
}

# 停止所有相关进程
stop_all() {
  print_message "正在停止所有后端相关进程..." "${BLUE}"
  
  # 停止开发服务器
  stop_dev_server
  
  # 停止生产服务器
  stop_prod_server
  
  # 查找所有Python进程
  PYTHON_PIDS=$(ps aux | grep "python.*app.py" | grep -v grep | awk '{print $2}')
  
  if [ ! -z "$PYTHON_PIDS" ]; then
    for pid in $PYTHON_PIDS; do
      kill $pid
      print_message "已停止Python进程，PID: $pid" "${GREEN}"
    done
  fi
  
  print_message "所有后端相关进程已停止" "${GREEN}"
}

# 显示帮助信息
show_help() {
  print_message "后端停止脚本使用方法:" "${GREEN}"
  print_message "  ./stop.sh dev     - 停止开发服务器" "${BLUE}"
  print_message "  ./stop.sh prod    - 停止生产服务器" "${BLUE}"
  print_message "  ./stop.sh all     - 停止所有相关进程" "${BLUE}"
  print_message "  ./stop.sh help    - 显示帮助信息" "${BLUE}"
}

# 主函数
main() {
  print_message "===== 后端停止脚本 =====" "${GREEN}"
  
  # 检查命令行参数
  case "$1" in
    "dev")
      stop_dev_server
      ;;
    "prod")
      stop_prod_server
      ;;
    "all" | "")
      stop_all
      ;;
    "help" | "-h" | "--help")
      show_help
      ;;
    *)
      print_message "未知命令: $1" "${RED}"
      show_help
      exit 1
      ;;
  esac
}

# 执行主函数
main "$@" 