#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/11 2:01 下午
# @Author  : yuhuiqing
from tool.atp import ATP
import pytest, allure, random, time
from common.mysqlComm import orderSeq as DB_orderSeq
from common.SwapServiceAPI import user01
from common.SwapServiceWS import user01 as ws_user01
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import retryUtil

@allure.epic('反向永续')
@allure.feature('指数基差')
@allure.story('预测资金费率')
@allure.tag('Script owner : 余辉青', 'Case owner : ')
@pytest.mark.stable
class TestSwapExIndex_estimatedrate_001:
    ids = ['TestSwapExIndex_estimatedrate_001',
           'TestSwapExIndex_estimatedrate_002',
           'TestSwapExIndex_estimatedrate_003',
           'TestSwapExIndex_estimatedrate_004',
           'TestSwapExIndex_estimatedrate_005',
           'TestSwapExIndex_estimatedrate_006',
           'TestSwapExIndex_estimatedrate_007',
           'TestSwapExIndex_estimatedrate_008',
           'TestSwapExIndex_estimatedrate_009']
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

    # @pytest.mark.flaky(reruns=3, reruns_delay=3)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title('预测资金费率 ' + params['case_name'])
        with allure.step('执行req请求'):
            To = int(time.time())
            From = To - 60
            subs = {
                "req": "market.{}.premium_index.{}".format(self.contract_code, params['period']),
                "id": "id1",
                "from": From,
                "to": To
            }
            result = retryUtil(ws_user01.swap_sub_index,subs,'data')
            pass
        with allure.step('验证响应结果'):
            assert result['data'] != [], 'data空值'
            # 待校验的字段
            checked_col = ['id', 'open', 'close', 'high', 'low', 'amount', 'vol', 'count']
            for data in result['data']:
                for col in checked_col:
                    assert data[col] is not None

            pass