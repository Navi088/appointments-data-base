from datetime import timedelta, datetime as dt
from hours import hours

class AvailableSchedule:
    def making_appointment(self, db, room, date):

        current_time = dt.now()
        format_ct = f"{current_time.year}-{current_time.month}-{current_time.day}"
        current_hour = timedelta(
            hours=current_time.hour, 
            minutes=current_time.minute,
            seconds=current_time.second)

        get_hours = []
        sch_list = []

        for x in hours:
            get_hours.append(x)

        cursor = db.connection.cursor()
        cursor.execute(f"""SELECT appt_hour FROM medical_appointment 
                    WHERE (appt_date = '{date}' AND room = {room})
                    ORDER BY appt_hour ASC""")
        data = cursor.fetchall()

        try:
            for x in data:
                element = x[0]
                search = [s for s in get_hours if element == s]
                sch_list.append(search[0])
                
            for y in sch_list:
                get_hours.remove(y)
        except:
            print ("ocurrio un error")
        
        preparing_date = dt.strptime(f"{date} 00:00:00","%Y-%m-%d %H:%M:%S")
        format_pd = f"{preparing_date.year}-{preparing_date.month}-{preparing_date.day}"

        counter_list = []

        n = 0
        for i in get_hours:
            if format_pd == format_ct and i > current_hour:
                n+=1
                counter_list.append(i)
                
            elif dt.strptime(f"{date} {i}", "%Y-%m-%d %H:%M:%S") > current_time:
                n+=1
                counter_list.append(i)
                
        return counter_list