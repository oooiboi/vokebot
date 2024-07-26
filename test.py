

import schedule
import time
import threading
from datetime import time, timedelta


def job():
    print("I'm working...")

reminder_time = time(18, 53, 00).strftime("%H:%M")


schedule.every().day.at(reminder_time).do(job)
while True:
    schedule.run_pending()

  
"""
reminder в определенное время

допустим 9 утра 15 дня и 7 вечера 

если йес произошел то можно отправлять похвальные сообщения в это время вместо напоминаний

стоит ли создавать временные погрешности в напоминаниях или эффективнее когда юзер ожидает конкретное время
например напоминание приходит в рандомный момент в промежутке с 14 00 до 16 00

"""
