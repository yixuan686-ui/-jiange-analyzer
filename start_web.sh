#!/bin/bash

# 健哥竞品分析 - Web应用启动脚本

echo "==================================="
echo "  📊 健哥竞品分析 - 启动中..."
echo "==================================="
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

echo "✅ Python环境检查通过"

# 检查是否安装了依赖
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  检测到未安装依赖，正在安装..."
    pip3 install -r requirements_web.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
    echo "✅ 依赖安装完成"
else
    echo "✅ 依赖检查通过"
fi

# 检查环境变量
if [ -z "$COZE_WORKLOAD_IDENTITY_API_KEY" ]; then
    echo "⚠️  警告: 未设置COZE_WORKLOAD_IDENTITY_API_KEY环境变量"
    echo "   请在 .env 文件中配置API密钥"
fi

# 创建必要的目录
mkdir -p assets

echo ""
echo "==================================="
echo "  🚀 启动Web服务..."
echo "==================================="
echo ""
echo "📝 访问地址: http://localhost:8501"
echo "📋 按 Ctrl+C 停止服务"
echo ""

# 启动Streamlit应用
streamlit run web_app.py --server.port=8501 --server.address=0.0.0.0
