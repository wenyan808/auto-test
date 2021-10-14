from pprint import pprint

import requests

from common.ContractServiceAPI import common_user_contract_service_api
from common.ContractServiceAPI import t as contract_api
from common.LinearServiceAPI import common_user_linear_service_api
from common.LinearServiceAPI import t as linear_api
from common.SwapServiceAPI import common_user_swap_service_api
from common.SwapServiceAPI import t as swap_api
from common.util import api_key_post, api_http_get
from config import conf


class ATP:
    ATPHost = 'http://172.18.6.52:8000'
    # ATPHost = 'http://0.0.0.0:8000'
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}

    price_precision = {'ETH-USDT': 3,
                       'BTC-USD': 6,
                       'BTC_CW': 2
                       }

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
        # Author : Guangnan Zhang
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        cls.cancel_all_order(contract_code=contract_code)
        json_body = cls.get_base_json_body(contract_code)

        if conf.SYSTEM_TYPE == 'LinearSwap' and iscross is True:
            response = api_key_post(conf.URL, conf.POSITION_INFO_URL.replace('swap_position_info',
                                                                             'swap_cross_position_info'),
                                    json_body, conf.ACCESS_KEY, conf.SECRET_KEY)
        else:
            response = api_key_post(conf.URL, conf.POSITION_INFO_URL, json_body, conf.ACCESS_KEY,
                                    conf.SECRET_KEY)

        position_list = response["data"]
        if conf.SYSTEM_TYPE == 'Delivery':
            volume_dict = {item['direction']: int(item['volume']) for item in
                           list(filter(
                               lambda i: i['contract_type'] == json_body['contract_type'], position_list))}
        else:
            volume_dict = {item['direction']: int(item['volume']) for item in position_list}

        # 下单平仓
        for direction, volume in volume_dict.items():
            if volume:
                print(cls.current_user_make_order(contract_code=contract_code, offset='close',
                                                  direction='buysell'.replace(direction, ''),
                                                  volume=volume, iscross=iscross))

        ATP.clean_market(contract_code=contract_code)
        return response

    @classmethod
    def get_current_price(cls, contract_code=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE

        trade_price_methods = {'Delivery': common_user_contract_service_api.contract_trade,
                               'Swap': common_user_swap_service_api.swap_trade,
                               'LinearSwap': common_user_linear_service_api.linear_trade,
                               }
        response = trade_price_methods[conf.SYSTEM_TYPE](contract_code)
        err_msg = {'status': 'error', 'err_msg': '获取最新价出错', 'response': response}
        tick = response.get('tick', {})
        if not tick:
            print(err_msg)
            return -1

        data = tick.get('data', [])
        if not data:
            print(err_msg)
            return -1
        current_price = float(data[0].get('price', -1))
        if current_price < 0:
            print(err_msg)
            return -1
        print(contract_code, '最新价 = ', current_price)
        return current_price

    @classmethod
    def get_index_price(cls, contract_code=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE

        index_price_methods = {'Delivery': common_user_contract_service_api.contract_index,
                               'Swap': common_user_swap_service_api.swap_index,
                               'LinearSwap': common_user_linear_service_api.linear_index,
                               }
        response = index_price_methods[conf.SYSTEM_TYPE](contract_code)
        print("===获取index价===")
        pprint(response)
        err_msg = {'status': 'error', 'err_msg': '获取index价出错', 'response': response}
        data = response.get('data', {})
        assert isinstance(data, list) and len(data) == 1, err_msg
        index_price_record = data[0]
        assert 'index_price' in index_price_record, err_msg
        index_price = index_price_record['index_price']
        print(f"当前index价 ： {index_price}")
        return index_price

    @classmethod
    def common_user_make_order(cls, contract_code=None, price=None, volume=10, direction='buy', offset='open',
                               lever_rate=5,
                               order_price_type='limit', user='common', iscross=False):
        if user == 'common':

            order_methods = {'Delivery': common_user_contract_service_api.contract_order,
                             'Swap': common_user_swap_service_api.swap_order,
                             'LinearSwap': common_user_linear_service_api.linear_order,
                             }
            if iscross:
                order_methods['LinearSwap'] = common_user_linear_service_api.linear_cross_order,

        else:
            order_methods = {'Delivery': contract_api.contract_order,
                             'Swap': swap_api.swap_order,
                             'LinearSwap': linear_api.linear_order,
                             }
            if iscross:
                order_methods['LinearSwap'] = linear_api.linear_cross_order,

        order_method = order_methods[conf.SYSTEM_TYPE]
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        if not price:
            price = cls.get_current_price(contract_code)
        if price < 0:
            return {"status": "err", "err_msg": "获取最新价失败"}
        json_body = cls.get_base_json_body(contract_code)
        order_json = {
            'price': price,
            'volume': volume, 'direction': direction,
            'offset': offset, 'lever_rate': lever_rate, 'order_price_type': order_price_type}
        order_json.update(json_body)
        return order_method(**order_json)

    @classmethod
    def current_user_make_order(cls, contract_code=None, price=None, volume=10, direction='buy', offset='open',
                                lever_rate=5,
                                order_price_type='limit', iscross=False):
        return cls.common_user_make_order(contract_code=contract_code, price=price, volume=volume, direction=direction,
                                          offset=offset, lever_rate=lever_rate,
                                          order_price_type=order_price_type, user='current', iscross=iscross)

    @classmethod
    def common_user_make_trigger_order(cls, contract_code=None, trigger_type=None, trigger_price=None, order_price=None,
                                       volume=10,
                                       direction='buy', offset='open',
                                       lever_rate=5,
                                       order_price_type='limit', user='common', iscross=False):
        if user == 'common':
            order_methods = {'Delivery': common_user_contract_service_api.contract_trigger_order,
                             'Swap': common_user_swap_service_api.swap_trigger_order,
                             'LinearSwap': common_user_linear_service_api.linear_trigger_order,
                             }
            if iscross:
                order_methods['LinearSwap'] = common_user_linear_service_api.linear_cross_trigger_order
        else:
            order_methods = {'Delivery': contract_api.contract_trigger_order,
                             'Swap': swap_api.swap_trigger_order,
                             'LinearSwap': linear_api.linear_trigger_order,
                             }
            if iscross:
                order_methods['LinearSwap'] = linear_api.linear_cross_trigger_order

        order_method = order_methods[conf.SYSTEM_TYPE]

        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE

        current_price = cls.get_current_price(contract_code)
        if current_price < 0:
            return {"status": "err", "err_msg": "获取最新价失败"}

        if not trigger_price:
            if direction == 'buy':
                trigger_price = cls.get_adjust_price(0.99)
            else:
                trigger_price = cls.get_adjust_price(1.01)

        if not order_price:
            order_price = trigger_price

        if not trigger_type:
            if trigger_price >= current_price:
                trigger_type = 'ge'
            else:
                trigger_type = 'le'

        json_body = cls.get_base_json_body(contract_code)
        order_json = {
            'trigger_type': trigger_type, 'trigger_price': trigger_price,
            'order_price': order_price,
            'volume': volume, 'direction': direction,
            'offset': offset, 'lever_rate': lever_rate, 'order_price_type': order_price_type}
        order_json.update(json_body)
        return order_method(**order_json)

    @classmethod
    def current_user_make_trigger_order(cls, contract_code=None, trigger_type=None, trigger_price=None,
                                        order_price=None,
                                        volume=10,
                                        direction='buy', offset='open',
                                        lever_rate=5,
                                        order_price_type='limit', iscross=False):
        return cls.common_user_make_trigger_order(contract_code=contract_code, trigger_type=trigger_type,
                                                  trigger_price=trigger_price, order_price=order_price, volume=volume,
                                                  direction=direction,
                                                  offset=offset, lever_rate=lever_rate,
                                                  order_price_type=order_price_type, user='current', iscross=iscross)

    @classmethod
    def make_market_depth(cls, contract_code=None, market_price=None, volume=10):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        # 清盘
        print(cls.clean_market(contract_code=contract_code))

        if not market_price:
            market_price = cls.get_current_price(contract_code=contract_code)
            if market_price < 0:
                return False

        # 按目标价格成交
        print(cls.common_user_make_order(price=market_price, direction='buy'))
        print(cls.common_user_make_order(price=market_price, direction='sell'))
        sell_price = cls.get_adjust_price(1.01, base_price=market_price)
        buy_price = cls.get_adjust_price(0.99, base_price=market_price)
        print(cls.common_user_make_order(price=buy_price, direction='buy', volume=volume))
        print(cls.common_user_make_order(price=sell_price, direction='sell', volume=volume))

        return True

    @classmethod
    def cancel_all_types_order(cls, contract_code=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        ATP.cancel_all_order(contract_code=contract_code)
        ATP.cancel_all_trigger_order(contract_code=contract_code)
        ATP.cancel_all_track_order(contract_code=contract_code)
        ATP.cancel_all_tpsl_order(contract_code=contract_code)

    @classmethod
    def get_adjust_price(cls, rate=1.01, contract_code=None, base_price=None):
        if not contract_code:
            contract_code = conf.DEFAULT_CONTRACT_CODE
        if not base_price:
            base_price = ATP.get_current_price(contract_code=contract_code)
        if contract_code in cls.price_precision:
            return round(base_price * rate, cls.price_precision[contract_code])
        else:
            return round(base_price * rate, 1)


if __name__ == '__main__':
    system_types = ['Delivery', 'Swap', "LinearSwap"]
    for system_type in system_types:
        conf.set_run_env_and_system_type('Test6', system_type)
        index_price = ATP.get_index_price()
        ATP.make_market_depth(market_price=index_price)
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
        # print(ATP.make_market_depth())
        # print(ATP.close_all_position())
    # conf.set_run_env_and_system_type('Test6', 'Swap')
    # print(ATP.make_market_depth(market_pirce=52000))
