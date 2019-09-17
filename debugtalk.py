# coding=utf-8
from hashlib import md5
import random
from decimal import Decimal
import time
import requests
import datetime
from config.skip import Skips


def get_next_issue(issue, i):
    """
    获取后n期 的期数
    :param issue: 当前期数
    :param i:  后第几期
    :return:
    """
    nums = issue.split('-')[1]
    n = len(nums)  # 期数格式
    target = issue.split('-')[0] + '-' + str(int(nums) + i).zfill(n)
    return target


def to_md5(password):
    """
    md5加密
    :param password:
    :return:
    """
    h = md5()
    h.update(password.encode(encoding='utf-8'))
    return h.hexdigest()


def pro_username(start_with='de'):
    """
    生成随机用户名
    :param start_with:
    :return:
    """
    username = start_with + str(random.randint(100, 999999999999))
    return username


def to_point(point):
    """
    返点模式转换
    :param point:
    :return:
    """
    r = float(Decimal(str(point)) * Decimal('100'))
    return r


# def not_eq(extract, expect):
#     """
#     自定义断言：两者不相等
#     :param extract:
#     :param expect:
#     :return:
#     """
#     assert extract != expect


def set_lottery_code(base_url, lotteryCode, t=6):
    """
    获取采种code并判断当期剩余投注时间，若小于 t,则等待下期开盘时再返回code
    :param  base_url:
    :param lotteryCode: 目标采种编码
    :param t: 设定目标时间,默认6s
    :return:
    """
    r = requests.get(base_url + '/lottery/api/call/v1/lottery/times')
    last_time = r.json()["result"]["time"][lotteryCode]
    if last_time < t:
        time.sleep(last_time + 2)
    return lotteryCode


def get_mmc_code(base_url):
    """
    获取不同平台秒秒彩对应编码
    :param base_url:平台域名
    :return:
    """
    code = 'WBGMMC'
    if 'moj' in base_url:
        code = 'MJMMC'
    return code


def get_transfer_msg(platform):
    """
    根据不同环境指定预期响应
    :param platform:
    :return:
    """
    if 'TK' in platform:
        msg = ["测试环境不允许转账，如需转账请联系管理员", "success"]
    else:
        msg = ["success"]
    return msg


def wait_to_trace(times, lotteryCode):
    """
    等待追号完成
    :param times: 各采种时间
    :param lotteryCode: 采种编码
    :return:
    """
    t = times[lotteryCode]
    ts = int(t) + 60
    print("等待追号 %s秒" % ts)
    while ts > 0:
        time.sleep(10)
        ts = ts - 10
        if ts <= 10:
            print("%s.." % ts)
            time.sleep(ts)
            break
        print("%s.." % ts)
    print("追号结束！")


def get_report_time():
    """
    获取报表查询起始时间（当天）
    :return:
    """
    today = datetime.date.today()
    t = today.strftime('%Y/%m/%d')
    return t


def get_query_start_time():
    """
    查询起始时间(当天)
    :return:
    """
    t = get_report_time() + ' 00:00'
    return t


def get_query_end_time():
    """
    查询结束时间（当天）
    :return:
    """
    t = get_report_time() + ' 23:59'
    return t


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"}


def add_favorite(base_url, lotteryCode, uid, cookies):
    """
    添加常玩游戏
    :param base_url:
    :param lotteryCode: 采种编码
    :param uid: 用户id
    :param cookies:
    :return:
    """
    urlDel = '/lottery/api/u/v1/lottery/delLotteryFavorite'
    urlAdd = '/lottery/api/u/v1/lottery/addLotteryFavorite'
    urlGet = '/lottery/api/u/v1/lottery/getLotteryFavorite'
    data = {"lottery": lotteryCode}
    list_F = requests.get(base_url + urlGet, headers=headers, cookies=cookies).json()["result"]
    for li in list_F:
        if li["user_id"] == uid and li["lottery_code"] == lotteryCode:
            print("用户已在常玩游戏中设置该游戏，自动移除设置...")
            requests.get(base_url + urlDel, params=data, headers=headers, cookies=cookies)
            print("移除成功")
    requests.get(base_url + urlAdd, params=data, headers=headers, cookies=cookies)
    print("添加到常玩列表")
    list_L = requests.get(base_url + urlGet, headers=headers, cookies=cookies).json()["result"]
    for li in list_L:
        if li["user_id"] == uid and li["lottery_code"] == lotteryCode:
            print("添加成功")
            return True
    else:
        print("添加失败")
        return False


