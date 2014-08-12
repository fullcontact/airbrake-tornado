import logging
import traceback

from tornado import httpclient
from xml.etree.ElementTree import Element, tostring


def _el_with_text(tag, text, **kwargs):
    el = Element(tag, **kwargs)
    el.text = text
    return el


def _traceback_line(filename, line, method):
    return Element("line",
                   dict(file=filename, method=method, number=str(line)))


def _cgi_data_element(req):
    cgi_data = Element("cgi-data")
    for key, val in [("HTTP_USER_AGENT", req.headers.get("User-Agent", ""))]:
        cgi_data.append(_el_with_text("var", val, key=key))
    return cgi_data


def _params_element(req):
    params = Element("params")
    for key, val in [("HTTP_METHOD", req.method)]:
        params.append(_el_with_text("var", val, key=key))
    return params


def _request_element(request):
    req = Element("request")
    req.append(_el_with_text("url", request.uri))
    req.append(_cgi_data_element(request))
    req.append(_params_element(request))
    return req


def _backtrace_element(exc_info):
    backtrace = Element("backtrace")
    for line in traceback.extract_tb(exc_info[2]):
        backtrace.append(_traceback_line(line[0], line[1], line[2]))
    return backtrace


def notify(exc_info, request, name, api_key=None, environment=None, url=None):

    if api_key is None or environment is None:
        return

    notice = Element("notice", version="2.3")
    notice.append(_el_with_text("api-key", api_key))

    notifier = Element("notifier")
    notifier.append(_el_with_text("name", name))
    notifier.append(_el_with_text("version", "1.00"))

    if url is not None:
        notifier.append(_el_with_text("url", url))

    notice.append(notifier)

    error = Element("error")
    error.append(_el_with_text("message", exc_info[1].message))

    error.append(_backtrace_element(exc_info))
    notice.append(error)

    notice.append(_request_element(request))

    def handle_request(response):
        if response.error:
            logging.error("Cannot submit exception: %s", response.error)

    httpclient.AsyncHTTPClient().fetch(
        "http://airbrake.io/notifier_api/v2/notices",
        method="POST",
        body=tostring(notice),
        callback=handle_request
    )


__all__ = ["notify"]
