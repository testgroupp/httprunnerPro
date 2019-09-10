# coding=utf-8


""" 用例开关：
       ON -->  执行
       OFF --> 跳过"""


class Skips(object):
    # 冒烟
    smoke = {"login": "OFF",  # 登陆
             "add_order": "OFF",  # 下单
             "cancel_order": "ON",  # 取消订单
             "trace": "ON",  # 追号
             "draw": "ON",  # 开奖
             "create_link": "ON",  # 生成推广链接
             "register": "ON",  # 注册下级
             "withdraw": "ON",  # 提现
             "recharge": "ON",  # 充值
             "transfer": "ON",  # 三方平台转账
             "dayReport": "OFF",  # 日报表
             "teamReport": "ON",  # 团队报表
             "add_order_now": "ON",  # 秒秒彩下单
             "mmc_dayReport": "OFF",  # 秒秒彩日报表
             "mmc_teamReport": "ON"  # 秒秒彩团队报表
             }

    # 业务模块
    modules = {"login": "OFF",
               "register": "ON",
               }
