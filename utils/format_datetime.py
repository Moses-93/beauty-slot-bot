from datetime import datetime

class FormatDate():

    def formats_datetime_to_date_str(self, date: datetime):
        return date.strftime('%Y-%m-%d')
    
    def formats_date_str_to_datetime(self, date: str):
        return datetime.strptime(date, '%Y-%m-%d')
    

class FormatTime():

    def formats_time_str_to_datetime(self, time: str):
        return datetime.strptime(time, '%H:%M')
    
    def formats_datetime_to_time_str(self, date: datetime):
        return date.strftime('%H:%M')

    def now_datetime(self):
        return datetime.now()
    

class NowDatetime():

    def now_datetime(self):
        return datetime.now()
    
