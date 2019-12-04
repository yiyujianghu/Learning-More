#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: test.py
@time: 2019/11/28 6:07 下午
"""


import re

datetime_dict = {'year_number':r"([1-9]\d)?\d{2}",
                 'month_number':r"0?[1-9]|1[0-2]",
                 'day_number':r"0?[1-9]|[1-2][0-9]|3[0-1]",
                 'hour_number':r"(20|21|22|23|[0-1]?\d)",
                 'min_sec_number':r"[0-5]?\d"
                 }

# datetime_std = r"(?P<year>(({year_number})(\-|\/|.)?年?)?)" \
#                r"(?P<month>({month_number})(\-|\/|.)?月?)" \
#                r"(?P<day>({day_number})(日|号)?)\s*" \
#                r"(?P<hour>({hour_number})(:|点|时))" \
#                r"(?P<min>({min_sec_number})(:|分))" \
#                r"(?P<second>(({min_sec_number})秒?)?)".format(**datetime_dict)
# datetime_mdhm = r"(?P<year>)" \
#                 r"(?P<month>(({month_number})(\-|\/|.|月))?)" \
#                 r"(?P<day>({day_number})(日|号))\s*" \
#                 r"(?P<hour>({hour_number})(:|点|时))" \
#                 r"(?P<min>(({min_sec_number})分)?)" \
#                 r"(?P<second>)".format(**datetime_dict)
# date_std = r"(?P<year>(({year_number})(\-|\/|.)?年?)?)" \
#            r"(?P<month>(({month_number}))(\-|\/|.)?月?)" \
#            r"(?P<day>(({day_number})(日|号)?)?)" \
#            r"(?P<hour>)(?P<min>)(?P<second>)".format(**datetime_dict)
# date_only = r"(?P<year>({year_number})年)|" \
#             r"(?P<month>({month_number})月)|" \
#             r"(?P<day>({day_number})(日|号))" \
#             r"(?P<hour>)(?P<min>)(?P<second>)".format(**datetime_dict)
# time_std = r"(?P<year>)(?P<month>)(?P<day>)" \
#            r"(?P<hour>(({hour_number})(:|点|时))?)" \
#            r"(?P<min>({min_sec_number})(:|分))" \
#            r"(?P<second>(({min_sec_number})秒?)?)".format(**datetime_dict)
# time_only = r"(?P<year>)(?P<month>)(?P<day>)" \
#             r"(?P<hour>({hour_number})(点|时))|" \
#             r"(?P<min>({min_sec_number})分)|" \
#             r"(?P<second>({min_sec_number})秒)".format(**datetime_dict)
#
#
#
# print(re.search(datetime_std, "2019-3-5 2:3:4").group())
# print(re.search(datetime_std, "99年3月5日12点2分3秒").group())
# print(re.search(datetime_std, "2019年3月5日12点2分3秒").group())
# print(re.search(datetime_std, "2019年3月5日1点2分").group())
# print(re.search(datetime_std, "3月5日12点3分3秒").group())
# print(re.search(datetime_mdhm, "3月5日1点2分").group())
# print(re.search(datetime_mdhm, "5日1点2分").group())
# print(re.search(datetime_mdhm, "5日1点").group())
#
#
# print(re.search(date_std, "2019-3-5").group())
# print(re.search(date_std, "2019年3月5日").group())
# print(re.search(date_std, "19年3月5日").group())
# print(re.search(date_std, "2019年3月").group())
# print(re.search(date_std, "3月5日").group())
# print(re.search(time_std, "12:3:4").group())
# print(re.search(time_std, "12点2分3秒").group())
# print(re.search(time_std, "1点2分").group())
# print(re.search(time_std, "1分3秒").group())
#
# print(re.search(date_only, "1999年").group())
# print(re.search(date_only, "3月").group())
# print(re.search(time_only, "1点").group())
# print(re.search(time_only, "5分").group())



# print(re.search(r"[一-零]+", "一九九九"))
# print(re.search(r"[一-零]+", "二零零零"))
# print(re.search(r"[一-五]+", "一二三四五六七八九"))
#
# result = re.search(r"(?P<num>\d{4})(?P<id>)", "2010")
# x = result.group("num")
# y = result.group("id")
# print(x)
# print(y)
# # print(result.group("num"))
# # print(result.group("id"))

# result = re.search(time_std, "1点2分")
#
# list = ["year", "month", "day", "hour", "min", "second"]
# for i in list:
#     print(result.group(i))

# date_ymd = r"(?P<year>({year_number})*[-/.年]*)" \
#            r"(?P<month>({month_number})*[-/.月]*)" \
#            r"(?P<day>({day_number})*[日号]*)".format(**datetime_dict)
#
# date_md = r"(?P<year>)" \
#           r"(?P<month>({month_number})[-/.月])" \
#           r"(?P<day>({day_number})?[日号]?)".format(**datetime_dict)
#
# date_d = r"(?P<year>)" \
#          r"(?P<month>)" \
#          r"(?P<day>({day_number})[日号])".format(**datetime_dict)
#
# time_HMS = r"(?P<hour>({hour_number})[:点时])" \
#            r"(?P<minute>({min_sec_number})?[:分]?)" \
#            r"(?P<second>({min_sec_number})?秒?)".format(**datetime_dict)
#
# time_MS = r"(?P<hour>)" \
#           r"(?P<minute>({min_sec_number})[:分])" \
#           r"(?P<second>({min_sec_number})?秒?)".format(**datetime_dict)
#
# time_S = r"(?P<hour>)" \
#          r"(?P<minute>)" \
#          r"(?P<second>({min_sec_number})秒)".format(**datetime_dict)



# date_ymd = r"(?P<year>({year_number})*[-/.年]*)" \
#            r"(?P<month>({month_number})*[-/.月]*)" \
#            r"(?P<day>({day_number})*[日号]*)".format(**datetime_dict)
#
# date_md = r"(?P<year>)" \
#            r"(?P<month>({month_number})[-/.月])" \
#            r"(?P<day>({day_number})?[日号]?)".format(**datetime_dict)
#
# date_d = r"(?P<year>)" \
#          r"(?P<month>)" \
#          r"(?P<day>({day_number})[日号])".format(**datetime_dict)
#
# time_std = r"(?P<hour>({hour_number})[:点时])" \
#             r"(?P<min>({min_sec_number})*[:分]*)" \
#             r"(?P<second>({min_sec_number})*秒*)".format(**datetime_dict)
#
#
#
# queryList = ["2019-3-5 2:3:4", "99年3月5日12点2分3秒", "3月5日12点3分3秒", "5日1点2分", "2019-3-5", "5点钟",
#              "2019年3月", "3月5日", "12点2分3秒", "12:13:14", "3月", "1999年", "1点2分", "20:25", "5-5", "2017/2"]
#
# for query in queryList:
#
#     # print("date_std", re.search(date_ymd, query))
#     print("time_std", re.search(time_std, query))


string = "MASK_DT_CAL_I#MASK_TIME_I#，我们在吃火锅，MASK_DT_CAL_II#MASK_DATE_I#的MASK_TIME_II#我们会出去办点事，MASK_DT_CAL_III#MASK_DATE_II#的时候是非常好的天气"

MASK = r"((?P<cal_mask>(MASK_DT_CAL_I+#)的?)|" \
       r"(?P<date_mask>(MASK_DATE_I+#)的?)|" \
       r"(?P<time_mask>(MASK_TIME_I+#)的?))+"

while re.search(MASK, string):
    content = re.search(MASK, string)
    print(content)
    string = re.sub(content.group(), "HAHAHA", string)

print('MASK_DT_CAL_II#MASK_DATE_I#的MASK_TIME_II#'.replace("的", "").split("#"))
