# main.py
from pkg.plugin.context import BasePlugin, APIHost, EventContext, register, handler
from pkg.plugin.events import PersonNormalMessageReceived  # 可按平台替换
import requests
from requests.exceptions import RequestException

class MCPQwenPlugin(BasePlugin):
    def __init__(self, host: APIHost):
        super().__init__(host)
        print("✅ MCP Qwen Plugin initialized")

    @handler(PersonNormalMessageReceived)
    async def on_person_message(self, ctx: EventContext):
        msg = ctx.event.text_message
        data = {"question": msg}
        try:
            resp = requests.post("http://18.163.69.177:8000/ask",
                                 json=data, timeout=10)
            resp.raise_for_status()
            ans = resp.json().get("answer", "无有效答案")
        except RequestException as e:
            ans = f"请求失败: {e}"
        except Exception as e:
            ans = f"内部错误: {e}"
        ctx.add_return("reply", [ans])
        ctx.prevent_default()

register(MCPQwenPlugin)
