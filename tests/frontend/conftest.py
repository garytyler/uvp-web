import pytest
from channels.testing import ChannelsLiveServerTestCase


@pytest.fixture(scope="function")
def channels_test_case(request):
    setattr(ChannelsLiveServerTestCase, request.function.__name__, request.function)
    channels_test_case = ChannelsLiveServerTestCase(request.function.__name__)
    channels_test_case._pre_setup()
    yield channels_test_case
    channels_test_case._post_teardown()


@pytest.fixture(scope="function")
def sign_in(request):
    def _sign_in(browser, guest_name, feature):
        channels_test_case = request.getfixturevalue("channels_test_case")
        browser.visit(channels_test_case.live_server_url + f"/{feature.slug}/")
        browser.find_by_name("guest_name").first.fill(guest_name)
        browser.find_by_value("Submit").first.click()

    return _sign_in
