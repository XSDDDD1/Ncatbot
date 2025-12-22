import requests
def api_call (text):
    url = "http://api.ziyi.site/voice"
    params = {
        "text" : f"{text}"
    }

    try:
        response = requests.get(url,params=params, timeout=10)
        # 检查响应状态
        if response.status_code == 200:
            return(f"{response.text.strip()}")
        else:
            return(f"请求失败，状态码: {response.status_code}"+f"{response.text}")         
    except Exception as e:
        return(f"错误: {e}")
