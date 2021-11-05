#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211013
# @Author : 
    用例标题
        WS订阅K线(sub) 1min
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        id、open、close、low、high价格正确；amount、vol、count值正确,不存在Null,[]
    优先级
        0
    用例别名
        TestLinearNoti_ws_kline_001
"""
from common.LinearServiceWS import t as linear_service_ws
import pytest, allure, random, time
from tool.atp import ATP
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('正向永续')  # 这里填业务线
@allure.feature('WS订阅')  # 这里填功能
@allure.story('WS订阅K线(sub)')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestLinearNoti_ws_kline_001:

    ids = [ "TestLinearNoti_ws_kline_001",
            "TestLinearNoti_ws_kline_002",
            "TestLinearNoti_ws_kline_003",
            "TestLinearNoti_ws_kline_004",
            "TestLinearNoti_ws_kline_005",
            "TestLinearNoti_ws_kline_006",
            "TestLinearNoti_ws_kline_007",
            "TestLinearNoti_ws_kline_008",
            "TestLinearNoti_ws_kline_009",
            "TestLinearNoti_ws_kline_019"]
    params = [
        {
            "case_name": "1min",
            "period": "1min"
        },{
            "case_name": "5min",
            "period": "5min"
        },{
            "case_name": "15min",
            "period": "15min"
        },{
            "case_name": "30min",
            "period": "30min"
        },{
            "case_name": "60min",
            "period": "60min"
        },{
            "case_name": "4hour",
            "period": "4hour"
        },{
            "case_name": "1day",
            "period": "1day"
        },{
            "case_name": "1week",
            "period": "1week"
        },{
            "case_name": "1mon",
            "period": "1mon"
        },{
            "case_name": "",
            "period": "1min"
        }
    ]
    contract_code = DEFAULT_CONTRACT_CODE

    @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        allure.dynamic.title("WS订阅K线(sub) "+params['case_name'])
        with allure.step('发送sub请求'):
            subs = {
                "sub": "market.{}.kline.{}".format(self.contract_code, params['period']),
                "id": "id1"
            }

            tryTimes = 1
            while True:
                result = linear_service_ws.linear_sub(subs)
                # 由于Kline可能更新有点慢，等1秒，再执行一次获取结果；避免失败用例造成死循环；这里重试5次
                if 'tick' in result:
                    break
                else:
                    # 超过5次，跳过循环
                    if tryTimes > 5:
                        break
                    else:
                        tryTimes = tryTimes + 1
                        time.sleep(1)
                        print('WS未返回预期数据，等待1秒，第', tryTimes - 1, '次重试………………')
            pass
            with allure.step('校验响应结果'):
                # 请求topic校验
                assert result['ch'] == "market." + self.contract_code + ".kline." + params['period']
                # 开仓价校验，不为空
                assert result['tick']['open'] is not None
                # 收仓价校验
                assert result['tick']['close'] is not None
                # 最低价校验,不为空
                assert result['tick']['low'] is not None
                # 最高价校验,不为空
                assert result['tick']['high'] is not None
                # 币的成交量
                assert result['tick']['amount'] >= 0
                # 成交量张数。 值是买卖双边之和
                assert result['tick']['vol'] >= 0
                # 成交笔数。 值是买卖双边之和
                assert result['tick']['count'] >= 0
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
