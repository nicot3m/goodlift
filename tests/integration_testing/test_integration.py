import json

import pytest

from ... import server


@pytest.fixture
def fixture_loadClubs(monkeypatch):
    def mock_loadClubs():
        with open('tests/integration_testing/test_clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs
    monkeypatch.setattr('GOODLIFT.server.clubs', mock_loadClubs())


@pytest.fixture
def fixture_loadCompetitions(monkeypatch):
    def mock_loadCompetitions():
        with open('tests/integration_testing/test_competitions.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
    monkeypatch.setattr('GOODLIFT.server.competitions', mock_loadCompetitions())


def loadClubs():
    with open('tests/integration_testing/test_clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('tests/integration_testing/test_competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


class TestIntegration:
    """ Test the integration of the following server functions:
        - loadClubs,
        - loadCompetitions,
        - index,
        - showSummary,
        - book,
        - purchasePlaces,
        - logout. """

    def test_load_club(self):
        """ Test load club test_name from json files"""
        test_club = {"name": "test_name", "email": "test@email.com", "points": "13"}
        assert loadClubs()[0] == test_club

    def test_load_competition(self):
        """ Test load competition test_competition from json files"""
        test_competition = {"name": "test_competition", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"}
        assert loadCompetitions()[0] == test_competition

    def test__index(self):
        """ Test index """
        response = server.app.test_client().get('/')
        assert response.status_code == 200
        assert b"Welcome to the GOODLIFT Registration Portal!" in response.data

    def test_show_summary(self, fixture_loadClubs):
        """ Test email test@email.com """
        response = server.app.test_client().post('/showSummary', data=dict(email="test@email.com"))
        assert response.status_code == 200
        assert b"Welcome, test@email.com" in response.data
        assert b"Points available: 13" in response.data
        assert b"Spring Festival" in response.data
        assert b"Number of Places: 25" in response.data

    def test__book(self, fixture_loadClubs, fixture_loadCompetitions):
        """ test book with test_name and test_competition"""
        response = server.app.test_client().get('/book/test_competition/test_name')
        assert response.status_code == 200
        assert b"test_competition" in response.data
        assert b"Places available: 25" in response.data

    def test_purchase(self, fixture_loadClubs, fixture_loadCompetitions):
        """ Test purchase 5 places """
        response = server.app.test_client().post('/purchasePlaces', data=dict(club="test_name",
                                                                              competition="test_competition",
                                                                              places="5"))

        assert response.status_code == 200
        assert b"Great-booking complete!" in response.data
        # Remaining_points = 13 - 5 = 8
        assert b"Points available: 8" in response.data
        # Remaining_places = 25 - 5 = 20
        assert b"Number of Places: 20" in response.data

    def test_logout(self):
        """ Test logout """
        response = server.app.test_client().get('/logout')
        assert response.status_code == 302
        # Test redirect to localhost
        assert response.location == "http://localhost/"
