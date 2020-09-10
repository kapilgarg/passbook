"""
email parser
"""
import re
from bs4 import BeautifulSoup

patterns = []

with open('templates.txt','r') as f:
    patterns = f.readlines()

def __parse_html(mime_message):
    payload = mime_message.get_payload()
    soup = BeautifulSoup(payload, 'html.parser')
    return soup.text

def parse(mime_message):
    body = __parse_html(mime_message)
    for pattern in patterns:
        pattern = pattern.replace('\n','')
        match = re.search(pattern,body)
        if match:
            return match.groupdict()
    return None



