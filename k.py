# from utils.db import get_service, get_notes, get_free_date
# from datetime import datetime, time

# durations = get_service(1).durations
# print(durations)

# date = get_free_date(1)
# print(date.date)
# busy_slots = []
# for time in get_notes(1):
#     time = datetime.strptime(time.time, '%H:%M')
#     end_time = time + durations
#     start_time = time - durations
#     busy_slots.append({"start": start_time.time(), "end": end_time.time()})

# # time = datetime.strptime('10:00', '%H:%M').time()
# # print(time)