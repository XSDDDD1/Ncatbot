import requests
def getsong(song , i):
    url = "https://api.317ak.cn/api/yljk/wyyundg/wyyundg"

    params = {
        "ckey": "PMZ6KAIL52O42ZEQJO2W",
        "msg": song, #获取歌曲
        "g": 10,
        "n" : i,  #查询列表里的第几首
        "br": 4,  #音质
        "type": "mp3"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        # 检查响应状态
        if response.status_code == 200:
            return(f"{response.text.strip()}")
        else:
            return(f"请求失败，状态码: {response.status_code}"+f"{response.text}")         
    except Exception as e:
        return(f"错误: {e}")
