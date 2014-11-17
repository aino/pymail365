#coding=utf8
import base64
import unittest
from pymail365 import EmailMessage, EmailMessageException, IMPORTANCE


defaults = {
    'user': 'test@test.com',
    'password': 'passw',
    'subject': 'subject',
    'body': 'body',
    'from_email': 'from@test.com',
    'to': ['to1@test.com', 'to2@test.com'],
    'cc': ['cc1@test.com', 'cc2@test.com'],
    'bcc': ['bcc1@test.com', 'bcc2@test.com'],
    'importance': 'High',
    'attachments': ['README.rst'],
}


class Pymail365TestCase(unittest.TestCase):
    def test_nouser(self):
        kwargs = defaults.copy()
        kwargs.pop('user')
        self.assertRaisesRegexp(EmailMessageException, 'user cannot be empty', EmailMessage, **kwargs)

    def test_nopassword(self):
        kwargs = defaults.copy()
        kwargs.pop('password')
        self.assertRaisesRegexp(EmailMessageException, 'password cannot be empty', EmailMessage, **kwargs)

    def test_noto(self):
        kwargs = defaults.copy()
        kwargs.pop('to')
        self.assertRaisesRegexp(EmailMessageException, 'to cannot be empty', EmailMessage, **kwargs)

    def test_nofrom_email(self):
        kwargs = defaults.copy()
        kwargs.pop('from_email')
        self.assertRaisesRegexp(EmailMessageException, 'from_email cannot be empty', EmailMessage, **kwargs)

    def test_bad_importance(self):
        kwargs = defaults.copy()
        kwargs['importance'] = 'FAIL'
        self.assertRaisesRegexp(EmailMessageException, 'FAIL not in %s' % ', '.join(list(IMPORTANCE)), EmailMessage, **kwargs)

    def test_message(self):
        kwargs = defaults.copy()
        m = EmailMessage(**kwargs)
        test_data = {
            "Subject": "subject",
            "Body": {"Content": "body", "ContentType": "HTML"},
            "ToRecipients": [{"EmailAddress": {"Address": "to1@test.com"}}, {"EmailAddress": {"Address": "to2@test.com"}}],
            "CcRecipients": [{"EmailAddress": {"Address": "cc1@test.com"}}, {"EmailAddress": {"Address": "cc2@test.com"}}],
            "BccRecipients": [{"EmailAddress": {"Address": "bcc1@test.com"}}, {"EmailAddress": {"Address": "bcc2@test.com"}}],
            "Attachments": [{"@odata.type": "#Microsoft.OutlookServices.FileAttachment", "Name": "README.rst"}],
            "Importance": "High",
        }
        with open(test_data['Attachments'][0]['Name']) as fp:
            test_data['Attachments'][0]['ContentBytes'] = base64.b64encode(fp.read())
        self.assertEqual(test_data, m.msg)

    def test_real(self):
        print '\n'
        user = raw_input('user: ')
        passw = raw_input('password: ')
        m = EmailMessage(
            user=user,
            password=passw,
            subject='test_subject',
            body='test_html',
            from_email=user,
            to=[user],
        )
        self.assertEqual(202, m.send())


if __name__ == '__main__':
    unittest.main()
