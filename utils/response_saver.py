import json
import pandas as pd

def save_response_to_file(response, file_path):
    """
    将响应内容保存到文件

    :param response: 响应内容
    :param file_path: 保存文件路径
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(response, file, ensure_ascii=False, indent=4)

def save_response_to_excel(response, file_path):
    """
    将响应内容保存到Excel文件

    :param response: 响应内容
    :param file_path: 保存文件路径
    """
    # 将响应内容转换为DataFrame
    if isinstance(response, dict):
        response = response.get('data', response)

    df = pd.DataFrame(response)

    # 分类保存
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for resource_type in df['resourceType'].unique():
            df_type = df[df['resourceType'] == resource_type]
            for quality_level in df_type['qualityLevel'].unique():
                df_quality = df_type[df_type['qualityLevel'] == quality_level]
                sheet_name = f"{resource_type}_Q{quality_level}"
                df_quality.to_excel(writer, sheet_name=sheet_name, index=False)
