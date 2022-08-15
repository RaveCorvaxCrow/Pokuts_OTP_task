import allure
from pytest import assume
import requests
from selene.support.shared import browser

from src.pages.main_page import MainPage


def test_main_page():
    page = MainPage()
    with allure.step(f"Open page {page._page_url}"):
        page.open_page()
    with allure.step("Checking header and footer is displayed"):
        with assume:
            assert page.header.displayed()
        with assume:
            assert page.footer.displayed()
    with allure.step("Checking count extracted links from page"):
        links = page.get_all_extracted_links()
        with assume:
            assert len(links) == 280
    with allure.step("Checking links response extracted from page"):
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
        with assume:
            assert len(err_links) == 0
    with allure.step("Checking links response extracted from page"):
        err_links = []
        screenshot_number = 0
        for link in links:
            try:
                browser.open(link)
                current_link = browser.driver.current_url
                assert current_link == link
            except Exception as e:
                screenshot_number += 1
                allure.attach(
                    name=f'скриншот {screenshot_number}',
                    body=browser.driver.get_screenshot_as_png(),
                    attachment_type=allure.attachment_type.PNG
                )
                err_links.append(link)
        with assume:
            assert len(err_links) == 0
