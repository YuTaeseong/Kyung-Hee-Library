from .models import library_profile, user_barrow_books, server_api, user_token
import json
from datetime import datetime
import requests

def scheduled_job():

    for user in library_profile.objects.all() :
        u = user_barrow_books.objects.get(username = user)
        t = user_token.objects.filters(username = user)

        info = json.loads(u.info)

        for key, value in info.items():
            if value == datetime.today().strftime("%Y/%m/%d") :
                for token in t :
                    headers = {
                        'Authorization': 'key='+ server_api.objects.get(pk=1),
                        'Content-Type': 'application/json',
                    }

                    data = '{\n  "notification": {\n    "title": '+key+',\n    "body": "반납 당일입니다. 빨리 반납하세요",\n    "click_action": "http://www.naver.com"\n  },\n  "to": '+ token.token +'\n}'

                    requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=data)