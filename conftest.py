from typing import Generator, Any
import pytest
import logging
import allure
import os
from playwright.sync_api import Playwright, sync_playwright, Browser, BrowserContext, Page, expect

@pytest.fixture(scope="session")
def browser() -> Generator[Browser, None, None]:
    chrome_options = [
        "--no-sandbox",
        "--disable-gpu",
        "--disable-translate",
        "--disable-extension",
        "--safebrowsing-disable-auto-update",
        "--disable-sync",
        "--disable-default-apps",
        "--mute-audio",
        "--no-first-run",
        "--window-size=1920,1080",
        "--disable-gpu-rasterization",
        "--disable-gl-drawing-for-tests",
        "--disable-glsl-translator"
    ]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=chrome_options)  # З headless=True для безголового режиму
        yield browser
        browser.close()


@pytest.fixture(scope="session")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Створює один контекст браузера для сесії.
    Усі вкладки (сторінки) будуть створені в цьому контексті.
    """
    context = browser.new_context(viewport={"width": 2560, "height": 1280})
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Створює нову сторінку (вкладку) для КОЖНОГО тесту.
    Це забезпечує ізоляцію тестів один від одного.
    """
    page = context.new_page()
    yield page
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Додає скріншот у Allure, якщо тест провалився"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)

        if page and not page.is_closed():
            try:
                screenshot_dir = os.path.join(os.path.dirname(__file__), "results", "allure-results")
                os.makedirs(screenshot_dir, exist_ok=True)

                screenshot_path = os.path.join(screenshot_dir, f"{item.name}.png")
                page.screenshot(path=screenshot_path)
                allure.attach.file(screenshot_path, name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)

            except Exception as e:
                logging.warning(f"Could not take or attach screenshot for failed test: {e}")