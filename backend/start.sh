#!/bin/bash

# 后端启动脚本
# 用于启动Flask后端应用

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
  if [ ! -f ".env" ]; then
    print_message "环境变量文件不存在，将从示例文件创建..." "${YELLOW}"
    cp .env.example .env
    print_message "已创建环境变量文件: .env" "${GREEN}"
    print_message "请记得更新环境变量文件中的配置！" "${RED}"
  fi
}

# 检查Python版本
check_python_version() {
  # 检查python3命令是否存在
  if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
  elif command -v python &> /dev/null; then
    # 检查python版本是否为3.x
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}' | cut -d. -f1)
    if [ "$PYTHON_VERSION" -ge 3 ]; then
      PYTHON_CMD="python"
    else
      print_message "错误: 需要Python 3.x版本" "${RED}"
      exit 1
    fi
  else
    print_message "错误: 未找到Python" "${RED}"
    exit 1
  fi
  
  print_message "使用Python命令: $PYTHON_CMD" "${BLUE}"
}

# 检查虚拟环境
check_venv() {
  if [ ! -d "venv" ]; then
    print_message "虚拟环境不存在，正在创建..." "${YELLOW}"
    
    # 尝试使用不同的方法创建虚拟环境
    if $PYTHON_CMD -m venv venv 2>/dev/null; then
      print_message "已使用venv模块创建虚拟环境" "${GREEN}"
    elif command -v virtualenv &> /dev/null; then
      virtualenv venv
      print_message "已使用virtualenv创建虚拟环境" "${GREEN}"
    else
      print_message "警告: 无法创建虚拟环境，将使用系统Python" "${YELLOW}"
      return
    fi
  fi
  
  # 激活虚拟环境
  if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    print_message "已激活虚拟环境" "${GREEN}"
  elif [ -f "venv/Scripts/activate" ]; then
    source venv/Scripts/activate
    print_message "已激活虚拟环境" "${GREEN}"
  else
    print_message "警告: 无法找到虚拟环境激活脚本，将使用系统Python" "${YELLOW}"
  fi
}

# 检查依赖
check_dependencies() {
  print_message "检查依赖..." "${BLUE}"
  
  if [ -f "requirements.txt" ]; then
    $PYTHON_CMD -m pip install -r requirements.txt
    print_message "依赖检查完成" "${GREEN}"
  else
    print_message "警告: 未找到requirements.txt文件" "${YELLOW}"
  fi
}

# 检查上传目录
check_upload_dir() {
  if [ ! -d "uploads" ]; then
    print_message "上传目录不存在，正在创建..." "${YELLOW}"
    mkdir -p uploads
    print_message "上传目录已创建" "${GREEN}"
  fi
}

# 启动开发服务器
start_dev_server() {
  print_message "正在启动开发服务器..." "${BLUE}"
  export FLASK_DEBUG=True
  export FLASK_APP=app.py
  $PYTHON_CMD app.py
}

# 启动生产服务器
start_prod_server() {
  print_message "正在启动生产服务器..." "${BLUE}"
  export FLASK_DEBUG=True
  export FLASK_APP=app.py
  
  if command -v gunicorn &> /dev/null; then
    gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app('production')"
  else
    print_message "警告: 未找到gunicorn，将使用Flask内置服务器" "${YELLOW}"
    $PYTHON_CMD app.py
  fi
}

# 启动测试服务器
start_test_server() {
  print_message "正在启动测试服务器..." "${BLUE}"
  export FLASK_ENV=testing
  export FLASK_APP=app.py
  $PYTHON_CMD app.py
}

# 运行测试
run_tests() {
  print_message "正在运行测试..." "${BLUE}"
  
  if command -v pytest &> /dev/null; then
    pytest
  else
    print_message "警告: 未找到pytest，将使用unittest" "${YELLOW}"
    $PYTHON_CMD -m unittest discover
  fi
  
  print_message "测试完成" "${GREEN}"
}

# 显示帮助信息
show_help() {
  print_message "后端启动脚本使用方法:" "${GREEN}"
  print_message "  ./start.sh dev     - 启动开发服务器" "${BLUE}"
  print_message "  ./start.sh prod    - 启动生产服务器" "${BLUE}"
  print_message "  ./start.sh test    - 启动测试服务器" "${BLUE}"
  print_message "  ./start.sh pytest  - 运行测试" "${BLUE}"
  print_message "  ./start.sh help    - 显示帮助信息" "${BLUE}"
}

# 主函数
main() {
  print_message "===== 后端启动脚本 =====" "${GREEN}"
  
  # 检查Python版本
  check_python_version
  
  # 检查环境变量文件
  check_env_file
  
  # 检查虚拟环境
  check_venv
  
  # 检查依赖
  check_dependencies
  
  # 检查上传目录
  check_upload_dir
  
  # 检查命令行参数
  case "$1" in
    "dev" | "")
      start_dev_server
      ;;
    "prod")
      start_prod_server
      ;;
    "test")
      start_test_server
      ;;
    "pytest")
      run_tests
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