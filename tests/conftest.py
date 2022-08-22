import pytest
from selene.support.shared import browser

base_url = 'https://www.mos.ru/'

browser.config.browser_name = 'chrome'


@pytest.fixture(scope='session', autouse=True)
def browser_manger():
    # set window size of browser
    browser.config.window_width = 1920
    browser.config.window_height = 1080
    browser.open(base_url)
    yield
    browser.quit()
