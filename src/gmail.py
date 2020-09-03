"""
This module is a wrapper for google mail api
"""
import email
import base64
from datetime import datetime
from bs4 import BeautifulSoup
from dateutil.parser import parse
from googleapiclient.discovery import build
from google_auth import creds
from config import EMAIL_ADDRESSES


service = build('gmail', 'v1', credentials=creds)
email_addresses = __get_source_addresses(EMAIL_ADDRESSES)

def __get_source_addresses(file_path):
    addresses = []
    with open(file_path, 'r') as f:
        addresses = f.readlines()
    return addresses

def get_mails(date_from, date_to):
        """
        tbd
        """
        messages = []
        date_after = (date_from).strftime("%Y/%m/%d")
        date_before = (date_to).strftime("%Y/%m/%d")
        for email_add in email_addresses:
            result = service.users().messages().list(
                userId='me', q="from:"+email_add + f' after:{date_after} before:{date_before}').execute()
            if 'messages' in result:
                messages += result['messages']
        return messages

def get_message(message_id):
    """
    returns mime message for message id
    Args:
        message_id:string : id of the message
    Returns:
        Mime message
    """
        message = self.service.users().messages().get(userId='me', id=message_id,
                                                      format='raw').execute()
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
        mime_msg = email.message_from_string(msg_str.decode())
        return mime_msg

def __subject(mime_msg):
        return mime_msg['subject']
    
def __date(mime_msg):
    date = mime_msg['Date']
    date = date[:date.index('(')]
    return parse(date).strftime("%Y-%m-%d")
    
def __body(mime_msg):
    html = mime_msg.get_payload()
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.text

def parse_email(self, mime_msg):
    """
    tbd
    """
    subject = __subject(mime_msg)
    date = __date(mime_msg)
    text = __body(mime_msg)   
    return {
        'subject': subject,
        'date': date,
        'text': text
    }