#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author : HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice

@allure.epic('反向永续')
@allure.feature('合约交易接口')
@allure.story('市场行情接口')
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
            cls.current_price = currentPrice()
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
        with allure.step('操作：执行sub订阅'):
            subs = {
                     "req": "market.{}.trade.detail".format(self.contract_code),
                     "size": 5 ,
                     "id": "id8"
                    }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if 'data' in result:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag,'未返回预期结果'
            pass
        with allure.step('验证：返回data下所有字段不为空'):
            checked_col = ['amount', 'quantity', 'id', 'price', 'direction']
            for data in result['data']:
                for col in checked_col:
                    assert data[col] is not None, str(col) + '为None,不符合预期'
            pass


if __name__ == '__main__':
    pytest.main()
