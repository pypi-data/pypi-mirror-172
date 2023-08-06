# -*- encoding: utf-8 -*-
import random

"""
@File: 第三方.py
@Time: 2022/10/17 11:37
@Author: HSQF
@Software: PyCharm

"""
import json
import re
import os
import requests
# linew below are to disable ssl warning when verify_ssl is set to False
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class ProcessErro(Exception):
  def __init__(self, process,msg):
    self.msg = f"{process} == > erroinfo:{msg}"

  def __str__(self):
    return self.msg

class PdfToXlsx(object):

    def __init__(self,path_file_name):
        self.path_file_name = path_file_name
        self.file_name = os.path.split(path_file_name)[-1]
        self.file_name_xlsx = os.path.splitext(path_file_name)[0]
        self.pdf_token = None
        self.pdf_taskid = None
        self.server = None
        self.server_file_name = None
        self.useragent = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.{random.randint(111,999)}.{random.randint(11,99)}'

    def get_auth(self):
        url = "https://www.ilovepdf.com/pdf_to_excel"
        headers = {
            'Host': 'www.ilovepdf.com',
            'User-Agent': self.useragent
        }
        response = requests.request("GET", url, headers=headers)
        data = json.loads(re.compile(r'var ilovepdfConfig = (\{.*?\});').search(response.text).group(1))
        pdf_token = data["token"]
        pdf_taskid = re.compile(r"ilovepdfConfig.taskId = '(.*?)';").search(response.text).group(1)
        print("pdf_token",pdf_token)
        print("pdf_taskid",pdf_taskid)
        self.pdf_token = pdf_token
        self.pdf_taskid = pdf_taskid
        self.server = random.choice(data["servers"]).replace("/", "")

    def upload(self):

        url = f"https://{self.server}/v1/upload"
        headers = {
          'accept': 'application/json',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
          'authorization': f'Bearer {self.pdf_token}',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'Host': f'{self.server}',
          'Origin': 'https://www.ilovepdf.com',
          'Pragma': 'no-cache',
          'Referer': 'https://www.ilovepdf.com/',
          'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-site',
          'User-Agent': self.useragent
        }
        payload={'name': f'{self.file_name}',
        'chunk': '0',
        'chunks': '1',
        'task': f'{self.pdf_taskid}',
        'preview': '1',
        'pdfinfo': '0',
        'pdfforms': '0',
        'pdfresetforms': '0',
        'v': 'web.0'}
        try:
            with open(self.path_file_name, 'rb') as f:
                response = requests.post(url, headers=headers, data=payload, files={"file": f}, verify=True,
                                         stream=None, proxies=None).json()
            self.server_file_name = response["server_filename"]
        except:
            raise ProcessErro("upload",response)

    def process(self):
        url = f"https://{self.server}/v1/process"
        payload = {'convert_to': 'xlsx',
        'output_filename': '{filename}',
        'packaged_filename': 'ilovepdf_converted',
        'ocr': '0',
        'task': f'{self.pdf_taskid}',
        'tool': 'pdfoffice',
        'files[0][server_filename]': f'{self.server_file_name}',
        'files[0][filename]': f'{self.file_name}'}

        headers = {
          'Accept': 'application/json',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
          'Authorization': f'Bearer {self.pdf_token}',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
          'Host': f'{self.server}',
          'Origin': 'https://www.ilovepdf.com',
          'Pragma': 'no-cache',
          'Referer': 'https://www.ilovepdf.com/',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-site',
          'User-Agent': self.useragent,
          'sec-ch-ua': '"Microsoft Edge";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
        }

        response = requests.post(url, headers=headers, data=payload,  verify=True, stream=None,
                                 proxies=None).json()
        try:
            status = response["status"]
            if "TaskSuccess" == status:
                print("sucess")
            else:
                print("fail")
        except:
            raise ProcessErro("process",response)

    def download(self):
        url = f"https://{self.server}/v1/download/{self.pdf_taskid}"
        headers = {
          'Host': f'{self.server}',
          'Connection': 'keep-alive',
          'Pragma': 'no-cache',
          'Cache-Control': 'no-cache',
          'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': self.useragent,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
          'Sec-Fetch-Site': 'same-site',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-Dest': 'document',
          'Referer': 'https://www.ilovepdf.com/',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        response = requests.request("GET", url, headers=headers)
        try:
            with open(f"{self.file_name_xlsx}.xlsx", "wb") as f:
                f.write(response.content)
            print(f"存储位置： {self.file_name_xlsx}.xlsx")
        except:
            raise ProcessErro("downlaod",response)

