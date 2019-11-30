import pytest
from channels.testing import ChannelsLiveServerTestCase


class TestGuestDisplayNameEntry(ChannelsLiveServerTestCase):
    @pytest.fixture(autouse=True)
    def _(self, browser, random_string_factory):
        self.browser = browser
        self.random_string_factory = random_string_factory

    @pytest.mark.django_db(transaction=True)
    def test_guest_display_name_submission_redirects_to_interact_page(self):
        display_name = self.random_string_factory(5, 9)
        self.browser.visit(self.live_server_url + "/home/")
        self.browser.find_by_name("your_name").first.fill(display_name)
        self.browser.find_by_value("Submit").first.click()
        assert self.browser.url.endswith("/interact/")
