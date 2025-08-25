import time
from tkinter.font import names
from xml.sax.xmlreader import Locator

import allure
from playwright.sync_api import expect

from pages.base_page import BasePage
import random
import os
import base64
from generator.generator import generated_person, generated_file


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
        return name.split(':')[1].strip(), email.split(':')[1].strip(), current_address.split(':')[1].strip(), permanent_address.split(':')[1].strip()

    @allure.step('get error message')
    def get_error(self):
        with allure.step('Get Error'):
            error = self.page.locator("xpath=//div[contains(@class, 'mr-sm-2 field-error form-control')]").is_visible()
            return error


class CheckBoxPage(BasePage):

    @allure.step('Open Full List')
    def click_on_open_full_list_button(self):
        with allure.step('Open Full List'):
            self.page.get_by_title('Expand all').click()

    @allure.step('Click on Checkbox')
    def click_on_check_box(self):
        item_list = self.page.locator("span[class='rct-title']").element_handles()
        count = 21
        while count != 0:
            item = item_list[random.randint(1, 15)]
            if count > 0:
                item.click()
                count -= 1
            else:
                break

    @allure.step('get checked checkboxes')
    def get_checked_checkboxes(self):
        checked_list = self.page.locator("svg[class='rct-icon rct-icon-check']").element_handles()
        data = []
        for box in checked_list:
            title_item = box.query_selector("xpath=ancestor::span[contains(@class, 'rct-text')]")
            if title_item:
                data.append(title_item.inner_text())
        return str(data).replace(' ', '').replace('doc', '').replace('.', '').lower()

    @allure.step('get output result')
    def get_output_result(self):
        result_list = self.page.locator("span[class='text-success']").element_handles()
        data = []
        for item in result_list:
            data.append(item.inner_text())
        return str(data).replace(' ', '').lower()


class RadioButtonPage(BasePage):

    @allure.step('Click radio button')
    def click_on_radio_button(self, radio_button):
        with allure.step('Click on Radio Button'):
            radio_buttons = {"yes": 'yes',
                            "impressive": 'impressive',
                            "no": 'no'
                            }
            self.page.get_by_text(radio_buttons[radio_button]).click(timeout=5000)

    @allure.step('Get Result')
    def get_result(self):
        result = self.page.locator("span[class='text-success']").text_content().lower()
        return result


class WebTablesPage(BasePage):

    @allure.step('Click Add button')
    def click_add_button(self):
        with allure.step('Click Add button'):
            self.page.locator('#addNewRecordButton').click()

    @allure.step('Create Person')
    def fill_person_inputs(self, first_name, last_name, email, age, salary, department):

        with allure.step('fill inputs'):
            self.page.locator("input[placeholder='First Name']").fill(first_name)
            self.page.locator("input[placeholder='Last Name']").fill(last_name)
            self.page.locator("input[placeholder='name@example.com']").fill(email)
            self.page.locator("input[placeholder='Age']").fill(age)
            self.page.locator("input[placeholder='Salary']").fill(salary)
            self.page.locator("input[placeholder='Department']").fill(department)
        with allure.step('Click Submit button'):
            self.page.locator('#submit').click()

    @allure.step('Click Edit Button')
    def click_edit_button(self):
        with allure.step('Click Edit button'):
            self.page.locator("span[title='Edit']").click()

    @allure.step('Get Result')
    def get_result(self):
        first_name = self.page.locator(".rt-tr-group").first.locator("div.rt-td").nth(0).inner_text()
        last_name = self.page.locator(".rt-tr-group").first.locator("div.rt-td").nth(1).inner_text()
        email = self.page.locator(".rt-tr-group").first.locator("div.rt-td").nth(2).inner_text()
        age = self.page.locator(".rt-tr-group").first.locator("div.rt-td").nth(3).inner_text()
        salary = self.page.locator(".rt-tr-group").first.locator("div.rt-td").nth(4).inner_text()
        department = self.page.locator(".rt-tr-group").first.locator("div.rt-td").nth(5).inner_text()
        return first_name, last_name, email, age, salary, department

    @allure.step('Search')
    def search(self, search):
        with allure.step('Use Search'):
            self.page.locator("input[placeholder='Type to search']").fill(search)

    @allure.step('Delete Person')
    def delete_person(self):
        with allure.step('Click Delete button'):
            self.page.locator("span[title='Delete']").click()

    @allure.step('Check Deleted Person')
    def check_deleted_person(self):
        no_result_message = self.page.locator("div[class='rt-noData']").text_content()
        return no_result_message


class ButtonsPage(BasePage):

    @allure.step('Click button')
    def click_button(self, button_type: str = "single"):
        with allure.step(f'Click "{button_type}" button'):
            if button_type == "double":
                self.page.locator('#doubleClickBtn').dblclick()
                return self.page.locator('#doubleClickMessage').text_content()
            elif button_type == "right":
                self.page.locator('#rightClickBtn').click(button="right")
                return self.page.locator('#rightClickMessage').text_content()
            elif button_type == "single":
                self.page.locator("button[class='btn btn-primary']").nth(2).click()
                return self.page.locator('#dynamicClickMessage').text_content()
            else:
                raise ValueError(f"Unsupported button_type: {button_type}")


class UploadAndDownloadPage(BasePage):

    @allure.step('Download file')
    def download_file(self):
        with allure.step('Download file'):
            link = self.page.locator('#downloadButton').get_attribute('href')
            link_b = base64.b64decode(link)
            path_name_file = os.path.abspath(f'../tests{random.randint(0, 999)}.jpeg')
            with open(path_name_file, 'wb+') as f:
                offset = link_b.find(b'\xff\xd8')
                f.write(link_b[offset:])
                check_file = os.path.exists(path_name_file)
                f.close()
            os.remove(path_name_file)
            return check_file


class DynamicPropertiesPage(BasePage):

    @allure.step('Get 5 seconds enable button')
    def get_enable_button_after_five_seconds(self):
        with allure.step('Get 5 seconds enable button'):
            return self.page.locator('#enableAfter')

    @allure.step('Get visible after 5 second button')
    def get_visible_after_button(self):
        with allure.step('Get visible after 5 second button'):
            return self.page.locator('#visibleAfter')