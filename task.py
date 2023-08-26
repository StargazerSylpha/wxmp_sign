import schedule
import wxmp_sign as sign
from datetime import datetime

def logInfo(_s: str):
    print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"] " + _s)

# @schedule.repeat(schedule.every().minute.at(":30"))
def wxmpSignTask():
    print("===================")
    logInfo("小程序签到")
    sign.cuihuaSignProxy(sign.cwsyh)
    print("===================")

def heartbeat():
    logInfo("心跳验证")


def func():
    # 定时任务 https://blog.csdn.net/cy15625010944/article/details/126281559
    schedule.clear()
    # schedule.every().minute.at(":30").do(wxmpSignTask)
    schedule.every().day.at("00:10").do(wxmpSignTask)
    # schedule.every().hour.at(":05").do(heartbeat)
    logInfo("task启动成功")
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    # 启动py文件
    func()


