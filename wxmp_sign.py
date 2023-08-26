import json
# import使用as后 只能使用简称来访问
import requests as req
# import logging as log
import urllib.parse
import uuid

#翠花科技/宝典数字化 小程序 示例店铺
cwsyh = {
    "storeName": "翠花科技/宝典数字化店铺",     #店铺名称
    "chainId": "3126",              #连锁id
    "shopId": "10705",              #店铺id
    "token": "<token>",               #header CH-TOKEN字段
    "signInId": "<SignInId>"      #SignInID，32位UUID，body字段
}

#未启用签到的店铺会提示未启用规则
xysbf = {
    "chainId": "3289",
    "shopId": "6623",
    "token": "<token>",
    "signInId": "<SignInId>"
}


smwl = {
    "storeName": "油菜花科技 店铺1",
    "token": "vjJTj25u20uyPgSUUicbr9kd"
}

hswl = {
    "storeName": "油菜花科技 店铺2",
    "token": "kXocwbm4uk6uCi8QZK1PLrTw"
}

pushplusToken = "0344b6fc88934c8fa8040fd52fad0f17"


#pushplus微信推送
def msgPersonalPush(_title: str, _content: str):
    '''
    微信推送，采用pushplus推送加，和wxplusher（预计支持）
    '''

    content = _content + str(uuid.uuid4())
    pushplusUrl = "http://www.pushplus.plus/send?token=" + pushplusToken + "&title=" + urllib.parse.quote(_title) + "&content=" + urllib.parse.quote(content)
    pushplusHeaders = {
        "Content-Type": "application/json"
    }

    # pushplusBody = {
    #     "token": pushplusToken,
    #     "title": urllib.parse.quote(_title),
    #     "content": urllib.parse.quote(_content),
    #     "channel": "wechat",
    #     "template": "html"
    # }

    resp = req.post(pushplusUrl,headers=pushplusHeaders )

    respObj = json.loads(resp.text)

    print(resp.text)

    if respObj["code"] == 200: 
        print("pushplus推送成功")
    else:
        print("pushplus推送失败")

    return




def logResult(_storeName: str, _msg: str):
    s = "【" + _storeName + "】 " + _msg
    print(s)
    # log.log(2,s)
    msgPersonalPush("python定时任务通知", s)
    return


#按顺序执行，先def函数再执行
def cuihuaSign(_chainId: str, _shopId: str, _token: str, _signInId: str, _storeName: str):
    '''
    翠花科技/宝点数字化 lzyun.vip
    每日自动签到领币

    Host: capi.lzyun.vip
    Connection: keep-alive
    Content-Length: 51
    content-type: application/json
    CH-BIZCODE: 0.14943712424370437
    CH-SHOPID: 10705
    CH-CHAINID: 3126
    CH-SEQID: 0.15802776862917034
    CH-SIGN: 123
    CH-TOKEN: _token
    CH-TIMESTAMP: 1688353286000
    CH-ISCHAIN: false
    Accept-Encoding: gzip,compress,br,deflate
    User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN
    Referer: https://servicewechat.com/wx56578536c91f32f1/4/page-frame.html
    '''
    cuihuaSignUrl = "https://capi.lzyun.vip/leaguers/signin"
    reqHeaders = {
        "Content-Type": "application/json",     #不能有分号，否则返回code=88报错
        "CH-SHOPID": _shopId,       #店铺ID
        "CH-CHAINID": _chainId,     #连锁ID，缺以上两项报http 500
        "CH-TOKEN": _token         #登录token，这里去掉逗号，否则会报缩进问题
        #"CH-TIMESTAMP": "1688353286000",
        #"CH-ISCHAIN": "false",
        #"CH-SEQID": "0.15802776862917034",
        #"CH-SIGN": "123",
        #"CH-BIZCODE": "0.14943712424370437"
    }
    
    #{"SignInID" : "74c931e6-e0e1-465f-9c97-c5864eda65ea"}
    
    reqBody = {
        "SignInID": _signInId
    }

    resp = req.post(cuihuaSignUrl, headers= reqHeaders, data= json.dumps(reqBody))
    #resp.content为bytes,vscode输出会乱码，windows terminal不会
    
    respObj = json.loads(resp.text)

    if respObj["success"]:
        logResult(_storeName, "签到成功")
    else:
        logResult(_storeName, "签到失败，原因：" + respObj["msg"])

    print(resp.text)
    return



def ychSign(_storeName: str, _token: str):
    '''
    广州油菜花 自动签到 gzych.vip
    每次登录都需要从微信方获取code，以此来换取token

    Host: pw.gzych.vip
    Content-Type: application/json
    Origin: https://res.gzych.vip
    Accept-Encoding: gzip, deflate, br
    Connection: keep-alive
    Accept: */*
    User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x1800262c) NetType/4G Language/zh_CN miniProgram/wx231fe4160b1b27b1
    Authorization: Token vjJTj25u20uyPgSUUicbr9kd
    Referer: https://res.gzych.vip/
    Accept-Language: zh-CN,zh-Hans;q=0.9
    '''

    ychSignUrl = "https://pw.gzych.vip/ykb_huiyuan/api/v1/MemberCheckIn/Submit"
    reqHeaders = {
        "Content-Type": "application/json",
        "Authorization": "Token " + _token      #推测一个店铺一个会员有唯一id
    }

    resp = req.get(ychSignUrl, headers= reqHeaders)
    respObj = json.loads(resp.text)  #一次解码，直接递归解码所有后代对象

    if respObj["ResponseStatus"]["ErrorCode"] == "0":
        logResult(_storeName, "签到成功")
    else:
        logResult(_storeName, "签到失败，原因：" + respObj["ResponseStatus"]["Message"])
    print(resp.text)
    return

def cuihuaSignProxy(_obj: dict):
    return cuihuaSign(_obj["chainId"], _obj["shopId"], _obj["token"], _obj["signInId"], _obj["storeName"])

def ychSignProxy(_obj: dict):
    return ychSign(_obj["storeName"], _obj["token"])

if __name__ == "__main__":
    cuihuaSignProxy(cwsyh)
    # ychSignProxy(smwl)
    # ychSignProxy(hswl)