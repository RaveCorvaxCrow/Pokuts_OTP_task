import time

import allure
from selene import command
from selene.support.conditions import be
from selene.support.shared import browser
from selene.support.shared.jquery_style import s, ss


class MainPage:

    def __init__(self):
        self._page_url = 'https://www.mos.ru/'
        self.header = PageElement(
            name='Header',
            locator='//div[@id="mos-header"]')
        self.footer = PageElement(
            name='Footer',
            locator='//div[@id="mos_footer"]')
        self.__links = '//a[@href]'

        self.agreement_use_info_system = PageElement(
            name="Agreement on the Use of Information Systems and Resources of the City of Moscow",
            locator='//div[contains(@class, "Agreement_agreement")]'
        )

    @allure.step('Open page')
    def open_page(self):
        browser.open(self._page_url)

    @allure.step('Get all the links extracted from the page')
    def get_all_extracted_links(self):
        height = browser.driver.execute_script("return document.body.scrollHeight")
        y = 0
        step = 50
        while y < height:
            browser.driver.execute_script(f'window.scrollBy(0,{step})')  # scroll by 20 on each iteration
            time.sleep(0.1)
            new_height = browser.execute_script("return document.body.scrollHeight")
            if height < new_height:
                height = new_height
            y += step
        browser.driver.execute_script(f'window.scrollBy(0,{step})')

        el_with_links = ss(self.__links)

        links = []
        for el_with_link in el_with_links:
            link = el_with_link.get_attribute('href')
            if link.startswith('/'):
                link = self._page_url + link
            links.append(link)
        return links


class PageElement:

    def __init__(self, name: str, locator: str):
        self.name = name
        self.locator = locator

    def displayed(self) -> bool:
        with allure.step(f'{self.name} is displayed'):
            return s(self.locator).matching(be.visible)

    def scroll_into_view(self):
        with allure.step(f'{self.name} scroll into view'):
            s(self.locator).perform(command.js.scroll_into_view)