def del_favorite(base_url, lotteryCode, uid, cookies):
    """
    删除常玩游戏
    :param base_url:
    :param lotteryCode: 采种编码
    :param uid: 用户id
    :param cookies:
    :return:
    """
    urlDel = '/lottery/api/u/v1/lottery/delLotteryFavorite'
    urlAdd = '/lottery/api/u/v1/lottery/addLotteryFavorite'
    urlGet = '/lottery/api/u/v1/lottery/getLotteryFavorite'
    data = {"lottery": lotteryCode}
    list_F = requests.get(base_url + urlGet, headers=headers, cookies=cookies).json()["result"]
    for li in list_F:
        if li["user_id"] == uid and li["lottery_code"] == lotteryCode:
            print("从常玩列表中删除")
            requests.get(base_url + urlDel, params=data, headers=headers, cookies=cookies)
            break
    else:
        print("用户暂未将此采种设置到常玩列表，自动添加...")
        requests.get(base_url + urlAdd, params=data, headers=headers, cookies=cookies)
        print("添加完成，准备删除..")
        requests.get(base_url + urlDel, params=data, headers=headers, cookies=cookies)
    list_L = requests.get(base_url + urlGet, headers=headers, cookies=cookies).json()["result"]
    for li in list_L:
        if li["user_id"] == uid and li["lottery_code"] == lotteryCode:
            print("删除失败")
            return False
    else:
        print("删除成功")
        return True


def get_draw_statu(base_url, times, lotteryCode, cookies):
    """
    等待开奖并获取订单中奖状态
    :param base_url:
    :param times:
    :param lotteryCode:
    :param cookies:
    :return:
    """
    url = base_url + '/lottery/api/u/v1/lottery/recent_order?lottery=%s' % lotteryCode
    last_time = times[lotteryCode]
    ts = int(last_time) + 10
    print("等待开奖，预计时间%s秒" % ts)
    while ts > 0:  # 等待开奖
        time.sleep(10)
        ts = ts - 10
        if ts <= 10:
            print("%s秒" % ts)
            time.sleep(ts)
            break
        print("%s秒" % ts)

    r = requests.get(url, cookies=cookies, headers=headers)
    statu = r.json()["result"][0]["status"]
    t = 50
    while t > 0:
        if statu != "未开奖":
            print("开奖成功！")
            time.sleep(3)  # 等数据进报表
            break
        else:
            print("开奖延时，再等待5秒！")
            time.sleep(5)
            t = t - 5
            r = requests.get(url, cookies=cookies, headers=headers)
            statu = r.json()["result"][0]["status"]
    if statu == "未开奖":
        print("开奖失败！")
    return statu


def teardown_hook_reset_payPassword(response, cookies, base_url, payPassword, newPassword):
    """
    还原支付密码
    :param response: 请求响应
    :param cookies:
    :param base_url:
    :param payPassword: 支付密码
    :param newPassword:过滤密码
    :return:
    """
    url_reset = '/sobet/userInfo/updatePayPassword'
    data = {"oldPassword": to_md5(newPassword),
            "newPassword": to_md5(payPassword),
            "confirm_password": to_md5(payPassword),
            "desPassword": "4860B1E277464DB150B87714D462E93300EEB35C43665871"}
    if response.json["msg"] == "success":
        print("密码修改成功，准备还原..")
        r = requests.post(base_url + url_reset, data=data, cookies=cookies, headers=headers)
        if r.json()["msg"] == "success":
            print("密码还原成功")
        else:
            print("密码还原失败！")
    else:
        print("密码修改失败！")


def teardown_hook_reset_password(response, cookies, base_url, password, newPassword):
    """
    还原登录密码
    :param response:
    :param cookies:
    :param base_url:
    :param password:
    :param newPassword:
    :return:
    """
    url_reset = '/sobet/userInfo/updatePasswordAjax'
    data = {"oldPassword": to_md5(newPassword),
            "newPassword": to_md5(password),
            "confirm_password": to_md5(password),
            "desPassword": "4860B1E277464DB1C804E426A2405196"}
    if response.json["result"]["msg"] == "密码修改成功!":
        print("密码修改成功，准备还原..")
        r = requests.post(base_url + url_reset, data=data, cookies=cookies, headers=headers)
        if r.json()["result"]["msg"] == "密码修改成功!":
            print("密码还原成功")
        else:
            print("密码还原失败！")
    else:
        print("密码修改失败！")


def teardown_hook_no_contract_alert(response):
    """
    未签订过分红契约提示
    :param response:
    :return:x
    """
    list_ = response.json["result"]["list"]
    if (list_ == []) is True:
        print("\033[31;43;1m该用户上级暂未向其发起契约签订申请！！！")
    else:
        for li in list_:
            if li["status"] == "1":
                break
        else:
            print("\033[31;43;1m该用户暂无已签订的契约！！！")


