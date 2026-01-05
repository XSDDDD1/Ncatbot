from ncatbot.plugin_system import NcatBotPlugin, command_registry
from ncatbot.core.event import BaseMessageEvent
import random
import json

class KFC_V50(NcatBotPlugin):
    name = "KFC_V50"
    version = "1.0.0"
    
    
    async def on_load(self):
        pass
        
       
    @command_registry.command("KFC")
    async def kfc(self, event: BaseMessageEvent):
        with open(r"plugins\KFC_VME50\kfc.json", 'r', encoding='utf-8') as f:
            parsed_data = json.load(f)
        await event.reply(random.choice(parsed_data)["text"])