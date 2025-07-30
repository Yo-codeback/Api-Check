import threading
import time
import requests
import psutil
import json
import os
from datetime import datetime, timedelta
from config import *

# 顏色代碼
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 全局狀態儲存
state = {
    "last_check_time": "尚未檢查",
    "next_check_time": "尚未設定",
    "status": "尚無資料",
    "latest_data": "",
    "logs": [],
    "program_status": "🟢 運作中",
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
    "cpu_percent": 0,
    "last_notification_time": None,
    "notification_cooldown": NOTIFICATION_COOLDOWN
}

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """顯示標題"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                    🚀 API 監控指揮中心 - CMD 版本 🚀                        ║")
    print("║                              System Dashboard                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

def print_status_grid():
    """顯示狀態網格"""
    print(f"{Colors.BLUE}{Colors.BOLD}┌─────────────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}│                           📊 系統狀態監控                                        │{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}├─────────────────────────────────────────────────────────────────────────────────────┤{Colors.RESET}")
    
    # 第一行：基本狀態
    status_color = Colors.GREEN if state["status"] == "✅ 成功" else Colors.RED
    print(f"{Colors.BLUE}│{Colors.RESET} 程式狀態: {Colors.CYAN}{state['program_status']:<15}{Colors.RESET} │ API狀態: {status_color}{state['status']:<15}{Colors.RESET} │ 運行時間: {Colors.YELLOW}{state['uptime']:<10}{Colors.RESET} {Colors.BLUE}│{Colors.RESET}")
    
    # 第二行：檢查統計
    success_rate = (state['successful_checks'] / state['total_checks'] * 100) if state['total_checks'] > 0 else 0
    print(f"{Colors.BLUE}│{Colors.RESET} 總檢查: {Colors.WHITE}{state['total_checks']:<8}{Colors.RESET} │ 成功: {Colors.GREEN}{state['successful_checks']:<8}{Colors.RESET} │ 失敗: {Colors.RED}{state['failed_checks']:<8}{Colors.RESET} │ 成功率: {Colors.CYAN}{success_rate:>6.1f}%{Colors.RESET} {Colors.BLUE}│{Colors.RESET}")
    
    # 第三行：時間資訊
    last_check = state['last_check_time'].split(' ')[1] if ' ' in state['last_check_time'] else state['last_check_time']
    next_check = state['next_check_time'].split(' ')[1] if ' ' in state['next_check_time'] else state['next_check_time']
    print(f"{Colors.BLUE}│{Colors.RESET} 上次檢查: {Colors.YELLOW}{last_check:<10}{Colors.RESET} │ 下次檢查: {Colors.YELLOW}{next_check:<10}{Colors.RESET} │ 回應時間: {Colors.MAGENTA}{state['avg_response_time']:>6.1f}ms{Colors.RESET} {Colors.BLUE}│{Colors.RESET}")
    
    print(f"{Colors.BLUE}└─────────────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")

def print_health_metrics():
    """顯示健康度指標"""
    print(f"{Colors.GREEN}{Colors.BOLD}┌─────────────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}│                           🏥 系統健康度指標                                      │{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}├─────────────────────────────────────────────────────────────────────────────────────┤{Colors.RESET}")
    
    # 健康度分數
    health_score = (state['successful_checks'] / state['total_checks'] * 100) if state['total_checks'] > 0 else 100
    health_color = Colors.GREEN if health_score >= 90 else Colors.YELLOW if health_score >= 70 else Colors.RED
    
    # 錯誤率
    error_rate = (state['failed_checks'] / state['total_checks'] * 100) if state['total_checks'] > 0 else 0
    error_color = Colors.RED if error_rate > 10 else Colors.YELLOW if error_rate > 5 else Colors.GREEN
    
    print(f"{Colors.GREEN}│{Colors.RESET} 健康度分數: {health_color}{health_score:>6.1f}%{Colors.RESET} │ 錯誤率: {error_color}{error_rate:>6.1f}%{Colors.RESET} │ 檢查間隔: {Colors.CYAN}{CHECK_INTERVAL//60:>3}分鐘{Colors.RESET} {Colors.GREEN}│{Colors.RESET}")
    
    # 系統資源
    ram_color = Colors.GREEN if state['ram_percent'] < 70 else Colors.YELLOW if state['ram_percent'] < 90 else Colors.RED
    cpu_color = Colors.GREEN if state['cpu_percent'] < 70 else Colors.YELLOW if state['cpu_percent'] < 90 else Colors.RED
    
    print(f"{Colors.GREEN}│{Colors.RESET} RAM使用率: {ram_color}{state['ram_percent']:>6.1f}%{Colors.RESET} │ RAM使用量: {Colors.YELLOW}{state['ram_usage']:>8.0f}MB{Colors.RESET} │ CPU使用率: {cpu_color}{state['cpu_percent']:>6.1f}%{Colors.RESET} {Colors.GREEN}│{Colors.RESET}")
    
    print(f"{Colors.GREEN}└─────────────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")

def print_latest_data():
    """顯示最新資料"""
    print(f"{Colors.YELLOW}{Colors.BOLD}┌─────────────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}│                           📄 最新資料摘要                                        │{Colors.RESET}")
    print(f"{Colors.YELLOW}{Colors.BOLD}├─────────────────────────────────────────────────────────────────────────────────────┤{Colors.RESET}")
    
    data_preview = state['latest_data'][:70] + "..." if len(state['latest_data']) > 70 else state['latest_data']
    print(f"{Colors.YELLOW}│{Colors.RESET} {Colors.WHITE}{data_preview:<75}{Colors.RESET} {Colors.YELLOW}│{Colors.RESET}")
    
    print(f"{Colors.YELLOW}└─────────────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")

def print_recent_logs():
    """顯示最近日誌"""
    print(f"{Colors.CYAN}{Colors.BOLD}┌─────────────────────────────────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}│                           📋 最近日誌記錄                                        │{Colors.RESET}")
    print(f"{Colors.CYAN}{Colors.BOLD}├─────────────────────────────────────────────────────────────────────────────────────┤{Colors.RESET}")
    
    recent_logs = state['logs'][-5:]  # 只顯示最近5筆
    for log in recent_logs:
        if '✅' in log:
            color = Colors.GREEN
        elif '🚨' in log:
            color = Colors.RED
        elif '⚠️' in log:
            color = Colors.YELLOW
        elif '📱' in log:
            color = Colors.MAGENTA
        else:
            color = Colors.WHITE
        
        log_preview = log[:75] + "..." if len(log) > 75 else log
        print(f"{Colors.CYAN}│{Colors.RESET} {color}{log_preview:<75}{Colors.RESET} {Colors.CYAN}│{Colors.RESET}")
    
    # 如果日誌不足5筆，用空行填充
    for _ in range(5 - len(recent_logs)):
        print(f"{Colors.CYAN}│{Colors.RESET} {'':<75} {Colors.CYAN}│{Colors.RESET}")
    
    print(f"{Colors.CYAN}└─────────────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")

def print_footer():
    """顯示頁腳"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Colors.BLUE}{Colors.BOLD}")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print(f"║ 最後更新: {current_time:<50} 版本: {SYSTEM_VERSION:<10} ║")
    print("║ 按 Ctrl+C 退出程式                                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

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
                
                # 發送FCM通知
                if IMMEDIATE_ERROR_NOTIFICATION:
                    state["logs"].append(f"[{time.strftime('%H:%M:%S')}] 📱 警報通知已發送 (本地)")
                
        except Exception as e:
            state["status"] = "🚨 異常"
            state["failed_checks"] += 1
            state["last_failure_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_msg = f"API連線異常: {str(e)}"
            state["logs"].append(f"[{time.strftime('%H:%M:%S')}] 🚨 {error_msg}")
            
            # 發送FCM通知
            if IMMEDIATE_ERROR_NOTIFICATION:
                state["logs"].append(f"[{time.strftime('%H:%M:%S')}] 📱 警報通知已發送 (本地)")
        
        state["last_check_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state["next_check_time"] = (datetime.now() + timedelta(seconds=CHECK_INTERVAL)).strftime("%Y-%m-%d %H:%M:%S")
        
        # 保持日誌在合理範圍內
        if len(state["logs"]) > MAX_LOGS:
            state["logs"] = state["logs"][-50:]
        
        time.sleep(CHECK_INTERVAL)

def update_display():
    """更新顯示"""
    while True:
        clear_screen()
        print_header()
        print_status_grid()
        print_health_metrics()
        print_latest_data()
        print_recent_logs()
        print_footer()
        time.sleep(2)  # 每2秒更新一次顯示

def main():
    """主函數"""
    print("正在啟動API監控指揮中心...")
    
    # 啟動後台執行緒
    threading.Thread(target=fetch_data, daemon=True).start()
    threading.Thread(target=update_uptime, daemon=True).start()
    threading.Thread(target=update_system_resources, daemon=True).start()
    
    # 等待一下讓初始數據載入
    time.sleep(3)
    
    try:
        # 開始顯示更新
        update_display()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}正在關閉API監控指揮中心...{Colors.RESET}")
        print(f"{Colors.GREEN}感謝使用！{Colors.RESET}")

if __name__ == "__main__":
    main() 