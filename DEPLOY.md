# Render 部署說明

## 部署步驟

### 1. 準備檔案
確保以下檔案都在專案根目錄：
- `app.py` - 主程式
- `config.py` - 設定檔
- `requirements.txt` - 依賴套件
- `render.yaml` - Render配置
- `Procfile` - 啟動指令
- `templates/dashboard.html` - 前端模板

### 2. 上傳到GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用戶名/你的專案名.git
git push -u origin main
```

### 3. 在Render上部署
1. 前往 [Render Dashboard](https://dashboard.render.com/)
2. 點擊 "New +" → "Web Service"
3. 連接你的GitHub專案
4. 設定部署選項：
   - **Name**: api-monitor-dashboard
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free

### 4. 環境變數設定（可選）
在Render的環境變數中可以設定：
- `PORT` - 端口號（Render會自動設定）
- `PYTHON_VERSION` - Python版本（已在render.yaml中設定）

## 部署後檢查

### 1. 健康檢查
訪問 `https://你的服務名.onrender.com/health`
應該看到：
```json
{
  "status": "healthy",
  "uptime": "00:00:00",
  "timestamp": "2025-07-30T..."
}
```

### 2. 主頁面
訪問 `https://你的服務名.onrender.com/`
應該看到API監控儀表板

### 3. API狀態
訪問 `https://你的服務名.onrender.com/api/status`
應該看到完整的系統狀態JSON

## 常見問題

### Q: 部署失敗怎麼辦？
A: 檢查Render的日誌，常見問題：
- 依賴套件版本衝突
- Python版本不支援
- 檔案路徑錯誤

### Q: 服務無法啟動？
A: 檢查：
- `app.py` 檔案是否存在
- `requirements.txt` 是否正確
- 端口設定是否正確

### Q: 健康檢查失敗？
A: 確保 `/health` 端點正常回應

## 監控功能

部署成功後，系統會：
- 每10分鐘檢查一次API狀態
- 即時更新系統資源使用情況
- 記錄所有操作日誌
- 提供Web介面查看狀態

## 免費方案限制

- 每月750小時運行時間
- 15分鐘無活動後會休眠
- 首次訪問需要重新啟動（約30秒） 