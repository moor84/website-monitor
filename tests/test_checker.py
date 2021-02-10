import pytest
import responses

from website_monitor.checker.check import check_url
from website_monitor.status import Status


class TestChecker:
    """
    Test the checker utils.
    """
    @pytest.mark.parametrize('url, status_code', (
        ('https://example.com', 200),
        ('https://google.com', 500),
    ))
    def test_check_url(self, url, status_code):
        with responses.RequestsMock() as mock:
            mock.add(responses.GET, url, body='I\'m alive!', status=status_code)
            status = check_url(url)
            assert isinstance(status, Status)
            assert status.url == url
            assert status.status_code == status_code
            assert status.regex_check is False

    @pytest.mark.parametrize('body, pattern, result', (
        ('<html><body>email: frodo.baggins@shire.com</body></html>', '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', True),
        ('<html><body>Something Wrong!</body></html>', '[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', False),
        ('<html><body>All OK!</body></html>', 'OK', True),
        ('<html><body>All OK!</body></html>', '', False),
        ('', 'somethingg?', False),
    ))
    def test_check_url_pattern(self, body, pattern, result):
        with responses.RequestsMock() as mock:
            mock.add(responses.GET, 'https://example.com', body=body, status=200)
            status = check_url('https://example.com', pattern=pattern)
            assert isinstance(status, Status)
            assert status.status_code == 200
            assert status.regex_check is result
