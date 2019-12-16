# -*- coding: utf-8 -*-
import traceback
from typing import List

from tools import spider_request, province_util
import json
import re
import datetime
import sys

# 天气信息爬取
from tools.db_connector import WeatherBasicCollection, WeatherHistoryCollection


def weather_spider():
    with WeatherHistoryCollection() as history_coll:
        with WeatherBasicCollection() as basic_coll:
            location_list = [
                x["weather_code"] for x in basic_coll.collection.find(
                    {},
                    {"weather_code": 1}
                )
            ]
            N = len(location_list)

            for index, weather_code in enumerate(location_list):
                try:
                    append_info = {"weather_code": weather_code}
                    target_url = "http://www.weather.com.cn/weather/{}.shtml".format(weather_code)
                    doc = spider_request.open_url(target_url)
                    # 当前时间往前24小时的天气明细:温度、风向、降水量等详细数据正则
                    regex_24 = '{"od".+}'
                    """
                    数据格式如下:
                         od21 时间
                         od22 温度
                         od23 分享角
                         od24 风向
                         od25 风力
                         od26 降水量
                         od27 相对湿度
                         od28 空气质量
                         正则匹配风向、降水量等
                    """
                    day_detail = re.findall(regex_24, doc)[0]
                    day_detail_json = json.loads(day_detail)
                    insert_batch = [
                        dict(weather_info, **append_info) for weather_info in
                        format_weather_data(day_detail_json['od']['od2'])
                    ]
                    cleaned_sum = history_coll.collection.delete_many({
                        "weather_code": weather_code,
                        "datetime": {
                            "$in": [x["datetime"] for x in insert_batch]
                        }
                    }).deleted_count
                    history_coll.collection.insert_many(insert_batch)
                    inserted_sum = len(insert_batch)
                    print("\rLocation:{}({}/{}) processed {} cleanned, {} has inserted.".format(
                        weather_code, index, N,
                        cleaned_sum, inserted_sum
                    ), end="    ")
                except Exception as ex:
                    print(" ")
                    print("Error while downloading data of:" + weather_code, file=sys.stderr)
                    print("Error info:" + str(ex), file=sys.stderr)
                    print(traceback.format_exc(), file=sys.stderr)


def float_or_null(anyvalue):
    """
    返回Float或者None（如果解析失败）
    :param anyvalue:
    :return:
    """
    try:
        return float(anyvalue)
    except:
        return None


def get_or_null(data: dict, key: object):
    try:
        return data.get(key)
    except:
        return None


def format_weather_data(day_detail_json) -> List[dict]:
    temp = -1
    update_time = datetime.datetime.now()
    date = update_time
    results = []
    for data in day_detail_json:
        current_result = {}
        hour = int(get_or_null(data, 'od21'))
        if temp == -1:
            temp = hour
        if hour - temp > 0:
            date = update_time - datetime.timedelta(days=1)
        date = datetime.datetime(date.year, date.month, date.day, hour)
        current_result["datetime"] = int(date.strftime("%Y%m%d%H"))
        current_result["temperature"] = float_or_null(get_or_null(data, 'od22'))
        current_result["wind"] = {
            "direction": float_or_null(get_or_null(data, 'od23')),
            "direction_text": get_or_null(data, 'od24'),
            "force": float_or_null(get_or_null(data, 'od25'))
        }
        current_result["rainfall"] = float_or_null(get_or_null(data, 'od26'))
        current_result["humidity"] = float_or_null(get_or_null(data, 'od27'))
        current_result["air_quality"] = get_or_null(data, 'od28')
        results.append(current_result)
    return results

