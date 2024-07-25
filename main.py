import os
import pandas as pd
from utils.log_parser import get_log_file_url, get_param_from_url
from utils.request_handler import send_post_request
from utils.response_saver import save_response_to_file, save_response_to_excel
from utils.statistics_calculator import calculate_statistics, calculate_five_star_intervals

def main():
    # 提示用户输入游戏根目录路径
    root_dir = input("请输入游戏根目录路径: ").strip()
    log_file_path = os.path.join(root_dir, 'Wuthering Waves Game', 'Client', 'Saved', 'Logs', 'Client.log')

    if not os.path.isfile(log_file_path):
        print(f"日志文件未找到: {log_file_path}")
        return

    url = get_log_file_url(log_file_path)
    if url:
        params = get_param_from_url(url)
        print("提取的URL参数:")
        for key, value in params.items():
            print(f"{key}: {value}")

        # 发送POST请求
        response = send_post_request(params)
        print("服务器响应:")
        print(response)

        # 确保Response文件夹存在
        response_dir = os.path.join(os.getcwd(), 'Response')
        os.makedirs(response_dir, exist_ok=True)
        save_txt_path = os.path.join(response_dir, 'response.txt')
        save_excel_path = os.path.join(response_dir, 'response.xlsx')

        # 删除已存在的文件以避免权限错误
        if os.path.exists(save_txt_path):
            os.remove(save_txt_path)
        if os.path.exists(save_excel_path):
            os.remove(save_excel_path)

        # 保存响应到文件
        save_response_to_file(response, save_txt_path)
        save_response_to_excel(response, save_excel_path)
        print(f"响应已保存到文件: {save_txt_path} 和 {save_excel_path}")

        # 计算统计信息并保存
        df = pd.DataFrame(response.get('data', []))
        stats = calculate_statistics(df)
        stats_file_path = os.path.join(response_dir, 'statistics.txt')
        with open(stats_file_path, 'w', encoding='utf-8') as file:
            for key, value in stats.items():
                file.write(f"{key}: {value}\n")
        print(f"统计信息已保存到文件: {stats_file_path}")

        # 计算五星角色间隔信息并保存
        intervals = calculate_five_star_intervals(df)
        intervals_file_path = os.path.join(response_dir, 'five_star_intervals.txt')
        with open(intervals_file_path, 'w', encoding='utf-8') as file:
            for interval in intervals:
                file.write(f"Name: {interval['name']}, Interval: {interval['interval']} draws, Draw Time: {interval['draw_time']}\n")
        print(f"五星角色间隔信息已保存到文件: {intervals_file_path}")

    else:
        print("日志文件中未找到卡池链接。")

if __name__ == "__main__":
    main()
