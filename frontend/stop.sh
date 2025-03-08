#!/bin/bash

# 前端停止脚本
# 用于停止Vue.js前端应用

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
  
  # 查找Vite进程
  VITE_PID=$(ps aux | grep "vite" | grep -v grep | awk '{print $2}')
  
  if [ ! -z "$VITE_PID" ]; then
    kill $VITE_PID
    print_message "已停止Vite进程，PID: $VITE_PID" "${GREEN}"
  else
    print_message "未找到运行中的Vite进程" "${YELLOW}"
  fi
  
  # 查找Node进程
  NODE_PID=$(ps aux | grep "node.*vite" | grep -v grep | awk '{print $2}')
  
  if [ ! -z "$NODE_PID" ]; then
    kill $NODE_PID
    print_message "已停止Node进程，PID: $NODE_PID" "${GREEN}"
  fi
}

# 停止预览服务器
stop_preview_server() {
  print_message "正在停止预览服务器..." "${BLUE}"
  
  # 查找预览服务器进程
  PREVIEW_PID=$(ps aux | grep "vite.*preview" | grep -v grep | awk '{print $2}')
  
  if [ ! -z "$PREVIEW_PID" ]; then
    kill $PREVIEW_PID
    print_message "已停止预览服务器进程，PID: $PREVIEW_PID" "${GREEN}"
  else
    print_message "未找到运行中的预览服务器进程" "${YELLOW}"
  fi
}

# 停止所有相关进程
stop_all() {
  print_message "正在停止所有前端相关进程..." "${BLUE}"
  
  # 停止开发服务器
  stop_dev_server
  
  # 停止预览服务器
  stop_preview_server
  
  print_message "所有前端相关进程已停止" "${GREEN}"
}

# 显示帮助信息
show_help() {
  print_message "前端停止脚本使用方法:" "${GREEN}"
  print_message "  ./stop.sh dev     - 停止开发服务器" "${BLUE}"
  print_message "  ./stop.sh preview - 停止预览服务器" "${BLUE}"
  print_message "  ./stop.sh all     - 停止所有相关进程" "${BLUE}"
  print_message "  ./stop.sh help    - 显示帮助信息" "${BLUE}"
}

# 主函数
main() {
  print_message "===== 前端停止脚本 =====" "${GREEN}"
  
  # 检查命令行参数
  case "$1" in
    "dev")
      stop_dev_server
      ;;
    "preview")
      stop_preview_server
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