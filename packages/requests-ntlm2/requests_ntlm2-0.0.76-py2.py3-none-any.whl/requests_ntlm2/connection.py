import logging
import re
import select
import socket

from requests.packages.urllib3.connection import DummyConnection
from requests.packages.urllib3.connection import HTTPConnection as _HTTPConnection
from requests.packages.urllib3.connection import HTTPSConnection as _HTTPSConnection
from requests.packages.urllib3.connection import VerifiedHTTPSConnection as _VerifiedHTTPSConnection
from six.moves.http_client import PROXY_AUTHENTICATION_REQUIRED, LineTooLong

from .core import NtlmCompatibility, get_ntlm_credentials, noop
from .dance import HttpNtlmContext


IO_WAIT_TIMEOUT = 0.1


logger = logging.getLogger(__name__)

# maximal line length when calling readline().
_MAXLINE = 65536

# maximum number of consecutive blank lines
# this is for parsing the html body
_MAX_CONSECUTIVE_BLANK_LINES = 10

_ASSUMED_HTTP09_STATUS_LINES = (
    ("HTTP/0.9", 200, ""),
    ("HTTP/0.9", 200, "OK"),
)

_TRACKED_HEADERS = (
    "proxy-authenticate",
    "proxy-support",
    "cache-control",
    "date",
    "server",
    "proxy-connection",
    "connection",
    "content-length",
    "content-type",
)

HTTP_VERSION_11 = "HTTP/1.1"
HTTP_VERSION_10 = "HTTP/1.0"
DEFAULT_HTTP_VERSION = HTTP_VERSION_10


class HTTPConnection(_HTTPConnection):
    pass


class HTTPSConnection(_HTTPSConnection):
    pass


