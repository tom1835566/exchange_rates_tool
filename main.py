
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 央行 NTD/USD 收盤匯率(16:00 ~ 17:00 更新當日匯率)，顯示目前近20筆匯率
url = "https://www.cbc.gov.tw/tw/lp-645-1.html"

r = requests.get(url)

dateList = []
exchangeList = []

if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")
    data = soup.select("table tr")[1:]
    for line in data:
        date = line.find_all("td")[0]
        exchange = line.find_all("td")[1]
        dateList.append(date.text)
        exchangeList.append(float(exchange.text))

result = pd.DataFrame({
    "日期": dateList[::-1],
    "匯率": exchangeList[::-1],
})

# Save to CSV
result.to_csv("exchange_rates.csv", index=False, encoding="utf-8-sig")

# Create and save plot
plt.figure(figsize=(12, 6))
plt.plot(result["日期"], result["匯率"], marker="o")
plt.title("NTD/USD Exchange Rate Trend (Last 20 Days)")
plt.xlabel("Date")
plt.ylabel("Exchange Rate")
plt.xticks(rotation=45)
y_min = min(result["匯率"]) - 0.05
y_max = max(result["匯率"]) + 0.05
plt.ylim(y_min, y_max)
plt.yticks(np.arange(round(y_min, 2), round(y_max + 0.05, 2), 0.05))  # 0.05 intervals
plt.grid(True)
plt.tight_layout()
plt.savefig("sample_output.png")
plt.close()

print(result)
