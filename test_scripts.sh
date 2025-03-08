#!/bin/bash

# 测试脚本
echo "测试启停脚本"
echo "============"

# 测试后端启动脚本
echo "测试后端启动脚本..."
cd backend
chmod +x start.sh
./start.sh &
BACKEND_PID=$!
sleep 2
echo "后端启动脚本测试完成"

# 测试后端停止脚本
echo "测试后端停止脚本..."
chmod +x stop.sh
./stop.sh
echo "后端停止脚本测试完成"

cd ..

# 测试前端启动脚本
echo "测试前端启动脚本..."
cd frontend
chmod +x start.sh
./start.sh &
FRONTEND_PID=$!
sleep 2
echo "前端启动脚本测试完成"

# 测试前端停止脚本
echo "测试前端停止脚本..."
chmod +x stop.sh
./stop.sh
echo "前端停止脚本测试完成"

cd ..

# 测试根目录启动脚本
echo "测试根目录启动脚本..."
chmod +x start.sh
./start.sh &
ROOT_PID=$!
sleep 2
echo "根目录启动脚本测试完成"

# 测试根目录停止脚本
echo "测试根目录停止脚本..."
chmod +x stop.sh
./stop.sh
echo "根目录停止脚本测试完成"

echo "所有测试完成" 