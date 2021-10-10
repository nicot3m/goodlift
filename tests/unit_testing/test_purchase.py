import json

import pytest

from ... import server


@pytest.fixture
def fixture_loadClubs(monkeypatch):
    def mock_loadClubs():
        with open('tests/unit_testing/test_clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs
    monkeypatch.setattr('GOODLIFT.server.clubs', mock_loadClubs())


@pytest.fixture
def fixture_loadCompetitions(monkeypatch):
    def mock_loadCompetitions():
        with open('tests/unit_testing/test_competitions.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
    monkeypatch.setattr('GOODLIFT.server.competitions', mock_loadCompetitions())


class TestPurchase:
    """ Test purchase places """
    def test_happy_purchase(self, fixture_loadClubs, fixture_loadCompetitions):
        response = server.app.test_client().post('/purchasePlaces', data=dict(club="test_name",
                                                                              competition="test_competition",
                                                                              places="2"))

        assert response.status_code == 200

        # Check that places are deducted from the competition places
        remaining_places = 25 - 2
        assert server.competitions[0]['numberOfPlaces'] == remaining_places

        # Check that points are deducted from the club points
        remaining_points = 13 - 2
        assert server.clubs[0]['points'] == remaining_points

    def test_sad_purchase(self, fixture_loadClubs, fixture_loadCompetitions):
        """ Test purchase more than 12 places """
        response = server.app.test_client().post('/purchasePlaces', data=dict(club="test_name",
                                                                              competition="test_competition",
                                                                              places="13"))

        assert response.status_code == 200
        assert b"You cannot buy more than 12 places!" in response.data

    def test_sad_purchase2(self, fixture_loadClubs, fixture_loadCompetitions):
        """ Test purchase not enough points """
        response = server.app.test_client().post('/purchasePlaces',
                                                 data=dict(club="test_name2",
                                                           competition="test_competition",
                                                           places="6"))

        assert response.status_code == 200
        assert b"You have not enough points!" in response.data

    def test_sad_purchase3(self, fixture_loadClubs, fixture_loadCompetitions):
        """ Test purchase more places than left in competition """
        response = server.app.test_client().post('/purchasePlaces',
                                                 data=dict(club="test_name",
                                                           competition="test_comp_one_left",
                                                           places="3"))
        assert response.status_code == 200
        assert b"Not so many places for sell!" in response.data
