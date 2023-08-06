import requests
import datetime

class Code_returner:
    def __init__(self,token=''):
        self.headers = {
                        "Authorization": "Bearer "+token,
                        #"Content-Type":"application/x-www-form-urlencoded"
                        }
    def send_message(self,message:str):
        params = {"message": f'[INFO] {datetime.datetime.now()}: {message}'}
        requests.post('https://notify-api.line.me/api/notify', headers=self.headers, params=params)
    def send_image(self,img_path:str,message=None):
        img=open(img_path,'rb')
        files = {"imageFile": img}
        data = {'message': f'[INFO] {datetime.datetime.now()}: {message}'}
        requests.post('https://notify-api.line.me/api/notify', headers=self.headers, files=files, data=data)

