# coding=utf-8


""" 用例开关：
       True -->  跳过
       False --> 执行"""


class Skips(object):
    # 冒烟
    smoke = {"login": False,  # 登陆
             "add_order": True,  # 下单
             "cancel_order": False,  # 取消订单
             "trace": False,  # 追号
             "draw": False,  # 开奖
             "create_link": False,  # 生成推广链接
             "register": False,  # 注册下级
             "withdraw": False,  # 提现
             "recharge": False,  # 充值
             "transfer": False,  # 三方平台转账
             "dayReport": True,  # 日报表
             "teamReport": False,  # 团队报表
             "add_order_now": False,  # 秒秒彩下单
             "mmc_dayReport": True,  # 秒秒彩日报表
             "mmc_teamReport": False  # 秒秒彩团队报表
             }

    # 业务模块
    modules = {"login": True,
               "register": False,
               }
