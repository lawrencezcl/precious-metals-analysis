#!/bin/bash
# GitHub配置和推送脚本

# 设置GitHub信息（请替换为您的实际信息）
export GITHUB_USERNAME="your_username"
export GITHUB_TOKEN="your_token"

# 运行分析并推送
cd /root/clawd/market_analysis
python3 realtime_analyzer.py

# 推送到GitHub
echo "推送到GitHub..."
git add .
git commit -m "更新贵金属分析报告 - $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main

echo "完成!"
