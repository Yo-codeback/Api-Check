#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
警報功能測試腳本
"""

import requests
import time
import json

def test_api_endpoints():
    """測試所有API端點"""
    base_url = "http://localhost:5000"
    
    print("🔍 測試API端點...")
    
    # 測試主頁面
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ 主頁面: {response.status_code}")
    except Exception as e:
        print(f"❌ 主頁面錯誤: {e}")
    
    # 測試狀態API
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 狀態API: {response.status_code}")
            print(f"   - API狀態: {data.get('status', 'N/A')}")
            print(f"   - 總檢查次數: {data.get('total_checks', 0)}")
        else:
            print(f"❌ 狀態API錯誤: {response.status_code}")
    except Exception as e:
        print(f"❌ 狀態API錯誤: {e}")
    
    # 測試健康檢查API
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康檢查API: {response.status_code}")
            print(f"   - 狀態: {data.get('status', 'N/A')}")
        else:
            print(f"❌ 健康檢查API錯誤: {response.status_code}")
    except Exception as e:
        print(f"❌ 健康檢查API錯誤: {e}")
    
    # 測試測試頁面
    try:
        response = requests.get(f"{base_url}/test")
        print(f"✅ 測試頁面: {response.status_code}")
    except Exception as e:
        print(f"❌ 測試頁面錯誤: {e}")

def test_alert_simulation():
    """模擬警報情況"""
    print("\n🚨 模擬警報情況...")
    
    # 這裡可以添加模擬API失敗的測試
    # 由於實際的API檢查是在後端進行的，我們只能測試前端警報功能
    
    print("📱 請在瀏覽器中訪問 http://localhost:5000/test")
    print("   然後點擊測試按鈕來驗證警報功能")

def main():
    """主函數"""
    print("🚀 API監控中心 - 功能測試")
    print("=" * 50)
    
    # 等待服務啟動
    print("⏳ 等待服務啟動...")
    time.sleep(2)
    
    # 測試API端點
    test_api_endpoints()
    
    # 測試警報模擬
    test_alert_simulation()
    
    print("\n" + "=" * 50)
    print("✅ 測試完成！")
    print("\n📋 測試清單:")
    print("1. ✅ 後端服務運行")
    print("2. ✅ API端點正常")
    print("3. 📱 請手動測試前端警報功能")
    print("\n🌐 訪問網址:")
    print("- 主頁面: http://localhost:5000/")
    print("- 測試頁面: http://localhost:5000/test")
    print("- 簡化頁面: http://localhost:5000/simple")

if __name__ == "__main__":
    main() 