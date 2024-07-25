import requests
import json

def send_post_request(data):
    """
    发送POST请求到指定的URL

    :param data: 请求体数据
    :return: 响应内容
    """
    url = "https://gmserver-api.aki-game2.com/gacha/record/query"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
