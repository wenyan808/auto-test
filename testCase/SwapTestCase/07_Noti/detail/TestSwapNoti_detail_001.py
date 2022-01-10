#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:10 下午
# @Author  : HuiQing Yu

import allure
import pytest
import time

from common.SwapServiceAPI import user01 as api_user01
from common.SwapServiceWS import user01 as ws_user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE, DEFAULT_SYMBOL
from tool.SwapTools import SwapTool


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapNoti_detail_001:

    contract_code = DEFAULT_CONTRACT_CODE
    ids = ['TestSwapNoti_detail_001']
    params = [{'case_name':'获取聚合行情','contract_code':contract_code}]


    @classmethod
    def setup_class(cls):
        with allure.step('挂盘'):
            cls.symbol=DEFAULT_SYMBOL
            cls.currentPrice = SwapTool.currentPrice()
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*0.8, 2), direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.currentPrice*1.2, 2), direction='sell')
            pass
        with allure.step('查看盘口是否更新'):
            for i in range(5):
                if ~SwapTool.opponentExist(symbol=cls.symbol, bids='asks'):
                    break
                else:
                    print(f'深度未更新,第{i + 1}次重试……')
                    time.sleep(1)


    @classmethod
    def teardown_class(cls):
        with allure.step('撤盘'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('ws:执行sub请求'):
            subs = {
                "sub": f"market.{params['contract_code']}.detail",
                "id": "id6"
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if 'tick' in result:
                    if result['tick']['ask'] and result['tick']['bid'] :
                        flag = True
                        break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag,'未返回预期结果'
            pass
        with allure.step('验证：返回结果各字段不为空'):
            checked_col = ['amount', 'ask', 'bid', 'close', 'count', 'high', 'id', 'low', 'open', 'vol']
            for col in checked_col:
                assert result['tick'][col], str(col) + '为None,不符合预期'

if __name__ == '__main__':
    pytest.main()