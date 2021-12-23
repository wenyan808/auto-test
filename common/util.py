#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


import base64
import datetime
import gzip
import hashlib
import hmac
import json
import time
import urllib.parse

import requests
import websocket
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA

# timeout in 5 seconds:
TIMEOUT = 15


# 各种请求,获取数据方式
def api_http_get(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept-language": "zh-CN",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    try:
        if params:
            response = requests.get(
                url=url, params=urllib.parse.urlencode(params), headers=headers, timeout=TIMEOUT)
        else:
            response = requests.get(
                url,  headers=headers, timeout=TIMEOUT)
        print('\033[1;32;49m%s\033[0m' %
              '\n请求地址= {}\n请求参数 = {}'.format(url, str(params)))
        print('\033[1;32;49m%s\033[0m' %
              '返回结果 = {}'.format(str(response.json())))
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}


def api_http_form_post(url, params, add_to_headers=None):
    headers = {
        "Accept": "text/plain, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-language": "zh-CN",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    try:
        print('\033[1;32;49m%s\033[0m' % "\n请求地址 = {}".format(url),
              '\033[1;32;49m%s\033[0m' % "\n参数 = {}".format(params),
              '\033[1;32;49m%s\033[0m' % "\nHeader = {}".format(headers))
        response = requests.post(
            url=url, params=params, headers=headers, timeout=TIMEOUT)
        print('\033[1;32;49m%s\033[0m' %
              "响应结果 = {}".format(str(response.content, 'utf-8')))
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}


def api_http_post(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json',
        "Accept-language": "zh-CN",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    try:
        print('\033[1;32;49m%s\033[0m' % "\n请求地址 = {}".format(url),
              '\033[1;32;49m%s\033[0m' % "\n参数 = {}".format(postdata),
              '\033[1;32;49m%s\033[0m' % "\nHeader = {}".format(headers))
        response = requests.post(
            url, postdata, headers=headers, timeout=TIMEOUT)
        print('\033[1;32;49m%s\033[0m' %
              "响应结果 = {}".format(str(response.text)))
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}


def api_key_get(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = url
    host_name = urllib.parse.urlparse(host_url).hostname.lower()
    params['Signature'] = createSign(
        params, method, host_name, request_path, SECRET_KEY)
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
    params_to_sign['Signature'] = createSign(
        params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + \
        urllib.parse.urlencode(params_to_sign)
    return api_http_post(url, params)


def order_http_get(host, request_path, params, hbsession):
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
        return {"status": "fail", "msg": "%s" % e}


def order_http_post(host, request_path, params, hbsession):
    headers = {
        "Content-type": "application/json; charset=UTF-8",
        "Accept-language": "zh-CN",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0",
        "source": "web",
        "hbsession": hbsession,
        "HB-PRO-TOKEN": "vk9w87vqyVg74DLLDwhnIqzwOH-KsLVkYgEc6-QFoqAY-uOP2m0-gvjE57ad1qDF",
    }
    url = host + request_path
    data = json.dumps(params)
    try:
        print("请求地址 = ", url, "参数 = ", data)
        response = requests.post(url, data, headers=headers, timeout=TIMEOUT)
        print("响应结果 = ", str(response.text))
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
    except Exception as e:
        print("httpPost failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}


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


# 鉴权订阅
def api_key_sub(url, access_key, secret_key, subs, path='/notification'):
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
    sign = createSign(data, "GET", host_url, path, secret_key)
    data["op"] = "auth"
    data["type"] = "api"
    data["cid"] = '11538447'
    data["Signature"] = sign
    try:
        ws = websocket.create_connection(url+path)
        msg_str = json.dumps(data)
        print("msg_str is:", msg_str)
        ws.send(msg_str)
        msg_result = json.loads(gzip.decompress(ws.recv()).decode())
        print("msg_result is:", msg_result)
        sub_str = json.dumps(subs)
        print("sub_str is:", sub_str)
        ws.send(sub_str)
        sub_result = json.loads(gzip.decompress(ws.recv()).decode())
        print("sub_result is :", sub_result)
        ws.close()
        return sub_result
    except Exception as e:
        print("Sub failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}


# 普通订阅
def sub(url, subs, keyword=None):
    try:
        ws = websocket.create_connection(url)
        sub_str = json.dumps(subs)
        print('\033[1;32;49m%s\033[0m' % f'\nWS请求信息：\n\turl={url},\n\t参数={str(subs)}' )
        ws.send(sub_str)
        sub_result = json.loads(gzip.decompress(ws.recv()).decode())
        if keyword:
            for i in range(3):
                if keyword in sub_result:
                    break
                else:
                    print(f'返回数据中无关键key={keyword},实际结果={sub_result},第{i+1}次重试……')
                    sub_result = json.loads(gzip.decompress(ws.recv()).decode())

        result_info = '请求结果：\n\t'+str(sub_result)
        print('\033[1;32;49m%s\033[0m' % result_info)
        ws.close()
        return sub_result
    except Exception as e:
        print("Sub failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}


""" 公共常用函数 """


# def compare_dict(expected: dict, actual: dict) -> bool:
#     for k, v in expected.items():
#         v_actual = actual.get(k, None)
#         if not v_actual:
#             # 没找到可能是0值，也可能是None
#             if v_actual != 0:
#                 raise Exception("{expected_k_v} not found in actual".format(expected_k_v={k: v}))
#         if actual.get(k) != expected.get(k):
#             raise Exception("expected: {expected_k_v}, actual: {actual_k_v}".format(expected_k_v={k: v}, actual_k_v={k: actual.get(k)}))
#     return True

def compare_dict(expected, result):
    err = 0
    for key in expected:
        if key not in result:
            print('结果里没有预期的项：', key)
            print(result)
            err = err + 1
            continue
        if isinstance(result[key], int) or isinstance(result[key], float):
            if float(result[key]) != float(expected[key]):
                print('%s的值实际和预期不一致，实际：%s，预期：%s' %
                      (key, result[key], expected[key]))
                err = err + 1
        else:
            if str(result[key]) != str(expected[key]):
                print('%s的值实际和预期不一致，实际：%s，预期：%s' %
                      (key, result[key], expected[key]))
                err = err + 1
    if err == 0:
        return True
    else:
        return False


def compare_dictkey(expected, result):
    err = 0
    for key in expected:
        if key not in result:
            print('结果里没有预期的项：', key)
            print(result)
            err = err + 1
            continue
    if err == 0:
        return True
    else:
        return False


def rsa_encrpt(password, public_key):
    rsakey = RSA.importKey(public_key)
    cipher = Cipher_pksc1_v1_5.new(rsakey)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()