class VerifiedHTTPSConnection(_VerifiedHTTPSConnection):
    ntlm_compatibility = NtlmCompatibility.NTLMv2_DEFAULT
    ntlm_strict_mode = False

    def __init__(self, *args, **kwargs):
        super(VerifiedHTTPSConnection, self).__init__(*args, **kwargs)
        self._continue_reading_headers = True
        if self.ntlm_compatibility is None:
            self.ntlm_compatibility = NtlmCompatibility.NTLMv2_DEFAULT

    @classmethod
    def set_ntlm_auth_credentials(cls, username, password):
        cls._ntlm_credentials = get_ntlm_credentials(username, password)

    @classmethod
    def set_http_version(cls, http_version):
        if http_version in (HTTP_VERSION_10, HTTP_VERSION_11):
            cls._http_version = http_version
        else:
            logger.info(
                "unsupported http-version %r, setting the default %r",
                http_version,
                DEFAULT_HTTP_VERSION
            )
            cls._http_version = DEFAULT_HTTP_VERSION

    @classmethod
    def clear_http_version(cls):
        cls._http_version = None
        del cls._http_version

    @classmethod
    def clear_ntlm_auth_credentials(cls):
        cls._ntlm_credentials = None
        del cls._ntlm_credentials

    @staticmethod
    def _is_line_blank(line):
        # for sites which EOF without sending a trailer
        if not line or line in (b"\r\n", b"\n", b"") or not line.strip():
            return True
        return False

    @staticmethod
    def _read_response_line_if_ready(response):
        (ready, _, _) = select.select([response.fp], (), (), IO_WAIT_TIMEOUT)
        if ready:
            return response.fp.readline()

    def handle_http09_response(self, response):
        status_line_regex = re.compile(
            br"(?P<version>HTTP/\d\.\d)\s+(?P<status>\d+)\s+(?P<message>.+)",
            re.DOTALL
        )

        while True:
            line = response.fp.readline()
            if not line:
                self._continue_reading_headers = False
                break
            match = status_line_regex.search(line)
            if match:
                status_line = match.groupdict()
                logger.info("< %r", "{version} {status} {message}".format(**status_line))
                return status_line["version"], int(status_line["status"]), status_line["message"]
        return None

    def _get_response(self):
        response = self.response_class(self.sock, method=self._method)
        version, code, message = response._read_status()

        if (version, code, message) in _ASSUMED_HTTP09_STATUS_LINES:
            logger.warning("server response used outdated HTTP version: HTTP/0.9")
            status_line = self.handle_http09_response(response)
            if status_line:
                old_status_line = version, code, message
                version, code, message = status_line
                logger.info("changed status line from %s, to %s", old_status_line, status_line)
            else:
                logger.warning("could not handle HTTP/0.9 server response")
                logger.info("HTTP/0.9: version=%s", version)
                logger.info("HTTP/0.9: code=%s", code)
                logger.info("HTTP/0.9: message=%s", message)
        else:
            logger.info("< %r", "{} {} {}".format(version, code, message))
        return version, code, message, response

    def _get_http_version(self):
        return DEFAULT_HTTP_VERSION

    def _get_header_bytes(self, proxy_auth_header=None):
        host, port = self._get_hostport(self._tunnel_host, self._tunnel_port)
        http_connect_string = "CONNECT {host}:{port} {http_version}\r\n".format(
            host=host,
            port=port,
            http_version=self._get_http_version()
        )
        logger.info("> %r", http_connect_string)
        header_bytes = http_connect_string
        if proxy_auth_header:
            self._tunnel_headers["Proxy-Authorization"] = proxy_auth_header
        self._tunnel_headers["Proxy-Connection"] = "Keep-Alive"
        self._tunnel_headers["Host"] = "{}:{}".format(host, port)

        for header in sorted(self._tunnel_headers):
            value = self._tunnel_headers[header]
            header_byte = "%s: %s\r\n" % (header, value)
            logger.info("> %r", header_byte)
            header_bytes += header_byte
        header_bytes += "\r\n"
        return header_bytes.encode("latin1")

    def _tunnel(self):
        username, password, domain = self._ntlm_credentials
        logger.info("* attempting to open tunnel using HTTP CONNECT")
        logger.info("* username=%r, domain=%r", username, domain)

        try:
            workstation = socket.gethostname().upper()
        except (AttributeError, TypeError, ValueError):
            workstation = None

        logger.info("* workstation=%r", workstation)

        ntlm_context = HttpNtlmContext(
            username,
            password,
            domain=domain,
            workstation=workstation,
            auth_type="NTLM",
            ntlm_compatibility=self.ntlm_compatibility,
            ntlm_strict_mode=self.ntlm_strict_mode
        )

        negotiate_header = ntlm_context.get_negotiate_header()
        header_bytes = self._get_header_bytes(proxy_auth_header=negotiate_header)
        self.send(header_bytes)
        version, code, message, response = self._get_response()

        if code == PROXY_AUTHENTICATION_REQUIRED:
            authenticate_hdr = None
            match_string = "Proxy-Authenticate: NTLM "
            content_length_match_string = "Content-Length:"
            previous_line = None
            content_length_header = None
            body_length = None
            num_blank_lines = 0
            num_lines = 1
            while True:
                num_lines += 1
                logger.info('* reading line number %s', num_lines)
                line = self._read_response_line_if_ready(response)
                this_line_is_blank = self._is_line_blank(line)

                if this_line_is_blank:
                    num_blank_lines += 1
                else:
                    num_blank_lines = 0

                if num_blank_lines >= _MAX_CONSECUTIVE_BLANK_LINES:
                    logger.warning('* stopping to read HTML because of 10 consecutive blank lines')
                    break

                if body_length is None and this_line_is_blank:
                    logger.info('* initializing body_length to zero; we done with headers now')
                    body_length = 0
                    previous_line = line
                    continue
                else:
                    if line is not None and body_length is not None:
                        body_length += len(line)

                    logger.info(
                        "* body length read so far: %s of %s",
                        body_length,
                        content_length_header or "unknown"
                    )

                    if (
                        body_length is not None
                        and content_length_header is not None
                        and body_length >= content_length_header
                    ):
                        # we have read the whole response body according to the
                        # Content-Length response header value.
                        # We break away from the loop because we have finished draining
                        # the socket.
                        break
                    elif (
                        this_line_is_blank
                        and content_length_header is None
                        and previous_line is not None
                        and self._is_line_blank(previous_line)
                    ):
                        # we have read all the response headers but there was no
                        # Content-Length header present in the response headers.
                        # This line is blank and the one before it was blank line too,
                        # we read the next line (if any) and if it is blank or does not
                        # exists, we break away from the loop because we have finished
                        # draining the socket.
                        line = self._read_response_line_if_ready(response)
                        if self._is_line_blank(line):
                            break

                if line is not None and line.decode("utf-8").startswith(match_string):
                    # we handle the NTLM challenge message
                    logger.info("< %r", line)
                    line = line.decode("utf-8")
                    previous_line = line
                    ntlm_context.set_challenge_from_header(line)
                    authenticate_hdr = ntlm_context.get_authenticate_header()
                    logger.info("* authenticate header: %r", authenticate_hdr)
                    continue
                elif (
                    line is not None
                    and line.decode("utf-8").startswith(content_length_match_string)
                ):
                    # we handle the Content-Length header
                    logger.info("< %r", line)
                    line = line.decode("utf-8")
                    try:
                        content_length_header = int(
                            line.replace(content_length_match_string, "").strip()
                        )
                        logger.info('* found content length header; value: %s', content_length_header)
                    except (ValueError, TypeError):
                        pass
                    previous_line = line
                    continue

                if line is not None and len(line) > _MAXLINE:
                    raise LineTooLong("header line")

                logger.info("< %r", line)
                previous_line = line

            logger.info('* authenticate header: %r', authenticate_hdr)
            header_bytes = self._get_header_bytes(proxy_auth_header=authenticate_hdr)
            logger.info("* sending authenticate header: %r", header_bytes)
            self.send(header_bytes)
            version, code, message, response = self._get_response()
            logger.info('* HTTP status code: %s', code)

        if code != 200:
            logger.error('* HTTP status code %s != 200', code)
            self.close()
            raise socket.error(
                "Tunnel connection failed: %d %s" % (code, message.strip())
            )

        logger.info('* draining the socket')
        line_count = 0
        while self._continue_reading_headers:
            line_count += 1
            logger.info('* draining socket, line %s', line_count)
            line = self._read_response_line_if_ready(response)
            logger.info('< %r', line)

            if line is not None and len(line) > _MAXLINE:
                raise LineTooLong("header line")
            if self._is_line_blank(line):
                logger.info('* line is blank, stopping to drain the socket')
                break

        logger.info('successfully established the proxy tunnel!')


try:
    noop()  # for testing purposes
    import ssl  # noqa

    # Make a copy for testing.
    UnverifiedHTTPSConnection = HTTPSConnection
    HTTPSConnection = VerifiedHTTPSConnection
except ImportError:
    HTTPSConnection = DummyConnection
