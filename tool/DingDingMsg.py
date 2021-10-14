import json
import os
import pathlib
import shutil
from string import Template


class DingDingMsg:
    ding_ding_msg = '''{
        "msgtype": "text",
        "text": {
        "content": "env: '${env}' system_type: '${system_type}' test_type: '${test_type}' \\ntotal: ${total} passed: ${passed}  \\nfailed: ${failed}  error: ${error} skipped: ${skipped}  \\nrun_time: ${run_time} \\nreport url: \\nhttp://172.18.6.183:8080/jenkins/view/autotest(%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95)/job/auto-test/${build_num}/allure/"
        }}'''

    @classmethod
    def init(cls, ):
        path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
        path = path.parent / 'report/allure/'
        if not path.exists():
            path.mkdir()
        else:
            shutil.rmtree(path)
            path.mkdir()

    @classmethod
    def update_json_file(cls, **kwargs):
        cls.ding_ding_msg = Template(cls.ding_ding_msg).safe_substitute(**kwargs, **cls.get_run_result())
        with open('report/dingding.json', 'w') as dingding_json_f:
            dingding_json_f.write(cls.ding_ding_msg)

    @classmethod
    def get_run_result(cls, ):
        path = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
        path = path.parent / 'report/allure/'
        if not path.exists():
            path.mkdir()
        total = 0
        case_result_summary = {
            'passed': set(),
            'failed': set(),
            'broken': set(),
            'skipped': set(),
        }
        for file in os.listdir(path):
            if file.endswith('-result.json'):
                total += 1
                with open(path / file) as result_json_file:
                    result_info = json.load(result_json_file)
                    case_result_summary[result_info["status"]].add(result_info['fullName'])
        passed_cases = case_result_summary.pop('passed')
        result = {'passed': len(passed_cases), 'total': total}
        result.update({key: len(value - passed_cases) for key, value in case_result_summary.items()})

        return result


if __name__ == '__main__':
    print(DingDingMsg.get_run_result())
