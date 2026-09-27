# Boeing's Components Record System

波音零件管理系統，國立臺灣大學資管系「資料庫管理（113-1）」期末專題（第 6 組）。

波音的製造流程牽涉全球數百家供應商和成千上萬個零件。這個系統記錄零件的組成與流向、訂單狀態、工廠與供應商資料，以及員工權限，讓組裝員工能即時掌握每個零件的生產和配送進度，也讓管理層能評估供應商表現。

**Demo 影片**：https://youtu.be/1AZcwfE1PLs
**期末報告**：[docs/final_report.pdf](docs/final_report.pdf)

## 技術架構

| 層級 | 使用技術 |
|------|----------|
| 前端 | HTML、CSS、JavaScript（Fetch API） |
| 後端 | Python、Flask、Flask-CORS |
| 資料庫 | PostgreSQL（psycopg2 connection pool） |
| 測試資料 | Python（Faker、pandas）產生約 10 萬名員工、20 萬筆訂單 |

## 主要功能

**User（組裝員工）**
- 新增訂單，更新訂單狀態（未出貨、運送中、已到貨、退貨、刪除）與到貨檢查回饋
- 查詢零件、子零件組成、工廠與供應商資訊
- 查詢某零件的歷史訂單

**Admin（管理層）**
- 以上所有功能
- 新增與修改零件、供應商、員工資料
- 為供應商年度表現評分，並查詢歷年評分
- 註冊新員工

## 資料庫設計

共 6 個實體（INVENTORY、PART、FACTORY、SUPPLIER、EMPLOYEE、ORDER）與 9 個關係，ER Diagram 請見期末報告。

- 同一種物件（PART）可由不同廠商供應，各自對應不同的零件（INVENTORY）
- 零件可由子零件組成，以 ITEM 表記錄父子關係
- 員工有上下級關係（mgr_id），工廠與供應商各有負責人
- 更新訂單狀態時使用 `SELECT ... FOR UPDATE` 鎖定該筆資料，避免多人同時修改造成衝突

## 安全性設計

- 資料庫帳密和 Flask secret key 放在環境變數（`.env`），不寫在程式碼裡
- 登入時由後端比對密碼，API 不會回傳密碼（範例資料皆為程式產生的假資料，密碼以明碼儲存）
- 帳號不存在與密碼錯誤回傳相同訊息，避免被用來試探帳號
- 所有查詢皆使用參數化查詢；可修改的欄位名稱另外以白名單檢查，防止 SQL injection

## 專案結構

```
├── app.py                  # Flask API
├── DB_utils.py             # 資料庫查詢函式
├── frontend/               # 前端頁面
├── data_final/             # 測試資料（CSV）
├── data_generator_final/   # 產生測試資料的程式
├── Backup.backup           # PostgreSQL 17 資料庫備份
└── docs/final_report.pdf   # 期末報告
```

## 執行方式

1. 安裝套件
   ```bash
   pip install -r requirements.txt
   ```
2. 還原資料庫（PostgreSQL 17 以上）
   ```bash
   createdb Final
   pg_restore -d Final Backup.backup
   ```
3. 複製 `.env.example` 為 `.env`，填入自己的資料庫密碼與 secret key
4. 啟動後端
   ```bash
   python app.py
   ```
5. 另開終端機啟動前端
   ```bash
   cd frontend
   python -m http.server 8000
   ```
6. 瀏覽器開啟 http://localhost:8000/login.html ，用 `data_final/employee_f.csv` 裡的員工 ID 和密碼登入（皆為程式產生的假資料）

## 組員

[@Chiangjc](https://github.com/Chiangjc)、[@CTHsin](https://github.com/CTHsin)、[@Dami-Chen](https://github.com/Dami-Chen)
