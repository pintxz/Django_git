

import json, requests


header_dict = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Mi 10 Build/QKQ1.191117.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.120  Mobile Safari/537.36 MMWEBID/4701 MicroMessenger/7.0.15.1680(0x27000FB3) Process/tools WeChat/arm64 NetType/4G Language/zh_CN ABI/arm64",
    "Content-Type": "application/json"}


call_url = 'https://itswkwc.dcits.com/wechatserver/sign/getSignRuleData?openId=ovfnh5KiLsE4C19Seo8Zk5s7YGGE'

call_result = requests.get(call_url, headers=header_dict, verify=False)


informations = json.loads(call_result.text)
information = informations['data']
# print(information['data'])


longitude = '112.569605'
latitude = '37.813705'
print(longitude[:6])
print(latitude[:5])


print(information['addressList'])
for addrIds in information['addressList']:
    if longitude[:5] == str(addrIds['attendanceLon'])[:5] and latitude[:4] == str(addrIds['attendanceLat'])[:4]:
        addrId = addrIds['id']
        break


textmod = {"userId": information['employeeId'], "projectId": information['projectId'], "ruleId": information['ID'],
           "addrId": addrId, "apprUserId": information['apprUserId'], "deptId": information['deptId'],
           "workReportType": information['missionType'], "longitude": 'location.longitude',
           "latitude": 'location.latitude', "address": 'location.address',
           "secondAppUser": information['SECONDAPPUSER'], "imagePath": ''}
print(textmod)
