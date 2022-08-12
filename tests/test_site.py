import allure
import requests
from selene import command
from selene.support.shared import browser

from src.pages.main_page import MainPage


class TestWebsiteMoscowMayor:

    @allure.title("Checking header and footer is displayed")
    def test_header_and_footer_displayed(self):
        page = MainPage()
        page.open_page()
        assert page.header.displayed()
        assert page.footer.displayed()

    @allure.title("Checking count extracted links from page")
    def test_checking_count_extracted_links(self):
        page = MainPage()
        page.open_page()
        links = page.get_all_extracted_links()
        assert len(links) == 280

    @allure.title("Checking links response extracted from page")
    def test_checking_links_response(self):
        page = MainPage()
        page.open_page()
        links = list(set(page.get_all_extracted_links()))
        err_links = []
        for link in links:
            r = 0
            try:
                r = requests.get(link).status_code
            except requests.ConnectionError as e:
                err_links.append(link)
            if r != 200:
                err_links.append(link)
        assert len(err_links) == 0

    @allure.title("Checking links extracted from page, open in browser")
    def test_checking_links_open_in_browser(self):
        page = MainPage()
        page.open_page()
        links = list(set(page.get_all_extracted_links()))
        err_links = []
        screenshot_number = 0
        for link in links:
            try:
                browser.open(link)
                current_link = browser.driver.current_url
                assert current_link == link
            except Exception as e:
                allure.attach(
                    name=f'скриншот {screenshot_number}',
                    body=browser.driver.get_screenshot_as_png(),
                    attachment_type=allure.attachment_type.PNG
                )
                err_links.append(link)
        assert len(err_links) == 0

