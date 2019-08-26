import json
import time
import logging

import requests

from config import Config

logging.basicConfig(format='%(asctime)s, %(levelname)s: %(message)s', level=logging.INFO)
cookies = {}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "CASCID=CID2BFCADB9A0154A9D877294366E144906; sdo_cas_id=10.129.20.137; CAS_LOGIN_STATE=1; sdo_dw_track=G81Y/L1voXjLY8VH5ZWfpw==; CASTGC=ULSTGT-f0caef48519646a09e4ecee2f864e40a",
    "Host": "cas.sdo.com",
    "Pragma": "no-cache",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
}


# 提交用户名和密码, 获取ticket
def step1() -> str:
    global cookies
    params = {
        "callback": "staticLogin_JSONPMethod",
        "inputUserId": Config.login_name,
        "password": Config.login_password,
        "appId": "991000350",
        "areaId": "1001",
        "serviceUrl": "http://act.ff.sdo.com/20180707jifen/Server/SDOLogin.ashx?returnPage=index.html",
        "productVersion": "v5",
        "frameType": "3",
        "locale": "zh_CN",
        "version": "21",
        "tag": "20",
        "authenSource": "2",
        "productId": "2",
        "scene": "login",
        "usage": "aliCode",
        "customSecurityLevel": "2",
        "autoLoginFlag": "0",
        "_": int(round(time.time() * 1000)),
    }
    url = "https://cas.sdo.com/authen/staticLogin.jsonp"
    r = requests.get(url, params=params, headers=headers)
    cookie = r.cookies.items()
    for c in cookie:
        cookies.setdefault(c[0], c[1])
    text = r.text
    print(text)
    # 需要验证码
    # staticLogin_JSONPMethod({ "return_code": 0, "error_type": 0, "return_message": "", "data": { "appId": 991000350, "areaId": 1001, "checkCodeUrl": "https:\/\/login.sdo.com\/sdo\/Login\/login_alitest.php?appkey=FFFF0000000001795A0A&scene=login", "guid": "6A87E461D3FD4427B180B475D66DA763unilinuxmc", "imagecodeType": 2, "isNeedFullInfo": 0, "nextAction": 8, "sdg_height": 276, "sdg_width": 320, "sndaId": "3494960800" } })
    # 不需要验证码
    # staticLogin_JSONPMethod({ "return_code": 0, "error_type": 0, "return_message": "", "data": { "appId": 991000350, "areaId": 1001, "isNeedFullInfo": 0, "nextAction": 0, "sndaId": "3494960800", "ticket": "ULS21-74e4c0451a5d49c9a517fbdcb0f308bd" } })
    text = text[text.find("(") + 1: text.rfind(")")]
    obj = json.loads(text)
    if "ticket" in obj["data"]:
        logging.info("登录成功, 正在设置cookie...")
        return obj["data"]["ticket"]
    else:
        logging.error("登录失败, 短期内登录失败次数过多, 服务器已开启验证码, 请在1-3天后再试...")
        return ""


# 设置cookie
def step2():
    global cookies
    url = "http://login.sdo.com/sdo/Login/Tool.php"
    params = {
        "value": "index|%s" % Config.login_name,
        "act": "setCookie",
        "name": "CURRENT_TAB",
        "r": "0.8326684884385089",
    }
    # 不返回值
    r = requests.get(url, params=params, cookies=cookies)
    print("step2")
    print(r.cookies.items())
    cookie = r.cookies.items()
    for c in cookie:
        cookies.setdefault(c[0], c[1])


# 设置cookie
def step3():
    global cookies
    url = "https://cas.sdo.com/authen/getPromotionInfo.jsonp"
    params = {
        "callback": "getPromotionInfo_JSONPMethod",
        "appId": "991000350",
        "areaId": "1001",
        "serviceUrl": "http://act.ff.sdo.com/20180707jifen/Server/SDOLogin.ashx?returnPage=index.html",
        "productVersion": "v5",
        "frameType": "3",
        "locale": "zh_CN",
        "version": "21",
        "tag": "20",
        "authenSource": "2",
        "productId": "2",
        "scene": "login",
        "usage": "aliCode",
        "customSecurityLevel": "2",
        "_": "1566623599098",
    }
    r = requests.get(url, params=params, cookies=cookies)
    print("setp3")
    print(r.text)
    print(r.cookies.items())
    cookie = r.cookies.items()
    for c in cookie:
        cookies.setdefault(c[0], c[1])


