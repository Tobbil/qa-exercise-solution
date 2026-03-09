import socket
import threading
import time

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from app.main import app as flask_app

PORT = 5050
BASE_URL = f'http://localhost:{PORT}'


# ---------------------------------------------------------------------------
# Application server
# ---------------------------------------------------------------------------

HEALTH_URL = f'{BASE_URL}/api/health'


def _app_is_running() -> bool:
    """Return True if the ShopEasy app is already up and healthy."""
    try:
        resp = requests.get(HEALTH_URL, timeout=2)
        return resp.status_code == 200 and resp.json().get('status') == 'ok'
    except requests.RequestException:
        return False


@pytest.fixture(scope="session")
def app_server():
    """Start the Flask app if it is not already running."""
    if _app_is_running():
        yield BASE_URL
        return

    thread = threading.Thread(
        target=lambda: flask_app.run(port=PORT, use_reloader=False, debug=False),
        daemon=True,
    )
    thread.start()

    # Wait up to 5 s for the server to become healthy.
    for _ in range(10):
        time.sleep(0.5)
        if _app_is_running():
            break
    else:
        pytest.exit(
            f'\n\nCould not reach the app at {HEALTH_URL} after 5 s.\n'
            f'Check that port {PORT} is free and the app starts correctly.\n',
            returncode=1,
        )

    yield BASE_URL


# ---------------------------------------------------------------------------
# UI fixtures
# ---------------------------------------------------------------------------

def _chrome_options() -> Options:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return options


@pytest.fixture(scope='function')
def driver(app_server):
    """Provide a headless Chrome WebDriver per test."""
    chrome = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=_chrome_options(),
    )
    chrome.implicitly_wait(5)
    yield chrome
    chrome.quit()


# ---------------------------------------------------------------------------
# API fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='function')
def api_client(app_server):
    """Provide a (requests.Session, base_url) tuple for API tests."""
    with requests.Session() as session:
        yield session, app_server
