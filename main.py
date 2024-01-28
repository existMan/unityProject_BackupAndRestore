import os
import zipfile
from datetime import datetime
import PySimpleGUI as sg


def backup_project(source_folder, backup_folder):
    # 创建备份文件夹，如果不存在
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    # 创建备份文件的名称，包含时间戳
    dt_string = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_zip_name = f"UnityBackup_{dt_string}.zip"
    backup_zip_path = os.path.join(backup_folder, backup_zip_name)
    # 创建zip文件
    with zipfile.ZipFile(backup_zip_path, 'w') as backup_zip:
        for folder_name, folders, filenames in os.walk(source_folder):
            for filename in filenames:
                # 创建文件的绝对路径
                file_path = os.path.join(folder_name, filename)
                # 排除不需要备份的文件夹
                if "Library" in file_path or "Logs" in file_path or "Temp" in file_path:
                    continue
                # 添加文件到zip
                backup_zip.write(file_path, os.path.relpath(file_path, source_folder))
    sg.popup('备份完成！', '备份文件已保存至：', backup_zip_path)

def ask_backup_confirmation():
    layout = [
        [sg.Text('在恢复之前，是否需要备份当前项目？')],
        [sg.Button('是'), sg.Button('否')]
    ]

    window = sg.Window('备份确认', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == '否':
            window.close()
            return False
        elif event == '是':
            window.close()
            return True

def restore_project(backup_zip_path, target_folder):

    # 提示用户是否在恢复前进行备份
    backup_confirmation = ask_backup_confirmation()
    if backup_confirmation == True:
        backup_project(target_folder, os.path.dirname(target_folder))

    # 确保备份文件存在
    if not os.path.isfile(backup_zip_path):
        sg.popup_error('错误', '指定的备份文件不存在。')
        return

    # 解压备份文件到目标文件夹
    with zipfile.ZipFile(backup_zip_path, 'r') as backup_zip:
        backup_zip.extractall(target_folder)
    sg.popup('恢复完成！', '您的项目已从以下位置恢复：', backup_zip_path)

# GUI布局
layout = [
    [sg.Text('Unity项目备份与恢复工具')],
    [sg.Text('源项目文件夹'), sg.InputText(), sg.FolderBrowse()],
    [sg.Text('备份文件夹'), sg.InputText(), sg.FolderBrowse()],
    [sg.Button('备份'), sg.Button('恢复')],
    [sg.Text('备份Zip文件路径'), sg.InputText(), sg.FileBrowse()],
    [sg.Text('目标恢复项目文件夹'), sg.InputText(), sg.FolderBrowse()],
]

# 创建窗口
window = sg.Window('Unity项目备份与恢复', layout)


# 事件循环
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == '备份':
        source_folder = values[0]
        backup_folder = values[1]
        if source_folder and backup_folder:
            backup_project(source_folder, backup_folder)
    if event == '恢复':
        backup_zip_path = values[2]
        target_folder = values[3]
        if backup_zip_path and target_folder:
            restore_project(backup_zip_path, target_folder)



# 关闭窗口
window.close()
