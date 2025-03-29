from playwright.sync_api import Page



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
