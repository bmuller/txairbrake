import traceback

from twisted.python.log import addObserver, removeObserver
from twisted.web.client import getPage

import xml.etree.ElementTree as ET


DEFAULT_AIRBRAKE_HOST = "api.airbrake.io"
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
        tree = self._eventDictToTree(eventDict)
        headers = {"Content-Type": "text/xml"}
        d = getPage(self.airbrakeURL, None, method="POST", postdata=ET.tostring(tree), headers=headers, timeout=2)
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


    def _eventDictToTree(self, eventDict):
        failure = eventDict['failure']

        notice = ET.Element('notice', version='2.0')
        api_key = ET.SubElement(notice, 'api-key', )
        api_key.text = self.apikey

        notifier = ET.SubElement(notice, 'notifier')
        notifier_name = ET.SubElement(notifier, 'name')
        notifier_name.text = 'txairbrake'
        notifier_version = ET.SubElement(notifier, 'version')
        notifier_version.text = version
        notifier_url = ET.SubElement(notifier, 'url')
        notifier_url.text = 'https://github.com/bmuller/txairbrake/'

        server_environment = ET.SubElement(notice, 'server-environment')
        environment_name = ET.SubElement(server_environment, 'environment-name')
        environment_name.text = self.environment

        error = ET.SubElement(notice, 'error')
        error_class = ET.SubElement(error, 'class')
        error_class.text = failure.value.__class__.__name__

        error_message = ET.SubElement(error, 'message')
        error_message.text = '%s: %s' % (error_class.text, failure.getErrorMessage())

        error.append(self._tracebackToTree(traceback.extract_tb(failure.getTracebackObject())))

        return notice


    def _tracebackToTree(self, tb):
        backtrace = ET.Element('backtrace')

        for filename, line_number, function_name, text in tb:
            attrib = {'file': filename,
                      'number': str(line_number),
                      'method': "%s: %s" % (function_name, text)}
            backtrace.append(ET.Element('line', attrib=attrib))

        return backtrace
