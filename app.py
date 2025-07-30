from flask import Flask, render_template, jsonify, request
import threading
import time
import requests
import psutil
import json
import os
from datetime import datetime, timedelta
from config import *

app = Flask(__name__)

# 全局狀態儲存
state = {
    "last_check_time": "尚未檢查",
    "next_check_time": "尚未設定",
    "status": "尚無資料",
    "latest_data": "",
    "logs": [],
    "program_status": "🟢 運作中",
    "check_interval": CHECK_INTERVAL,
    "total_checks": 0,
    "successful_checks": 0,
    "failed_checks": 0,
    "uptime": "00:00:00",
    "start_time": datetime.now(),
    "last_success_time": None,
    "last_failure_time": None,
    "response_times": [],
    "avg_response_time": 0,
    "system_version": SYSTEM_VERSION,
    "ram_usage": 0,
    "ram_total": 0,
    "ram_percent": 0,
    "cpu_percent": 0
}

def update_uptime():
    """更新程式運行時間"""
    while True:
        uptime_delta = datetime.now() - state["start_time"]
        hours, remainder = divmod(int(uptime_delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        state["uptime"] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        time.sleep(1)

def update_system_resources():
    """更新系統資源使用情況"""
    while True:
        try:
            memory = psutil.virtual_memory()
            state["ram_usage"] = round(memory.used / 1024 / 1024, 1)
            state["ram_total"] = round(memory.total / 1024 / 1024, 1)
            state["ram_percent"] = round(memory.percent, 1)
            state["cpu_percent"] = round(psutil.cpu_percent(interval=1), 1)
        except Exception as e:
            state["logs"].append(f"[{time.strftime('%H:%M:%S')}] ⚠️ 系統資源監控錯誤: {str(e)}")
        time.sleep(5)

def fetch_data():
    """API數據抓取"""
    while True:
        try:
            state["total_checks"] += 1
            start_time = time.time()
            
            resp = requests.get(API_URL, timeout=10)
            response_time = round((time.time() - start_time) * 1000, 2)
            
            if resp.status_code == 200 and "種類代碼" in resp.text:
                state["status"] = "✅ 成功"
                state["successful_checks"] += 1
                state["last_success_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                state["latest_data"] = resp.text.splitlines()[0][:200]
                state["logs"].append(f"[{time.strftime('%H:%M:%S')}] ✅ 成功取得資料 (回應時間: {response_time}ms)")
                
                # 更新回應時間統計
                state["response_times"].append(response_time)
                if len(state["response_times"]) > MAX_RESPONSE_TIMES:
                    state["response_times"] = state["response_times"][-MAX_RESPONSE_TIMES:]
                state["avg_response_time"] = round(sum(state["response_times"]) / len(state["response_times"]), 2)
            else:
                state["status"] = "🚨 異常"
                state["failed_checks"] += 1
                state["last_failure_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_msg = f"API回應異常 (狀態碼: {resp.status_code}, 回應時間: {response_time}ms)"
                state["logs"].append(f"[{time.strftime('%H:%M:%S')}] 🚨 {error_msg}")
                
        except Exception as e:
            state["status"] = "🚨 異常"
            state["failed_checks"] += 1
            state["last_failure_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_msg = f"API連線異常: {str(e)}"
            state["logs"].append(f"[{time.strftime('%H:%M:%S')}] 🚨 {error_msg}")
        
        state["last_check_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state["next_check_time"] = (datetime.now() + timedelta(seconds=CHECK_INTERVAL)).strftime("%Y-%m-%d %H:%M:%S")
        
        # 保持日誌在合理範圍內
        if len(state["logs"]) > MAX_LOGS:
            state["logs"] = state["logs"][-50:]
        
        time.sleep(CHECK_INTERVAL)

# 啟動後台執行緒
threading.Thread(target=fetch_data, daemon=True).start()
threading.Thread(target=update_uptime, daemon=True).start()
threading.Thread(target=update_system_resources, daemon=True).start()

@app.route("/")
def index():
    return render_template("dashboard.html", state=state)

@app.route("/api/status")
def api_status():
    return jsonify(state)

@app.route("/api/update", methods=["POST"])
def api_update():
    data = request.json
    state.update(data)
    return jsonify({"status": "updated"})

@app.route("/health")
def health_check():
    """健康檢查端點，用於Render的存活檢查"""
    return jsonify({
        "status": "healthy",
        "uptime": state["uptime"],
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    # 從環境變數獲取端口，預設為5000
    port = int(os.environ.get("PORT", 5000))
    
    # 在Render上使用0.0.0.0綁定所有網路介面
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False) 