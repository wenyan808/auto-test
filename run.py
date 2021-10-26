#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan


import os, sys
import time
from copy import copy
from string import Template

import pytest

from config.conf import set_run_env_and_system_type
from tool.DingDingMsg import DingDingMsg


"""
pytest 命令中加入 '-n 数字'可实现分布式执行测试用例，数字表示执行用例的机器数，但是由于速度过快被api接口限频，如果需要可考虑调大测试环境限频
pytest 命令中加入 --html=./report/html/TestReoprt%s.html  --self-contained-html  可生成htlm测试报告
pytest  -m "not xxx" 表示不执行有@pytest.mark.xxx标记的用例 

要使用allure生成测试报告需要经过两步

1 生成测试结果的json文件
使用pytest运行测试脚本时，添加参数pytest --alluredir=json文件生成路径
可以将参数直接写道配置文件中addopts = -s --alluredir=./report
有几个测试用例就会生成几个测试结果的json文件，这些文件在其他语言中也是通用的
多次运行，之前保存的json会保留下来，而且可以在报告中查看之前的测试结果

2 将json数据文件生成HTML测试报告
使用allure generate json文件路径可以生成测试报告，默认生成文件夹为allure-report，指定文件夹可以使用-o参数allure generate json文件路径 -o HTML报告路径
如果JSON文件路径错误，也可以生成测试报告不会报错，但是打开HTML文件是空的
当生成过测试报告，如果已经存在报告路径文件夹时，再次使用会提示添加--clean参数来重写
allure generate ./report --clean
allure generate ./report -o ./html_report --clean
不生成HTML文件，直接在浏览器打开allure serve json文件路径。运行后生成临时文件夹存放HTML报告，在浏览器打开
使用命令打开HTML报告：allure open html报告路径，也可以直接打开index.html。
参考文档：https://www.codenong.com/cs107116946/
        https://blog.csdn.net/liuchunming033/article/details/79624474
        https://www.cnblogs.com/poloyy/category/1690628.html
#将xml报告转换成html,启动allure服务，在浏览器中展示报告
# os.system('allure generate report/allure -o report/html --clean')
# os.system('allure open report/html')
"""
from multiprocessing import Process


def run(system_type=None, run_env='Test6', test_type=''):
    """
    新执行脚本由jenkins中的shell传入执行模块，执行方式为
    python3 run.py 模块名
    exit 0
    """
    system_types = {
        'Contract': 'Delivery',
        'Swap': 'Swap',
        'Linear': 'LinearSwap',
        'Option': 'Option',
        'Schema': 'Schema'
    }
    args = ["--alluredir=report/allure"]
    if test_type:
        args.append(f'-m={test_type}')
        args.append('--reruns=2')

    if system_type == 'ALL':
        for system_types_item in ['Contract', 'Swap', 'Linear']:
            set_run_env_and_system_type(run_env, system_types[system_types_item])
            run_args = copy(args)
            run_args.append(f"testCase/{system_types_item}TestCase")
            pytest.main(args=run_args)
        # os.system('pytest --alluredir report/allure testCase/')

    elif type(system_type) == str:
        if system_type.capitalize() in ['Contract', 'Swap', 'Linear', 'Option', 'Schema']:
            set_run_env_and_system_type(run_env, system_types[system_type.capitalize()])
            from tool.atp import ATP
            index_price = ATP.get_index_price()
            ATP.make_market_depth(market_price=index_price if index_price > 0 else ATP.get_current_price())
            args.append(f"testCase/{system_type.capitalize()}TestCase")
            pytest.main(args=args)
            ATP.cancel_all_types_order()
            time.sleep(2)
            ATP.close_all_position()
            time.sleep(2)

            if system_type.capitalize() == 'Linear':
                ATP.close_all_position(iscross=True)
                time.sleep(2)

            ATP.clean_market()
            time.sleep(2)
            ATP.make_market_depth(market_price=ATP.get_index_price())
            # os.system(
            #     'pytest --alluredir report/allure testCase/{}TestCase'.format(system_type.capitalize()))

        else:
            print('输入错误')
    else:
        print('输入错误')


if __name__ == '__main__':
    # run cmd ： python3 run.py Test6 ALL 300 stable
    test_env = sys.argv[1]
    system_type = sys.argv[2]
    build_num = sys.argv[3]
    if len(sys.argv) > 4:
        test_type = sys.argv[4]
    else:
        test_type = ''
    # for debug
    # test_env = 'Test6'
    # system_type = 'ALL'
    # build_num = 30000
    # test_type = 'stable'
    DingDingMsg.init()
    start = time.time()
    if system_type == 'ALL':
        ps_list = []
        for system_types_item in ['Contract', 'Swap', 'Linear']:
            ps = Process(target=run, args=(system_types_item, test_env, test_type))
            ps_list.append(ps)
            ps.start()
        for ps in ps_list:
            ps.join()
    else:
        run(run_env=test_env, system_type=system_type, test_type=test_type)
    run_time = time.time() - start
    DingDingMsg.update_json_file(env=test_env, system_type=system_type, test_type=test_type, run_time=run_time,
                                 build_num=build_num)
