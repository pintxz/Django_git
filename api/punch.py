import json, requests, random, logging
from web import models

logger = logging.getLogger('log')


def dcits(request,name):
    logger.info('-------------------------------%s开始！------------------------------' % name)
    # user_obj = models.location.objects.all()
    username = models.ask.objects.get(name=name)
    user_obj = models.location.objects.filter(prefectural=username.prefectural)
    subscript = random.randint(0, len(user_obj) - 1)
    location = user_obj[subscript]
    # header = models.phone_model.objects.get(model=username.model)
    # header_dict = json.loads(header.header_dict)
    header_dict = {
        "User-Agent":request.environ['HTTP_USER_AGENT'],
        "Content-Type": "application/json"
    }
    result = {'dk': '', 'dz': '', 'fh': ''}
    addrId = 0

    front_url = 'https://itswkwc.dcits.com/wechatserver/sign/getSignRuleData?openId=%s' % username.openId
    logger.info('请求：%s' % front_url)
    try:
        informations = requests.get(front_url, headers=header_dict, verify=False)
    except:
        result['dz'] = '第一请求异常！！！'
        result['fh'] = '请联系管理员！！！'
        logger.info('-------------------------------%s结束！------------------------------' % name)
        return result

    informations = json.loads(informations.text)
    logger.info('information值：%s' % informations)
    information = informations['data']
    logger.info('information值：%s' % information)
    for addrIds in information['addressList']:
        if location.longitude[:6] == str(addrIds['attendanceLon'])[:6] and location.latitude[:5] == str(
                addrIds['attendanceLat'])[:5]:
            addrId = addrIds['id']
            break
    if addrId == 0:
        result['dz'] = '请求异常！！！'
        result['fh'] = '没有找到匹配的打卡地址，请联系管理员！！！'
        logger.info('----没有找到匹配的打卡地址，请联系管理员！！！----%s结束！------------------------------' % name)
        return result

    url = 'https://itswkwc.dcits.com/wechatserver/sign/saveSignRuleData'
    textmod = {"userId": information['employeeId'], "projectId": information['PROJECTID'], "ruleId": information['ID'],
               "addrId": addrId, "apprUserId": information['apprUserId'], "deptId": information['deptId'],
               "workReportType": information['missionType'], "longitude": location.longitude,
               "latitude": location.latitude, "address": location.address,
               "secondAppUser": information['SECONDAPPUSER'], "imagePath": ""}
    logger.info('请求：%s' % url)
    logger.info('参数：%s' % textmod)
    try:
        results = requests.post(url, json=textmod, headers=header_dict, verify=False)
        logger.info(results.text)
        result['dk'] = '打卡成功！'
        if '保存成功' != json.loads(results.text)['msg']:
            result['dk'] = '打卡返回值异常，请联系管理员，并去微信小程序进行核实打卡结果！'
            logger.info(results)
    except:
        result['dk'] = '打卡请求异常！！！'
        logger.info('-------------------------------%s结束！------------------------------' % name)
        return result

    call_url = 'https://itswkwc.dcits.com/wechatserver/sign/getCard?openId=%s' % username.openId
    logger.info('请求：%s' % call_url)
    try:
        call_result = requests.get(call_url, headers=header_dict, verify=False)
    except:
        result['dz'] = '请求异常！！！'
        result['fh'] = '请联系管理员！！！'
        logger.info('-------------------------------%s结束！------------------------------' % name)
        return result

    informationz = call_result.text
    logger.info(call_result.text)
    result['dz'] = informationz[informationz.rfind('address') + 11:informationz.rfind('secondAppUser') - 4]
    result['fh'] = informationz[informationz.rfind('msg'):len(informationz) - 1]
    logger.info('-------------------------------%s结束！------------------------------' % name)
    return result
