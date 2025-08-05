# main.py
from pkg.plugin.context import BasePlugin, APIHost, EventContext, register
import requests

class MCPPlugin(BasePlugin):
    @register()
    def mcp_call(self, ctx: EventContext):
        """
        用户消息事件处理
        :param ctx: 上下文对象，包含用户发送的信息
        """
        question = ctx.event.message.content  # 用户的输入内容

        try:
            response = requests.post(
                "http://18.163.69.177:8000/ask",
                headers={"Content-Type": "application/json"},
                json={"question": question},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            answer = result.get("answer", "MCP 未返回有效答案")
        except Exception as e:
            answer = f"请求失败：{e}"

        # 回复给用户
        ctx.reply(answer)
