# -*- coding: utf-8 -*-
"""
 天气网站：http://www.weather.com.cn/
 获取天气网站对应省市县编码,并且生成文件
"""
from tools import province_util

if __name__ == "__main__":
    province_util.update_weather_code()
