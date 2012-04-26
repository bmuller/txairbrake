import traceback

from twisted.python.log import addObserver, removeObserver
from twisted.words.xish import domish
from twisted.web.client import getPage

DEFAULT_AIRBRAKE_HOST = "airbrakeapp.com"
AIRBRAKE_API_PATH = "/notifier_api/v2/notices"

from txairbrake import version

class AirbrakeLogObserver:
    def __init__(self, apikey, environment=None, use_ssl=False, airbrakeHost=None):
        self.apikey = apikey
        self.environment = environment or "unknown"
        host = airbrakeHost or DEFAULT_AIRBRAKE_HOST
        protocol = "https://" if use_ssl else "http://"       
        self.airbrakeURL = protocol + host + AIRBRAKE_API_PATH


    def emit(self, eventDict):
        if not eventDict['isError'] or not 'failure' in eventDict:
            return
        xml = self.generateXML(eventDict['failure'])
        headers = {"Content-Type": "text/xml"}
        d = getPage(self.airbrakeURL, None, method="POST", postdata=xml, headers=headers, timeout=2)
        d.addErrback(self._onError)
        return d


    def _onError(self, error):
        """
        Stop observer, raise exception, then restart.  This prevents an infinite ping pong game of exceptions.
        """
        self.stop()
        error.raiseException()
        self.start()
        

    def start(self):
        addObserver(self.emit)


    def stop(self):
        removeObserver(self.emit)
        

    def generateXML(self, record):
        # XML API described here: http://help.airbrake.io/kb/api-2/notifier-api-version-22
        notice = domish.Element((None, 'notice'), attribs={'version': '2.0'})
        notice.addElement('api-key', content=self.apikey)

        notifier = notice.addElement('notifier')
        notifier.addElement('name', content='txairbrake')
        notifier.addElement('version', content=version)
        notifier.addElement('url', content="http://github.com/bmuller/txairbrake")

        se = notice.addElement('server-environment')
        se.addElement('environment-name', content=self.environment)

        error = notice.addElement('error')
        error.addElement('class', content=record.value.__class__.__name__)
        error.addElement('message', content=record.getErrorMessage())
        backtrace = error.addElement('backtrace')
        for filename, line_number, function_name, text in traceback.extract_tb(record.getTracebackObject()):
            attribs = {'file': filename, 'number': str(line_number), 'method': "{0}: {1}".format(function_name, text)}
            backtrace.addChild(domish.Element((None, 'line'), attribs=attribs))

        return str(notice.toXml())
