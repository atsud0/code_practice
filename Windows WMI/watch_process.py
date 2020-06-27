"""

使用Win32 api接口做各種各樣的事情.

暫時構想:

枚舉目標機器的各類信息(服務,自啓動項,運行的進程,共享目錄等)
當枚舉以上信息完畢後,由用戶選擇是否開啓監控.

目前已實現
- 列出已運行進程
- 共享目錄
- 自啓動項
- 服務狀態
- 監控後續打開的進程
- 枚舉機器用戶



TODO:
格式化輸出
在輸出中篩選出對後續滲透流程有幫助的信息
添加其他枚舉的信息
把信息都寫到一個文件裏?

"""
import win32con
import win32api
import win32security
import wmi
import sys
import os

# 初始化wmi接口

c = wmi.WMI()


def log_to_file(message):
    with open("./process_monitor_log.csv", "ab") as file:
        file.write("{}\r\n".format(message).encode())


def watch_process():
    # 寫監控日誌文件頭
    log_to_file("Time,User,Executable,CommandLine,PID,Parent PID,Privileges")
    # 創建一個進程監控
    process_watcher = c.Win32_Process.watch_for("creation")

    while True:
        try:
            new_process = process_watcher()
            proc_owner = new_process.GetOwner()
            proc_owner = "{}\\{}".format(proc_owner[0], proc_owner[2])  # 域/用戶
            create_date = new_process.CreationDate  # 進程創建日期
            executable = new_process.ExecutablePath  # 進程的執行文件名字
            cmdline = new_process.CommandLine  # 進程的執行文件所在
            pid = new_process.ProcessId  # 進程的ID
            parent_pid = new_process.ParentProcessId  # 進程的父進程的ID
            privileges = "N/A"  # 權限

            # 格式化輸出
            process_log_message = "{},{},{},{},{},{},{}".format(create_date, proc_owner, executable, cmdline, pid,
                                                                parent_pid, privileges)

            # 在終端打印輸出
            print(process_log_message)

            log_to_file(process_log_message)
        except Exception as error:
            print(error)
            pass


"""
列出已經在運行的進程的進程
"""


def list_now_process():
    print("-" * 100 + "Process" + "-" * 100)
    for process in c.Win32_Process():
        # 打印進程的執行文件名字+進程ID+進程名+進程狀態
        print(process.ExecutablePath, process.ProcessID, process.Name, process.Status)
    print("-" * 100 + "END" + "-" * 100)


"""
查看自啓動項
"""


def Look_Startup_Command():
    for command in c.Win32_StartupCommand():
        # 位置,標題,命令
        print("{}\t{}\t{}".format(command.Location, command.Caption, command.Command))


"""
查看共享目錄
"""


def Look_Share_Path():
    print("Name\tPath\t")
    for share in c.Win32_Share():
        print("{}\t{}\t".format(share.Name, share.Path))


"""
枚舉服務
"""


def Look_Service():
    for service in c.Win32_Service():
        print(service.Caption, service.Name, service.State, service.PathName, service.StartName)


"""
枚舉主機用戶名
"""


def Look_User_Account():
    for Account in c.Win32_UserAccount():
        print("Domain:{}\nName:{}\nSID:{}\nDisable:{}".format(Account.Domain, Account.Name, Account.SID,
                                                              Account.Disabled), end="\n{}\n".format("-" * 50))


def main():
    Look_Startup_Command()
    Look_Share_Path()
    Look_User_Account()

    char = input("Enable Watch Process?(Y/N):")
    if char == 'Y':
        watch_process()
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
