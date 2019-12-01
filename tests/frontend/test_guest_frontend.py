import pytest
from channels.testing import ChannelsLiveServerTestCase


class ChannelsLiveServerTestCaseWithStockFixtures(ChannelsLiveServerTestCase):
    @pytest.fixture(autouse=True)
    def set_fixtures_to_attributes(
        self, browser, feature_factory, random_string_factory
    ):
        self.browser = browser
        self.feature_factory = feature_factory
        self.random_string_factory = random_string_factory


class TestGuestDisplayNameSubmission(ChannelsLiveServerTestCaseWithStockFixtures):
    @pytest.mark.django_db(transaction=True)
    def test_method(self):
        feature = self.feature_factory()
        display_name = self.random_string_factory(5, 9)
        self.browser.visit(self.live_server_url + f"/{feature.slug}")
        self.browser.find_by_name("your_name").first.fill(display_name)
        self.browser.find_by_value("Submit").first.click()
        assert self.browser.url.endswith("/guest/interact/")


class TestFeatureSlugAsUrlPath(ChannelsLiveServerTestCaseWithStockFixtures):
    @pytest.mark.django_db(transaction=True)
    def test_method(self):
        feature = self.feature_factory()
        self.browser.visit(self.live_server_url + f"/{feature.slug}/")
        assert self.browser.url.endswith("/guest/welcome/")
