# coding:utf-8
import re
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class DateRange:
    def __init__(self):
        self.now = datetime.now()
        self.today = self.now.date()
        self.tomorrow = (self.now + timedelta(days=1)).date()

        self.yesterday = (self.now - timedelta(days=1)).date()
        self.the_day_before_yesterday = (self.now - timedelta(days=2)).date()

        self.this_month = (self.now.replace(day=1)).date()
        self.next_month = (self.now + relativedelta(months=1)).replace(day=1).date()
        self.last_month = (self.now - relativedelta(months=1)).replace(day=1).date()

        self.last_year = (self.today - relativedelta(months=12)).replace(month=1, day=1)
        self.llast_year = self.last_year - relativedelta(months=12)
        self.lllast_year = self.last_year - relativedelta(months=24)
        self.this_year = (self.now.replace(month=1,day=1)).date()
        self.next_year = (self.now + relativedelta(months=12)).replace(month=1, day=1).date()

        self.this_week = (self.now - timedelta(self.now.weekday())).date()
        self.last_week = (self.this_week - timedelta(days=7))

        self.year = (self.now.replace(month=1,day=1)).date().year

    def replace(self, datestr):
        datestr = datestr.replace('一', '1').replace('二', '2').replace('三', '3').replace('四', '4').replace('五', '5').replace('六', '6') \
        .replace('七', '7').replace('八', '8').replace('九', '9').replace('十一', '11').replace('十二', '12').replace('十', '10')\
        .replace('零', '0').replace('〇', '0').replace(' ', '')
        print(datestr)
        return datestr

    def parser(self, datestr):

        reg = re.findall(r'(\d+).(\d+).(\d+)', datestr)
        if len(reg) == 1: 
            y, m, d = reg[0]
            return datetime(int(y), int(m), int(d)), timedelta(days=1)

        reg = re.findall(r'(\d+)年(\d+)月', datestr)
        if len(reg) == 1: 
            y, m = reg[0]
            return datetime(int(y), int(m), 1), relativedelta(months=1)
        
        reg = re.findall(r'^(\d+)月(\d+)', datestr)
        if len(reg) == 1: 
            m, d = reg[0]
            y = self.today.year
            return datetime(int(y), int(m), int(d)), timedelta(days=1)

        reg = re.findall(r'^(\d+).(\d+)', datestr)
        if len(reg) == 1:
            m, d = reg[0]
            y = self.today.year
            return datetime(int(y), int(m), int(d)), timedelta(days=1)

        if '现在' in datestr: return self.today, timedelta(days=1)

        __day = {
                "昨天": (self.yesterday, timedelta(days=1)),
                "前天": (self.the_day_before_yesterday, timedelta(days=1)),
                "大前天": (self.the_day_before_yesterday - timedelta(days=1), timedelta(days=1)),
                "今天": (self.today, timedelta(days=1)),
        }

        __week = {
                "本周": (self.this_week, self.today - self.this_week + timedelta(days=1)),
                "上周": (self.last_week, timedelta(days=7)),
                "上周日": (self.last_week + timedelta(days=7), timedelta(days=1)),
                "本周日": (self.this_week + timedelta(days=7), timedelta(days=1))
        }

        __month = {
                "上个月": (self.last_month, relativedelta(months=1)),
                "本月": (self.this_month, self.today - self.this_month + timedelta(days=1)),
                "这个月": (self.this_month, self.today - self.this_month + timedelta(days=1))
        }

        __year = {
                "去年": (self.last_year, relativedelta(months=12)),
                "前年": (self.llast_year, relativedelta(months=12)),
                "大前年": (self.lllast_year, relativedelta(months=12)),
                "今年": (self.this_year, relativedelta(months=12)) 
        }


        ### 处理天的问题
        keywords_day = ["昨天", "大前天", "前天", "今天"]
        for word in keywords_day:
            if word in datestr:
                return __day.get(word)

        ### 处理周的问题
        keywords_weekend = ["本周日", "上周日"]
        for word in keywords_weekend:
            if word in datestr:
                return __week.get(word)


        keywords_week = ["本周", "上周"] 
        reg = re.findall(r'(\d+)', datestr)
        reg2 = re.findall(r'上周\D+', datestr)
        reg3 = re.findall(r'上周$', datestr)

        if reg2 or reg3:
            return __week.get("上周")

        if len(reg) == 1: day = int(reg[0])
        else: day = 1
        for word in keywords_week:
            if word in datestr:
                return  __week.get(word)[0] + timedelta(days=day), timedelta(days=1)

        ### 处理月的问题
        keywords_month = ["上个月", "本月", "这个月"]
        reg = re.findall(r'月(\d+)', datestr)
        if len(reg) == 0:
            for word in keywords_month:
                if word in datestr:
                    return __month.get(word)

        if len(reg) == 1:
            for word in keywords_month:
                if word in datestr:
                    y = self.today.year
                    m = __month.get(word)[0].month
                    d = int(reg[0])
                    return datetime(y, m, d), timedelta(days=1)

        ### 处理年的问题
        keywords_year = ["去年", "今年", "前年", "大前年"]
        reg1 = re.findall(r'年(\d+)月(\d+)', datestr)
        reg2 = re.findall(r'年(\d+)月\D?', datestr)
        for word in keywords_year:
            if word in datestr and len(reg1) == 1:
                ### 年月日都存在
                y = __year.get(word)[0].year
                m, d = reg1[0]
                return datetime(y, int(m), int(d)), timedelta(days=1)
            if word in datestr and len(reg2) == 1:
                y = __year.get(word)[0].year
                m = int(reg2[0])
                print(reg2)
                d = 1
                return datetime(y, m, d), relativedelta(months=1)

            if '去年' in datestr and len(reg1) == 0 and len(reg2) == 0:
                return self.last_year, relativedelta(months=12)

            if '前年' in datestr and len(reg1) == 0 and len(reg2) == 0:
                return self.llast_year, relativedelta(months=12)

            if '今年' in datestr and len(reg1) == 0 and len(reg2) == 0:
                return self.this_year, relativedelta(months=12)

        return None, None

    def date_range(self, datestr):

        ## 如果有多个-号，正常来说应该成对出现，如果不是成对出现，不予理会
        minus_count = datestr.count('-')
        if minus_count >= 2 and minus_count % 2 == 0: datestr = datestr.replace('-', '/')

        ## 不对称，姑且认为中间的是个分隔符，我们认为这是非法的，毕竟这种表述人都不愿意看
        ## 所以没必要在处理这种特殊情况
        if minus_count >= 3 and minus_count % 2 != 0:
            return None, None

        self.datestr = self.replace(datestr)
        ran = re.split(r'[-到至]', self.datestr)
        ran_length = len(ran)
        if ran_length == 2:
            a, b = ran
            begin = self.parser(a)[0]
            if begin is None: return None, None
            end = self.parser(b)[0]
            if end is None: return None, None
            end = end + timedelta(days=1)
            return begin, end
        elif ran_length == 1:
            a, b = self.parser(self.datestr)
            if a is None: return None, None
            begin = a
            end = a + b
            return begin, end
        else:
            return None, None


def get_date_range(datestr):
    dt = DateRange()
    return dt.date_range(datestr)

def date_parser(datestr):
    datestr = datestr.replace('-', '/')
    dt = DateRange()
    return dt.parser(datestr)
