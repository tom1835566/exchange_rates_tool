
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

def fetch_exchange_rates(url):
    """爬取央行匯率資料"""
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()  # 檢查HTTP錯誤
    except requests.exceptions.RequestException as e:
        print(f"❌ 網路請求失敗: {e}")
        sys.exit(1)  # 立即停止程式，返回錯誤代碼 1

    dateList = []
    exchangeList = []

    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        data = soup.select("table tr")[1:]

        if not data:
            print("❌ 未找到匯率資料,網頁結構可能已改變")
            sys.exit(1)

        for line in data:
            try:
                date = line.find_all("td")[0]
                exchange = line.find_all("td")[1]
                dateList.append(date.text.strip())
                exchangeList.append(float(exchange.text.strip()))
            except (IndexError, ValueError) as e:
                print(f"⚠️  解析資料時發生錯誤: {e}")
                continue

    return dateList[::-1], exchangeList[::-1]

def save_to_csv(dates, rates, filename="exchange_rates.csv"):
    """儲存為CSV檔案"""
    result = pd.DataFrame({
        "日期": dates,
        "匯率": rates,
    })
    result.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"✅ 已儲存至 {filename}")
    return result

def plot_exchange_rate(df, filename="sample_output.png"):
    """繪製匯率走勢圖"""
    plt.figure(figsize=(12, 6))
    plt.plot(df["日期"], df["匯率"], marker="o", linewidth=2, markersize=6)
    plt.title("NTD/USD Exchange Rate Trend (Last 20 Days)", fontsize=16, fontweight='bold')
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Exchange Rate (TWD)", fontsize=12)
    plt.xticks(rotation=45, ha='right') # ha 文字水平對齊方式

    # 動態調整Y軸
    y_min = min(df["匯率"]) - 0.05
    y_max = max(df["匯率"]) + 0.05
    plt.ylim(y_min, y_max)
    plt.yticks(np.arange(round(y_min, 2), round(y_max + 0.05, 2), 0.05))

    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150) # dpi 圖片解析度，每英吋有 n 個像素點，預設為 100
    plt.close()
    print(f"✅ 圖表已儲存至 {filename}")

def main():
    url = "https://www.cbc.gov.tw/tw/lp-645-1.html"
    print("🔍 正在爬取央行匯率資料...")

    dates, rates = fetch_exchange_rates(url)

    if not dates or not rates:
        print("❌ 無有效資料")
        sys.exit(1)

    df = save_to_csv(dates, rates)
    plot_exchange_rate(df)

    print("\n📊 最新匯率資料:")
    print(df.tail(5))  # 只顯示最近5筆
    print(f"\n📈 平均匯率: {df['匯率'].mean():.3f}")
    print(f"📉 最低匯率: {df['匯率'].min():.3f} (於 {df.loc[df['匯率'].idxmin(), '日期']})")
    print(f"📈 最高匯率: {df['匯率'].max():.3f} (於 {df.loc[df['匯率'].idxmax(), '日期']})")

    # 趨勢分析
    if len(rates) >= 5:
        last_rate = rates[-1]
        week_ago_rate = rates[-5]
        change = ((last_rate - week_ago_rate) / week_ago_rate) * 100

        trend = "上漲" if change > 0 else "下跌"
        print(f"\n📊 近期趨勢: 相較5個交易日前{trend} {abs(change):.2f}%")
    else:
        print(f"\n⚠️  資料僅有 {len(rates)} 筆，無法計算趨勢變化")

if __name__ == "__main__":
    main()