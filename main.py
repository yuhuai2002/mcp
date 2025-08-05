# main.py
# -*- coding: utf-8 -*-
from pkg.plugin.models import PluginMetadata
from pkg.plugin.host import EventContext, PluginHost
from pkg.plugin.decorator import plugin, event

import requests
from requests.exceptions import RequestException

@plugin(
    metadata=PluginMetadata(
        name="mcp-qwen-plugin",
        description="通过 MCP 调用 Qwen-Plus 模型",
        version="1.0.0",
        author="yuhuai2002",
    )
)
class MCPQwenPlugin:
    def __init__(self, host: PluginHost):
        self.host = host
        print("✅ MCP Qwen Plugin initialized")

    @event("ON_HANDLE_CONTEXT")
    def handle_message(self, ctx: EventContext):
        """
        处理用户输入消息，转发给 MCP 模型
        """
        question = ctx.event.text  # 获取用户输入的消息文本

        data = {
            "question": question
        }

        try:
            response = requests.post(
                "http://18.163.69.177:8000/ask",
                headers={"Content-Type": "application/json"},
                json=data,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            answer = result.get("answer", "MCP 未返回有效答案")

        except RequestException as e:
            answer = f"请求 MCP 服务失败: {str(e)}"
        except Exception as e:
            answer = f"内部错误: {str(e)}"

        ctx.add_return("reply", answer)
