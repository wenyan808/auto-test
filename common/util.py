#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


import urllib.parse
import requests
import datetime
import websocket
import json
import hmac
import base64
import hashlib
import gzip
import time

# timeout in 5 seconds:
TIMEOUT = 15


#各种请求,获取数据方式
def api_http_get(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept-language": "zh-CN",
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    # # #新加坡环境经常超时，重试到成功为止
    #Retry_times = 0
    # while True:
    #     response = requests.get(url, postdata, headers=headers, timeout=TIMEOUT)
    #     try:
    #         if response.json()['err_code'] == 403:
    #             Retry_times = Retry_times + 1
    #             continue
    #     except:
    #         try:
    #             if response.status_code == 200:
    #                 print('重试次数：', Retry_times)
    #                 return response.json()
    #             else:
    #                 print('重试次数：', Retry_times)
    #                 return response.text
    #         except Exception as e:
    #             print('重试次数：', Retry_times)
    #             return e
    #     break
    # 不重试
    try:
        response = requests.get(url, postdata, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status":"fail","msg": "%s"%e}

def api_http_post(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        "Accept-language": "zh-CN",
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    #新加坡环境经常超时，重试到成功为止
    #Retry_times = 0
    # while True:
    #     response = requests.post(url, postdata, headers=headers, timeout=TIMEOUT)
    #     try:
    #         if response.json()['err_code'] == 403:
    #             Retry_times = Retry_times + 1
    #
    #             continue
    #     except:
    #         try:
    #             if response.status_code == 200:
    #                 print('重试次数：', Retry_times)
    #                 return response.json()
    #             else:
    #                 print('重试次数：', Retry_times)
    #                 return response.text
    #         except Exception as e:
    #             print('重试次数：', Retry_times)
    #             return e
    #     break
    # 不重试
    try:
        response = requests.post(url, postdata, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status":"fail","msg": "%s"%e}


def api_key_get(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = url
    host_name = urllib.parse.urlparse(host_url).hostname.lower()
    params['Signature'] = createSign(params, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path
    return api_http_get(url, params)


def api_key_post(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = url
    host_name = urllib.parse.urlparse(host_url).hostname.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return api_http_post(url, params)



def order_http_get(host,request_path,params,hbsession):
    headers = {
        "Content-type": "application/json; charset=UTF-8",
        "Accept-language": "zh-CN",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "source": "web",
        "hbsession": hbsession
    }
    url = host + request_path + '?' + params
    try:
        response = requests.get(url=url, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status":"fail","msg": "%s"%e}



def order_http_post(host,request_path,params,hbsession):
    headers = {
        "Content-type": "application/json; charset=UTF-8",
        "Accept-language": "zh-CN",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "source": "web",
        "hbsession": hbsession
    }
    url = host + request_path
    data = json.dumps(params)
    try:
        response = requests.post(url=url, data=data, headers=headers, timeout=TIMEOUT)
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status":"fail","msg": "%s"%e}



def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature
















""" 下面的方法是ws用的 """
#鉴权订阅
def api_key_sub(url, access_key, secret_key, subs):
    host_url = urllib.parse.urlparse(url).hostname.lower()
    print(host_url)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    data = {
        "AccessKeyId": access_key,
        "SignatureMethod": "HmacSHA256",
        "SignatureVersion": "2",
        "Accept-language": "zh-CN",
        "Timestamp": timestamp
    }
    # sign = createSign(data, "GET", host_url, '/linear_swap_notification', secret_key)
    sign = createSign(data, "GET", host_url, '/notification', secret_key)
    data["op"] = "auth"
    data["type"] = "api"
    data["Signature"] = sign
    try:
        ws = websocket.create_connection(url)
        msg_str = json.dumps(data)
        print("msg_str is:",msg_str)
        ws.send(msg_str)
        msg_result =json.loads(gzip.decompress(ws.recv()).decode())
        print("msg_result is:",msg_result)
        sub_str = json.dumps(subs)
        print("sub_str is:",sub_str)
        ws.send(sub_str)
        sub_result = json.loads(gzip.decompress(ws.recv()).decode())
        print("sub_result is :",sub_result)
        ws.close()
        return sub_result
    except Exception as e:
        print("Sub failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}

#普通订阅
def sub(url,subs):
    try:
        ws = websocket.create_connection(url)
        sub_str = json.dumps(subs)
        ws.send(sub_str)
        sub_result = json.loads(gzip.decompress(ws.recv()).decode())
        ws.close()
        return sub_result
    except Exception as e:
        print("Sub failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}



