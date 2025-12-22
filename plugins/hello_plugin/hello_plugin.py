from ncatbot.utils import ncatbot_config
from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.plugin_system import command_registry
from ncatbot.plugin_system import filter_registry
from ncatbot.core.event import BaseMessageEvent, PrivateMessageEvent , GroupMessageEvent

class HelloPlugin(NcatBotPlugin):
    name = "HelloPlugin"
    version = "1.0.0"

    async def on_load(self):
        # 可留空，保持轻量
        pass

    @command_registry.command("help")
    async def hello_cmd(self, event: BaseMessageEvent):

        
        if event.user_id == "2465838253":  #过滤白÷
            return
        

        await event.reply("\n查找歌曲，获取歌曲列表：/查歌 歌曲名称"
            "\n\n获取歌曲文件（不一定有）：/点歌 歌曲名称 [参数](获取查歌列表中的对应的歌曲，选填)"
        "\n\n将文本转换为语音输出：/tts 文本信息"
        "\n\n戳一戳回戳（双击机器人头像）"
        "\n\n以上所有指令均支持首字母缩写"
        "\n\n================"
        "\n机器人聊天功能：@机器人发送文本即可聊天"
        "\n\n重置人格和记忆：/reset"
        "\n\n切换人格（建议先重置）：/set人格 人格" \
        "\n\n人格列表：/list人格")

    """
    @filter_registry.private_filter
    async def on_private_msg(self, event: PrivateMessageEvent):
        await event.reply("你发送了一条私聊消息！")
    """