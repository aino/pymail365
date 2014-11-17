import base64
import json
import os
import requests


IMPORTANCE = ('Low', 'Normal', 'High')
SEND_URL = 'https://outlook.office365.com/ews/odata/Me/sendmail'


def recipient(email):
    return {'EmailAddress': {'Address': email}}


class EmailMessageException(Exception):
    pass


class EmailMessage(object):
    def __init__(self, user=None, password=None, subject='', body='',
            html=True, from_email=None, to=[], cc=[], bcc=[], attachments=[],
            importance='Normal'):
        if not user:
            raise EmailMessageException('user cannot be empty')
        if not password:
            raise EmailMessageException('password cannot be empty')
        if not to:
            raise EmailMessageException('to cannot be empty')
        if not from_email:
            raise EmailMessageException('from_email cannot be empty')
        if importance not in IMPORTANCE:
            raise EmailMessageException(
                '%s not in %s' % (importance, ', '.join(list(IMPORTANCE)))
            )
        self.user = user
        self.password = password
        self.msg = {
            'Subject': subject,
            'Importance': importance,
            'Body': {'Content': body, 'ContentType': 'HTML' if html else 'Text'},
        }
        self.msg['ToRecipients'] = []
        for email in to:
            self.msg['ToRecipients'].append(recipient(email))
        if cc:
            self.msg['CcRecipients'] = []
            for email in cc:
                self.msg['CcRecipients'].append(recipient(email))
        if bcc:
            self.msg['BccRecipients'] = []
            for email in bcc:
                self.msg['BccRecipients'].append(recipient(email))
        if attachments:
            self.msg['Attachments'] = []
            for a in attachments:
                with open(a) as fp:
                    head, tail = os.path.split(a)
                    self.msg['Attachments'].append({
                        '@odata.type': '#Microsoft.OutlookServices.FileAttachment',
                        'Name': tail,
                        'ContentBytes': base64.b64encode(fp.read())
                    })

    def send(self):
        data = json.dumps({'Message': self.msg})
        headers = {'content-type': 'application/json'}
        auth = (self.user, self.password)
        r = requests.post(SEND_URL, data=data, headers=headers, auth=auth)
        if r.status_code != 202:
            raise EmailMessageException('(%s) %s' % (r.status_code, r.text))
