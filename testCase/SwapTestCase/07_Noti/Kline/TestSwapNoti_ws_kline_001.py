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
class TestSwapNoti_ws_kline_001:
    ids = ['TestSwapNoti_ws_kline_001'
           ]
    params = [{'case_name': 'WS订阅K线(sub)-1min','period':'1min'}
              ]


    @classmethod
    def setup_class(cls):
        cls.contract_code = DEFAULT_CONTRACT_CODE
        cls.redisClient = redisConf('redis7001').instance()
        cls.currentPrice = SwapTool.currentPrice()
        api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*1.01, 2), direction='buy')
        api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*1.01, 2), direction='sell')

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作:执行sub请求'):
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id1"
            }
            result = ws_user01.swap_sub(subs=subs, keyword='tick')
            assert 'tick' in result,'未返回预期结果'
            pass
        with  allure.step('操作:查询redis'):
            # 1609430400 = 2021-01-01 00:00:00
            currentSecond = int(time.time()) - 1609430400
            currentSecond = int(currentSecond/60)
            key = f'market.{self.contract_code}.kline.1min.1609430400'
            redis_kline = self.redisClient.lrange(key,currentSecond,currentSecond)
            print('redis结果：',redis_kline)
            kline01 = str(redis_kline[0]).split(',')
            pass
        with allure.step('验证:返回结果与redis一致'):
            assert result['ch'] == "market."+self.contract_code+".kline."+params['period'],'topic校验失败'
            assert str(result['tick']['open']) == kline01[1],'开仓价校验与redis不一致'
            assert str(result['tick']['close']) == kline01[2],'收仓价校验与redis不一致'
            assert str(result['tick']['low']) == kline01[3],'最低价校验与redis不一致'
            assert str(result['tick']['high']) == kline01[4],'最高价校验与redis不一致'
            assert result['tick']['amount'] - float(kline01[5]) < 0.0000000001 ,'币成交量校验与redis不一致'
            assert str(result['tick']['vol']) == kline01[6],'成交张数校验与redis不一致'
            assert str(result['tick']['count']) == kline01[7],'在成笔数校验与redis不一致'
            pass


if __name__ == '__main__':
    pytest.main()
