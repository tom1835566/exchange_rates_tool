# 匯率查詢小工具

## 📌 專案介紹
本專案提供一個簡單的匯率查詢工具，會自動爬取 **中央銀行公布的 NTD/USD 匯率**，並輸出：
- 📂 CSV 檔（方便後續分析）
- 📊 匯率走勢圖（快速觀察趨勢）

---

## 💡 開發動機
作為經常關注國際市場的研究人員,我發現:
- 央行網站資料不易追蹤歷史趨勢
- 需要手動複製貼上才能做進一步分析
- 缺乏視覺化工具快速判斷匯率波動

因此開發了這個自動化工具,**10秒內**就能獲得近20日匯率數據與趨勢圖。

---

## 🚀 功能特色
- ✅ 自動爬取最近 20 筆匯率
- ✅ 匯出 CSV 檔案
- ✅ 動態產生趨勢圖
- ✅ 自動計算統計數據(平均/最高/最低)
- ✅ 錯誤處理機制
- ✅ 匯率變化分析(與一週前比較)
- ✅ 換匯時機提醒

---

## 🤔 技術選擇考量
- **為何選擇爬蟲而非API?**
  央行未提供公開API,因此採用BeautifulSoup解析HTML表格資料
- **為何使用 pandas?**
  方便後續擴充為時間序列分析
- **圖表為何選matplotlib?**
  輕量、可客製化程度高,適合快速產出靜態圖表

---

## 🛠 使用技術
- **Python 3.8+**
- **requests** - HTTP 請求
- **BeautifulSoup4** - HTML 解析
- **pandas** - 資料處理
- **matplotlib** - 資料視覺化
- **pytest** - 單元測試

---

## 📥 安裝與執行

### 方法一:使用 pip
```bash
# 1. Clone 專案
git clone https://github.com/tom1835566/exchange_rates_tool.git
cd exchange_rates_tool

# 2. 安裝相依套件
pip install -r requirements.txt

# 3. 執行程式
python main.py
```

### 方法二:使用虛擬環境(推薦)
```bash
# 1. Clone 專案
git clone https://github.com/tom1835566/exchange_rates_tool.git
cd exchange_rates_tool

# 2. 建立虛擬環境
python -m venv venv

# 3. 啟動虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安裝相依套件
pip install -r requirements.txt

# 5. 執行程式
python main.py
```

---

## 🧪 執行測試
```bash
# 安裝測試套件
pip install pytest

# 執行單元測試
pytest test_main.py -v
```

測試涵蓋：
- ✅ 正常資料爬取流程
- ✅ 網路錯誤處理
- ✅ 空資料表處理

---

## 🐛 開發過程中遇到的問題

### 問題1: 資料順序錯誤
**現象**: 爬取的資料是由新到舊,但繪圖需要由舊到新
**解決**: 使用 `[::-1]` 反轉串列順序

### 問題2: Y軸刻度過於密集
**現象**: 匯率變化幅度小(如30.2~30.4),預設刻度不易觀察
**解決**:
```python
y_min = min(result["匯率"]) - 0.05
y_max = max(result["匯率"]) + 0.05
plt.yticks(np.arange(round(y_min, 2), round(y_max + 0.05, 2), 0.05))
```
動態調整Y軸範圍與間距,讓趨勢更明顯

### 問題3: 中文檔名在某些系統會亂碼
**現象**: Windows與Mac對中文編碼處理不同,CSV可能出現亂碼
**解決**: CSV存檔時加入 `encoding="utf-8-sig"` 確保跨平台相容

### 問題4: 網路不穩定時程式會崩潰
**現象**: 爬蟲過程若遇到網路中斷,程式直接報錯退出
**解決**:
```python
try:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"❌ 網路請求失敗: {e}")
    sys.exit(1)
```
加入 try-except 錯誤處理機制,並設定10秒timeout避免無限等待

---

## 📊 成果展示

### 程式執行輸出
```text
🔍 正在爬取央行匯率資料...
✅ 已儲存至 exchange_rates.csv
✅ 圖表已儲存至 sample_output.png

📊 最新匯率資料:
         日期     匯率
15  2025/09/26  32.123
16  2025/09/27  32.145
17  2025/09/28  32.098
18  2025/09/29  32.156
19  2025/09/30  32.134

📈 平均匯率: 32.131
📉 最低匯率: 32.098 (於 2025/09/28)
📈 最高匯率: 32.156 (於 2025/09/29)
📊 相較一週前變化: +0.34%
```

### 匯率 CSV 範例
|    日期    |  匯率  |
| ---------- | ------ |
| 2025/09/10 | 30.310 |
| 2025/09/11 | 30.344 |
| 2025/09/12 | 30.246 |
| ...        | ...    |

### 匯率走勢圖
<img width="800" alt="sample_output" src="https://github.com/user-attachments/assets/75c1999b-950b-4a36-8f9e-5ccad35418fa" />

---

## 🎯 學習收穫
- 理解網頁爬蟲的資料清洗重要性
- 學會動態調整圖表參數提升可讀性
- 實踐錯誤處理確保程式穩定性
- 體會單元測試對程式品質的重要性

---

## 🔮 未來改進方向
- [ ] 支援多幣別查詢(EUR, JPY, CNY等)
- [ ] 整合 LINE Notify 推播
- [ ] 部署為 Web API (FastAPI)
- [ ] 加入技術指標分析(移動平均線)
- [ ] 改用央行官方API(若有提供)

---

## 📄 授權
MIT License

## 👨‍💻 作者
- **開發者**: 胡智勝 / tom1835566
- **Email**: [tom1835566@gmail.com](mailto:tom1835566@gmail.com)
- **LinkedIn**: [智勝-胡](https://www.linkedin.com/in/智勝-胡-9590b7386)

## 🙏 致謝
- 資料來源: [中華民國中央銀行](https://www.cbc.gov.tw/tw/lp-645-1.html)