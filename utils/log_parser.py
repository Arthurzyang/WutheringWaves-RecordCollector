import re

def get_log_file_url(file_path):
    """
    从日志文件读取卡池链接

    :param file_path: 日志文件路径
    :return: 卡池链接字符串或None
    """
    pattern = re.compile(r"https.*/aki/gacha/index.html#/record[?=&\w\-]+")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                matcher = pattern.search(line)
                if matcher:
                    return matcher.group(0)
    except IOError as e:
        print(f"Error reading file: {e}")
    return None

def get_param_from_url(url):
    """
    获取卡池链接的参数

    :param url: 卡池链接
    :return: 参数字典
    """
    parameters = {
        "playerId": "",
        "recordId": "",
        "cardPoolId": "",
        "cardPoolType": "1",
        "serverId": "",
        "languageCode": ""
    }
    param_string = url.split('?')[1]
    pairs = param_string.split('&')

    for pair in pairs:
        key, value = pair.split('=')
        if key == "player_id":
            parameters["playerId"] = value
        elif key == "record_id":
            parameters["recordId"] = value
        elif key == "resources_id":
            parameters["cardPoolId"] = value
        elif key == "gacha_type":
            parameters["cardPoolType"] = value
        elif key == "svr_id":
            parameters["serverId"] = value
        elif key == "lang":
            parameters["languageCode"] = value

    return parameters
