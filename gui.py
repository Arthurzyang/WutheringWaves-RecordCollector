import os
import tkinter as tk
from tkinter import filedialog
from utils.log_parser import get_log_file_url, get_param_from_url
from utils.request_handler import send_post_request
from utils.response_saver import save_response_to_file, save_response_to_excel
from utils.statistics_calculator import calculate_statistics, calculate_five_star_intervals
import pandas as pd

def generate_project_structure(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(dirpath)))
        subindent = ' ' * 4 * (level + 1)
        for filename in filenames:
            print('{}{}'.format(subindent, filename))

def process_log_file():
    root_dir = filedialog.askdirectory()
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

# 创建GUI应用
root = tk.Tk()
root.title("Wuthering Waves Record Collector")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

select_button = tk.Button(frame, text="选择游戏根目录", command=process_log_file)
select_button.pack(padx=5, pady=5)

root.mainloop()
