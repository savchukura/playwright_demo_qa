import allure
from pages.base_page import BasePage
import random


class FormsPage(BasePage):

    @allure.step('Fill First Name')
    def fill_first_name(self, first_name):
        with allure.step('Fill First name'):
            self.page.locator('#firstName').fill(first_name)

    @allure.step('Fill Last Name')
    def fill_last_name(self, last_name):
        with allure.step('Fill last name'):
            self.page.locator('#lastName').fill(last_name)

    @allure.step('Fill Email')
    def fill_email(self, email):
        with allure.step('Fill Email'):
            self.page.locator('#userEmail').fill(email)

    @allure.step('Chose Gender')
    def choose_gender(self):
        with allure.step('Choose gender'):
            gender_buttons = {"male": 'Male',
                              "female": 'Female',
                              "other": 'Other'
                              }
            gender = random.choice(['male', 'female', 'other'])
            self.page.get_by_text(gender_buttons[gender], exact=True).click()
            return gender

    @allure.step('fill Mobile No')
    def fill_mobile_no(self, mobile_no):
        with allure.step('Fill mobile number'):
            self.page.locator('#userNumber').fill(mobile_no)

    @allure.step('Fill date of birth')
    def fill_date_of_birth(self, date_of_birth):
        with allure.step('Fill date of birth'):
            self.page.locator('#dateOfBirthInput').fill(date_of_birth)
            self.page.keyboard.press("Enter")

    @allure.step('Fill subjects')
    def fill_subjects(self, subject):
        with allure.step('Fill subjects'):
            self.page.locator("input[id='subjectsInput']").fill(subject)
            self.page.keyboard.press("ArrowDown")
            self.page.keyboard.press("Enter")

    @allure.step('Choose hobbies')
    def choose_hobby(self):
        with allure.step('Choose Hobbies'):
            hobbies_buttons = {"sports": 'Sports',
                               "reading": 'Reading',
                               "music": 'Music'
                               }
            hobbies = random.choice(['sports', 'reading', 'music'])
            self.page.get_by_text(hobbies_buttons[hobbies], exact=True).click()
            return hobbies

    @allure.step('Fill address')
    def fill_address(self, address):
        with allure.step('Fill current address'):
            self.page.locator('#currentAddress').fill(address)

    @allure.step('Select State')
    def select_state(self):
        with allure.step('select state'):
            self.page.locator("#state").click()
            self.page.keyboard.press("ArrowDown")
            self.page.keyboard.press("Enter")
            state = self.page.locator("div[class=' css-1uccc91-singleValue']").inner_text()
            return state

    @allure.step('Select City')
    def select_city(self):
        with allure.step('select City'):
            self.page.locator("#city").click()
            self.page.keyboard.press("ArrowDown")
            self.page.keyboard.press("Enter")
            city_locator = self.page.locator("div[class=' css-1uccc91-singleValue']")
            second_city_element = city_locator.nth(1)
            city = second_city_element.inner_text()
            return city

    @allure.step("Click Submit button")
    def click_submit_button(self):
        with allure.step('Click Submit button'):
            self.page.locator("button[class='btn btn-primary']").click()

    @allure.step('Get Result')
    def get_result(self):
        with allure.step("Get Result"):
            result_list = self.page.locator("//div[@class='table-responsive']//td[2]")
            data = []
            for i in range(result_list.count()):
                text = result_list.nth(i).inner_text()
                data.append(text)
            return data