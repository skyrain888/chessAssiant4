#!/bin/bash

# 前端启动脚本
# 用于启动Vue.js前端应用

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
check_env_file() {
  if [ ! -f ".env.local" ]; then
    print_message "环境变量文件不存在，将从示例文件创建..." "${YELLOW}"
    cp .env.example .env.local
    print_message "已创建环境变量文件: .env.local" "${GREEN}"
    print_message "请记得更新环境变量文件中的配置！" "${RED}"
  fi
}

# 检查依赖
check_dependencies() {
  if [ ! -d "node_modules" ]; then
    print_message "依赖不存在，正在安装..." "${YELLOW}"
    npm install
    print_message "依赖安装完成" "${GREEN}"
  fi
}

# 启动开发服务器
start_dev_server() {
  print_message "正在启动开发服务器..." "${BLUE}"
  npm run dev
}

# 构建生产版本
build_production() {
  print_message "正在构建生产版本..." "${BLUE}"
  npm run build
  print_message "构建完成，输出目录: dist/" "${GREEN}"
}

# 预览生产版本
preview_production() {
  print_message "正在预览生产版本..." "${BLUE}"
  npm run preview
}

# 显示帮助信息
show_help() {
  print_message "前端启动脚本使用方法:" "${GREEN}"
  print_message "  ./start.sh dev     - 启动开发服务器" "${BLUE}"
  print_message "  ./start.sh build   - 构建生产版本" "${BLUE}"
  print_message "  ./start.sh preview - 预览生产版本" "${BLUE}"
  print_message "  ./start.sh help    - 显示帮助信息" "${BLUE}"
}

# 主函数
main() {
  print_message "===== 前端启动脚本 =====" "${GREEN}"
  
  # 检查环境变量文件
  check_env_file
  
  # 检查依赖
  check_dependencies
  
  # 检查命令行参数
  case "$1" in
    "dev" | "")
      start_dev_server
      ;;
    "build")
      build_production
      ;;
    "preview")
      preview_production
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