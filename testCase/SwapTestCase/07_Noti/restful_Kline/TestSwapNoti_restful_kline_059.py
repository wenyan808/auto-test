#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""# @Date    : 20211015
# @Author : 
    用例标题
        restful请求K线1day 只传to,不传from
    前置条件
        
    步骤/文本
        详见官方文档
    预期结果
        
    优先级
        2
    用例别名
        TestSwapNoti_restful_kline_059
"""

from common.SwapServiceAPI import t as swap_api
import pytest, allure, random, time


@allure.epic('反向永续')  # 这里填业务线
@allure.feature('restful请求K线')  # 这里填功能
@allure.story('restful请求K线1day 选填参数验证：只传to,不传from')  # 这里填子功能，没有的话就把本行注释掉
@pytest.mark.stable
@allure.tag('Script owner : 余辉青', 'Case owner : 吉龙')
class TestSwapNoti_restful_kline_059:

    @allure.step('前置条件')
    def setup(self):
        print("\n自动化步骤："
              "\n*、发送restful请求kline的请求,类型=1day；"
              "\n*、选填参数是否传参：from【N】 ,to【Y】 , size【Y】"
              "\n*、验证Kline返回结果：返回topic正确，data不为空")

    @allure.title('restful请求K线1day 只传to,不传from')
    @allure.step('测试执行')
    def test_execute(self, contract_code):
        with allure.step('详见官方文档'):
            period = '1day'
            size = 10
            toTime = int(time.time())
            kLineInfo = swap_api.swap_kline(contract_code=contract_code, period=period, size=size, to=toTime)
            assert 'market.' + contract_code + '.kline.'+period in kLineInfo['ch']
            assert 'data' in kLineInfo and [] not in kLineInfo['data']
            assert len(kLineInfo['data']) <= size
            pass

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')


if __name__ == '__main__':
    pytest.main()
