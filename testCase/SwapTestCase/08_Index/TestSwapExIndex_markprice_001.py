#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/11 2:01 下午
# @Author  : yuhuiqing

import pytest, allure, random, time
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE

@allure.epic('反向永续')
@allure.feature('指数基差')
@allure.story('标记价格')
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
@pytest.mark.stable
class TestSwapExIndex_markprice_001:
    ids = ['TestSwapExIndex_markprice_001',
           'TestSwapExIndex_markprice_002',
           'TestSwapExIndex_markprice_003',
           'TestSwapExIndex_markprice_004',
           'TestSwapExIndex_markprice_005',
           'TestSwapExIndex_markprice_006',
           'TestSwapExIndex_markprice_007',
           'TestSwapExIndex_markprice_008',
           'TestSwapExIndex_markprice_009']
    params = [{'case_name':'1min','period':'1min'},
              {'case_name':'5min','period':'5min'},
              {'case_name':'15min','period':'15min'},
              {'case_name':'30min','period':'30min'},
              {'case_name':'60min','period':'60min'},
              {'case_name':'4hour','period':'4hour'},
              {'case_name':'1day','period':'1day'},
              {'case_name':'1week','period':'1week'},
              {'case_name':'1mon','period':'1mon'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step(''):
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('标记价格' + params['case_name'])
        with allure.step('操作：执行req请求'):
            To = int(time.time())
            From = To - 60 * 60 * 24
            subs = {
                "req": "market.{}.mark_price.{}".format(self.contract_code, params['period']),
                "id": "id1",
                "from": From,
                "to": To
            }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub_index(subs)
                if result['data']:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag
            pass
        with allure.step('验证：返回结果各字段不为空'):
            assert result['data'], 'data空值'
            # 待校验的字段
            checked_col = ['id', 'open', 'close', 'high', 'low', 'amount', 'vol', 'count']
            for data in result['data']:
                for col in checked_col:
                    assert data[col] is not None

            pass