#!/usr/bin/env python
# encoding: utf-8
"""
@author: Dong Jun
@file: DateNumParser.py
@time: 2019/11/30 5:48 下午
"""


import time, datetime
import re
from number_extract import NumberExtract
from Rules_of_Number import Rules_of_Number


class DateNumParser():
    def __init__(self, content, source_DT=None):
        self.content = content
        self.res_content = content
        self.source_DT = datetime.datetime.now() if not source_DT else self.parseSourceDT(source_DT)
        # 以下四个属性是为了给数字日期等打MASK，便于循环检测到最后，然后按照标识依次拼接
        self.MASK_DT_CAL = {"count":0, "default":{"analyzed": {}, "original": "", "time_interval": -1}}
        self.MASK_DATE = {"count":0, "default":{'analyzed':[-1, -1, -1], 'original':""}}
        self.MASK_TIME = {"count":0, "default":{'analyzed':[-1, -1, -1], 'original':""}}
        self.MASK_FINAL = {"count":0}

        self.result_display = ""


    def parseSourceDT(self, sourceDT):
        if sourceDT:
            if isinstance(sourceDT, datetime.datetime):
                refTime = sourceDT
            elif isinstance(sourceDT, time.struct_time):
                refTime = datetime.datetime(*sourceDT[:6])
            else:
                refTime = datetime.datetime.now()   # 这里其实可以写成字符串处理方法
        else:
            refTime = datetime.datetime.now()   # 这里其实可以写成字符串处理方法
        return refTime


    def time_special_parse(self, query):
        time_special_rule_subtract_front = Rules_of_Number.time_special_rule_subtract_front
        time_special_rule_subtract_back = Rules_of_Number.time_special_rule_subtract_back
        time_special_rule_plus = Rules_of_Number.time_special_rule_plus
        time_special_dict = {"半":30, "一刻":15, "三刻":45}
        char_new = query
        def time_special_rule_subtract_extract(time_special_min, time_special_hour):
            if time_special_min in time_special_dict.keys():
                time_special_min_num = time_special_dict.get(time_special_min)
            else:
                time_special_min_num = NumberExtract.detect(time_special_min)
            time_special_min_num = 60 - int(time_special_min_num)
            time_special_hour_num = int(NumberExtract.detect(time_special_hour))
            time_special_hour_num = time_special_hour_num-1 if time_special_hour_num >= 1 else 23
            time_special_num = ":".join([str(time_special_hour_num), str(time_special_min_num)])
            return time_special_num

        while re.search(time_special_rule_subtract_front, char_new) or re.search(time_special_rule_subtract_back, char_new):
            if re.search(time_special_rule_subtract_front, char_new):
                time_special_query = re.search(time_special_rule_subtract_front, char_new).group()
                time_special_min, time_special_hour = time_special_query.\
                    replace("点", "").replace("差", "").replace("一刻","一刻分").split("分")
                time_special_num = time_special_rule_subtract_extract(time_special_min, time_special_hour)
                char_new = re.sub(time_special_rule_subtract_front, time_special_num, char_new, count=1)
            elif re.search(time_special_rule_subtract_back, char_new):
                time_special_query = re.search(time_special_rule_subtract_back, char_new).group()
                time_special_hour, time_special_min = time_special_query.\
                    replace("点", "").replace("分", "").split("差")
                time_special_num = time_special_rule_subtract_extract(time_special_min, time_special_hour)
                char_new = re.sub(time_special_rule_subtract_back, time_special_num, char_new, count=1)
            else:
                break

        while re.search(time_special_rule_plus, char_new):
            time_special_query = re.search(time_special_rule_plus, char_new).group()
            time_special_hour, time_special_min = time_special_query.replace("分", "").split("点")
            if time_special_min in time_special_dict.keys():
                time_special_min_num = time_special_dict.get(time_special_min)
            elif time_special_min == "":
                time_special_min_num = "00"
            else:
                time_special_min_num = NumberExtract.detect(time_special_min)
            time_special_hour_num = NumberExtract.detect(time_special_hour)
            time_special_num = ":".join([str(time_special_hour_num), str(time_special_min_num)])
            char_new = re.sub(time_special_rule_plus, time_special_num, char_new, count=1)
        return char_new


    def numeric_tag(self, number):
        if isinstance(number, float):
            number = int(number)
        elif isinstance(number, str):
            try:
                number = int(number)
            except:
                return ""
        if isinstance(number, int):
            result = "".join(["I" for i in range(number)])
            return result
        else:
            return ""


    def special_parse(self):
        pass



    def synonym_normalizer(self):
        pass


    def datetime_offset_calculate(self, dt_cal_dict):
        time_interval = Rules_of_Number.dt_calculate_dict["time_interval"][dt_cal_dict["time_interval"]]
        dt_offset = {"year_offset":0, "month_offset":0, "week_offset":0, "day_offset":0,
                     "hour_offset":0, "minute_offset":0, "second_offset":0, "week_value":-1}
        for offset in dt_offset.keys():
            string_offset = NumberExtract.detect(dt_cal_dict[offset])
            if re.search(r"\d+", string_offset):
                value = re.search(r"\d+", string_offset).group()
                if re.search(r"前", string_offset):
                    value = ~int(value)+1
                dt_offset[offset] = value
            else:
                continue
        week_value = dt_offset["week_value"]
        time_delta_dict = {}
        time_delta_dict["weeks"] = Rules_of_Number.dt_calculate_dict["weeks"][dt_cal_dict["weeks"]] + dt_offset["week_offset"]
        time_delta_dict["days"] = (Rules_of_Number.dt_calculate_dict["days"][dt_cal_dict["days"]] + dt_offset["day_offset"]) + \
                                  (Rules_of_Number.dt_calculate_dict["months"][dt_cal_dict["months"]] + dt_offset["month_offset"]) * 30 + \
                                  (Rules_of_Number.dt_calculate_dict["years"][dt_cal_dict["years"]] + dt_offset["year_offset"]) * 365
        time_delta_dict["hours"] = dt_offset["hour_offset"]
        time_delta_dict["minutes"] = dt_offset["minute_offset"]
        time_delta_dict["seconds"] = dt_offset["second_offset"]
        return time_delta_dict, time_interval, week_value


    def dt_offset_analyze(self, query):
        dt_cal_list = ["years", "year_offset", "months", "month_offset", "weeks", "week_value", "week_offset",
                       "days", "day_offset", "time_interval", "hour_offset", "minute_offset", "second_offset"]
        res_query = query
        while re.search(Rules_of_Number.dt_calculate_rule, res_query):
            # 计数-->re.search提取-->生成结果dict-->转化成timedelta能解析的模式-->拼接计数的key-->存入self.MASK-->原文替换
            self.MASK_DT_CAL["count"] += 1
            current_dt_cal = re.search(Rules_of_Number.dt_calculate_rule, res_query)
            current_dt_cal_dict = {}
            for dt in dt_cal_list:
                if current_dt_cal.group(dt):
                    current_dt_cal_dict[dt] = current_dt_cal.group(dt).replace("的", "")
                else:
                    current_dt_cal_dict[dt] = "default"
            time_delta_dict, time_interval, week_value = self.datetime_offset_calculate(current_dt_cal_dict)
            MASK_DT_CAL_FLAG = "MASK_DT_CAL_{}_".format(self.numeric_tag(self.MASK_DT_CAL["count"]))
            origin_str = current_dt_cal.group()
            self.MASK_DT_CAL[MASK_DT_CAL_FLAG] = {"analyzed":time_delta_dict, "original":origin_str,
                                                  "time_interval":time_interval, "week_value":week_value}
            res_query = re.sub(origin_str, MASK_DT_CAL_FLAG, res_query, count=1)
        return res_query


    def datetime_std_parse(self, query, type="TIME"):
        if type == "DATE":
            rules = [Rules_of_Number.date_ymd, Rules_of_Number.date_md, Rules_of_Number.date_d]
            MASK_DICT = self.MASK_DATE
            MASK_STR = "MASK_DATE_{}_"
            dt_range = (0, 3)
        elif type == "TIME":
            rules = [Rules_of_Number.time_std]
            MASK_DICT = self.MASK_TIME
            MASK_STR = "MASK_TIME_{}_"
            dt_range = (3, 6)
        else:
            return query
        res_content_dt = query
        dt_char_list = ["year", "month", "day", "hour", "minute", "second"]
        for rule in rules:
            while re.search(rule, res_content_dt):
                MASK_DICT["count"] += 1
                current_dt = re.search(rule, res_content_dt)
                current_dt_list = []
                for dt_count in range(*dt_range):
                    if current_dt.group(dt_char_list[dt_count]):
                        current_dt_list.append(
                            int("".join(filter(str.isdigit, current_dt.group(dt_char_list[dt_count])))))
                    else:
                        current_dt_list.append(-1)
                MASK_DATE_FLAG = MASK_STR.format(self.numeric_tag(MASK_DICT["count"]))
                origin_str = current_dt.group()
                MASK_DICT[MASK_DATE_FLAG] = {"analyzed": current_dt_list, "original": origin_str}
                res_content_dt = re.sub(origin_str, MASK_DATE_FLAG, res_content_dt, count=1)
        return res_content_dt


    def datetime_connect(self, query):
        dt_final_list = ["cal_mask", "date_mask", "time_mask"]
        dt_char_list = ["year", "month", "day", "hour", "minute", "second"]
        source_dt_list = [self.source_DT.__getattribute__(dt) for dt in dt_char_list]   # 标准时间
        res_query = query
        while re.search(Rules_of_Number.MASK_RULE, res_query):
            self.MASK_FINAL["count"] += 1
            content_mask_final = re.search(Rules_of_Number.MASK_RULE, res_query)
            content_mask_dict = {}
            for dt in dt_final_list:
                if content_mask_final.group(dt):
                    content_mask_dict[dt] = content_mask_final.group(dt).replace("的", "")
                else:
                    content_mask_dict[dt] = "default"
            BASE_DT_LIST = self.MASK_DATE[content_mask_dict['date_mask']]["analyzed"] + \
                           self.MASK_TIME[content_mask_dict['time_mask']]["analyzed"]
            time_interval = self.MASK_DT_CAL[content_mask_dict['cal_mask']]["time_interval"]
            if len(BASE_DT_LIST) == 6:
                for i in range(6):
                    if i == 3 and time_interval != -1:
                        BASE_DT_LIST[i] = BASE_DT_LIST[i] if BASE_DT_LIST[i] != -1 else time_interval
                        BASE_DT_LIST[i] = BASE_DT_LIST[i]+12 if (time_interval>12 and BASE_DT_LIST[i]<12) else BASE_DT_LIST[i]
                    BASE_DT_LIST[i] = BASE_DT_LIST[i] if BASE_DT_LIST[i] != -1 else source_dt_list[i]
            else:
                print("时间日期数组长度出错")
                return ""
            BASE_DT = datetime.datetime(*BASE_DT_LIST)
            # 以下为日期推算
            BASE_WEEK = BASE_DT.strftime("%w")
            week_value = self.MASK_DT_CAL[content_mask_dict['cal_mask']]["week_value"]
            if week_value != -1:
                week_days_offset = int(week_value) - int(BASE_WEEK)
            else:
                week_days_offset = 0

            BASE_DT_FINAL = BASE_DT + \
                            datetime.timedelta(**self.MASK_DT_CAL[content_mask_dict['cal_mask']]["analyzed"]) + \
                            datetime.timedelta(days=week_days_offset)
            MASK_DT_FINAL_FLAG = "MASK_DT_FINAL_{}_".format(self.numeric_tag(self.MASK_FINAL["count"]))
            ORIGIN_STR =self.MASK_DT_CAL[content_mask_dict['cal_mask']]["original"] + \
                        self.MASK_DATE[content_mask_dict['date_mask']]["original"] + \
                        self.MASK_TIME[content_mask_dict['time_mask']]["original"]
            self.MASK_FINAL[MASK_DT_FINAL_FLAG] = {"analyzed": BASE_DT_FINAL, "original": ORIGIN_STR}
            print("self.MASK_DT_FINAL", self.MASK_FINAL)
            res_query = re.sub(content_mask_final.group(), MASK_DT_FINAL_FLAG, res_query)
        return res_query


    def datetime_parse(self, content):
        # 考虑到下周一这种，避免"下周13：20"这种干扰出现，将其替换为_MASK_DT_CAL_，并依次存入self.dt_cal_result
        res_content_cal_dt = self.dt_offset_analyze(content)
        # 提取特殊时间，如一点半，差5分3点等，变成带"xx:xx"的指定字符串，并将其他汉字也转成数字
        res_content_special_dt = self.time_special_parse(res_content_cal_dt)
        # 排除了上边两步之后，将所有汉字转化为阿拉伯数字
        res_content_char2num = NumberExtract.detect(res_content_special_dt)
        # 将字符串中的标准日期解析出来，替换为_MASK_DT_STD_，然后依次存入self.dt_result
        res_content_std_time = self.datetime_std_parse(res_content_char2num, type="TIME")
        res_content_std_date = self.datetime_std_parse(res_content_std_time, type="DATE")
        # 这里已经将所有的数字格式时间提取出来，然后根据上下文做推理，然后拼接到current_dt_list中，然后拼入datetime
        res_mask_dt = self.datetime_connect(res_content_std_date)
        print(res_mask_dt)
        return res_mask_dt


    def display(self):
        pass


    def quantifier_parse(self):
        pass


    def parse(self):
        pass


if __name__ == "__main__":
    # parse = DateNumParser("今天下午三点半，我和他一起出去，明天下午两点二十,后天二十三点一刻和大后天十点零二分,上午十点")
    # parse = DateNumParser("今天下午差五分五点，我们在吃火锅，去年五月三号的六点半我们会出去办点事，今年五月十五号的时候是非常好的天气")
    parse = DateNumParser("时间定在下周一下午的五点半")
    parse.datetime_parse("时间定在下周一下午的五点半")

