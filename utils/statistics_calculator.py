import pandas as pd

def calculate_statistics(df):
    """
    计算抽卡统计信息

    :param df: DataFrame 格式的抽卡数据
    :return: 统计信息字典
    """
    # 确保resourceType和qualityLevel字段存在且类型正确
    if 'resourceType' not in df.columns or 'qualityLevel' not in df.columns:
        raise ValueError("数据框缺少必要的列：resourceType或qualityLevel")

    # 将qualityLevel列转换为整数类型
    df['qualityLevel'] = df['qualityLevel'].astype(int)

    total_draws = len(df)
    stats = {
        'total_draws': total_draws,
        '3_star_weapons': len(df[(df['resourceType'] == '武器') & (df['qualityLevel'] == 3)]),
        '4_star_weapons': len(df[(df['resourceType'] == '武器') & (df['qualityLevel'] == 4)]),
        '5_star_weapons': len(df[(df['resourceType'] == '武器') & (df['qualityLevel'] == 5)]),
        '4_star_characters': len(df[(df['resourceType'] == '角色') & (df['qualityLevel'] == 4)]),
        '5_star_characters': len(df[(df['resourceType'] == '角色') & (df['qualityLevel'] == 5)])
    }

    # 计算占比
    for key in list(stats.keys()):
        if key != 'total_draws':
            stats[f'{key}_percentage'] = stats[key] / total_draws * 100 if total_draws > 0 else 0

    return stats

import pandas as pd

def calculate_five_star_intervals(df):
    """
    计算每次出QualityLevel为5的间隔和对应角色信息

    :param df: DataFrame 格式的抽卡数据
    :return: 包含每个五星角色间隔信息的列表
    """
    # 确保字段存在且类型正确
    if 'qualityLevel' not in df.columns or 'name' not in df.columns or 'time' not in df.columns:
        raise ValueError("数据框缺少必要的列：qualityLevel、name或time")

    # 将qualityLevel列转换为整数类型，time列转换为datetime类型
    df['qualityLevel'] = df['qualityLevel'].astype(int)
    df['time'] = pd.to_datetime(df['time'])

    # 获取所有五星角色的记录
    five_star_rows = df[df['qualityLevel'] == 5].sort_values(by='time')
    intervals = []
    previous_index = None

    # 计算每个五星角色之间的间隔
    for index, row in five_star_rows.iterrows():
        if previous_index is not None:
            interval = index - previous_index
            intervals.append({
                'name': row['name'],
                'interval': interval,
                'draw_time': row['time']
            })
        previous_index = index

    return intervals

