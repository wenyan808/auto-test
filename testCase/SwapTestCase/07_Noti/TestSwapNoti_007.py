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
class TestSwapNoti_007:
    ids = ['TestSwapNoti_007']
    params = [{'case_name': '获取最新成交记录'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('成交'):
            # cls.current_price = ATP.get_current_price()
            # api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.current_price , 2),
            #                       direction='buy')
            # api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.current_price , 2),
            #                       direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        with allure.step('执行接口'):
            subs = {
                     "sub": "market.{}.trade.detail".format(self.contract_code),
                     "id": "id7"
                    }
            result = retryUtil(ws_user01.swap_sub, subs, ["tick", "data"])
            pass
        with allure.step('校验返回结果'):
            checked_col = ['amount', 'quantity', 'id', 'price', 'direction', 'direction']
            for data in result['tick']['data']:
                for col in checked_col:
                    assert data[col] is not None, str(col) + '为None,不符合预期'
                    allure.step('字段' + str(col) + "不为空校验通过")

            pass


if __name__ == '__main__':
    pytest.main()
