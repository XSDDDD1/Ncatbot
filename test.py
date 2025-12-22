import requests

url = "https://s.jina.ai/?q=Jina+AI"


response = requests.get(url)

# If you need to check the response status or content, you can use:
print(response.status_code)
print(response.content)