def login_admin(base_url, username):
    """
    后台登录：admin,获取登录cookies
    :param base_url:
    :param username:
    :return:
    """
    url_login = base_url + "/admin/pages/PreAdminUser/login.do"
    url_admin = base_url + "/admin/pages/OtherSystem/lotteryLogin.do"
    data_login = {"name": username, "pwd": "Li/uUFeGhQV6sJncTG7OhQ=="}
    r_login = requests.post(url_login, data=data_login, headers=headers)
    data_admin = {"pid": 430}
    r_admin = requests.post(url_admin, data=data_admin, cookies=r_login.cookies, headers=headers)
    url = eval(r_admin.text)[0]["url"]
    r = requests.post("http:" + url, headers=headers)
    headers_ = r.request.headers  # 携带cookies
    return headers_


def get_expect_money(m1, m2):
    """
    获取报表预期金额
    :param m1:
    :param m2:
    :return:
    """
    r = str(Decimal(str(m1)) + Decimal(str(m2)))
    return r


def get_expect_draw_status(mode, odds):
    """
    获取全选订单预期 状态值
    :param mode: 投注模式
    :param odds: 对应玩法奖金组
    :return:
    """
    # status = (Decimal(str(odds)) / (Decimal('2') / Decimal(str(mode)))).quantize(Decimal('0.0000'))
    status = float(odds) / (2 / float(mode))
    s = '%.4f' % status  # 保留四位小数,字符串类型
    return s


def get_bet_money(order):
    """
    获取注单金额
    :param order:
    :return:
    """
    print("等待3秒，数据进报表..")
    time.sleep(3)  # 等待数据进报表
    t = eval(order)[0]["amount"]
    print("投注金额%s" % t)
    return t


skips = Skips()


def skip_case(skip, case):
    """
    用例开关
    :param skip: 开关名
    :param case: 用例名
    :return:
    """
    s = skips.__getattribute__(skip)
    r = str(s[case]).lower()
    if r == "off":
        return True
    else:
        return False


def to_string(s):
    """
    类型转换 --> 字符串
    :param s:
    :return:
    """
    return str(s)


def gen_card_num(start_with='622609', total_num=16):
    """
    生成随机银行卡号
    :param start_with:
    :param total_num:
    :return:
    """
    result = start_with
    # 随机生成前N-1位
    while len(result) < total_num - 1:
        result += str(random.randint(0, 9))

    # 计算前N-1位的校验和
    s = 0
    card_num_length = len(result)
    for _ in range(2, card_num_length + 2):
        t = int(result[card_num_length - _ + 1])
        if _ % 2 == 0:
            t *= 2
            s += t if t < 10 else t % 10 + t // 10
        else:
            s += t

    # 最后一位当做是校验位，用来补齐到能够整除10
    t = 10 - s % 10
    result += str(0 if t == 10 else t)
    return result


def get_question_id(cookies, base_url):
    """
    获取密保问题编号
    :param cookies:
    :param base_url:
    :return:
    """
    url_info = '/sobet/userInfo/userCenterAjax'
    try:
        r = requests.get(base_url + url_info, headers=headers, cookies=cookies)
        qids = r.json()["result"]["userInfo"]["securityQuestion"]
        qid = qids[:qids.rfind(',')]
        return qid
    except Exception as e:
        print("\033[31;43;1m请确认该账号是否已设置密保问题！！！\t", e)


def get_answers(cookies, base_url):
    """
    获取密保答案
    :param cookies:
    :param base_url:
    :return:
    """
    url_info = '/sobet/userInfo/userCenterAjax'
    try:
        r = requests.get(base_url + url_info, headers=headers, cookies=cookies)
        answers = r.json()["result"]["userInfo"]["securityAnswer"]
        answer = answers[:answers.rfind(',')]
        return answer
    except Exception as e:
        print("\033[31;43;1m请确认该账号是否已设置密保问题！！！\t", e)


def get_usable_lower(contracts, users):
    """
    获取可用下级代理账号：没有待签约契约
    :param contracts: 下级契约列表
    :param users: 下级列表
    :return:
    """
    names_ = []  # 有待签订状态契约用户
    if (contracts != []) is True:
        for con in contracts:
            if con["status"] == '0':
                names_.append(con["userName"])
    for user in users:
        if user["userType"] == 1 and user["userName"] not in names_:
            return user["userName"]
    else:
        print("\033[31;43;1m暂无可新增契约的下级,请检查！！！")
        return "暂无可新增契约的下级，请检查！！！"
