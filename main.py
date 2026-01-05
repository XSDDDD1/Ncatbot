# ========= 导入必要模块 ==========
from ncatbot.core import BotClient

# ========== 创建 BotClient ==========
bot = BotClient()

# ========== 启动 BotClient==========
bot.run_frontend(
    bt_uin="3032969320",   # 机器人 QQ
)  


#pip install -U ncatbot -i https://mirrors.aliyun.com/pypi/simpley 