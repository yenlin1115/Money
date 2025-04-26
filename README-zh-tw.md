# AI MCP 儀表板

## 概覽
本專案實作了一個由 AI 驅動的市場控制面板 (Market Control Panel, MCP) 儀表板，利用人工智慧提供增強的市場洞察和交易分析。此儀表板結合市場數據與先進的 AI 演算法，以提供即時的市場分析和預測性見解。

## 功能特色
- 即時市場數據整合 (未來版本計劃整合彭博終端)
- AI 驅動的市場趨勢分析與預測
- 互動式數據視覺化與圖表
- 針對市場變動的自訂警報系統
- 投資組合優化建議
- 風險評估指標
- 歷史數據分析

## 技術棧
- Python 3.x
- 機器學習函式庫：
  - TensorFlow/PyTorch
  - scikit-learn
  - pandas
- 資料視覺化：
  - Plotly
  - Dash
- 網站框架：
  - FastAPI
  - Django

## 安裝說明

1.  複製儲存庫：
    ```bash
    git clone https://github.com/yenlin1115/Money.git
    cd Money
    ```

2.  建立並啟用虛擬環境 (使用 uv)：
    ```bash
    # 安裝 uv (如果尚未安裝): https://github.com/astral-sh/uv
    uv init
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```

3.  安裝依賴套件 (使用 uv)：
    ```bash
    uv add -r requirements.txt
    ```

## 使用方式
1.  啟動儀表板伺服器：
    ```bash
    uv run python manage.py runserver
    ```

2.  在瀏覽器中開啟 `http://localhost:8000` 來訪問儀表板

## 專案結構 (根據 README.md)
```
Money/
├── api/              # API 端點與資料整合
├── dashboard/        # 儀表板 UI 元件
├── ml_models/        # 機器學習模型與演算法
├── utils/            # 公用函式與輔助工具
├── tests/            # 測試套件
└── config/           # 設定檔
```
**注意:** 實際目錄結構可能與 README.md 中描述略有不同。

## 發展藍圖
- [ ] 整合彭博終端 (Bloomberg Terminal)
- [ ] 增加更多市場數據來源
- [ ] 開發更進階的交易演算法
- [ ] 支援行動應用程式

## 貢獻
歡迎各種貢獻！請隨時提交 Pull Request。

## 授權
本專案採用 MIT 授權 - 詳情請參閱 LICENSE 檔案。

## 聯絡方式
若有任何問題或建議，請聯絡：
- Email: yenlin1115@gmail.com
- GitHub: [@yenlin1115](https://github.com/yenlin1115)

## 致謝
- 感謝本專案所使用的開源函式庫的貢獻者與維護者
