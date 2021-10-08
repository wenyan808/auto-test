import json
from decimal import Decimal

import requests

from common.util import api_key_post, api_http_get
from config import conf
from pprint import pprint
from common.ContractServiceAPI import t as contract_api
from common.ContractServiceAPI import common_user_contract_service_api
from common.LinearServiceAPI import t as linear_api
from common.LinearServiceAPI import common_user_linear_service_api
from common.SwapServiceAPI import t as swap_api
from common.SwapServiceAPI import common_user_swap_service_api


class ATP:
    ATPHost = 'http://172.18.6.52:8000'
    # ATPHost = 'http://0.0.0.0:8000'
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}

    @classmethod
    def get_base_json_body(cls, contract_code=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        json_body = {}
        if conf.SYSTEM_TYPE == 'Delivery':
            contract_types = {'CW': "this_week", 'NW': "next_week", 'CQ': "quarter", 'NQ': "next_quarter"}
            if '_' in contract_code:
                json_body['symbol'] = contract_code.split('_')[0]
                json_body['contract_type'] = contract_types[contract_code.split('_')[1]]
            else:
                json_body['symbol'] = contract_code[:-6]
                json_body['contract_type'] = contract_types['CW']
        else:
            json_body['contract_code'] = contract_code
        return json_body

    @classmethod
    def key_post(cls, api_url, json_body):
        return api_key_post(conf.URL, api_url, json_body, conf.ACCESS_KEY, conf.SECRET_KEY)

    @classmethod
    def common_user_key_post(cls, api_url, json_body):
        return api_key_post(conf.URL, api_url, json_body, conf.COMMON_ACCESS_KEY, conf.COMMON_SECRET_KEY)

    @classmethod
    def get(cls, api_url, json_body, headers=None):
        return api_http_get(conf.URL + api_url, json_body, headers)

    @classmethod
    def get_api_test_data(cls, script_path, priority_list=[], tags=[]):
        data_keys, variables_values_list = cls.get_api_test_data_old(script_path,
                                                                     priority_list=priority_list,
                                                                     tags=tags)
        api_test_data_list = [dict(zip(data_keys, variables_values)) for variables_values in variables_values_list]
        return api_test_data_list

    @classmethod
    def get_api_test_data_old(cls, script_path, priority_list=[], tags=[]):
        atp_url = cls.ATPHost + "/api_case/get_pytest_api_test_data_by_script_path"
        body = {"script_path": script_path,
                "priority_list": priority_list,
                "tags": tags}
        response = requests.post(atp_url, headers=cls.header, json=body)
        data_keys = response.json()['variables_keys_str'].split(",")
        variables_values_list = response.json()['variables_values_list']
        return data_keys, variables_values_list

    @classmethod
    def clean_market(cls, contract_code=None, direction=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        atp_url = cls.ATPHost + "/jobs/market_control"
        body = {"env": conf.ENV,
                "system_type": conf.SYSTEM_TYPE,
                'contract_code': contract_code,
                'job_name': 'CleanMarket'
                }
        if direction == 'sell':
            body['job_name'] = 'CleanSell'
        if direction == 'buy':
            body['job_name'] = 'CleanBuy'
        response = requests.post(atp_url, headers=cls.header, json=body)
        return response.json()

    @classmethod
    def cancel_all_order(cls, contract_code=None):
        json_body = cls.get_base_json_body(contract_code)

        response = cls.key_post(conf.CANCEL_ALL_ORDER_URL, json_body)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = cls.key_post(conf.CANCEL_ALL_ORDER_URL.replace('swap_cancelall', 'swap_cross_cancelall'),
                                          json_body)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        print('撤销当前用户 某个品种所有限价挂单')
        pprint(response)
        return response

    @classmethod
    def switch_level(cls, contract_code=None, lever_rate=5):
        json_body = cls.get_base_json_body(contract_code)
        json_body['lever_rate'] = lever_rate

        response = cls.key_post(conf.SWITCH_LEVER_URL, json_body)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = cls.key_post(conf.SWITCH_LEVER_URL.replace('swap_switch_lever_rate',
                                                                        'swap_cross_switch_lever_rate'), json_body)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        pprint('修改当前品种杠杆 默认5倍')
        pprint(response)
        return response

    @classmethod
    def cancel_all_trigger_order(cls, contract_code=None):
        json_body = cls.get_base_json_body(contract_code)
        response = cls.key_post(conf.CANCEL_ALL_TRIGGER_ORDER_URL, json_body)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = cls.key_post(conf.CANCEL_ALL_TRIGGER_ORDER_URL.replace('swap_trigger_cancelall',
                                                                                    'swap_cross_trigger_cancelall'),
                                          json_body)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        print('撤销当前用户 某个品种所有计划委托挂单')
        pprint(response)
        return response

    @classmethod
    def cancel_all_tpsl_order(cls, contract_code=None):
        json_body = cls.get_base_json_body(contract_code)

        response = cls.key_post(conf.CANCEL_ALL_TPSL_ORDER_URL, json_body)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = cls.key_post(
                conf.CANCEL_ALL_TPSL_ORDER_URL.replace('swap_tpsl_cancelall',
                                                       'swap_cross_tpsl_cancelall'), json_body)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        print('撤销当前用户 某个品种所有止盈止损委托挂单')
        pprint(response)
        return response

    @classmethod
    def cancel_all_track_order(cls, contract_code=None):
        json_body = cls.get_base_json_body(contract_code)
        response = cls.key_post(conf.CANCEL_ALL_TRACK_ORDER_URL, json_body)
        if conf.SYSTEM_TYPE == 'LinearSwap':
            cross_response = cls.key_post(
                conf.CANCEL_ALL_TRACK_ORDER_URL.replace('swap_track_cancelall',
                                                        'swap_cross_track_cancelall'), json_body)
            response = {
                "cross": cross_response,
                "isolated": response

            }
        print('撤销当前用户 某个品种所有跟踪委托挂单')
        pprint(response)
        return response

    @classmethod
    def close_all_position(cls, contract_code=None, iscross=False):
        contract_type = ''
        symbol = ''
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        json_body = {}
        if conf.SYSTEM_TYPE == 'Delivery':
            contract_type_dic = {'CW': 'this_week', 'NW': 'next_week', 'CQ': 'quarter', 'NQ': 'next_ quarter'}

            if '_' in contract_code:
                symbol = contract_code.split('_')[0]
                json_body['symbol'] = symbol
                contract_type = contract_type_dic[contract_code.split('_')[1]]
            else:
                symbol = contract_code[:-6]
                json_body['symbol'] = symbol
                contract_type = ''

        else:
            json_body['contract_code'] = contract_code

        if conf.SYSTEM_TYPE == 'LinearSwap' and iscross is True:
            response = api_key_post(conf.URL, conf.POSITION_INFO_URL.replace('swap_position_info',
                                                                             'swap_cross_position_info'),
                                    json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
        else:
            response = api_key_post(conf.URL, conf.POSITION_INFO_URL, json_body, conf.ACCESS_KEY,
                                    conf.SECRET_KEY)

        position_list = response["data"]

        if conf.SYSTEM_TYPE == 'Delivery':
            json_body['contract_type'] = contract_type
        response = api_key_post(conf.URL, conf.CONTRACT_INFO_URL, json_body, conf.ACCESS_KEY,
                                conf.SECRET_KEY)
        price_tick = str(response['data'][0]['price_tick'])

        for position in position_list:
            order_json_body = {}
            if conf.SYSTEM_TYPE == 'Delivery':
                if position['contract_type'] != contract_type:  # 如果这个持仓和当前在测的合约周期不一致，就跳过
                    continue
                order_json_body['contract_type'] = contract_type
                order_json_body['symbol'] = symbol
            else:
                json_body['contract_code'] = contract_code
            order_json_body['global'] = str(int(position['volume']))
            order_json_body['lever_rate'] = position['lever_rate']
            order_json_body['offset'] = 'close'
            order_json_body['order_price_type'] = 'limit'
            if position['direction'] == "buy":
                order_json_body['direction'] = 'sell'
            else:
                order_json_body['direction'] = 'buy'
            price = str(position['cost_open'])
            order_json_body['orderprice'] = str(Decimal(price).quantize(Decimal(price_tick)))

            if conf.SYSTEM_TYPE == 'LinearSwap' and iscross is True:
                response = api_key_post(conf.URL,
                                        conf.PLACE_ORDER_URL.replace('swap_order', 'swap_cross_order'),
                                        json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
            else:
                response = api_key_post(conf.URL, conf.PLACE_ORDER_URL,
                                        json_body, conf.ACCESS_KEY, conf.SECRET_KEY)

        print('撤销当前用户 某个品种所有跟踪委托挂单')
        pprint(response)
        return response

    @classmethod
    def make_market_depth(cls, contract_code=None, market_pirce=None, volume=10):
        json_body = cls.get_base_json_body(contract_code)
        order_json = {
                      'price': None,
                      'volume': volume, 'direction': None,
                      'offset': 'open', 'lever_rate': 5, 'order_price_type': "limit"}
        order_json.update(json_body)
        order_methods = {'Delivery': common_user_contract_service_api.contract_order,
                         'Swap': common_user_swap_service_api.swap_order,
                         'LinearSwap': common_user_linear_service_api.linear_order,
                         }
        trade_price_methods = {'Delivery': common_user_contract_service_api.contract_trade,
                               'Swap': common_user_swap_service_api.swap_trade,
                               'LinearSwap': common_user_linear_service_api.linear_trade,
                               }
        order_method = order_methods[conf.SYSTEM_TYPE]
        # 清盘
        print(cls.clean_market())

        # 获取最新价
        response = trade_price_methods[conf.SYSTEM_TYPE](conf.DEFAULT_CONTRACT_CODE)
        if not market_pirce:
            # 获取最新价
            err_msg = {'status': 'error', 'err_msg': '获取最新价出错', 'response': response}
            tick = response.get('tick', {})
            if not tick:
                return err_msg

            data = tick.get('data', [])
            if not data:
                return err_msg

            current_price = float(data[0].get('price', -1))
            if current_price < 0:
                return err_msg

            # 确定挂单买价 和 挂单卖价
            sell_price = round(current_price * 1.01, 1)
            buy_price = round(current_price * 0.99, 1)
        else:
            # 按目标价格成交
            order_json.update({'price': market_pirce, 'direction': 'buy'})
            print(order_method(**order_json))
            order_json.update({'price': market_pirce, 'direction': 'sell'})
            print(order_method(**order_json))

            sell_price = round(market_pirce * 1.01, 1)
            buy_price = round(market_pirce * 0.99, 1)

        # 挂单
        order_json.update({'price': buy_price, 'direction': 'buy'})
        print(order_method(**order_json))
        order_json.update({'price': sell_price, 'direction': 'sell'})
        print(order_method(**order_json))

        return response


if __name__ == '__main__':
    system_types = ['Delivery', 'Swap', "LinearSwap"]
    for system_type in system_types:
        conf.set_run_env_and_system_type('Test6', system_type)
        # print(ATP.get_api_test_data("test_linear_account_info"))
        # print(ATP.get_api_test_data("test_linear_account_info", priority_list=["P0", "P1"]))
        #
        # # 清除盘口所有卖单
        # print(ATP.clean_market())
        # # 清除盘口所有买单
        # print(ATP.clean_market())
        # # 清除盘口所有买卖挂单
        # print(ATP.clean_market())
        #
        # # 撤销当前用户 某个品种所有限价挂单
        # print(ATP.cancel_all_order())
        # # 修改当前品种杠杆 默认5倍
        # print(ATP.switch_level())

        print(ATP.make_market_depth())
    # conf.set_run_env_and_system_type('Test6', 'Swap')
    # print(ATP.make_market_depth(market_pirce=52000))