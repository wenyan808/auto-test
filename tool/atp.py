import json

import requests


class ATP:
    ATPHost = 'http://10.151.110.63:8000'
    header = {'accept': 'application/json', 'Content-Type': 'application/json'}

    @classmethod
    def get_api_test_data(cls, script_path, priority_list=[], tags=[]):
        atp_url = cls.ATPHost + "/api_case/get_pytest_api_test_data_by_script_path"
        body = {"script_path": script_path,
                "priority_list": priority_list,
                "tags": tags}
        response = requests.post(atp_url, headers=cls.header, json=body)
        data_keys = response.json()['variables_keys_str'].split(",")
        variables_values_list = response.json()['variables_values_list']
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
    def get_global_data(cls, env=None, system_type=None):
        atp_url = cls.ATPHost + "/api_case/get_all_global_data_by_env_and_system_type"
        params = {"env": env,
                  "system_type": system_type}
        response = requests.get(atp_url, headers=cls.header, params=params)
        return response.json()


if __name__ == '__main__':
    print(ATP.get_api_test_data("test_linear_account_info"))
    print(ATP.get_api_test_data("test_linear_account_info", priority_list=["P0", "P1"]))
    print(ATP.get_global_data())
    print(ATP.get_global_data(env='Test6'))
    print(ATP.get_global_data(env='Test20', system_type='LinearSwap'))
