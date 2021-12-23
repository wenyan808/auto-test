#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from tool.SwapTools import SwapTool
from common.redisComm import redisConf
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_010:
    ids = ['TestSwapNoti_ws_kline_010'
           ]
    params = [{'case_name': 'WS请求K线(req)-1min','period':'1min'}
              ]
    contract_code = DEFAULT_CONTRACT_CODE
    redisClient = redisConf('redis7001').instance()

    @classmethod
    def setup_class(cls):
        with allure.step('成交更新k线'):
            cls.currentPrice = SwapTool.currentPrice()  # 最新价
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作:执行sub请求'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 10
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs=subs)
                if 'data' in result:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i+1}次重试………………………………')
            assert flag,'重试3次未返回预期结果'
            pass
        with  allure.step('操作:查询redis'):
            # 1609430400 = 2021-01-01 00:00:00
            currentSecond = int(time.time()) - 1609430400
            currentSecond = int(currentSecond / 60)
            key = 'market.{}.kline.1min.1609430400'.format(self.contract_code)
            redis_kline = self.redisClient.lrange(key, currentSecond, currentSecond)
            kline01 = str(redis_kline[0]).split(',')
            pass
        with allure.step('验证：返回字段非空'):
            # 请求topic校验
            for data in result['data']:
                assert data['open'],'开仓价校验失败'
                assert data['close'],'收仓价校验失败'
                assert data['low'],'最低价校验失败'
                assert data['high'],'最高价校验失败'
                assert data['amount']>=0,'币的成交量校验失败'
                assert data['vol']>=0,'成交量张数校验失败'
                assert data['count']>=0,'成交笔数校验失败'
            pass
        with allure.step('验证：最后一个1min的数据与redis结果对比校验'):
            # 请求topic校验
            assert result['rep'] == "market."+self.contract_code+".kline."+params['period']
            dataLen=len(result['data'])- 1
            # 开仓价校验，不为空
            assert str(result['data'][dataLen]['open']) == kline01[1]
            # 收仓价校验
            assert str(result['data'][dataLen]['close']) == kline01[2]
            # 最低价校验,不为空
            assert str(result['data'][dataLen]['low']) == kline01[3]
            # 最高价校验,不为空
            assert str(result['data'][dataLen]['high']) == kline01[4]
            # 币的成交量
            assert result['data'][dataLen]['amount'] - float(kline01[5]) < 0.0000000001 #取9位小数精度
            # 成交量张数。 值是买卖双边之和
            assert str(result['data'][dataLen]['vol']) == kline01[6]
            # 成交笔数。 值是买卖双边之和
            assert str(result['data'][dataLen]['count']) == kline01[7]
            pass
        with allure.step('验证：最后一条数据与当前时间对比校验'):
            assert int(time.time()) - result['data'][dataLen]['id']  < 60
            pass
        with allure.step('验证：数据连续性校验'):
            for i in range(len(result['data'])):
                if i == len(result['data'])-1:
                    break
                # 开仓价校验，不为空
                assert result['data'][i]['id'] + 60 == result['data'][i+1]['id']
            pass
if __name__ == '__main__':
    pytest.main()
