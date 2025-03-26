import asyncio
from playwright.async_api import async_playwright
from utils.logger_config import setup_logger

logger = setup_logger(__name__)

async def get_auth_credentials_playwright(username, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.moonboard.com/Account/Login")
        await page.fill('input[name="Login.Username"]', username)
        await page.fill('input[name="Login.Password"]', password)
        await page.click('button[name="send"]')
        # Wait for a logout indicator to ensure login was successful.
        await page.wait_for_selector("#main-section-header")
        
        # Extract RequestVerificationToken
        token = await page.locator("#sidebar-nav input[name='__RequestVerificationToken']").get_attribute('value')
        
        cookies = await page.context.cookies()
        await browser.close()
        return {
            'cookies': {cookie['name']: cookie['value'] for cookie in cookies},
            'token': token
        }

def get_auth_credentials(username, password):
    logger.info("Getting authentication credentials...")
    result = asyncio.run(get_auth_credentials_playwright(username, password))
    cookie = "; ".join(f"{k}={v}" for k, v in result['cookies'].items())
    logger.info("Authentication credentials retrieved.")
    return {
        'cookie': cookie,
        'token': result['token']
    }
