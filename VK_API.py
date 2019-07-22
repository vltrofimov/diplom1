# from urllib.parse import urlencode
import requests
import time
from pprint import pprint

# APP_ID = 7064612
# AUTH_URL = 'https://oauth.vk.com/authorize'
# AUTH_DATA = {
#     "client_id": APP_ID,
#     "display":'page',
#     "scope":'friends',
#     "response_type":'token'
# }
# print('?'.join((AUTH_URL, urlencode(AUTH_DATA))))

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
ID_eshmargunov = '171691064'

#Описывается класс VK_user с методами Get_friends и Get_groups
class VK_user:
    def __init__(self,token,ID):
        self.token=token
        self.ID=ID

    def get_params(self):
        return{
            'access_token':self.token,
            'v':'5.52',
            'user_id': self.ID,
            'order':'hints',
            'name_case' :'nom',
            'ref' :'255',
            'fields' :'nickname'
        }

    def request(self,method,params):
        response = requests.get(
            'https://api.vk.com/method/'+method,
            params=params
        )
        print('.')
        #time.sleep(1)
        return(response)

    def get_banned(self):
        response = self.request('account.getBanned',
                                params={
                                    'access_token':self.token,
                                    'v':'5.52',
                                    'user_id':self.ID,
                                    'count': 200})
        dict_of_banned = response.json()['response']['items']
        list_of_banned = []
        for banned in dict_of_banned:
            list_of_banned.append(banned['id'])
        return(list_of_banned)

    def get_groups(self):
        response = self.request('groups.get',
                                params={
                                    'access_token':self.token,
                                    'v':'5.52',
                                    'user_id':self.ID,
                                    'extended': 1})
        time.sleep(1)
        return(response.json()['response']['items'])
    def get_friends(self):
        params=self.get_params()
        response=self.request(
            'friends.get',
            params=params
        )
        dict_of_friends=response.json()['response']['items']
        list_of_friends=[]
        for friend in dict_of_friends:
            list_of_friends.append(friend['id'])
        return (list_of_friends)

eshmargunov = VK_user(TOKEN, ID_eshmargunov)
list_of_groups_ID=[]
for i in eshmargunov.get_groups():
    list_of_groups_ID.append(i['id']) #формируется список ID групп Евгения Шмаргунова
    set_of_groups_ID=set(list_of_groups_ID) #формируется множество для дальнейшего сравнения с мнодествами групп друзей Евгения
print(set_of_groups_ID)

list_of_friends=[]
list_of_groups=[]
list_of_friends_groups_ID=[]
# # set_of_friend_group_ID=()
# #
for friend_id in eshmargunov.get_friends():
    list_of_friends.append(VK_user(TOKEN, friend_id))
for friend in list_of_friends:
    try:
        list_of_groups.append(friend.get_groups())
    except:
        continue
for groups in list_of_groups:
    for group in groups:
        try:
            list_of_friends_groups_ID.append(group['id'])
        except:
            continue

set_of_friend_group_ID=set(list_of_friends_groups_ID)
list_of_result=[]
for i in eshmargunov.get_groups():
    if i['id'] in (set_of_groups_ID-set_of_friend_group_ID):
        list_of_result.append(i)
pprint(list_of_result)