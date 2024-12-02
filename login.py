from encryption.srun_md5 import *
from encryption.srun_sha1 import *
from encryption.srun_base64 import *
from encryption.srun_xencode import *

from bs4 import BeautifulSoup
import requests
import json
import re

header={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}


class Login:
    def __init__(self, urls, account):
        self.urls = urls
        self.account = account
        self.ip = None
    
    def get_ip(self):
        response = requests.get(self.urls['login_page'], headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        self.ip = soup.find('input', {'name': 'user_ip'})['value']
        
    def get_challenge(self):
        challenge_info = {
            "callback": "jsnop998244353",
            "username": self.account['username'],
            "ip": self.ip
        }
        response = requests.get(self.urls['get_challenge_api'], params=challenge_info, headers=header)
        self.token = re.search('"challenge":"(.*?)"', response.text).group(1)
        print("token:", self.token)
    
    def get_checksum(self):
        chkstr = self.token + self.account['username']
        chkstr += self.token + self.md5
        chkstr += self.token + self.account['acid']
        chkstr += self.token + self.ip
        chkstr += self.token + self.account['n']
        chkstr += self.token + self.account['vtype']
        chkstr += self.token + self.encrypted_info
        return chkstr

    def generate_login_info(self):
        info_prams = {
            "username": self.account['username'],
            "password": self.account['password'],
            "ip": self.ip,
            "acid": self.account['acid'],
            "enc_ver": self.account['enc'],
        }
        self.info = json.dumps(info_prams)
        self.encrypted_info = "{SRBX1}" + get_base64(get_xencode(self.info, self.token))
        
        self.md5 = get_md5("",self.token)
        self.encrypted_md5 = "{MD5}" + self.md5
        
        self.chkstr = self.get_checksum()
        self.encrypted_chkstr = get_sha1(self.chkstr)

    def send_login_info(self):
        login_info = {
            "callback": "jsnop998244353",
            "action": "login",
            "username": self.account['username'],
            "password": self.encrypted_md5,
            "ac_id": self.account['acid'],
            "ip": self.ip,
            "info": self.encrypted_info,
            "chksum": self.encrypted_chkstr,
            "n": self.account['n'],
            "type": self.account['vtype']
        }
        response = requests.get(self.urls['login_api'], params=login_info, headers=header)
        return response
    
    def resolve_login_response(self, response):
        res=re.search('"suc_msg":"(.*?)"', response.text)
        if res != None and res.group(1) == "login_ok":
            print("Login successfully!")
            print("IP:", self.ip)
        else:
            print("Login failed!")
            print("Login Response:",response.text)

    def get_login_response(self):
        self.generate_login_info()
        response = self.send_login_info()
        self.resolve_login_response(response)

if __name__ == '__main__':
    path = 'configure.json'
    with open(path, 'r') as f:
        config = json.load(f)
    
    login = Login(config['urls'], config['account'])
    login.get_ip()
    login.get_challenge()
    login.get_login_response()      
