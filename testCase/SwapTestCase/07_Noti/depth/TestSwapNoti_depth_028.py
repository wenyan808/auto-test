#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : 张广南

import time
import allure
import pytest

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
from common.CommonUtils import currentPrice,opponentExist
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][4])
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestSwapNoti_depth_028:
    ids = [
        'TestSwapNoti_depth_028',
        'TestSwapNoti_depth_031',
    ]
    params = [
        {'case_name': 'WS订阅深度 150档不合并  无卖单 有买单)', 'type': 'step0'},
        {'case_name': 'WS订阅深度 20档不合并 无卖单 有买单)', 'type': 'step6'}
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.contract_code = DEFAULT_CONTRACT_CODE
            cls.symbol = DEFAULT_SYMBOL
            cls.currentPrice = currentPrice()  # 最新价
            pass
        with allure.step('挂单更新深度'):
            for i in range (5):
                api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice * (1-0.01*i), 2), direction='buy')
            pass
        with allure.step('查询redis深度更新'):
            for i in range (5):
                if opponentExist(symbol=cls.symbol,bids='bids'):
                    break
                else:
                    print('深度未更新,第{}次重试……'.format(i+1))
                    time.sleep(1)

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境，撤销挂单'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code, params['type']),
                "id": "id5"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if 'tick' in result:
                    if result['tick']['bids']:
                        flag = True
                        break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '未返回预期结果'
        with allure.step('验证：返回结果有买单'):
            assert result['tick']['bids'] is not None
            pass
        with allure.step('验证：返回结果无卖单'):
            assert 'asks' not in result['tick']
            pass


if __name__ == '__main__':
    pytest.main()
