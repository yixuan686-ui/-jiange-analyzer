#!/bin/bash

# 健哥竞品分析 - GitHub上传助手

echo "==================================="
echo "  📦 健哥竞品分析 - GitHub上传助手"
echo "==================================="
echo ""

# 检查Git是否安装
if ! command -v git &> /dev/null; then
    echo "❌ 错误: 未找到Git，请先安装Git"
    echo "   下载地址: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git环境检查通过"
echo ""

# 检查是否在正确的目录
if [ ! -f "web_app.py" ]; then
    echo "❌ 错误: 未找到web_app.py文件"
    echo "   请确保在正确的目录运行此脚本"
    exit 1
fi

echo "✅ 项目文件检查通过"
echo ""

# 检查Git仓库
if [ ! -d ".git" ]; then
    echo "📝 初始化Git仓库..."
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ Git仓库已存在"
fi

echo ""

# 检查Git配置
git_user=$(git config user.name)
git_email=$(git config user.email)

if [ -z "$git_user" ]; then
    echo "📝 需要配置Git用户信息"
    read -p "请输入你的GitHub用户名: " git_user
    read -p "请输入你的GitHub邮箱: " git_email
    git config user.name "$git_user"
    git config user.email "$git_email"
    echo "✅ Git用户信息配置完成"
fi

echo ""

# 添加文件
echo "📦 添加文件到Git..."
git add .

# 显示要提交的文件
echo ""
echo "📋 将要提交的文件:"
git status --short

echo ""
read -p "是否继续提交？(y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "❌ 已取消"
    exit 0
fi

# 提交
echo ""
echo "💾 提交更改..."
git commit -m "初始化健哥竞品分析项目"

echo ""
echo "==================================="
echo "  🚀 下一步：上传到GitHub"
echo "==================================="
echo ""
echo "请在GitHub创建仓库，然后执行以下命令："
echo ""
echo "git remote add origin https://github.com/$git_user/jiange-analyzer.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "详细步骤请查看: GITHUB_UPLOAD_GUIDE.md"
echo ""
echo "提示: 如果提示需要密码，输入你的GitHub Personal Access Token"
echo ""
