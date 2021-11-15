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
@allure.feature('WebSocket')  # 这里填功能
@allure.story('市场行情')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_002:
    ids = ['TestSwapNoti_002','TestSwapNoti_003']
    params = [{'case_name': '订阅深度-150档不合并', 'depth_type': 'step0'},
              {'case_name': '订阅深度-20档不合并', 'depth_type': 'step6'},]
    contract_code = DEFAULT_CONTRACT_CODE
    @classmethod
    def setup_class(cls):
        with allure.step('挂盘'):
            cls.current_price = ATP.get_current_price()
            api_user01.swap_order(contract_code=cls.contract_code,price=round(cls.current_price*0.5,2),direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code,price=round(cls.current_price*1.5,2),direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤单恢复环境'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=3, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self,params):
        with allure.step('执行请求'):
            subs = {
                "sub": "market.{}.depth.{}".format(self.contract_code, params['depth_type']),
                "id": "id1"
            }
            result = retryUtil(ws_user01.swap_sub,subs,'tick')
            pass
        with allure.step('校验返回结果'):
            assert 'tick' in result, '返回结果无tick,校验不通过'
            assert 'bids' in result['tick'], '返回结果无买盘,校验不通过'
            assert 'asks' in result['tick'], '返回结果无卖盘,校验不通过'
            pass



if __name__ == '__main__':
    pytest.main()
