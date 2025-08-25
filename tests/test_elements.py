import time
from playwright.sync_api import Page, expect
from pages.elements_page import TextBoxesPage, CheckBoxPage, RadioButtonPage, WebTablesPage, ButtonsPage, UploadAndDownloadPage, DynamicPropertiesPage
from generator.generator import generated_person
import allure
import pytest


def generate_persons():
    return [next(generated_person()), next(generated_person())]

@allure.suite("Elements Page")
class TestElements:

    @allure.feature("Text Box Page")
    class TestTextBox:


        @pytest.mark.parametrize('name,email,current_address,permanent_address', [
            (person.full_name, person.email, person.current_address, person.permanent_address)
            for person in generate_persons()
        ])
        @pytest.mark.smoke
        @allure.title('Text Box Page valid data')
        def test_valid_data(self, page, base_url, name, email, current_address, permanent_address):

            page.goto(base_url + '/text-box')
            text_box_page = TextBoxesPage(page)
            text_box_page.write_all_inputs(name, email, current_address, permanent_address)
            text_box_page.click_text_submit_button()

            result_name, result_email, result_current_address, result_permanent_address = text_box_page.get_results()

            assert result_name == name
            assert result_email == email
            assert result_current_address == current_address
            assert result_permanent_address == permanent_address


    @allure.feature("Check Box Page")
    class TestCheckBox:

        @pytest.mark.regression
        @allure.title('Check box page valid data')
        def test_check_box(self, page, base_url):
            page.goto(base_url + '/checkbox')
            check_box_page = CheckBoxPage(page)
            check_box_page.click_on_open_full_list_button()
            check_box_page.click_on_check_box()
            input_check_box = check_box_page.get_checked_checkboxes()
            output_result = check_box_page.get_output_result()
            assert input_check_box == output_result


    @allure.feature("Radio buttons Page")
    class TestRadioButton:

        @pytest.mark.parametrize('radio_button', ['yes','impressive'])
        @pytest.mark.ui
        @allure.title('Radio button page valid data')
        def test_radio_button_valid_data(self, page, base_url, radio_button):
            page.goto(base_url + '/radio-button')
            radio_button_page = RadioButtonPage(page)
            radio_button_page.click_on_radio_button(radio_button)
            result = radio_button_page.get_result()
            assert result == radio_button


    @allure.feature("Web Tables Page")
    class TestWebTables:

        @allure.title('Web Tables page valid data')
        def test_create_person(self, page, base_url):
            page.goto(base_url + '/webtables')
            web_tables_page = WebTablesPage(page)
            person = next(generated_person())
            web_tables_page.click_add_button()
            web_tables_page.fill_person_inputs(person.firstname, person.lastname, person.email, str(person.age), str(person.salary), person.department)
            web_tables_page.search(person.firstname)
            result = web_tables_page.get_result()
            assert result == (person.firstname, person.lastname, str(person.age), person.email, str(person.salary), person.department)

        def test_edit_person(self, page, base_url):

            page.goto(base_url + '/webtables')
            web_tables_page = WebTablesPage(page)
            person = next(generated_person())
            web_tables_page.click_add_button()
            web_tables_page.fill_person_inputs(person.firstname, person.lastname, person.email, str(person.age), str(person.salary), person.department)
            web_tables_page.search(person.firstname)
            web_tables_page.click_edit_button()
            person_edit = next(generated_person())
            web_tables_page.fill_person_inputs(person_edit.firstname, person_edit.lastname, person_edit.email, str(person_edit.age), str(person_edit.salary), person_edit.department)
            web_tables_page.search(person_edit.firstname)
            result = web_tables_page.get_result()
            assert result == (person_edit.firstname, person_edit.lastname, str(person_edit.age), person_edit.email, str(person_edit.salary), person_edit.department)

        @allure.title('Web Tables delete Person')
        def test_delete_person(self, page, base_url):
            page.goto(base_url + '/webtables')
            web_tables_page = WebTablesPage(page)
            person = next(generated_person())
            web_tables_page.click_add_button()
            web_tables_page.fill_person_inputs(person.firstname, person.lastname, person.email, str(person.age),
                                          str(person.salary), person.department)
            web_tables_page.search(person.firstname)
            web_tables_page.delete_person()
            text = web_tables_page.check_deleted_person()
            assert text == 'No rows found'


    @allure.feature("Buttons Page")
    class TestButtons:

        @pytest.mark.parametrize(
            'button,result',
            [
                ('double', 'You have done a double click'),
                ('right', 'You have done a right click'),
                ('single', 'You have done a dynamic click')
            ]
        )
        @allure.title('Click button: {button}')
        def test_click_button(self, page, base_url, button, result):
            page.goto(base_url + '/buttons')
            buttons_page = ButtonsPage(page)
            message = buttons_page.click_button(button)
            assert message == result


    @allure.feature('Download and upload Page')
    class TestDownloadAndUpload:

        @allure.title('Download File')
        def test_download_file(self, page, base_url):
            page.goto(base_url + '/upload-download')
            dau_page = UploadAndDownloadPage(page)
            check = dau_page.download_file()
            assert check is True, "File has not been downloaded"

        @allure.title('Upload File')
        def test_upload_file(self, page, base_url):
            page.goto(base_url + '/upload-download')
            dau_page = UploadAndDownloadPage(page)
            file_name, result = dau_page.upload_file()
            assert file_name == result, "File has not been uploaded"


    @allure.feature('Dynamic Properties page')
    class TestDynamicProperties:

        @allure.title('Enable after 5 seconds')
        def test_enable_button(self, page, base_url):
            page.goto(base_url + '/dynamic-properties')
            dynamic_page = DynamicPropertiesPage(page)
            expect(dynamic_page.get_enable_button_after_five_seconds()).to_be_enabled(timeout=10000)

        def test_color_change(self, page, base_url):
            page.goto(base_url + '/dynamic-properties')
            dynamic_page = DynamicPropertiesPage(page)
            expect(dynamic_page.get_visible_after_button()).to_be_visible(timeout=6000)