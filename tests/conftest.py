import pytest
from selene.support.shared import browser

base_url = 'https://www.mos.ru/'

browser.config.browser_name = 'chrome'


@pytest.fixture(scope='session', autouse=True)
def browser_manger():
    browser.open(base_url)
    yield
    browser.quit()
