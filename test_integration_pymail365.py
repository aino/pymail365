import unittest
from pymail365 import EmailMessage, EmailMessageException


class Pymail365IntegrationTestCase(unittest.TestCase):
    user = None
    password = None

    def test_real(self):
        m = EmailMessage(
            user=self.user,
            password=self.password,
            subject='test_subject',
            body='test_html',
            from_email=self.user,
            to=[self.user],
        )
        self.assertEqual(None, m.send())

    def test_bad_body(self):
        m = EmailMessage(
            user=self.user,
            password=self.password,
            subject='test_subject',
            body='test_html',
            from_email=self.user,
            to=[self.user],
        )
        m.msg['Body'] = 'FAIL'
        self.assertRaisesRegexp(
            EmailMessageException,
            '^\(400\) {"error":{"code":"ErrorInvalidRequest","message":"Cannot read the request body."}}$',
            m.send
        )


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print 'Please provide user and password'
    else:
        Pymail365IntegrationTestCase.password = sys.argv.pop()
        Pymail365IntegrationTestCase.user = sys.argv.pop()
        unittest.main()
