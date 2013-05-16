from twisted.trial.unittest import TestCase
from twisted.python.failure import Failure

from txairbrake.observers import AirbrakeLogObserver


class TestException(Exception):
    """
    An exception class that we can use for our tests.
    """


def fail():
    try:
        raise TestException("this is a test exception")
    except:
        return Failure()



class XMLTests(TestCase):
    def setUp(self):
        self.observer = AirbrakeLogObserver('API-KEY', environment='testing')
        self.failure = fail()
        self.eventDict = {'failure': self.failure,
                          'why': 'Test why.'}
        self.root = self.observer._eventDictToTree(self.eventDict)


    def test_noticeVersion(self):
        """
        notice tag with version 2.0 attribute.
        """
        self.assertEqual(self.root.tag, 'notice')
        self.assertEqual(self.root.get('version'), '2.0')


    def test_noticeApiKey(self):
        """
        notice tag includes an api-key child that wraps the api key argument
        to AirbrakeLogObserver.
        """
        api_key = self.root.find('api-key')
        self.assertEqual(api_key.text, 'API-KEY')


    def test_environmentName(self):
        """
        notice includes environment argument at
        server-environment/environment-name
        """
        environment_name = self.root.find('server-environment/environment-name')
        self.assertEqual(environment_name.text, 'testing')


    def test_notifier(self):
        """
        notice includes notifier name, version, and url.
        """
        self.assertEqual(self.root.find('notifier/name').text, 'txairbrake')
        self.assertNotIdentical(self.root.find('notifier/url'), None)
        self.assertNotIdentical(self.root.find('notifier/version'), None)


    def test_error(self):
        """
        notice includes an error tag.
        """
        self.assertNotIdentical(self.root.find('error'), None)


    def test_errorClass(self):
        """
        error/class is a fully qualified exception class name.
        """
        error_class = self.root.find('error/class')
        self.assertEqual(error_class.text, 'TestException')


    def test_errorMessage(self):
        """
        error/message is a string message of the failure.
        """
        error_message = self.root.find('error/message')
        self.assertEqual(error_message.text, 'TestException: this is a test exception')


    def test_errorBacktrace(self):
        """
        error/backtrace has a number of line children with file, line number,
        method.

        The values in this test will need to change if it moves or if the fail
        function moves.
        """
        lines = self.root.findall('error/backtrace/line')
        self.assertNotEqual(len(lines), 0)
        last_line = lines[0]
        self.assertTrue(last_line.get('file').endswith('txairbrake/tests/test_observer.py'))
        self.assertEqual(last_line.get('method'),
                         'fail: raise TestException("this is a test exception")')
        self.assertEqual(last_line.get('number'), '15')
