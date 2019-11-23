import random
from string import ascii_letters

import pytest
from channels.testing import ChannelsLiveServerTestCase
from django.test import Client
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from live.models import MediaPlayer


@pytest.fixture
def driver(request):
    try:
        # NOTE: Requires "chromedriver" binary to be installed in $PATH
        _driver = webdriver.Chrome()
    except WebDriverException:
        _driver = webdriver.Firefox()
    request.cls.driver = _driver
    yield _driver
    _driver.quit()


class GuestClient(Client):
    def __init__(self,):
        self.name = "".join(random.choices(ascii_letters, k=random.randint(5, 9)))


@pytest.mark.usefixtures("driver")
class TestInteractInterface(ChannelsLiveServerTestCase):
    client_class = GuestClient

    @pytest.mark.django_db(transaction=True)
    def test_guest_connect_when_media_player_not_available(self):
        MediaPlayer.objects.all().delete()
        self._enter_interact_queue()
        message_display_element = self.driver.find_element_by_id("message_display")
        assert message_display_element.is_displayed()
        assert message_display_element.text == "Media player not available."

    def _enter_interact_queue(self):
        self.driver.get(self.live_server_url)
        display_name_form = self.driver.find_element_by_id("id_your_name")
        display_name_form.send_keys(self.client.name)
        display_name_form.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 2).until(
            lambda _: self.driver.current_url.endswith("/interact/")
        )
