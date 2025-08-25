from playwright.sync_api import Page
import allure
from generator.generator import generated_person, generated_file, generated_image
import os


class BasePage:

    def __init__(self, page: Page):
        self.page = page


    def choose_section(self, section):
        sections = {"elements": 'Elements',
                    "forms": 'Forms',
                    "alerts": 'Alerts, Frame & Windows',
                    "widget": 'Widgets',
                    "interactions": 'Interactions',
                    "application": 'Book Store Application'}
        self.page.get_by_text(sections[section]).click()

    @allure.step('Upload file')
    def upload_file(self):
        with allure.step('Upload File'):
            file_name, path = generated_file()
            self.page.locator("#uploadFile").set_input_files(path)
            os.remove(path)
            text = self.page.locator('#uploadedFilePath').text_content()
            return file_name.split('/')[-1], text.split('\\')[-1]

    @allure.step('Upload Image')
    def upload_image(self):
        with allure.step('Upload File'):
            file_name, path = generated_image()
            self.page.locator("#uploadPicture").set_input_files(path)
            os.remove(path)
            return file_name.split('/')[-1]