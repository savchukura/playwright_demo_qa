import time
from playwright.sync_api import Page
from pages.elements_page import TextBoxesPage

from pages.forms_page import FormsPage
from generator.generator import generated_person
import allure
import pytest


def generate_persons():
    return [next(generated_person()), next(generated_person())]

@allure.suite("Main class")
class TestCreating:

    @allure.feature("Second Class")
    class TestGeneration:



        @pytest.mark.parametrize('name,email,current_address,permanent_address', [
            (person.full_name, person.email, person.current_address, person.permanent_address)
            for person in generate_persons()
        ])
        @allure.title('Test One')
        def test_one(self, page, name, email, current_address, permanent_address):

            page.goto('https://demoqa.com/text-box')
            text_box_page = TextBoxesPage(page)
            text_box_page.write_all_inputs(name, email, current_address, permanent_address)
            text_box_page.click_text_submit_button()

            result_name, result_email, result_current_address, result_permanent_address = text_box_page.get_results()

            assert result_name == name
            assert result_email == email
            assert result_current_address == current_address
            assert result_permanent_address == permanent_address

        def test_two(self, page):
            page.goto('https://demoqa.com/automation-practice-form')
            forms_page = FormsPage(page)
            file = forms_page.upload_image()
            print(file)
            time.sleep(5)