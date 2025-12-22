from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.core.event import BaseMessageEvent
from ncatbot.plugin_system import on_message
from .getSong_api import getsong
from .searchSong_api import searchsong
class GetSongPlugin(NcatBotPlugin):
    name = "GetSongPlugin"
    version = "1.0.1"

    def extract_text(self, message_array):
       # 从消息段中提取纯文本
        return "".join(seg.text for seg in message_array.filter_text())

    async def on_load(self):
        #留空
        pass


#点歌=====================================================

    @on_message
    async def order1(self, event: BaseMessageEvent):

        if event.user_id == "2465838253":  #过滤白÷
            return


#其实是我穷尽了，系统自带的方法是识别不了带空格的歌曲名的，guzuoyixia
        text = self.extract_text(event.message).strip()
        if text.startswith("/点歌 ") or text.startswith("/song ") or text.startswith("/dg "):  #识别开头是否为指定格式的指令
            song = text.split(" ", 1)[1].strip()       #分割指令后的字符
            
            if song.split()[-1].isdigit() :   # 检查点歌时有没有带参数，没有就默认第一首
                i= int(song.split()[-1])    # 获取参数
                song = " ".join(song.split()[:-1]) #去掉数字
            else :
                i = 1

            if song:
                result = getsong(song , i)
                await event.reply(result)
                
            if not song:
                await event.reply("歌名不能为空！\n正确用法：/点歌 告白气球 [参数](获取查歌列表中的对应的歌曲，选填)")
                return
    

#查歌====================================================

    @on_message
    async def order2(self, event: BaseMessageEvent):

        if event.user_id == "2465838253":  #过滤白÷
            return
        

        text = self.extract_text(event.message).strip()
        if text.startswith("/查歌 ") or text.startswith("/cg "):
            song = text.split(" ", 1)[1].strip()

            if not song:
                await event.reply("歌名不能为空！\n正确用法：/查歌 告白气球")
                return

            if song:
                data = searchsong(song)

                lines = []
                for idx, item in enumerate(data["result"], start=1):
                    lines.append(
                        f"{idx}、\n"
                        f"歌名：{item.get('name', '未知')}\n"
                        f"作者：{item.get('artists', '未知')}\n"
                    )
                await event.reply("".join(lines))

            