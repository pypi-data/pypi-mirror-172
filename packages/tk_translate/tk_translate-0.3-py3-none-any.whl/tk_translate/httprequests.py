# encoding: utf-8
# api: python
##type: classes
# category: http
# title: request/fallback
# description: loads requests, or similuates API via urllib
# version: 0.7
# state: beta
# depends: python:requests (>= 2.5)
# config: -
# pylint: disable=invalid-name, missing-function-docstring, missing-module-docstring
#
# Wraps requests or fakes a http.get() implementation.
#


__all__ = ["http", "urllib", "urlencode", "quote", "quote_plus", "update_headers"]


# http preparations
import logging as log
import urllib
from json import loads, dumps
try:
    from urllib.parse import urlencode, quote, quote_plus
    from urllib.request import urlopen, Request
except ImportError:
    from urllib import urlencode, quote, quote_plus
    from urllib2 import urlopen, Request
#else:
#    from six.moves.urllib import urlencode, quote, quote_plus
#    from six.moves.urllib.request import urlopen, Request


class FauxResponse:
    """ shallow copy """

    def __init__(self, response):
        self.content = response.read()
        self.status_code = response.code
        self.__dict__.update(response.__dict__)
        #print(response, response.info, dir(response))

    def json(self):
        """ decode """
        return loads(self.content)

    def raise_for_status(self):
        """ exc """
        if self.status_code >= 400:
            raise Exception("HTTP failure code", self.status_code)

    @property
    def text(self):
        return self.content.decode("utf-8")

class FauxRequests:
    """ rudimentary shim """

    ssl_args = {}
    headers = {}

    def __init__(self):
        """ optional ssl """
        log.info("using FauxRequests() for now")
        import ssl
        if not hasattr(ssl, "create_default_context"):
            return
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        self.ssl_args["context"] = context

    def get(self, url, **kwargs):
        """ urlopen """
        kwargs["headers"] = dict(
            list(self.headers.items()) + list(kwargs.get("headers", {}).items())
        )
        return FauxResponse(
            urlopen(
                Request(url, **kwargs), **self.ssl_args
            )
        )

    def post(self, url, data=None, params=None, json=None, **kwargs):
        """ POST just adds data= """
        if json:
            data = dumps(json).encode("utf-8")
        if params:
            data = urlencode(params).encode("utf-8")
        return self.get(url, data=data, **kwargs)


try:
    import requests
    http = requests.Session()
except ImportError:
    log.error(
        "Missing library: `pip install requests` (system-wide, or into libreoffice program/ dir)"
    )
    http = FauxRequests()


# headers
def update_headers(office_version="LibreOffice/7.x", pt_version="2.0"):
    http.headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux; "+office_version+"), PageTranslate/"+pt_version,
        "Accept-Language": "*; q=1.0",
        "Accept-Encoding": "utf-8"
    })
update_headers()
