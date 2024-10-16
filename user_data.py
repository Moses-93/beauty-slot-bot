user_data = {}
from db.commands import GetService, GetFreeDate, GetNotes


def get_user_data(user_id, *args):

    if not args:
        return user_data[user_id]

    return tuple(user_data[user_id].get(key) for key in args)


def set_user_data(user_id, **kwargs):

    if user_id not in user_data:
        user_data[user_id] = {}

    for key, value in kwargs.items():
        user_data[user_id][key] = value


notes = GetNotes(user_id=1763711362).get_all_notes()
for n in notes:
    print(n)
