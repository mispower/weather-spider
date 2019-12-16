# -*- coding: utf-8 -*-
"""
省市县编码信息
获取对应省市县天气编码
解析天气编码到省市县编码
"""
from tools import spider_request
import json

from tools.db_connector import WeatherBasicCollection

ZHIXIA_CITY = {'10101', '10102', '10103', '10104'}


# 获取省份
def get_province():
    target_url = "http://js.weather.com.cn/data/city3jdata/china.html"
    return open_url_json(target_url)


# 获取市级
def get_city(province_code):
    city_url = "http://js.weather.com.cn/data/city3jdata/provshi/{}.html".format(province_code)
    return open_url_json(city_url)


# 获取县级code
def get_county(province_code, city_code):
    county_url = "http://js.weather.com.cn/data/city3jdata/station/{}{}.html".format(province_code, city_code)
    return open_url_json(county_url)


def open_url_json(target_url):
    response = spider_request.open_url(target_url)
    response_json = json.loads(response)
    return response_json


def get_gps_info(key: str, address: str):
    url = "http://restapi.amap.com/v3/geocode/geo?key={}&address={}&city=".format(key, address)
    gps_data = json.loads(spider_request.open_url(url))["geocodes"]
    assert len(gps_data) > 0, "no gps info"
    return {
        "type": "Point",
        "coordinates": [float(s) for s in gps_data[0]["location"].split(",")]
    }


def update_weather_code():
    """
    爬取所有的WeatherCode和地理信息并且写入数据库
    :return:
    """
    amap_key = input("Input Amap key:")
    with WeatherBasicCollection() as coll:
        # 删光政策
        existed_count = coll.collection.delete_many({}).deleted_count
        print(existed_count)
        for province_code, province_name in get_province().items():
            for city_code, city_name in get_city(province_code).items():
                for county_code, county_name in get_county(province_code, city_code).items():
                    """
                    4个直辖市的天气区域编码是省+区+市
                    其他省市的天气区域编码市省+市+县
                    个别地区直接返回全码
                    """
                    if len(county_code) > 5:
                        query_code = county_code
                    elif province_code in ZHIXIA_CITY:
                        query_code = province_code + county_code + city_code
                    else:
                        query_code = province_code + city_code + county_code
                    basic_data = {
                        "weather_code": query_code,
                        "location_info": {
                            "province": province_name,
                            "city": city_name,
                            "county": county_name
                        },
                        "gps_info": get_gps_info(
                            amap_key, province_name + city_name + county_name
                        )
                    }
                    coll.collection.insert_one(basic_data)
