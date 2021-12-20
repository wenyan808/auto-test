#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211012
# @Author : HuiQing Yu

import time
import allure
import pytest

from tool.SwapTools import SwapTool, opponentExist
from common.SwapServiceAPI import user01 as api_user01
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][4])
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_restful_depth_001:
    contract_code = DEFAULT_CONTRACT_CODE
    ids = [
        'TestSwapNoti_restful_depth_023',
        'TestSwapNoti_restful_depth_024',
    ]
    params = [
        {'case_name': 'restful请求最优挂单 传参合约code)', 'contract_code': contract_code},
        {'case_name': 'restful请求最优挂单 不传参合约code)', 'contract_code': ''},
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):
            cls.symbol = DEFAULT_SYMBOL
            cls.currentPrice = currentPrice()  # 最新价
            cls.bestBuyPrice = round(cls.currentPrice * (1 - 0.01 * 1), 2)
            cls.bestSellPrice = round(cls.currentPrice * (1 + 0.01 * 1), 2)
            pass
        with allure.step('挂单更新深度'):
            for i in range(5):
                api_user01.swap_order(contract_code=cls.contract_code,
                                      price=round(cls.currentPrice * (1 - 0.01 * i), 2), direction='buy')
                api_user01.swap_order(contract_code=cls.contract_code,
                                      price=round(cls.currentPrice * (1 + 0.01 * i), 2), direction='sell')
            pass
        with allure.step('查询redis深度更新'):
            for i in range(5):
                if opponentExist(symbol=cls.symbol, asks='asks', bids='bids'):
                    break
                else:
                    print('深度未更新,第{}次重试……'.format(i + 1))
                    time.sleep(1)

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境，撤销挂单'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            result = api_user01.swap_bbo(contract_code=params['contract_code'])
            pass
        with allure.step('验证：返回结果买单卖单为最优单'):
            assert result['ticks'][0]['bid'][0] == self.bestBuyPrice
            assert result['ticks'][0]['ask'][0] == self.bestSellPrice
            pass


if __name__ == '__main__':
    pytest.main()
