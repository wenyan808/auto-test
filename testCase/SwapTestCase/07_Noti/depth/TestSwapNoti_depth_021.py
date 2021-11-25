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

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('行情')  # 这里填功能
@allure.story('深度')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 张广南', 'Case owner : 吉龙')
class TestSwapNoti_depth_021:
    contract_code = DEFAULT_CONTRACT_CODE
    symbol = DEFAULT_SYMBOL
    ids = [
        'TestSwapNoti_depth_021',
        'TestSwapNoti_depth_022',
    ]
    params = [
        {'case_name': 'WS订阅深度 合约代码大写)', 'contract_code': contract_code},
        {'case_name': 'WS订阅深度 合约代码大小写)', 'contract_code': symbol+'-usd'}
    ]

    @classmethod
    def setup_class(cls):
        with allure.step('实始化变量'):

            cls.currentPrice = currentPrice()  # 最新价
            pass
        with allure.step('挂单更新深度'):
            for i in range (2):
                api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice * (1-0.01*i), 2), direction='buy')
                api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice * (1+0.01*i), 2), direction='sell')
            pass
        with allure.step('查询redis深度更新'):
            for i in range (5):
                if opponentExist(symbol=cls.symbol,asks='asks',bids='bids'):
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
                "sub": "market.{}.depth.step6".format(params['contract_code']),
                "id": "id5"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if 'tick' in result:
                    if result['tick']['asks'] and result['tick']['bids']:
                        flag = True
                        break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '未返回预期结果'
            pass
        with allure.step('验证：返回结果买单卖单不为空'):
            assert result['tick']['bids']
            assert result['tick']['asks']


if __name__ == '__main__':
    pytest.main()
