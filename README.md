# 贵金属技术分析自动报告系统

自动生成国际黄金(XAU/USD)和国际白银(XAG/USD)的短线技术分析报告，并推送到GitHub仓库。

## 功能特点

- 自动获取实时贵金属价格
- 1分钟和5分钟K线技术分析
- 自动计算关键支撑阻力位
- 生成可执行的交易计划
- 每15分钟自动更新
- 自动推送到GitHub仓库

## 文件结构

```
market_analysis/
├── market_analyzer.py    # 主分析脚本
├── run_analysis.sh       # 定时任务脚本
├── init_github.sh        # GitHub初始化脚本
├── README.md            # 说明文档
├── logs/                # 日志目录
├── XAU_USD_*.md         # 黄金分析报告
├── XAG_USD_*.md         # 白银分析报告
└── XAU_USD_*.json       # 黄金原始数据
└── XAG_USD_*.json       # 白银原始数据
```

## 报告内容

每份报告包含:
- 核心指标摘要
- 1分钟K线分析（趋势、EMA、布林带、RSI）
- 5分钟K线分析（趋势、EMA排列、RSI、MACD）
- 关键支撑阻力位
- 枢轴点分析
- 交易计划（回踩做多、突破做多）
- 执行要点

## 快速开始

### 1. 运行单次分析

```bash
cd /root/clawd/market_analysis
python3 market_analyzer.py
```

### 2. 初始化GitHub仓库

```bash
export GITHUB_USERNAME="your_username"
export GITHUB_TOKEN="your_token"
bash init_github.sh
```

### 3. 设置定时任务（自动每15分钟运行）

```bash
# 定时任务已自动设置，可通过以下命令查看
crontab -l
```

## 环境要求

- Python 3.6+
- git
- curl

## 数据来源

价格数据来自公开API，包括:
- Open Exchange Rates API
- Metals-API
- 备用默认数据

## 免责声明

本报告由自动化系统生成，仅供参考，不构成投资建议。投资有风险，交易需谨慎。

## 许可证

MIT License
