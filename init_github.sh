#!/bin/bash
# GitHub仓库初始化脚本
# 用于创建新的GitHub仓库并推送本地文件

REPO_NAME="precious-metals-analysis"
GITHUB_USERNAME="${GITHUB_USERNAME:-}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

# 检查参数
if [ -z "$GITHUB_USERNAME" ]; then
    echo "请设置环境变量: export GITHUB_USERNAME='your_username'"
    echo "可选: export GITHUB_TOKEN='your_token'"
    exit 1
fi

WORK_DIR="/root/clawd/market_analysis"
cd $WORK_DIR

# 初始化git仓库
echo "初始化Git仓库..."
git init
git add .
git commit -m "初始化贵金属分析报告仓库"

# 创建GitHub仓库（使用API）
echo "创建GitHub仓库..."
if [ -n "$GITHUB_TOKEN" ]; then
    curl -u "$GITHUB_USERNAME:$GITHUB_TOKEN" \
        https://api.github.com/user/repos \
        -d '{"name":"'$REPO_NAME'","description":"Precious Metals Technical Analysis Reports","private":false}'
    
    # 添加remote并推送
    git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
    git push -u origin main
    
    echo "仓库创建成功: https://github.com/$GITHUB_USERNAME/$REPO_NAME"
else
    echo "未设置GITHUB_TOKEN，仅初始化本地仓库"
    echo "请手动创建GitHub仓库并推送"
fi
