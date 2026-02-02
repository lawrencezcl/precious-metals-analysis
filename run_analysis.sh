#!/bin/bash
# 贵金属分析报告自动生成和推送脚本
# 每15分钟运行一次

# 设置工作目录
WORK_DIR="/root/clawd/market_analysis"
cd $WORK_DIR

# 获取当前时间
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$WORK_DIR/logs/analysis_$(date +%Y%m%d).log"

# 创建日志目录
mkdir -p $WORK_DIR/logs

# 记录开始
echo "[$TIMESTAMP] 开始生成贵金属分析报告" >> $LOG_FILE

# 运行分析脚本
python3 $WORK_DIR/market_analyzer.py >> $LOG_FILE 2>&1

# 检查是否成功
if [ $? -eq 0 ]; then
    echo "[$TIMESTAMP] 分析报告生成成功" >> $LOG_FILE
else
    echo "[$TIMESTAMP] 分析报告生成失败" >> $LOG_FILE
fi

# 推送到GitHub（如果配置了remote）
if [ -n "$GITHUB_REPO_URL" ]; then
    cd $WORK_DIR
    git add .
    git commit -m "更新分析报告 - $TIMESTAMP" >> $LOG_FILE 2>&1
    git push origin main >> $LOG_FILE 2>&1
    echo "[$TIMESTAMP] 已推送到GitHub" >> $LOG_FILE
fi

echo "[$TIMESTAMP] 完成" >> $LOG_FILE
