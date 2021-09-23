from string import Template


class DingDingMsg:
    ding_ding_msg = '''{
        "msgtype": "text",
        "text": {
        "content": "total: ${total} \\n\\n passed: ${passed}  \\n\\nfailed: ${failed}  \\n\\n error: ${error} \\n\\n  skipped: ${skipped}  \\n\\n run_time: ${run_time} \\n\\n report url: http://172.18.6.183:8080/jenkins/view/autotest(%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95)/job/auto-test/${build_num}/allure/"
        }}'''

    @classmethod
    def set_result(cls, total, passed, failed, error, skipped, run_time):
        with open('report/dingding.json', 'w') as dingding_json_f:
            msg = Template(cls.ding_ding_msg).safe_substitute(total=total, passed=passed, failed=failed,
                                                              error=error, skipped=skipped,
                                                              run_time=run_time)
            dingding_json_f.write(msg)

    @classmethod
    def update_json_file(cls, build_num):
        msg = ''
        with open('report/dingding.json', 'r') as dingding_json_f:
            msg = dingding_json_f.read()
            print(msg)
            with open('report/dingding.json', 'w') as dingding_json_f:
                dingding_json_f.write(Template(msg).safe_substitute(build_num=build_num))
