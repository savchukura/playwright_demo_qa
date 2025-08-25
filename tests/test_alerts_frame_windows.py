from pages.alerts_frame_windows_page import BrowserWindowsPage
import allure
import time
from generator.generator import generated_person

@allure.suite("Alerts, Frame, Windows Page")
class TestAlertsFrameWindows:

    @allure.feature("Browser Windows Tab")
    class TestBrowserWindows:

        @allure.title("Click New Tab button")
        def test_click_new_tab_button(self, page, base_url):
            page.goto(base_url + '/browser-windows')
            browser_windows_page = BrowserWindowsPage(page)
            with page.context.expect_page() as new_page_info:
                browser_windows_page.click_button('new_tab')
            new_page = new_page_info.value
            new_page.wait_for_load_state()
            assert new_page.url == base_url + '/sample'
            assert new_page.locator("h1").inner_text() == "This is a sample page"


        @allure.title("Click New Window Button")
        def test_click_new_window_button(self, page, base_url):
            page.goto(base_url + '/browser-windows')
            browser_windows_page = BrowserWindowsPage(page)
            with page.expect_popup() as popup_info:
                browser_windows_page.click_button('new_window')
            new_page = popup_info.value
            new_page.wait_for_load_state()
            assert new_page.url == base_url + '/sample'
            assert new_page.locator("h1").inner_text() == "This is a sample page"
