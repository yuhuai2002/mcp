# plugin.py
import requests

def handle_message(message):
    # 构造请求数据
    data = {
        "question": message
    }
    
    # 调用 MCP 服务
    response = requests.post(
        "http://127.0.0.1:8000/ask",
        headers={"Content-Type": "application/json"},
        json=data
    )
    
    # 解析响应
    if response.status_code == 200:
        result = response.json()
        return result.get("answer", "无法获取答案")
    else:
        return f"错误: {response.status_code} - {response.text}"
