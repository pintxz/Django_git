import json, requests, time, random, logging
from datetime import datetime
from web import models

logger = logging.getLogger('log')


def dcits(name):
    # user_obj = models.location.objects.all()
    username = models.ask.objects.get(name=name)
    user_obj = models.location.objects.filter(prefectural=username.prefectural)
    subscript = random.randint(0, len(user_obj) - 1)
    location = user_obj[subscript]
    header = models.phone_model.objects.get(model=username.model)
    header_dict = json.loads(header.header_dict)
    result = {'dk': '', 'dz': '', 'fh': ''}
    addrId = 0

    front_url = 'https://itswkwc.dcits.com/wechatserver/sign/getSignRuleData?openId=%s' % username.openId
    try:
        informations = requests.get(front_url, headers=header_dict, verify=False)
    except:
        result['dz'] = '第一请求异常！！！'
        result['fh'] = '请联系管理员！！！'
        return result

    informations = json.loads(informations.text)
    information = informations['data']
    for addrIds in information['addressList']:
        if location.longitude[:6] == str(addrIds['attendanceLon'])[:6] and location.latitude[:5] == str(addrIds['attendanceLat'])[:5]:
            addrId = addrIds['id']
            break
    if addrId == 0:
        result['dz'] = '请求异常！！！'
        result['fh'] = '没有找到匹配的打卡地址，请联系管理员！！！'
        return result

    url = 'https://itswkwc.dcits.com/wechatserver/sign/saveSignRuleData'
    textmod = {"userId": information['employeeId'], "projectId": information['projectId'], "ruleId": information['ID'],
                "addrId": addrId, "apprUserId": information['apprUserId'], "deptId": information['deptId'],
               "workReportType": information['missionType'], "longitude": location.longitude,
               "latitude": location.latitude, "address": location.address,
               "secondAppUser": information['SECONDAPPUSER'], "imagePath": ""}
    logger.info(textmod)
    try:
        results = requests.post(url, json=textmod, headers=header_dict, verify=False)
        logger.info(results.text)
        result['dk'] = '打卡成功！'
        if '保存成功' != json.loads(results.text)['msg']:
            result['dk'] = '打卡返回值异常，请联系管理员，并去微信小程序进行核实打卡结果！'
            logger.info(results)
    except:
        result['dk'] = '打卡请求异常！！！'
        return result

    call_url = 'https://itswkwc.dcits.com/wechatserver/sign/getCard?openId=%s' % username.openId
    try:
        call_result = requests.get(call_url, headers=header_dict, verify=False)
    except:
        result['dz'] = '请求异常！！！'
        result['fh'] = '请联系管理员！！！'
        return result

    information = json.loads(call_result.text)
    result['dz'] = information['firstCard']['address']
    if 'lastCard' in information:
        result['dz'] = information['lastCard']['address']
    result['fh'] = information['msg']
    logger.info(call_result.text)

    return result
