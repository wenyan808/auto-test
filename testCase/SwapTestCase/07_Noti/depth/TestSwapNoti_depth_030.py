#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : 张广南

import time

import allure
import pytest

from common.redisComm import redisConf
from tool.SwapTools import SwapTool
from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from common.SwapServiceAPI import user01 as api_user01


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][4])
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestSwapNoti_depth_030:
    ids = [
        'TestSwapNoti_depth_030',
        'TestSwapNoti_depth_033',
    ]
    params = [
        {'case_name': 'WS订阅深度 150档不合并  无卖单 无买单)', 'type': 'step0'},
        {'case_name': 'WS订阅深度 20档不合并 无卖单 无买单)', 'type': 'step6'}
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.currentPrice = SwapTool.currentPrice()  # 最新价
            cls.redisClient = redisConf('redis6379').instance()
            pass
        with allure.step('等待清盘'):
            for i in range(5):
                if ~SwapTool.opponentExist(symbol=cls.symbol, bids='asks'):
                    break
                else:
                    print(f'深度未更新,第{i + 1}次重试……')
                    time.sleep(1)


    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code, params['type']),
                "id": "id5"
            }
            result = ws_user01.swap_sub(subs=subs,keyword='tick')
        with allure.step('验证：返回结果无卖单'):
            assert 'asks' not in result['tick']
            pass
        with allure.step('验证：返回结果无买单'):
            assert 'bids' not in result['tick']
            pass


if __name__ == '__main__':
    pytest.main()
