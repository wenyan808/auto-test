#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 20211009
# @Author :  HuiQing Yu

from common.SwapServiceWS import user01 as ws_user01
from common.SwapServiceAPI import user01 as api_user01
import pytest, allure, random, time
from config.conf import DEFAULT_CONTRACT_CODE
from common.CommonUtils import currentPrice
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[6]['feature'])
@allure.story(features[6]['story'][0])
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
            for i in range(3):
                result = ws_user01.swap_sub(subs)
                if result['tick']:
                    if 'ask' in result['tick'] and 'bid' in result['tick']:
                        flag = True
                        break
                time.sleep(1)
                print(f'未返回预期结果，第{i+1}次重试………………………………')
            assert flag,'未返回预期结果'
            pass
        with allure.step('验证：返回结果tick下各字段不为空'):
            checked_col = ['amount','ask','bid','close','count','high','id','low','open','vol']
            for col in checked_col:
                assert result['tick'][col],str(col)+'为None,不符合预期'
            pass

if __name__ == '__main__':
    pytest.main()
