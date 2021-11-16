#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from tool.atp import ATP
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil
from common.redisComm import reid7001Conn

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(req 传参from,to)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_010:
    ids = ['TestSwapNoti_ws_kline_010'
           ]
    params = [{'case_name': '1min','period':'1min'}
              ]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('成交更新k线'):
            cls.currentPrice = ATP.get_current_price()  # 最新价
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice, 2), direction='sell')
            time.sleep(1)#等待成交k线更新
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    # @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title('WS订阅K线(req)' + params['period'])
        with allure.step('执行sub请求'):
            self.toTime = int(time.time())
            self.fromTime = self.toTime - 60 * 10
            subs = {
                "req": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id4",
                "from": self.fromTime,
                "to": self.toTime
            }
            result = retryUtil(ws_user01.swap_sub,subs,'data')
            pass
        with  allure.step('查询redis'):
            # 1609430400 = 2021-01-01 00:00:00
            currentSecond = int(time.time()) - 1609430400
            currentSecond = int(currentSecond / 60)
            key = 'market.{}.kline.1min.1609430400'.format(self.contract_code)
            redis_kline = reid7001Conn.lrange(key, currentSecond, currentSecond)
            print(redis_kline)
            kline01 = str(redis_kline[0]).split(',')
            pass
        with allure.step('校验返回结果：非空校验'):
            # 请求topic校验
            for data in result['data']:
                # 开仓价校验，不为空
                assert data['open'] is not None
                # 收仓价校验
                assert data['close'] is not None
                # 最低价校验,不为空
                assert data['low'] is not None
                # 最高价校验,不为空
                assert data['high'] is not None
                # 币的成交量
                assert data['amount'] >= 0
                # 成交量张数。 值是买卖双边之和
                assert data['vol'] >= 0
                # 成交笔数。 值是买卖双边之和
                assert data['count'] >= 0
            pass
        with allure.step('验证点：最后一个1min的数据与redis结果对比校验'):
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
        with allure.step('验证点：最后一条数据与当前时间对比校验'):
            assert int(time.time()) - result['data'][dataLen]['id']  < 60
            pass
        with allure.step('验证点：数据连续性校验'):
            for i in range(len(result['data'])):
                if i == len(result['data'])-1:
                    break
                # 开仓价校验，不为空
                assert result['data'][i]['id'] + 60 == result['data'][i+1]['id']
            pass
if __name__ == '__main__':
    pytest.main()
