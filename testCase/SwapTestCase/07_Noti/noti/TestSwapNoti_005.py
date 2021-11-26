#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author :  HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice

@allure.epic('反向永续')  # 这里填业务线
@allure.feature('合约交易接口')  # 这里填功能
@allure.story('市场行情接口')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.link(url='https://docs.huobigroup.com/docs/coin_margined_swap/v1/cn/#0d9cec2a3b',name='文档地址')
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_005:
    ids = ['TestSwapNoti_005']
    params = [{'case_name': '获取聚合行情'}]
    contract_code = DEFAULT_CONTRACT_CODE

    @classmethod
    def setup_class(cls):
        with allure.step('挂盘'):
            cls.current_price = currentPrice()
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.current_price * 0.5, 2),
                                  direction='buy')
            api_user01.swap_order(contract_code=cls.contract_code, price=round(cls.current_price * 1.5, 2),
                                  direction='sell')
            pass

    @classmethod
    def teardown_class(cls):
        with allure.step('撤单恢复环境'):
            api_user01.swap_cancelall(contract_code=cls.contract_code)
            pass

    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    @pytest.mark.parametrize('params', params, ids=ids)
    def test_execute(self, params):
        allure.dynamic.title(params['case_name'])
        with allure.step('操作：发送sub订阅'):
            api_user01.swap_order(contract_code=self.contract_code, price=round(self.current_price, 2),
                                  direction='buy')
            api_user01.swap_order(contract_code=self.contract_code, price=round(self.current_price, 2),
                                  direction='sell')
            time.sleep(2)
            subs = {
                      "sub": "market.{}.detail".format(self.contract_code),
                      "id": "id6"
                     }
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                result = ws_user01.swap_sub(subs)
                if result['tick']:
                    if result['tick']['ask'] and result['tick']['bid']:
                        flag = True
                        break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag,'未返回预期结果'
            pass
        with allure.step('验证：返回结果tick下各字段不为空'):
            checked_col = ['amount','ask','bid','close','count','high','id','low','open','vol']
            for col in checked_col:
                assert result['tick'][col],str(col)+'为None,不符合预期'
            pass

if __name__ == '__main__':
    pytest.main()
