# main.py
from pkg.plugin.context import register, handler, BasePlugin, EventContext
from pkg.plugin.events import PersonNormalMessageReceived, GroupNormalMessageReceived
import requests
import pkg.platform.types as platform_types


@register(name="MCPQwenPlugin", description="通过 MCP 调用 Qwen-Plus 模型", version="1.0.0", author="yuhuai2002")
class MCPQwenPlugin(BasePlugin):

    @handler(PersonNormalMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def handle_message(self, ctx: EventContext):
        # 获取用户发送的文本消息
        question = ctx.event.text_message.strip()

        # 只在消息以 !qwen 开头时触发
        if not question.startswith("!qwen"):
            return

        # 提取实际问题
        query = question[5:].strip()
        if not query:
            ctx.add_return("reply", ["请在 !qwen 后输入你要问的问题"])
            ctx.prevent_default()
            return

        try:
            response = requests.post(
                "http://18.163.69.177:8000/ask",
                headers={"Content-Type": "application/json"},
                json={"question": query},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            answer = result.get("answer", "MCP 未返回有效答案")
        except Exception as e:
            answer = f"请求失败：{e}"

        # 构造回复消息链
        msg_chain = platform_types.MessageChain([
            platform_types.Plain(answer)
        ])

        # 回复消息
        await ctx.send_message(
            target_type=ctx.event.type,  # "person" 或 "group"
            target_id=ctx.event.sender_id if ctx.event.type == "person" else ctx.event.group_id,
            message_chain=msg_chain
        )

        # 阻止默认行为（不让 AI 再回复一次）
        ctx.prevent_default()

        # 阻止后续插件处理
        ctx.prevent_postorder()
