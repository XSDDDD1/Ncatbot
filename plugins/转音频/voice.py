from .getVoice_api import api_call
from ncatbot.plugin_system import command_registry
from ncatbot.core.event import BaseMessageEvent
from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.core import MessageArray, Record

class GetVoicePlugin(NcatBotPlugin):
    name = "GetVoicePlugin"
    version = "1.0.1"

    async def on_load(self):
        pass

    @command_registry.command("tts")
    async def tts(self, event: BaseMessageEvent,text :str):

        
        if event.user_id == "2465838253":  #过滤白÷
            return
        

        if not text.strip():
            await event.reply("文本信息不能为空！\n正确用法:/tts 文本信息")
        try:

            url = api_call(text)  #获取语音url
            voice = MessageArray(Record(url))#转语音条

            if hasattr(event, "group_id"):  #输出回去            
                await self.api.post_group_array_msg(event.group_id, voice)
            else:
                await self.api.post_private_array_msg(event.user_id, voice)

        except Exception as e:
            await event.reply(f"❌ 语音发送失败：{e}")