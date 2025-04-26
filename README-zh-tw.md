# AI 市場控制面板

## 概述
本專案實現了一個基於人工智慧的市場控制面板（MCP），利用 AI 技術提供增強型市場洞察和交易分析。該面板結合市場數據與先進的 AI 算法，提供即時市場分析和預測洞察。

## 功能特點
- 即時市場數據整合
- AI 驅動的市場趨勢分析和預測
- 互動式數據視覺化和圖表
- 使用機器學習的股價預測
- 投資組合追蹤和分析
- 歷史數據分析
- 交易代理整合

## 技術堆疊
- Python 3.x
- Django 網頁框架
- 機器學習函式庫：
  - scikit-learn
  - pandas
  - numpy
- 數據視覺化：
  - Plotly
  - Matplotlib
- OpenAI API 整合

## 安裝步驟

1. 複製專案：
```bash
git clone https://github.com/yenlin1115/Money.git
cd Money
```

2. 建立並啟動虛擬環境：
```bash
python -m venv .venv
source .venv/bin/activate  # Windows 系統：.venv\Scripts\activate
```

3. 安裝依賴套件：
```bash
pip install -r requirements.txt
```

4. 設定環境變數：
```bash
cp .env.example .env
# 編輯 .env 檔案設定您的配置
```

## 使用方式
1. 啟動面板伺服器：
```bash
python manage.py runserver
```

2. 在瀏覽器中訪問 `http://localhost:8000`

## 專案結構
```
Money/
├── Moneytest/        # Django 專案配置
├── companies/        # 股票和公司數據模型與視圖
├── templates/        # HTML 模板
├── data/            # 數據儲存
├── plots/           # 生成的圖表
├── trading_agents/  # 交易代理實現
└── utils/           # 工具函數
```

## 開發路線圖
- [ ] 增強市場數據來源
- [ ] 進階交易算法
- [ ] 行動應用程式支援
- [ ] 即時數據串流
- [ ] 投資組合優化

## 貢獻
歡迎貢獻！請隨時提交 Pull Request。

## 授權
本專案採用 MIT 授權條款 - 詳見 LICENSE 檔案。

## 聯絡方式
如有任何問題或建議，請聯絡：
- 電子郵件：yenlin1115@gmail.com
- GitHub：[@yenlin1115](https://github.com/yenlin1115)

## 致謝
- 本專案使用的開源函式庫的貢獻者和維護者
