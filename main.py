# main.py

# --- 调试 1: 文件是否被导入？---
print("🔥 MCPQwenPlugin: 文件开始执行，正在被导入！")

try:
    from pkg.plugin.context import register, handler, BasePlugin, EventContext, APIHost
    print("✅ MCPQwenPlugin: 成功导入 pkg.plugin.context")
except Exception as e:
    print(f"❌ MCPQwenPlugin: 导入 pkg.plugin.context 失败: {type(e).__name__}: {e}")

try:
    from pkg.plugin.events import PersonNormalMessageReceived, GroupNormalMessageReceived
    print("✅ MCPQwenPlugin: 成功导入事件类")
except Exception as e:
    print(f"❌ MCPQwenPlugin: 导入事件类失败: {type(e).__name__}: {e}")

try:
    import requests
    print("✅ MCPQwenPlugin: 成功导入 requests")
except Exception as e:
    print(f"❌ MCPQwenPlugin: 导入 requests 失败: {type(e).__name__}: {e}")

try:
    import pkg.platform.types as platform_types
    print("✅ MCPQwenPlugin: 成功导入 platform.types")
except Exception as e:
    print(f"❌ MCPQwenPlugin: 导入 platform.types 失败: {type(e).__name__}: {e}")


# --- 插件主体 ---
@register(name="MCPQwenPlugin", description="通过 MCP 调用 Qwen-Plus 模型", version="1.0.0", author="yuhuai2002")
class MCPQwenPlugin(BasePlugin):
    def __init__(self, host):
        super().__init__(host)
        # --- 调试 2: 插件类是否被实例化？---
        self.ap.logger.info("🎉 MCPQwenPlugin: 插件类 __init__ 被调用，插件已成功实例化！")
        self.ap.logger.info(f"📌 插件作者: {self.author}, 版本: {self.version}")

    @handler(PersonNormalMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def handle_message(self, ctx: EventContext):
        self.ap.logger.info("📩 MCPQwenPlugin: 收到消息事件，开始处理...")

        question = ctx.event.text_message.strip()
        self.ap.logger.info(f"💬 收到消息: '{question}'")

        if not question.startswith("!qwen"):
            self.ap.logger.debug("⏭️ 消息不以 !qwen 开头，跳过处理")
            return

        query = question[5:].strip()
        if not query:
            self.ap.logger.info("⚠️ 用户只发送了 !qwen，无问题内容")
            ctx.add_return("reply", ["请在 !qwen 后输入你要问的问题"])
            ctx.prevent_default()
            return

        self.ap.logger.info(f"🚀 正在向 MCP 请求: {query}")
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
            self.ap.logger.info("✅ MCP 请求成功")
        except Exception as e:
            answer = f"请求失败：{e}"
            self.ap.logger.error(f"❌ MCP 请求失败: {type(e).__name__}: {e}")

        msg_chain = platform_types.MessageChain([
            platform_types.Plain(answer)
        ])

        await ctx.send_message(
            target_type=ctx.event.type,
            target_id=ctx.event.sender_id if ctx.event.type == "person" else ctx.event.group_id,
            message_chain=msg_chain
        )

        ctx.prevent_default()
        ctx.prevent_postorder()

        self.ap.logger.info("📤 回复已发送，处理结束")
