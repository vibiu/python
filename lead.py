# coding: utf-8

import time
import json
import requests
import xml.etree.ElementTree as ET
from templates import text_template
data = {
    "to_user": "me",
    "from_user": "vibiu",
    "time": "now",
    "content": "hello world"
}


class xmlRequest():
    def __init__(self, first_request):
        self.xml = first_request.data
        self.xml_object = ET.fromstring(self.xml)
        self.from_user = self.xml_object.find('FromUserName').text
        self.to_user = self.xml_object.find('ToUserName').text
        self.msg_type = self.xml_object.find('MsgType').text
        self.content = self.xml_object.find('Content')

    def time_now(self):
        return str(int(time.time()))

    def format_text(self, text):
        data = {
            "to_user": self.from_user,
            "from_user": self.to_user,
            "time": self.time_now(),
            "content": text
        }
        formated_text = text_template.format(**data)
        return formated_text

    def robort_reply(self):
        if self.msg_type == 'text':
            api_url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={msg}'.format(
                msg=self.content.text.encode('utf-8'))
            res = requests.get(api_url)
            res_dict = json.loads(res.content)
            res_content = res_dict.get('content').encode('utf-8')
            return self.format_text(res_content)
        error_message = 'can\'t understand what you mean'
        return self.format_text(error_message)
