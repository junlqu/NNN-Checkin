import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time

load_dotenv()

config = {
  "type": os.getenv("TYPE"),
  "project_id": os.getenv("PROJECT_ID"),
  "private_key_id": os.getenv("PRIVATE_KEY_ID"),
  "private_key": os.getenv("PRIVATE_KEY"),
  "client_email": os.getenv("CLIENT_EMAIL"),
  "client_id": os.getenv("CLIENT_ID"),
  "auth_uri": os.getenv("AUTH_URI"),
  "token_uri": os.getenv("TOKEN_URI"),
  "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER"),
  "client_x509_cert_url": os.getenv("CLIENT_URL")
}
url = os.getenv("URL")
cred = credentials.Certificate(config)

app = firebase_admin.initialize_app(
    cred,
    {'databaseURL' : url}
)

def create_dictionary():
    date = time.localtime().tm_mday
    d = {}
    for i in range(1, 31):
        d[str(i)] = True if i <= date else False
    return d

def set_up(id):
    ref = db.reference(f'/')
    ref.push(id)
    ref = db.reference(f'/{id}')
    ref.update(create_dictionary())

# Return 0 if newly updated, 1 if already updated, 2 if already failed
def update_current_date(id):
    ref = db.reference(f'/{id}')
    if ref.get() == None:
        set_up(id)
        return 0
    else:
        date = time.localtime().tm_mday
        ref1 = ref.child(f'{date}')
        ref0 = ref.child(f'{date - 1}')
        
        if ref0.get() == False:
            return 2
        if ref1.get() == True:
            return 1

        ref.update({date: True})
        return 0

# Return the number of days the person lasted
def days_lasted(id):
    counter = 0
    r = db.reference(f'/{id}')
    while (r.child(f'{counter + 1}').get()):
        counter = counter + 1
    return counter

# Returns filtered dictionary of only user ids
def user_ids(dic):
    new = dict()
    for (key, val) in dic.items():
        if key.isnumeric():
            new[key] = val
    return new

# Return a list of users that failed to check in
def users_failed():
    failed = []
    ref = db.reference(f'/')
    users = user_ids(ref.get())
    print(users)
    for (user, vals) in users.items():
        if vals[time.localtime().tm_mday - 1] == False and vals[time.localtime().tm_mday - 2] == True:
            failed.append(user)
    print(failed)
    return failed

# Return a list of users that failed the challenge
def failed_chal():
    failed = []
    ref = db.reference(f'/')
    users = user_ids(ref.get())
    for (user, vals) in users.items():
        if vals[time.localtime().tm_mday - 1] == False:
            failed.append(user)
    return failed

# Return a list of the users that are still in the challenge
def in_chal():
    cont = []
    ref = db.reference(f'/')
    users = user_ids(ref.get())
    for (user, vals) in users.items():
        if vals[time.localtime().tm_mday - 1] == True:
            cont.append(user)
    return cont

# Return a list of users that are in the challenge that have not checked in today
def not_checked():
    cont = []
    ref = db.reference(f'/')
    users = user_ids(ref.get())
    for (user, vals) in users.items():
        if vals[time.localtime().tm_mday] == False and vals[time.localtime().tm_mday - 1] == True:
            cont.append(user)
    return cont

# Returns the seconds before december ends
def countdown():
    t = time.localtime()
    return (30 - t.tm_mday) * 86400 + (23 - t.tm_hour) * 3600 + (59 - t.tm_min) * 60 + (59 - t.tm_sec)