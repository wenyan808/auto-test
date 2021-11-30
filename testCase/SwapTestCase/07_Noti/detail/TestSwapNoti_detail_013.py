#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/15 2:26 下午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][2])
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapNoti_detail_013:
    ids = ['TestSwapNoti_detail_013']
    params = [{'case_name':'WS订阅 OverView'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('执行sub订阅'):
            subs = {
                "op": "sub",
                "sub": "market.overview",
                "zip": 1
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
            assert flag, '未返回预期结果'
            pass
            pass
        with allure.step('验证：返回结果各字段不为空'):
            checked_col = ['amount', 'symbol', 'close', 'count', 'high', 'low', 'open', 'vol']
            for data in result['data']:
                for col in checked_col:
                    assert data[col] is not None, str(col) + '为None,不符合预期'

if __name__ == '__main__':
    pytest.main()