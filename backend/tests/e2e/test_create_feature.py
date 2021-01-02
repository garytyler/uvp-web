# import html

# import pytest


# @pytest.mark.asyncio
# async def test_guest_interaction(
#     create_random_feature,
#     browser,
#     frontend_base_url,
#     take_screenshot,
# ):
#     feature_obj = await create_random_feature()
#     page = await browser.newPage(ignoreHTTPSErrors=True)
#     async with page.expect_load_state("load"):
#         await page.goto(f"{frontend_base_url}/live/{feature_obj.slug}")
#     await take_screenshot(page)
#     assert feature_obj.title in html.unescape(await page.content())
