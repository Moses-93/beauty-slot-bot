user_data = {}
from utils.db import get_service

def get_user_data(user_id, *args):

    if not args:
        return user_data[user_id]
    
    return {key: user_data[user_id].get(key) for key in args}


def set_user_data(user_id, **kwargs):

    if user_id not in user_data:
        user_data[user_id] = {}
    
    for key, value in kwargs.items():
        user_data[user_id][key] = value

# service = get_service(1)
# res = set_user_data(1, service=service)
# print(res)
# print(user_data[1].get('service').name)
