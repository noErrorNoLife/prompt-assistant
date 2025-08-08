#!/usr/bin/env python3
"""
API测试脚本 - 测试修复后的/api/prompts端点
"""
import requests
import json

API_BASE_URL = 'http://localhost:5000/api'

def test_api():
    print("=== 测试 /api/prompts API ===\n")
    
    # 测试用例1: GET /api/prompts
    print("1. 测试 GET /api/prompts")
    try:
        response = requests.get(f'{API_BASE_URL}/prompts')
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"返回数据数量: {len(data)}")
        else:
            print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    print()
    
    # 测试用例2: POST /api/prompts (有效数据)
    print("2. 测试 POST /api/prompts (有效数据)")
    valid_data = {
        'title': '测试提示词',
        'content': '这是一个测试提示词的内容',
        'category': '测试分类',
        'tags': '测试,API'
    }
    try:
        response = requests.post(f'{API_BASE_URL}/prompts', json=valid_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
        if response.status_code == 201:
            created_id = response.json().get('id')
            print(f"创建成功，ID: {created_id}")
        else:
            print("创建失败")
    except Exception as e:
        print(f"请求失败: {e}")
    print()
    
    # 测试用例3: POST /api/prompts (缺少title)
    print("3. 测试 POST /api/prompts (缺少title)")
    invalid_data1 = {
        'content': '这是内容',
        'category': '分类'
    }
    try:
        response = requests.post(f'{API_BASE_URL}/prompts', json=invalid_data1)
        print(f"状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    print()
    
    # 测试用例4: POST /api/prompts (空title)
    print("4. 测试 POST /api/prompts (空title)")
    invalid_data2 = {
        'title': '   ',  # 只有空格
        'content': '这是内容'
    }
    try:
        response = requests.post(f'{API_BASE_URL}/prompts', json=invalid_data2)
        print(f"状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    print()
    
    # 测试用例5: POST /api/prompts (缺少content)
    print("5. 测试 POST /api/prompts (缺少content)")
    invalid_data3 = {
        'title': '测试标题'
    }
    try:
        response = requests.post(f'{API_BASE_URL}/prompts', json=invalid_data3)
        print(f"状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    print()
    
    # 测试用例6: PUT /api/prompts/1 (部分更新)
    print("6. 测试 PUT /api/prompts/1 (部分更新)")
    update_data = {
        'title': '更新后的标题'
    }
    try:
        response = requests.put(f'{API_BASE_URL}/prompts/1', json=update_data)
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    print()
    
    # 测试用例7: PUT /api/prompts/1 (空title)
    print("7. 测试 PUT /api/prompts/1 (空title)")
    invalid_update = {
        'title': '',
        'content': '新内容'
    }
    try:
        response = requests.put(f'{API_BASE_URL}/prompts/1', json=invalid_update)
        print(f"状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    print()
    
    # 测试用例8: PUT /api/prompts/999 (不存在的ID)
    print("8. 测试 PUT /api/prompts/999 (不存在的ID)")
    update_data = {
        'title': '测试标题'
    }
    try:
        response = requests.put(f'{API_BASE_URL}/prompts/999', json=update_data)
        print(f"状态码: {response.status_code}")
        print(f"错误信息: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")
    print()

if __name__ == '__main__':
    print("请先启动Flask服务器: python3 app.py")
    print("然后运行此测试脚本")
    print()
    
    try:
        # 检查服务器是否运行
        response = requests.get(f'{API_BASE_URL}/prompts', timeout=2)
        test_api()
    except requests.exceptions.RequestException:
        print("错误: 无法连接到API服务器 (http://localhost:5000)")
        print("请确保Flask服务器正在运行")