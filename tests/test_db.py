# import unittest
# from unittest.mock import patch

# from datetime import datetime, timedelta
# from utils.time_processing import find_nearest_available_time, time_check, date_check, get_busy_slots, check_slot

# class TestTimeProcessing(unittest.TestCase):

#     def setUp(self):
#         # Підготовка тестових даних
#         self.busy_slots = [
#             {"start": datetime(2024, 10, 15, 14, 0), "end": datetime(2024, 10, 15, 15, 0)},
#             {"start": datetime(2024, 10, 15, 16, 0), "end": datetime(2024, 10, 15, 17, 0)},
#         ]
#         self.service_duration = timedelta(minutes=30)
#     @patch('user_data.get_user_data')
#     def test_find_nearest_available_time(self, mock_get_user_data):
#         mock_get_user_data.return_value =
#         current_time = datetime(2024, 10, 15, 13, 30)
#         nearest_time = find_nearest_available_time()
