import html
from urllib.parse import urlparse

import pytest

from app.models.users import User


@pytest.mark.asyncio
async def test_create_user_account(
    take_screenshot,
    xserver,
    browser,
    faker,
    create_random_password,
    frontend_base_url,
):
    user_name = faker.name()
    user_email = faker.safe_email()
    user_password = create_random_password()

    # Create new user account
    page = await browser.newPage(ignoreHTTPSErrors=True)
    await page.goto(frontend_base_url)
    async with page.expect_navigation():
        await page.click("//a[normalize-space(.)='Sign up']")
    await page.click('input[type="text"]')
    await page.fill('input[type="text"]', user_name)
    await page.press('input[type="text"]', "Tab")
    await page.fill('input[type="email"]', user_email)
    await page.press('input[type="email"]', "Tab")
    await page.fill('input[type="password"]', user_password)
    await page.press('input[type="password"]', "Tab")
    await page.fill(
        "//div[normalize-space(.)='Confirm Password']"
        + "/input[normalize-space(@type)='password']",
        user_password,
    )
    async with page.expect_navigation(waitUntil="networkidle"):
        await page.click("text=/.*Submit.*/")
    await take_screenshot(page)

    # Check new url
    assert urlparse(page.url).path == "/login"
    await take_screenshot(page)

    assert await User.get_or_none(email=user_email)


@pytest.mark.asyncio
async def test_login_user(
    take_screenshot,
    xserver,
    browser,
    faker,
    create_random_password,
    create_random_user,
    frontend_base_url,
):
    user_password = create_random_password()
    user_obj = await create_random_user(password=user_password)

    # Create new user account
    page = await browser.newPage(ignoreHTTPSErrors=True)
    await page.goto(f"{frontend_base_url}/login")

    # Login as new user
    await page.click('input[name="login"]')
    await page.fill('input[name="login"]', user_obj.email)
    await page.press('input[name="login"]', "Tab")
    await page.fill('input[name="password"]', user_password)
    await page.click("//button/span[normalize-space(.)='Login']")
    async with page.expect_navigation(waitUntil="load"):
        await page.click("//button/span[normalize-space(.)='Login']")

    # await take_screenshot(page)
    await take_screenshot(page)

    # Check welcome message with user's name is displayed
    assert user_obj.name in html.unescape(await page.content())
