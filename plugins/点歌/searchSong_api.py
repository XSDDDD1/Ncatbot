import requests
def searchsong(song):
    url = "https://api.317ak.cn/api/yljk/wyyundg/wyyundg"
    params = {
        "ckey": "PMZ6KAIL52O42ZEQJO2W",
        "msg": song, #获取歌曲
        "g": 10,
        "br": 1,
        "type": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        # 检查响应状态
        if response.status_code == 200:
        
            return(response.json())


        else:
            return(f"请求失败，状态码: {response.status_code}"+f"{response.text}")         
    except Exception as e:
        return(f"错误: {e}")
