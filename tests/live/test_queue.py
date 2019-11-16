# import pytest
# from channels.testing import ChannelsLiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.common.exceptions import WebDriverException


# class TestQueue(ChannelsLiveServerTestCase):
#     serve_static = True  # emulate StaticLiveServerTestCase

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         try:
#             # NOTE: Requires "chromedriver" binary to be installed in $PATH
#             cls.driver = webdriver.Chrome()
#         except WebDriverException:
#             cls.driver = webdriver.Firefox()
#         except WebDriverException:
#             super().tearDownClass()
#             raise

#     @classmethod
#     def tearDownClass(cls):
#         cls.driver.quit()
#         super().tearDownClass()

#     # def test_add_to_queue(self):
#     #     self.driver.get(self.live_server_url + "/index/")
#     #     self.driver.find_element_by_css_selector("id_your_name")
#     #     print()
#     #     # print(self.driver.title)
#     #     # assert self.driver.title
