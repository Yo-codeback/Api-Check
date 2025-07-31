# API 監控指揮中心

## 功能特色

- 🚀 即時API監控
- 📱 FCM推送通知
- 💾 系統資源監控 (RAM/CPU)
- 📊 一屏顯示儀表板
- 🔄 自動錯誤檢測
- ⏰ 通知冷卻機制

## 安裝需求

```bash
pip install flask requests psutil
```

## FCM設定

### 1. 取得Google Service Account憑證

1. 前往 [Firebase Console](https://console.firebase.google.com/)
2. 選擇或創建專案
3. 前往「專案設定」>「服務帳戶」
4. 點擊「產生新的私密金鑰」
5. 下載JSON檔案並重命名為 `maker-bvc-appversion-3289f38926c9.json`
6. 將檔案放在專案根目錄

### 2. 設定Topic

在Firebase Console中：
1. 前往「雲端通訊」>「主題」
2. 創建主題：`system_updates`

### 3. 更新配置

編輯 `config.py` 文件：

```python
FCM_CREDENTIALS_FILE = "maker-bvc-appversion-3289f38926c9.json"
FCM_TOPIC = "system_updates"
```

## 運行方式

```bash
python "api check.py"
```

然後打開瀏覽器訪問：`http://localhost:5000`

## 通知機制

### 觸發條件
- API回應異常 (狀態碼非200)
- API連線失敗
- 系統資源異常

### 通知內容
- 標題：異常類型
- 內容：詳細錯誤訊息
- 數據：包含時間戳和錯誤詳情

### 通知機制
- **立即通知**：API錯誤時立即發送通知
- **冷卻機制**：每小時最多發送一次通知
- **智能過濾**：避免重複通知打擾

## 監控項目

### API監控
- 回應狀態
- 回應時間
- 成功/失敗統計
- 成功率

### 系統監控
- RAM使用率
- CPU使用率
- 程式運行時間
- 系統健康度

### 通知狀態
- FCM連接狀態
- 上次通知時間
- 通知冷卻時間

## 配置選項

在 `config.py` 中可以調整：

```python
# 檢查間隔（秒）
CHECK_INTERVAL = 600

# 通知冷卻時間（秒）
NOTIFICATION_COOLDOWN = 3600  # 1小時

# 日誌保留數量
MAX_LOGS = 100

# 回應時間記錄數量
MAX_RESPONSE_TIMES = 50
```

## 故障排除

### FCM通知不工作
1. 檢查 `maker-bvc-appversion-3289f38926c9.json` 檔案是否存在
2. 確認Google Service Account權限設定正確
3. 確認網路連線正常
4. 查看日誌中的錯誤訊息

### 系統資源監控異常
1. 確認已安裝 `psutil`
2. 檢查程式權限

## 版本資訊

- 版本：v2.0.0
- 支援：Windows/Linux/macOS
- Python：3.7+ 