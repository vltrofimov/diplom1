import requests
import time
from pprint import pprint
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
        return(response)

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

def set_of_user_group_id(token, id):
    user = VK_user(token,id)
    list_of_groups_ID = []
    for group in user.get_groups():
        list_of_groups_ID.append(group['id'])
        set_of_groups_ID=set(list_of_groups_ID)
    return (set_of_groups_ID)

def set_of_friends_group_id(token,id):
    user = VK_user(token, id)
    list_of_friends=[]
    list_of_groups=[]
    list_of_friends_groups_ID=[]

    for friend_id in user.get_friends():
        list_of_friends.append(VK_user(token, friend_id))
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
    return (set_of_friend_group_ID)

if __name__ == '__main__':
    list_of_result=[]
    eshmargunov = VK_user(TOKEN,ID_eshmargunov)
    set_of_result = set_of_user_group_id(TOKEN,ID_eshmargunov) - set_of_friends_group_id(TOKEN,ID_eshmargunov)
    for group in eshmargunov.get_groups():
        if group['id'] in set_of_result:
            list_of_result.append(group)
    pprint(list_of_result)