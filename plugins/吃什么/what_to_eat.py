from ncatbot.plugin_system import command_registry, filter_registry
from ncatbot.plugin_system import NcatBotPlugin, filter_registry
from ncatbot.plugin_system.event import NcatBotEvent
from ncatbot.utils.assets.literals import OFFICIAL_PRIVATE_MESSAGE_EVENT, OFFICIAL_GROUP_MESSAGE_EVENT
from ncatbot.core.event import BaseMessageEvent,PrivateMessageEvent,GroupMessageEvent
from ncatbot.core.event.message_segment import MessageArray, Image
from ncatbot.utils import get_log
from ncatbot.core import PrivateMessage
from urllib.parse import quote
from ncatbot.plugin_system import param
import aiohttp
import asyncio
import random
import time
from typing import Dict


LOG = get_log("WhatToEat")

BAIDU_IMG_API = "http://101.35.2.25/api/img/apihzimgbaidu.php"
BAIDU_ID = "10011705"      # ← 用户id，可以用我的
BAIDU_KEY = "e42bbda272b013ee0f445e0a15d77966"     # ← 密钥，应该也不用换

class WhatToEatPlugin(NcatBotPlugin):
    name = "WhatToEatPlugin" # 必须，插件名称，要求全局独立
    version = "1.0.2" # 必须，插件版本
    dependencies = {}  # 必须，依赖的其他插件和版本
    description = "今天吃什么" # 可选
    author = "fish" # 可选
    DISHES = ["蒸羊羔", "蒸熊掌", "蒸鹿尾儿", "烧花鸭", "烧雏鸡", "烧子鹅", "卤猪", "卤鸭", "酱鸡",
    "腊肉", "松花小肚儿", "晾肉", "香肠儿", "什锦苏盘", "清蒸八宝猪", "江米酿鸭子", "罐儿野鸡",
    "熏鸡白肚儿", "罐儿鹌鹑", "卤什件儿", "卤子鹅", "山鸡", "兔脯", "银鱼", "清蒸哈什蚂",
    "烩鸭丝", "烩鸭腰", "烩鸭条", "清拌鸭丝", "黄心管儿", "焖白鳝", "焖黄鳝", "豆豉鲇鱼",
    "锅烧鲤鱼", "菜蟒", "烀烂甲鱼", "抓炒鲤鱼", "抓炒对儿虾", "软炸里脊", "软炸鸡", "麻酥油卷儿",
    "什锦套肠儿", "卤煮寒鸦儿", "熘鲜蘑", "熘鱼脯", "熘鱼肚", "熘鱼片儿", "醋熘肉片儿", "烩三鲜",
    "烩白蘑", "烩鸽子蛋", "炒银丝", "烩鳗鱼", "炒白虾", "炝青蛤", "炒面鱼", "炒竹笋", "芙蓉燕菜",
    "炒虾仁儿", "烩虾仁儿", "烩腰花儿", "烩海参", "炒蹄筋儿", "锅烧海参", "锅烧白菜", "炸木耳",
    "炒肝尖儿", "桂花翅子", "清蒸翅子", "炸飞禽", "炸汁儿", "炸排骨", "清蒸江瑶柱", "糖熘芡仁米",
    "拌鸡丝", "拌肚丝", "什锦豆腐", "什锦丁儿", "糟鸭", "糟熘鱼片儿", "熘蟹肉", "炒蟹肉",
    "烩蟹肉", "清拌蟹肉"]
    async def on_load(self):
        LOG.info(f"{self.name} 已加载")
        self.states: Dict[str, dict] = {} 
        self.register_handler(OFFICIAL_PRIVATE_MESSAGE_EVENT, self.listen_all)
        self.register_handler(OFFICIAL_GROUP_MESSAGE_EVENT, self.listen_all)
        self.expire: Dict[str, float] = {}
    @command_registry.command("今天吃什么", aliases=["吃什么"], description="今天吃什么完整版")
    @param(name="sub", default="", help="子命令：空=正常选菜；用法=发说明书")
    async def cmd_what_to_eat(self, event: BaseMessageEvent, sub: str = ""):
        if sub == "用法":
            await event.reply(MessageArray([
                "用法",
                Image(r"plugins\what_to_eat_plugin\usage.png")
            ]))
            return
        menu = ["🍽️ 今日可选菜单："] + [f"{i+1}. {d}" for i, d in enumerate(self.DISHES)]
        menu.append("\n主人需要删掉哪些菜吗？请输入序号（不需要删就回复 0）")
        await event.reply("\n".join(menu))
        #await reply(text=None, image=None, rtf=None) -> str：私聊回复，会自动引用原消息，返回消息 ID
        self.states[event.user_id] = {"avail": self.DISHES.copy(), "selected": set(), "current": None}


    #中间这个监听有点问题于是加的real_event=event，其他块不用换，监听用户所有回复
    @filter_registry.private_filter
    @filter_registry.group_filter
    async def listen_all(self, event: NcatBotEvent):
        now = time.time()
        real_event = event.data
        uid = real_event.user_id  
        if uid in self.expire and now - self.expire[uid] > 60:
            del self.states[uid]
            del self.expire[uid]
            await real_event.reply("太久没选，本次点餐已结束~ 再想吃请重新 /今天吃什么")
            return
        text = "".join(seg.text for seg in real_event.message.filter_text()).strip()
              
        st = self.states.get(uid)

        if not st:  #直接好耶的情况，会话提前结束，不监听数字
                    return
        
        if text == "好耶":
            if uid in self.states:
                del self.states[uid]
                del self.expire[uid]
            await real_event.reply("好耶！今天就这么愉快地决定啦~ 祝你用餐愉快！")
            return   
        
        if st:
            self.expire[uid] = now 
            st = self.states.get(uid)
            if not st:
                return
            text = "".join(seg.text for seg in real_event.message.filter_text()).strip()
            if text.isdigit():    
                idx = int(text)
                avail = st["avail"]
                if idx == 0:
                    await real_event.reply("不删除，即将随机选菜...")
                elif 1 <= idx <= len(avail):
                    removed = avail.pop(idx - 1)
                    await real_event.reply(f"已删除：{removed}")
                else:
                    await real_event.reply(f"请输入 1-{len(avail)} 之间的数字")
                    return
                await self.step3_random(real_event, st)
                return

        if st.get("current") and "不想吃" in text:
            if st["current"] in st["avail"]:
                st["avail"].remove(st["current"])
            if not st["avail"]:
                await real_event.reply("没有更多菜了！请重新输入 /今天吃什么")
                del self.states[uid]
                return
            await real_event.reply(" 好的，我再为您选一个...")
            await asyncio.sleep(1)
            await self.step3_random(real_event, st)
            self.expire[uid] = now
            return
        

    async def step3_random(self, event: BaseMessageEvent, st: dict):
        dish = random.choice(st["avail"])
        st["current"] = dish
        await event.reply(f"正在为您搜索 {dish} 的图片...")
        img_url = await self.search_baidu_image(dish)
        if img_url:
            await event.reply(MessageArray([
                f"为您选择了：{dish}",
                Image(img_url),
                "主人今天吃这个吧！",
                "主人不想吃可以回复我\"不想吃，继续选哦\""
            ]))
        else:
            await event.reply(f"为您选择了：{dish}\n主人今天吃这个吧！\n不想吃请回复\"不想吃，继续选哦\"")

    async def search_baidu_image(self, keyword: str, limit: int = 1) -> str:
        params = {
            "id": BAIDU_ID,
            "key": BAIDU_KEY,
            "words": quote(keyword, encoding="utf-8"),
            "page": 1,
            "limit": limit,
            "type": 1  # 1=百度预览图
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(BAIDU_IMG_API, params=params, timeout=10) as resp:
                    data = await resp.json()
                    if data.get("code") == 200 and data.get("res"):
                        return data["res"][0]
                    LOG.warning(f"百度图片API无结果：{data.get('msg')}")
        except Exception as e:
            LOG.error(f"百度图片API调用失败：{e}")
        return ""