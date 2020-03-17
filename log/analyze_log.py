# -*- coding: utf-8 -*
from __future__ import print_function
from datetime import datetime, timedelta
import json

# 按照字典值降序打印字典
def print_dict(d, dict_name):
    print("\nprint", dict_name)
    result_sorted_keys = sorted(d, key=d.get, reverse=True)
    for r in result_sorted_keys:
        print(r, d[r])


def calc_request(filename, count_dict, get_dict, set_dict, get_group_dict, set_group_dict):
    with open(filename) as f:
        for line in f:
            # line=[INFO][2020-03-17...][foo/bar.go:98] _com_request_in||traceid=xxxyyy||...
            elements = line.split("||", 10)
            first_element = elements[0]
            func_category = first_element[first_element.rfind("]") + 2:]  # func_category=_com_request_in
            if func_category != '_com_request_in':  # 只统计_com_request_in的行
                continue
            last_element = elements[-1]  # request={"ID":1,"featureKeys":["setting.tel"]}
            json_content = last_element[last_element.find("{"):last_element.rfind("}") + 1]  # {"ID":1,"featureKeys":["setting.tel"]}
            resp_data = json.loads(json_content)
            count_dict["count"] = count_dict.get("count", 0) + 1
            if 'featureKeys' in resp_data:
                count_dict["featureKeys_count"] = count_dict.get("featureKeys_count", 0) + 1
                for key in resp_data["featureKeys"]:  # 遍历json数组
                    get_dict[key] = get_dict.get(key, 0) + 1
                    # key=qualification.face_status, 那么group=qualification。key=order_num，那么group=order_num
                    group = key[:key.find(".")] if "." in key else key
                    get_group_dict[group] = get_group_dict.get(group, 0) + 1
            if 'kvMap' in resp_data:
                count_dict["kvMap_count"] = count_dict.get("kvMap_count", 0) + 1
                # 遍历json对象
                for key in resp_data["kvMap"]:
                    set_dict[key] = set_dict.get(key, 0) + 1
                    group = key[:key.find(".")] if "." in key else key
                    set_group_dict[group] = set_group_dict.get(group, 0) + 1
    print_dict(count_dict, "count_dict")
    print_dict(get_dict, "get_dict")
    print_dict(set_dict, "set_dict")
    print_dict(get_group_dict, "get_group_dict")
    print_dict(set_group_dict, "set_group_dict")


# filename = "./biz.log.2020031713"
filename = "biz.log"

calc_request(filename, dict(), dict(), dict(), dict(), dict())

# 读取22个小时的日志，避免24个小时前的日志被删除
def calc_multi_files():
    result, get_dict, set_dict, get_group_dict, set_group_dict = dict(), dict(), dict(), dict(), dict()
    today = datetime.today()
    for i in range(22, 0, -1):
        d = today - timedelta(hours=i)
        filename = './biz.log.%s' % d.strftime('%Y%m%d%H')
        print(filename)
        calc_request(filename, result, get_dict, set_dict, get_group_dict, set_group_dict)

calc_multi_files()

