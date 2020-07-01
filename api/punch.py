import json, requests, time, random, logging
from datetime import datetime

logger = logging.getLogger('log')


def dcits(textmod):
    url = 'https://itswkwc.dcits.com/wechatserver/sign/saveSignRuleData'
    header_dict = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Mi 10 Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120  Mobile Safari/537.36 MMWEBID/4701 MicroMessenger/7.0.15.1680(0x27000FB3) Process/tools WeChat/arm64 NetType/4G Language/zh_CN ABI/arm64',
        "Content-Type": "application/json"}
    #                    Mozilla/5.0 (Linux; Android 9; MIX 3 Build/PKQ1.180729.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.18 SP-engine/2.14.0 baiduboxapp/11.18.0.12 (Baidu; P1 9) NABar/1.1
    #                    Mozilla/5.0 (Linux; Android 6.0.1; SM-J5108 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/appbrand2
    #                               (Linux; Android 10; Mi 10 Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120  Mobile Safari/537.36 MMWEBID/4701 MicroMessenger/7.0.15.1680(0x27000FB3) Process/tools WeChat/arm64 NetType/4G Language/zh_CN ABI/arm64
    #                               (Linux; U; Android 10; zh-cn; Mi 10 Build/QKQ1.191117.002) AppleWebKit/537.36 (KHTML, like Gecko)      Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/12.3.20
    try:
        result = requests.post(url, json=textmod, headers=header_dict, verify=False)
    except:
        return '打卡请求异常！！！'
    logger.info(result.text)

    call_url = 'https://itswkwc.dcits.com/wechatserver/sign/getCard?openId=ovfnh5Bjt_BojFvtBYd845ducgh4'
    try:
        call_result = requests.get(call_url, headers=header_dict, verify=False)
    except:
        return '打卡结果：%s；\n检查结果：请求异常！！！' % result.text
    logger.info(call_result.text)
    return '打卡结果：%s；\n检查结果：%s' % (result.text, call_result.text)
