import asyncio
import logging
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

async def renew_cookie_playwright(username, password):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.moonboard.com/Account/Login")
        await page.fill('input[name="Login.Username"]', username)
        await page.fill('input[name="Login.Password"]', password)
        await page.click('button[name="send"]')
        # Wait for a logout indicator to ensure login was successful.
        await page.wait_for_selector("#main-section-header")
        cookies = await page.context.cookies()
        await browser.close()
        return {cookie['name']: cookie['value'] for cookie in cookies}

def get_renewed_cookie(username, password):
    logger.info("Renewing cookie...")
    cookie_dict = asyncio.run(renew_cookie_playwright(username, password))
    cookie = "; ".join(f"{k}={v}" for k, v in cookie_dict.items())
    logger.info("Cookie renewed.")
    return cookie
