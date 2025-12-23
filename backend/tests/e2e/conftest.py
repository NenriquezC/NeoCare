import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    """Crea una instancia del browser para toda la sesión."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Crea una nueva página para cada test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
