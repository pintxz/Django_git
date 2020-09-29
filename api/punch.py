import json, requests, time, random, logging
from datetime import datetime
from web import models

logger = logging.getLogger('log')


def dcits(name):
    # user_obj = models.location.objects.all()
    username = models.ask.objects.get(name=name)
    user_obj = models.location.objects.filter(prefectural=username.prefectural)
    subscript = random.randint(1, len(user_obj))
    location = models.location.objects.get(id=subscript)
    header = models.phone_model.objects.get(model=username.model)
    header_dict = json.loads(header.header_dict)
    result = {'dk':'','dz':'','fh':''}
    url = 'https://itswkwc.dcits.com/wechatserver/sign/saveSignRuleData'
    '''
    header_dict = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mi 10 Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120  Mobile Safari/537.36 MMWEBID/4701 MicroMessenger/7.0.15.1680(0x27000FB3) Process/tools WeChat/arm64 NetType/4G Language/zh_CN ABI/arm64",
        "Content-Type": "application/json"}
    header_dict = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.17 SP-engine/2.13.0 baiduboxapp/11.17.0.13 (Baidu; P1 9) NABar/1.0",
        "Content-Type": "application/json"}
    header_dict = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 8.1.0; vivo s1 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0)",
        "Content-Type": "application/json"}
    '''
    textmod = {"userId": username.userId, "projectId": username.projectId, "ruleId": username.ruleId,
               "addrId": username.addrId, "apprUserId": username.apprUserId, "deptId": username.deptId,
               "workReportType": username.workReportType, "longitude": location.longitude,
               "latitude": location.latitude, "address": location.address,
               "secondAppUser": username.secondAppUser, "imagePath": username.imagePath}
    print(textmod)

    try:
        results = requests.post(url, json=textmod, headers=header_dict, verify=False)
    except:
        result['dk'] = '打卡请求异常！！！'
        return result

    logger.info(results.text)
    result['dk'] = '打卡成功！'
    if '保存成功' != json.loads(results.text)['msg']:
        result['dk'] = '打卡返回值异常，请联系管理员，并去微信小程序进行核实打卡结果！'
        logger.info(results)
    call_url = 'https://itswkwc.dcits.com/wechatserver/sign/getCard?openId=%s' % username.openId
    try:
        call_result = requests.get(call_url, headers=header_dict, verify=False)
    except:
        result['dz'] = '请求异常！！！'
        result['fh'] = '请联系管理员！！！'
        return result
    result['dz'] = json.loads(call_result.text)['firstCard']['address']
    result['fh'] = json.loads(call_result.text)['msg']
    logger.info(call_result.text)
    return result
