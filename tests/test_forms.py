from pages.forms_page import FormsPage
import allure
import time
from generator.generator import generated_person


@allure.suite('Forms Page')
class TestFormsPage:

    @allure.title("Create Person")
    def test_create_person(self, page, base_url):
        page.goto(base_url + '/automation-practice-form')

        person = next(generated_person())

        forms_page = FormsPage(page)
        forms_page.fill_first_name(person.firstname)
        forms_page.fill_last_name(person.lastname)
        forms_page.fill_email(person.email)
        gender = forms_page.choose_gender()
        forms_page.fill_mobile_no(person.mobile)
        forms_page.fill_date_of_birth('22')
        forms_page.fill_subjects('English')
        hobby = forms_page.choose_hobby()
        file = forms_page.upload_image()
        forms_page.fill_address(person.current_address)
        state = forms_page.select_state()
        city = forms_page.select_city()
        forms_page.click_submit_button()

        results = forms_page.get_result()

        assert person.firstname + " " + person.lastname == results[0]
        assert person.email == results[1]
        assert gender == results[2].lower()
        assert person.mobile == results[3]
        assert '22' in results[4]
        assert 'English' == results[5]
        assert hobby == results[6].lower()
        assert file == results[7]
        assert person.current_address.replace('\n', ' ') == results[8]
        assert state in results[9]
        assert city in results[9]

