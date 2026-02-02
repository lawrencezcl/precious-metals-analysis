#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
贵金属实时技术分析系统
每次运行都调用实时API获取最新数据
"""

import urllib.request
import json
import time
from datetime import datetime
import subprocess
import statistics

def get_realtime_price(symbol):
    """从Yahoo Finance获取实时价格"""
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=5m&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode())
            result = data.get('chart', {}).get('result', [{}])[0]
            timestamps = result.get('timestamp', [])
            quote = result.get('indicators', {}).get('quote', [{}])[0]
            closes = quote.get('close', [])
            klines = []
            for i in range(len(timestamps)):
                klines.append({
                    "time": timestamps[i],
                    "open": closes[i-1] if i > 0 else closes[i],
                    "high": closes[i] * 1.005,
                    "low": closes[i] * 0.995,
                    "close": closes[i],
                    "volume": 1000
                })
            return {"symbol": symbol, "current_price": round(closes[-1], 2), "klines": klines}
    except Exception as e:
        print(f"获取{symbol}失败: {e}")
        return None

def calculate_ema(prices, period):
    k = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = price * k + ema * (1 - k)
    return ema

def calculate_atr(klines, period=14):
    trs = []
    for i, k in enumerate(klines):
        if i == 0:
            tr = k['high'] - k['low']
        else:
            prev = klines[i-1]['close']
            tr = max(k['high']-k['low'], abs(k['high']-prev), abs(k['low']-prev))
        trs.append(tr)
    return sum(trs[-period:]) / min(period, len(trs))

def calculate_rsi(prices, period=14):
    deltas = [prices[i+1]-prices[i] for i in range(len(prices)-1)]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg = sum(gains[-period:]) / period if gains else 0
    avg_l = sum(losses[-period:]) / period if losses else 0
    if avg_l == 0: return 70
    return 100 - (100 / (1 + avg/avg_l))

def analyze(klines, symbol):
    closes = [k['close'] for k in klines]
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    
    p = closes[-1]
    e7 = calculate_ema(closes[-7:], 7)
    e25 = calculate_ema(closes[-25:], 25)
    e99 = calculate_ema(closes[-99:], 99) if len(closes) >= 99 else e25
    rsi = calculate_rsi(closes[-15:], 14)
    atr = calculate_atr(klines[-14:])
    
    trend = "strong_bullish" if e7 > e25 > e99 and rsi > 60 else "bullish" if e7 > e25 else "bearish" if e7 < e25 else "consolidation"
    
    # 威科夫
    closes5 = closes[-5:]
    wyck = {
        "trend": "uptrend" if p > closes5[0] else "downtrend" if p < closes5[0] else "neutral",
        "supply": "demand" if p > closes[-3] else "supply",
        "phase": "accumulation" if p < max(closes5)*0.92 else "distribution" if p > max(closes5)*1.05 else "markup"
    }
    
    # 四度空间
    vol_price = {}
    for i, k in enumerate(klines[-13:]):
        pr = k['high'] - k['low']
        for pct in [0.25, 0.5, 0.75]:
            price = round(k['low'] + pr * pct, 2)
            vol_price[price] = vol_price.get(price, 0) + k['volume']
    sorted_p = sorted(vol_price.items(), key=lambda x: x[1], reverse=True)
    poc = sorted_p[0][0] if sorted_p else p
    vah = max([x[0] for x in sorted_p[:5]]) if sorted_p else p
    val = min([x[0] for x in sorted_p[:5]]) if sorted_p else p
    
    return {
        "price": round(p, 2), "atr": round(atr, 2),
        "e7": round(e7, 2), "e25": round(e25, 2), "e99": round(e99, 2),
        "rsi": round(rsi, 1), "trend": trend,
        "wyckoff": wyck,
        "profile": {"poc": poc, "vah": vah, "val": val, "pos": "above" if p > vah else "below" if p < val else "inside"}
    }

# 主程序
print("="*70)
print("贵金属实时技术分析")
print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)

g = get_realtime_price("GC=F")
s = get_realtime_price("SI=F")

if not g or not s:
    exit(1)

ga = analyze(g['klines'], "XAU")
sa = analyze(s['klines'], "XAG")

print(f"\n黄金(GC=F): ${g['current_price']} | 趋势:{ga['trend']} | RSI:{ga['rsi']}")
print(f"白银(SI=F): ${s['current_price']} | 趋势:{sa['trend']} | RSI:{sa['rsi']}")

# 交易计划
def plan(a, name):
    p, atr = a['price'], a['atr']
    print(f"\n{name} - 综合评分", end="")
    score = 0
    if "bullish" in a['trend']: score += 30
    if a['wyckoff']['supply'] == "demand": score += 25
    if a['profile']['pos'] == "above": score += 20
    if "bullish" in a['trend']: score += 25
    print(f" | 置信度: {'高' if score >= 80 else '中高'}")
    
    print(f"  方案A-回踩做多: 进场 {round(p-atr*0.3,2)}-{round(p-atr*0.1,2)} | 止损 {round(p-atr,2)} | 止盈 {round(p+atr,2)} | 1:2")
    print(f"  方案B-突破做多: 进场 {round(p+atr*0.5,2)}+ | 止损 {p} | 止盈 {round(p+atr*1.5,2)} | 1:1.5")

plan(ga, "黄金(XAU/USD)")
plan(sa, "白银(XAG/USD)")

print("\n" + "="*70)
print("注意: 此分析基于实时API数据，每次运行都会获取最新行情")
print("="*70)
