#	天气爬虫介绍

本项目主要用于爬取[http://www.weather.com.cn](http://www.weather.com.cn "中国天气网")的过去24小时的天气数据。用于后续结合gps信息做相关精准分析。


##	天气对应省市县编码：main\generate\_weather\_code.py

主要抓取各个省市县对应中国天气网所对应的省市县编码：

- 直辖市的编码规则:省县市
- 其他省市县的编码规则:省市县

该脚本只在初始化的时候执行一次

## 工具类:tools

- province_util:省市县编码操作类
- spider_request:request辅助类
- db_connector:db连接器

## 天气爬取：weather\weather_spider.py

该脚本主要根据获取的天气编码获取对应的天气信息，并序列化成指定格式

- 使用方式：weather_spider.weather_spider()
- 返回数据格式：

	
```json

[
  {
    "weather_code": "101010100",
    "province": "10101",
    "city": "00",
    "county": "01",
    "data": [
      {
        "datetime": "2018-04-27 16:00:00",
        "temperature": "25",
        "winddirection": "\u897f\u5357\u98ce",
        "windforce": "3",
        "rainfall": "0.0",
        "humidity": "21",
        "airquality": ""
      },
      {
        "datetime": "2018-04-27 15:00:00",
        "temperature": "25",
        "winddirection": "\u897f\u5357\u98ce",
        "windforce": "4",
        "rainfall": "0.0",
        "humidity": "22",
        "airquality": "111"
      }
    ]
  },
  {
    "weather_code": "101020100",
    "province": "10102",
    "city": "00",
    "county": "01",
    "data": [
      {
        "datetime": "2018-04-27 16:00:00",
        "temperature": "25",
        "winddirection": "\u897f\u5357\u98ce",
        "windforce": "3",
        "rainfall": "0.0",
        "humidity": "21",
        "airquality": ""
      },
      {
        "datetime": "2018-04-27 15:00:00",
        "temperature": "25",
        "winddirection": "\u897f\u5357\u98ce",
        "windforce": "4",
        "rainfall": "0.0",
        "humidity": "22",
        "airquality": "111"
      }
    ]
  }
]
```
	



##	代理爬取脚本：proxies\proies_spider.py

目前还未完善

