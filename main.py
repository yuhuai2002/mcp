# -*- coding: utf-8 -*-
# main.py

import requests
from requests.exceptions import RequestException

def main(message):
    """
    LangBot 插件的入口函数
    :param message: 用户发送的消息
    :return: 返回给用户的回复
    """
    # 构造请求数据
    data = {
        "question": message
    }
    
    # 调用 MCP 服务（使用公网 IP）
    try:
        response = requests.post(
            "http://18.163.69.177:8000/ask",
            headers={"Content-Type": "application/json"},
            json=data,
            timeout=10  # 设置超时，避免阻塞
        )
        
        # 检查 HTTP 状态码
        response.raise_for_status()
        
        # 解析 JSON 响应
        result = response.json()
        return result.get("answer", "MCP 未返回有效答案")
        
    except RequestException as e:
        return f"请求 MCP 服务失败: {str(e)}"
    except Exception as e:
        return f"内部错误: {str(e)}"
