import pytest


@pytest.mark.django_db(transaction=True)
def test_guest_sign_in(
    channels_test_case,
    connected_presenter_feature_objs,
    guest_name_factory,
    browser,
    sign_in,
):
    presenter, feature = connected_presenter_feature_objs
    guest_name = guest_name_factory()
    sign_in(browser=browser, guest_name=guest_name, feature=feature)
    expected_url = channels_test_case.live_server_url + f"/{feature.slug}/interact/"
    assert browser.url == expected_url


@pytest.mark.django_db(transaction=True)
def test_first_guest_sign_in_loads_interact_buttons(
    channels_test_case,
    connected_presenter_feature_objs,
    guest_name_factory,
    browser,
    sign_in,
):
    presenter, feature = connected_presenter_feature_objs
    guest_name = guest_name_factory()
    sign_in(browser=browser, guest_name=guest_name, feature=feature)
    assert browser.is_element_present_by_value("Start", wait_time=2)
    assert browser.is_element_present_by_value("Stop", wait_time=2)
    # TODO: Test for visibility
