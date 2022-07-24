import requests
from attrs import define
import pytest

from eve_utils.EveUtils import EveUtils


@pytest.fixture
def system_name():
    return "Jita"


@pytest.fixture
def system_id():
    return "30000142"


@pytest.fixture
def character_name():
    return "Sapporo Jones"


@pytest.fixture
def character_id():
    return "772506501"


@pytest.fixture
def corp_name():
    return "Upvote"


@pytest.fixture
def corp_id():
    return "416584095"


@pytest.fixture
def alice_name():
    return "Test Alliance Please Ignore"


@pytest.fixture
def item_name():
    return "Ibis"


@pytest.fixture
def item_id():
    return "601"


# jita's const id is 20000020
# jita's region id is 10000002
@pytest.fixture
def region_id():
    return "10000002"


eu = EveUtils()


def test_find_id_from_system(system_name):
    x = eu.find_id_from_system(system_name)
    assert x == str("30000142")
    assert eu.system_id == "30000142"


def test_find_system_from_id(system_id):
    x = eu.find_system_from_id(system_id)
    assert x == "Jita"
    assert eu.system_name == "Jita"


def test_get_jumps(system_id):
    x = eu.get_jumps(system_id)
    # num jumps for Jita (the biggest market hub) should never be 0
    assert x > 0


def test_get_character_id(character_name):
    x = eu.get_character_id(character_name)
    assert x == "772506501"


def test_get_corp_id(corp_name):
    x = eu.get_corp_id(corp_name)
    assert x == "416584095"


def test_get_alliance_id(alice_name):
    x = eu.get_alliance_id(alice_name)
    assert x == "498125261"


def test_get_item_name(item_id):
    x = eu.get_item_name(item_id)
    assert x == "Ibis"


def test_get_item_id(item_name):
    x = eu.get_item_id(item_name)
    assert x == "601"


def test_get_region_id(system_id):
    x = eu.get_region_id(system_id)
    assert x == "10000002"


def test_get_num_stargates(system_id):
    x = eu.get_num_stargates(system_id)
    assert x >= 1


def test_get_plex_prices():
    x = eu.get_plex_prices()
    assert x > 0  # plex prices will never be zero so this should never be none or zero
