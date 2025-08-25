import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
import random
import os
import base64



class BrowserWindowsPage(BasePage):

    @allure.step('Click Browser Button')
    def click_button(self, button):
        with allure.step('Choose button'):
            window_buttons = {"new_tab": 'New Tab',
                              "new_window": 'New Window',
                              "new_window_message": 'New Window Message'
                                }

            self.page.get_by_text(window_buttons[button], exact=True).click()

