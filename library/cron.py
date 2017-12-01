#-*-coding utf-8-*-
from .models import library_profile, user_barrow_books, server_api, user_token
import json
from datetime import datetime
import requests
import ruamel.yaml as yaml

def scheduled_job():
    print('really')
    for user in library_profile.objects.all() :
        u = user_barrow_books.objects.get(username = user.username)
        t = user_token.objects.filter(username = user.username)

        info = json.loads(u.info)
        print(type(info))
        print(type(yaml.safe_load(u.info)))

        for key, value in info.items():
	    #test datetime.today().strftime("%Y/%m/%d")
            if value == '2017/11/29' :

                for token in t :
                    headers = {
                        'Authorization': 'key='+ server_api.objects.get(pk=1).server_api,
                        'Content-Type': 'application/json',
                    }

                    data = '{\n  "notification": {\n    "title": '+'"'+key+'"'+',\n    "body": "please test",\n    "click_action": "http://www.naver.com"\n  },\n  "to": '+ '"'+token.token+'"' +'\n}'
                    print(data)
                    a = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=data.encode('utf-8'))
                    print(a.text)