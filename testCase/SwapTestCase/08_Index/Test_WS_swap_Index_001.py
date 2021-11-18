#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/11 2:01 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')
@allure.feature('指数基差')
@allure.story('sub订阅')
@allure.tag('Script owner : 陈维', 'Case owner : 吉龙')
@pytest.mark.stable
class Test_WS_swap_Index_001:
    ids = ['Test_WS_swap_Index_001',
           'Test_WS_swap_Index_002',
           'Test_WS_swap_Index_003',
           'Test_WS_swap_Index_004',
           'Test_WS_swap_Index_005']
    params = [{'case_name':'WS订阅指数K线数据','type':'index','period':'1min'},
              {'case_name':'WS订阅溢价指数K线数据','type':'premium_index','period':'1min'},
              {'case_name':'WS订阅预测资金费率K线数据','type':'estimated_rate','period':'1min'},
              {'case_name':'WS订阅基差数据','type':'basis','period':'1min.open'},
              {'case_name':'WS订阅标记价格K线数据','type':'mark_price','period':'1min'}]
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
        allure.dynamic.title('指数基差(sub) ' + params['case_name'])
        with allure.step('操作：执行sub请求'):
            subs =  {
                        "sub": "market.{}.{}.{}".format(self.contract_code,params['type'],params['period']),
                        "id": "id1"
                     }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub_index(subs)
                if 'tick' in result:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag
            pass
        with allure.step('验证：返回结果各字段不为空'):
            assert result['tick'] != [], 'data空值'
            # 待校验的字段
            checked_col = ['id', 'open', 'close', 'high', 'low', 'amount', 'vol', 'count']
            for col in checked_col:
                assert result['tick'][col] is not None

            pass