# 设置cookie
def step4(ticket: str):
    global cookies
    print("setp4")
    url = "http://act.ff.sdo.com/20180707jifen/Server/SDOLogin.ashx?returnPage=index.html&ticket=" + ticket
    r = requests.get(url, cookies=cookies)
    print(r.text)
    print(r.cookies.items())
    cookie = r.cookies.items()
    for c in cookie:
        cookies.setdefault(c[0], c[1])
    logging.info("设置cookie成功...")


# 查询角色列表
def step5() -> str:
    print("step5")
    ipid = "1"
    if Config.area_name == "莫古力":
        ipid = "6"
    url = "http://act.ff.sdo.com/20180707jifen/Server/ff14/HGetRoleList.ashx"
    params = {
        "method": "queryff14rolelist",
        "ipid": ipid,
        "i": "0.8075943537407986",
    }
    r = requests.get(url, params=params, cookies=cookies)
    print(r.text)
    text = r.text
    # text = '{"Code":1,"Message":"成功","Attach":[{"cicuid":"11412792","areaName":null,"groupName":null,"realRoleName":null,"name":"南五猫大王","worldname":"JingYuZhuangYuan","characterstatus":1,"lodestoneid":null,"renameflag":false,"worldnameZh":"静语庄园","ipid":0,"groupid":24,"AreaId":0,"characterid":null},{"characterstatus":1,"cicuid":"12061680","lodestoneid":null,"name":"南五猫","renameflag":false,"worldname":"ShenYiZhiDi","areaName":null,"groupName":null,"realRoleName":null,"worldnameZh":"神意之地","ipid":0,"groupid":23,"AreaId":0,"characterid":null},{"characterstatus":1,"cicuid":"12061275","lodestoneid":null,"name":"南五猫大王","renameflag":false,"worldname":"ShenYiZhiDi","areaName":null,"groupName":null,"realRoleName":null,"worldnameZh":"神意之地","ipid":0,"groupid":23,"AreaId":0,"characterid":null},{"characterstatus":1,"cicuid":"11412830","lodestoneid":null,"name":"南五猫","renameflag":false,"worldname":"ZiShuiZhanQiao","areaName":null,"groupName":null,"realRoleName":null,"worldnameZh":"紫水栈桥","ipid":0,"groupid":4,"AreaId":0,"characterid":null}],"Success":true}'
    obj = json.loads(text)
    attach = obj["Attach"]
    role = "{0}|{1}|{2}"
    logging.info("正在获取角色列表...")
    for r in attach:
        if r["worldnameZh"] == Config.server_name and r["name"] == Config.role_name:
            logging.info("获取角色成功...")
            return role.format(r["cicuid"], r["worldname"], r["groupid"])
    logging.error("获取角色失败...")
    return ""


# 选择区服及角色
def step6(role: str):
    global cookies
    url = "http://act.ff.sdo.com/20180707jifen/Server/ff14/HGetRoleList.ashx"
    AreaId = "1"
    if Config.area_name == "莫古力":
        AreaId = "6"
    params = {
        "method": "setff14role",
        "AreaId": AreaId,
        "AreaName": Config.area_name,
        "RoleName": "[%s]%s" % (Config.server_name, Config.role_name),
        "Role": role,
        "i": "0.8326684884385089",
    }
    r = requests.post(url, params=params, cookies=cookies)
    cookie = r.cookies.items()
    for c in cookie:
        cookies.setdefault(c[0], c[1])
    logging.info("选择角色...")


# 签到
def step7():
    global cookies
    url = "http://act.ff.sdo.com/20180707jifen/Server/User.ashx"
    params = {
        "method": "signin",
        "i": "0.855755357775076"
    }
    r = requests.post(url, params=params, cookies=cookies)
    print("step7")
    print(r.text)
    print(r.cookies.items())


def main():
    ticket = step1()
    if ticket == "":
        return
    step2()
    step3()
    step4(ticket)
    role = step5()
    if role == "":
        return
    step6(role)
    print(cookies)


if __name__ == "__main__":
    main()
