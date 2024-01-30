import os
from tinydb import TinyDB
# As you can see the path of your accounts accounts username and password
# are visible to anyone on github so it is your responsibility to protect this file
# or change it to something else. Whatever you choose is your responsibility.
db_path = os.path.join(os.getenv('LOCALAPPDATA'), 'List-App', 'ListAppDB.json')
db_dir = os.path.dirname(db_path)
if not os.path.exists(db_dir):
    os.makedirs(db_dir)
    print(db_path)

def get_database():
    return TinyDB(db_path)
