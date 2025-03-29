import time
from tkinter.font import names
import allure
from pages.base_page import BasePage



class TextBoxesPage(BasePage):

    @allure.step('Fill all inputs')
    def write_all_inputs(self, name, email, current_address, permanent_address):
        with allure.step('Fill User Name'):
            self.page.locator('#userName').fill(name)
        with allure.step('Fill User Email'):
            self.page.locator('#userEmail').fill(email)
        with allure.step('Fill User Current Address'):
            self.page.locator('#currentAddress').fill(current_address)
        with allure.step('Fill User Permanent Address'):
            self.page.locator('#permanentAddress').fill(permanent_address)

    @allure.step('Click submit button')
    def click_text_submit_button(self):
        with allure.step('Click submit button'):
            self.page.locator('#submit').click()

    @allure.step('Get Result')
    def get_results(self):
        with allure.step('Get Result'):
            name = self.page.locator('#name').text_content()
            email = self.page.locator('#email').text_content()
            current_address = self.page.locator("//p[@id='currentAddress']").text_content()
            permanent_address = self.page.locator("//p[@id='permanentAddress']").text_content()
        return name.split(':')[1], email.split(':')[1], current_address.split(':')[1].rstrip(), permanent_address.split(':')[1]
