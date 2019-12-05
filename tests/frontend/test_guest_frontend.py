import pytest
from channels.testing import ChannelsLiveServerTestCase


class SeeVrTestCase(ChannelsLiveServerTestCase):
    @pytest.fixture(autouse=True)
    def set_fixtures_to_attributes(
        self, browser, feature_factory, random_string_factory
    ):
        self.browser = browser
        self.feature_factory = feature_factory
        self.random_string_factory = random_string_factory


class TestGuestDisplayNameSubmission(SeeVrTestCase):
    @pytest.mark.django_db(transaction=True)
    def test_method(self):
        feature = self.feature_factory()
        guest_name = self.random_string_factory()
        self.browser.visit(self.live_server_url + f"/{feature.slug}")
        self.browser.find_by_name("guest_name").first.fill(guest_name)
        self.browser.find_by_value("Submit").first.click()
        assert self.browser.url == self.live_server_url + f"/{feature.slug}/interact/"
