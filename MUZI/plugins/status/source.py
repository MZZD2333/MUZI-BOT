import psutil
import time
from datetime import datetime

def get_status():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    inteSENT = psutil.net_io_counters().bytes_sent / 1000000  # type: ignore
    inteRECV = psutil.net_io_counters().bytes_recv / 1000000  # type: ignore

    now = time.time()
    boot = psutil.boot_time()
    up_time = str(
        datetime.utcfromtimestamp(now).replace(microsecond=0)
        - datetime.utcfromtimestamp(boot).replace(microsecond=0)
    )
    status = (
        "当前状态:\n"
        f"* CPU: {cpu}%\n"
        f"* 内存: {mem}%\n"
        f"* 硬盘: {disk}%\n"
        f"* 发送: {inteSENT:.2f}MB\n"
        f"* 接收: {inteRECV:.2f}MB\n"
        f"* 开机: {up_time}"
    )
    return status