#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author :  HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][0])
@pytest.mark.stable
@allure.link(url='https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#0d9cec2a3b',name='文档地址')
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_006:
    ids = ['TestSwapNoti_006']
    params = [{'case_name': '批量Overview'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：执行sub订阅'):
            subs = {
                  "op": "sub",
                  "sub": "market.overview",
                  "zip": 1
                }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                result = ws_user01.swap_sub(subs=subs)
                if 'data' in result:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i + 1}次重试………………………………')
            assert flag
            pass
        with allure.step('验证：返回结果data字段下字段不为空'):
            checked_col = ['amount','symbol','close','count','high','low','open','vol']
            for data in result['data']:
                for col in checked_col:
                    assert data[col] is not None,str(col)+'为None,不符合预期'

            pass
if __name__ == '__main__':
    pytest.main()
