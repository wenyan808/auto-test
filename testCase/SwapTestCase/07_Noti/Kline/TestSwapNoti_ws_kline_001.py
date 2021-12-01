#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice
from common.redisComm import redisConf
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][6])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_ws_kline_001:
    ids = ['TestSwapNoti_ws_kline_001'
           ]
    params = [{'case_name': 'WS订阅K线(sub)-1min','period':'1min'}
              ]
    contract_code = DEFAULT_CONTRACT_CODE
    redisClient = redisConf('redis7001').instance()

    @classmethod
    def setup_class(cls):
        cls.currentPrice = currentPrice()
        api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*1.01, 2), direction='buy')
        api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*1.01, 2), direction='sell')

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作:执行sub请求'):
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id1"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1,4):
                result = ws_user01.swap_sub(subs)
                if 'tick' in result:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag
            pass
        with  allure.step('操作:查询redis'):
            # 1609430400 = 2021-01-01 00:00:00
            currentSecond = int(time.time()) - 1609430400
            currentSecond = int(currentSecond/60)
            key = 'market.{}.kline.1min.1609430400'.format(self.contract_code)
            redis_kline = self.redisClient.lrange(key,currentSecond,currentSecond)
            print('redis结果：',redis_kline)
            kline01 = str(redis_kline[0]).split(',')
            pass
        with allure.step('验证:返回结果与redis一致'):
            # 请求topic校验
            assert result['ch'] == "market."+self.contract_code+".kline."+params['period']
            # 开仓价校验，不为空
            assert str(result['tick']['open']) == kline01[1]
            # 收仓价校验
            assert str(result['tick']['close']) == kline01[2]
            # 最低价校验,不为空
            assert str(result['tick']['low']) == kline01[3]
            # 最高价校验,不为空
            assert str(result['tick']['high']) == kline01[4]
            # 币的成交量
            assert result['tick']['amount'] - float(kline01[5]) < 0.0000000001 #取9位小数精度
            # 成交量张数。 值是买卖双边之和
            assert str(result['tick']['vol']) == kline01[6]
            # 成交笔数。 值是买卖双边之和
            assert str(result['tick']['count']) == kline01[7]
            pass


if __name__ == '__main__':
    pytest.main()
