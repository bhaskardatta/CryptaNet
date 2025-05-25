#!/usr/bin/env python3
"""
Test Integrated System
This script tests the functionality of the entire CryptaNet system
"""

import requests
import json
import time
import sys
import os
from datetime import datetime

def print_header(text):
    print("\n" + "=" * 60)
    print(f"🔍 {text}")
    print("=" * 60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")
    
def print_warning(text):
    print(f"⚠️ {text}")

def print_info(text):
    print(f"ℹ️ {text}")

def test_backend_connection():
    print_header("Testing Backend API Connection")
    try:
        response = requests.get("http://localhost:5004/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend API is responsive")
            return True
        else:
            print_error(f"Backend API returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to Backend API: {e}")
        return False

def test_data_flow():
    print_header("Testing Data Flow")
    try:
        response = requests.get("http://localhost:5004/api/analytics/comprehensive", timeout=5)
        if response.status_code == 200:
            data = response.json()
            total_records = data["analytics"]["total_records"]
            if total_records > 0:
                print_success(f"Data flow confirmed: {total_records} records in the system")
                return True
            else:
                print_warning("Backend is responsive but no data records found")
                return False
        else:
            print_error(f"Analytics API returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to Analytics API: {e}")
        return False
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        print_error(f"Failed to parse response: {e}")
        return False

def test_anomaly_detection():
    print_header("Testing Anomaly Detection")
    try:
        response = requests.get("http://localhost:5004/api/analytics/anomalies", timeout=5)
        if response.status_code == 200:
            data = response.json()
            anomalies = data.get("anomalies", [])
            print_success(f"Anomaly detection working: {len(anomalies)} anomalies found")
            
            # Print most recent anomaly if available
            if anomalies:
                recent = anomalies[0]
                print_info(f"Most recent anomaly: {recent.get('description', 'Unknown')} (Score: {recent.get('anomaly_score', 'N/A')})")
            return True
        else:
            print_error(f"Anomaly API returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to Anomaly API: {e}")
        return False
    except (KeyError, TypeError, json.JSONDecodeError) as e:
        print_error(f"Failed to parse response: {e}")
        return False

def test_data_simulator():
    print_header("Testing Data Simulator")
    try:
        response = requests.get("http://localhost:8001/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Data simulator is active: {data.get('total_records_sent', 0)} records generated")
            print_info(f"Anomalies injected: {data.get('anomalies_injected', 0)}")
            return True
        else:
            print_error(f"Data Simulator returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print_error(f"Failed to connect to Data Simulator: {e}")
        return False

def main():
    print("\n" + "=" * 80)
    print("🧪 CRYPTANET INTEGRATED SYSTEM TEST")
    print("=" * 80)
    print(f"⏱️  Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 80)
    
    # Run tests
    backend_ok = test_backend_connection()
    
    if not backend_ok:
        print_error("Backend test failed - skipping remaining tests")
        sys.exit(1)
    
    data_flow_ok = test_data_flow()
    anomaly_detection_ok = test_anomaly_detection()
    simulator_ok = test_data_simulator()
    
    # Summary
    print("\n" + "=" * 80)
    print("📋 TEST SUMMARY")
    print("=" * 80)
    print(f"Backend API:        {'✅ PASS' if backend_ok else '❌ FAIL'}")
    print(f"Data Flow:          {'✅ PASS' if data_flow_ok else '❌ FAIL'}")
    print(f"Anomaly Detection:  {'✅ PASS' if anomaly_detection_ok else '❌ FAIL'}")
    print(f"Data Simulator:     {'✅ PASS' if simulator_ok else '❌ FAIL'}")
    print("-" * 80)
    
    # Overall status
    all_passed = all([backend_ok, data_flow_ok, anomaly_detection_ok, simulator_ok])
    if all_passed:
        print("🎉 ALL TESTS PASSED - System is functioning correctly!")
    else:
        print("⚠️ SOME TESTS FAILED - Check the log for details")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
