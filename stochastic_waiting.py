import time
import random


def sleep(mean=5, std_dev=2):
    """
    生成一个随机等待时间，基于正态分布。
    mean: 平均等待时间
    std_dev: 等待时间的标准差
    """
    # 生成正态分布的随机数
    wait_time = random.normalvariate(mean, std_dev)

    # 确保等待时间不为负数
    wait_time = max(0, wait_time)

    # 打印等待时间，四舍五入到两位小数
    print(f'耐心等待{wait_time:.2f}秒')

    # 等待
    time.sleep(wait_time)
