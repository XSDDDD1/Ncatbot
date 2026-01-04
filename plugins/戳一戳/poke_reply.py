import time
import random
from collections import deque
from ncatbot.utils import ncatbot_config
from ncatbot.plugin_system import NcatBotPlugin
from ncatbot.plugin_system import filter_registry
from ncatbot.core.event import NoticeEvent

class PokeReplyPlugin(NcatBotPlugin):
    name = "PokeReply"
    version = "1.2.0"
    """
    1.1.0新增私聊回戳
    1.1.1修复了一直回戳的BUG
    1.1.2新增戳一戳人的名称
    1.2.0新增一分钟戳三次随机冷却功能

    """
    
    async def on_load(self):
        self.poke_time: deque[float] = deque() # 存取戳一戳的双端队列，存60s
        self.cd : float = 0.0 #冷却时间
        self.register_handler(
            "ncatbot.notice_event",
            self.on_poke,
            priority=10
        )
    
    async def on_poke(self, event):



        notice: NoticeEvent = event.data
        if notice.notice_type != "notify" or notice.sub_type != "poke":        # 先过滤子类型，过滤出戳一戳这个类型，其他notify通知事件直接跳过
            return
        
        now = time.time()

        if now < self.cd:  #没过cd，后续啥都不干
            return
        if notice.user_id == ncatbot_config.bt_uin or notice.target_id != ncatbot_config.bt_uin:  #首先发起拍一拍人的id不能是机器人本身，其次被拍人不能是机器人以外的人
            return        
        
        while self.poke_time and self.poke_time[0] < now - 60:  #将超过60s的弹出
            self.poke_time.popleft()         
        self.poke_time.append(now) #存入这次的戳一戳时间

        if len(self.poke_time)>=3: #先跳过再进cd，免得在cd期间+cd
            minutes = (random.randint(5,10)) #随机冷却5-10分钟
            self.cd = now + minutes* 60
            await self.api.post_group_msg(   group_id=notice.group_id,text=f"呜呜被戳傻了喵！休息 {minutes} 分钟在玩吧~")
            return

        if notice.group_id :
            await self.api.send_poke(user_id=notice.user_id,group_id=notice.group_id)# 回戳
            time.sleep(0.5)#先戳再回复
            await self.api.post_group_msg(group_id=notice.group_id,text="不要戳我QAQ！")  # 回复消息   (以后再搞随机文本)
        else :
            await self.api.send_poke(user_id=notice.user_id)# 回戳
            time.sleep(0.5)
            await self.api.post_private_msg(notice.user_id,text="不要戳我QAQ！")   # 回复消息