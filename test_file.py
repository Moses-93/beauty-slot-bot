from db.db_writer import service_manager, date_manager
import asyncio
from datetime import timedelta, datetime, time
from db.db_reader import GetService, GetFreeDate


# async def main(date):
#     date_time = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time(18, 0))
#     await date_manager.create(date=date_time.date(), free=True, now=date_time)


# asyncio.run(main("2024-11-01"))

# date = GetFreeDate(date="2024-10-31").date
# print(date)