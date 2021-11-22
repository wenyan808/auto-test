#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil
from tool.atp import ATP

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('合约交易接口')  # 这里填功能
@allure.story('市场行情接口')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.link(url='https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#a690ab6851',name='文档地址')
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_008:
    ids = ['TestSwapNoti_008']
    params = [{'case_name': '获取批量最近成交记录'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('成交'):
            cls.current_price = ATP.get_current_price()
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.current_price , 2),
                                  direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.current_price , 2),
                                  direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        with allure.step('执行接口'):
            subs = {
                     "req": "market.{}.trade.detail".format(self.contract_code),
                     "size": 5 ,
                     "id": "id8"
                    }
            result = retryUtil(ws_user01.swap_sub, subs, "data")
            pass
        with allure.step('校验返回结果'):
            checked_col = ['amount', 'quantity', 'id', 'price', 'direction', 'contract_code']
            for data in result['data']:
                for col in checked_col:
                    assert data[col] is not None, str(col) + '为None,不符合预期'
            pass


if __name__ == '__main__':
    pytest.main()
