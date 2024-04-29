import requests
import os
import json
from Crypto.Util.number import long_to_bytes, bytes_to_long
import time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

BASE_URL = 'http://130.192.5.212:6522'
LOGIN_URL = f'{BASE_URL}/login'
FLAG_URL = f'{BASE_URL}/flag'

K_TIME = 24 * 60 * 60


def get_cookie(username, admin, expire_date):
    return f"username={username}&expires={expire_date}&admin={admin}"
    
def main():

    with requests.Session() as sess:

        username = 'admin'
        admin = 1
        r = sess.get(LOGIN_URL, params={
            'username': username,
            'admin': admin
        })
        expire_date = int(time.time()) + 30 * K_TIME
        cookie = get_cookie(username, admin, expire_date)

        res = json.loads(r.text)

        res['cookie'] = long_to_bytes(res['cookie'])
        # print(res)
        assert len(res['cookie']) == len(cookie.encode())

        key = bytes([a^b for a,b in zip(res['cookie'], cookie.encode())])


        n1 = 290 * K_TIME
        n2 = 300 * K_TIME

        for i in range(10, 300):

            forged_time = int(time.time()) + i * K_TIME
            # print('forged_time: ', forged_time)
            forged_cookie = get_cookie('admin', 1, forged_time)
            encoded = bytes_to_long(bytes([a^b for a,b in zip(key, forged_cookie.encode())]))

            res['cookie'] = encoded

            r = sess.get(FLAG_URL, params=res)
            if 'OK' in r.text:
                print('flag: ', r.text)
                break
        else: 
            print('flag not found')


    pass

if __name__ == "__main__":
    main()