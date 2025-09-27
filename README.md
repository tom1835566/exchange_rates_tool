# 匯率查詢小工具

## 📌 專案介紹
本專案提供一個簡單的匯率查詢工具，會自動爬取 **中央銀行公布的 NTD/USD 匯率**，並輸出：
- 📂 CSV 檔（方便後續分析）
- 📊 匯率走勢圖（快速觀察趨勢）

---

## 🚀 功能特色
- 爬取最近 20 筆匯率資料
- 匯出 CSV 檔案 `exchange_rates.csv`
- 繪製折線圖 `sample_output.png`

---

## 🛠 使用套件
- requests  
- BeautifulSoup4  
- pandas  
- matplotlib  

---

## 📥 安裝與執行
```bash
# 下載專案
git clone https://github.com/tom1835566/exchange_rates_tool.git
cd exchange_rates_tool

# 安裝套件
pip install -r requirements.txt

# 執行程式
python main.py

```
---

## 📊 成果展示
- 匯率 CSV 範例
|    日期    |  匯率  |
| :--------: | :----: |
| 2025/09/10 | 30.310 |
| 2025/09/11 | 30.344 |
| 2025/09/12 | 30.246 |


日期	匯率
2025/09/10	30.31
2025-09-11	32.48
2025-09-12	32.51
...	...

- 匯率走勢圖
<img width="1200" height="600" alt="sample_output" src="https://github.com/user-attachments/assets/75c1999b-950b-4a36-8f9e-5ccad35418fa" />

## 🔮 未來改進方向

支援多幣別查詢（如 NTD/EUR, NTD/JPY）
自動排程每日更新
提供 Web 版查詢介面（Flask / FastAPI）

## 👨‍💻 作者
開發者：你的名字 / GitHub ID
聯繫方式：Email 或 LinkedIn（選填）
