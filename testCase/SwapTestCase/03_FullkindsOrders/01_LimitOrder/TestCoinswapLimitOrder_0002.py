"""#!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    # @Date    : 20210916
    # @Author :
        用例Id

        所属分组
            限价委托
        用例标题
            限价委托输入价格下单卖出开空后撤单测试
        前置条件
            初始化环境准备
            1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
            1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
            2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
            3、每次完成测试后再还原环境
            4、本次用例场景为无成交下撤单场景
        类型
            文本
        步骤/文本
            1、卖出开空限价手动输入价格高于买一价
            2、观察盘口有结果A
            3、观察当前委托-限价委托页面有结果B
            4、观察资产信息有结果C
            5、在当前委托-限价委托点击撤单
            6、观察历史委托-限价委托有结果D
            7、观察资产信息有结果E
        预期结果
            A)订单未成交，盘口卖方展示挂单数据
            B)当前委托-限价委托统计数量+1，列表数量+1,展示合约交易类型，委托类型，倍数，时间，委托数量，委托价信息和下单数值一致
            C)资产信息冻结相应资产
            D)撤单后，历史委托-限价委托最新数据展示的为刚撤单信息，信息置灰，状态为已撤销，列表信息展示合约交易类型，委托类型倍数，时间，委托数量，委托价信息
            E)释放冻结担保资产

        标签
            P0
        优先级
            0
        用例别名
            TestCoinswapLimitOrder_002
"""


from common.SwapServiceAPI import t as swap_api
from common.util import compare_dict

from pprint import pprint
import pytest, allure, random, time


@allure.epic('业务线')  # 这里填业务线
@allure.feature('功能')  # 这里填功能
@allure.story('子功能')  # 这里填子功能，没有的话就把本行注释掉
class TestCoinswapLimitOrder_002:

    @allure.step('前置条件')
    def setup(self):
        print(''' 初始化环境准备
        1、建议准备两个账户，一个用于初始化环境，一个用于测试下单验证。
        1、建议初始化环境是初始化账户吃掉其他所有买卖挂单，盘口无任何挂单
        2、再根据测试场景进行拿初始化账户进行买一卖一挂单作为对手方
        3、每次完成测试后再还原环境
        4、本次用例场景为无成交下撤单场景 ''')

    @allure.title('限价委托输入价格下单卖出开空后撤单测试')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        self.contract_code = contract_code
        leverrate = '5'

        self.orderid1 = ''

        with allure.step('1、卖出开空限价手动输入价格高于买一价'):
            print('\n获取最近价\n')
            r = swap_api.swap_history_trade(contract_code=contract_code, size='1')

            lastprice = r['data'][0]['data'][0]['price']
            orderprice = round((lastprice * 1.02), 1)

            print('\n下一个买单\n')

            r = swap_api.swap_order(contract_code=contract_code, price=str(lastprice), volume='1',
                                        direction='buy', offset='open', lever_rate=leverrate,
                                        order_price_type='limit')

            time.sleep(1)
            self.orderid1 = r['data']['order_id']
            """获取当前冻结保证金"""
            r = swap_api.swap_account_info(contract_code=contract_code)

            frozen1 = r['data'][0]['margin_frozen']

            """获取当前委托数量"""
            r = swap_api.swap_openorders(contract_code=contract_code, page_index='', page_size='')
            totalsize1 = r['data']['total_size']

            print('\n下一个高于买一价格的卖单\n')

            r = swap_api.swap_order(contract_code=contract_code, price=orderprice, volume='1',
                                        direction='sell', offset='open', lever_rate=leverrate,
                                        order_price_type='limit')

            time.sleep(2)

            orderid2 = r['data']['order_id']

        with allure.step('2、观察盘口有结果A'):
            r = swap_api.swap_depth(contract_code=contract_code, type='step0')
            book_price, book_amount = r['tick']['asks'][0]
            assert float(book_price) == float(orderprice)
            assert book_amount == 1

        with allure.step('3、观察当前委托-限价委托页面有结果B'):
            """获取当前冻结保证金"""
            r = swap_api.swap_account_info(contract_code=contract_code)

            frozen2 = r['data'][0]['margin_frozen']

            """获取当前委托数量及详情"""
            r = swap_api.swap_openorders(contract_code=contract_code, page_index='', page_size='')
            totalsize2 = r['data']['total_size']
            actual_orderinfo = r['data']['orders'][0]
            expectdic = {'contract_code': contract_code,
                         'order_price_type': 'limit',
                         'lever_rate': leverrate,
                         'price': orderprice,
                         'volume': '1'}

            assert (totalsize2 - totalsize1 == 1)

            assert compare_dict(expectdic, actual_orderinfo)

        with allure.step('4、观察资产信息有结果C'):
            assert frozen2 > frozen1

        with allure.step('5、在当前委托-限价委托点击撤单'):
            r = swap_api.swap_cancel(contract_code=contract_code, order_id=orderid2)

            time.sleep(5)
        with allure.step('6、观察历史委托-限价委托有结果D'):
            """获取历史订单"""
            r = swap_api.swap_hisorders_exact(contract_code=contract_code, trade_type='0', type='2', status='7')

            actual_orderinfo2 = r['data']['orders'][0]

            assert compare_dict(expectdic, actual_orderinfo2)

        with allure.step('7、观察资产信息有结果E'):
            """获取当前冻结保证金"""
            r = swap_api.swap_account_info(contract_code=contract_code)

            frozen3 = r['data'][0]['margin_frozen']

            assert frozen3 == frozen1

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        if self.orderid1:
            r = swap_api.swap_cancel(contract_code=self.contract_code, order_id=self.orderid1)


if __name__ == '__main__':
    pytest.main()
