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


class TestBook:
    """ Test book """

    def test_happy_book(self, fixture_loadClubs, fixture_loadCompetitions):
        """ test book with correct club and competition names """
        response = server.app.test_client().get('/book/test_competition/test_name')
        assert response.status_code == 200

    def test_sad_book_wrong_name(self, fixture_loadClubs, fixture_loadCompetitions):
        """ test book with wrong club name """
        response = server.app.test_client().get('/book/test_competition/test_wrong_name')
        assert response.status_code == 302

    def test_sad_book_wrong_competition(self, fixture_loadClubs, fixture_loadCompetitions):
        """ test book with wrong competition name """
        response = server.app.test_client().get('/book/test_wrong_competition/test_name')
        assert response.status_code == 302

    def test_sad_book_competition_full(self, fixture_loadClubs, fixture_loadCompetitions):
        """ test book competition full"""
        response = server.app.test_client().get('/book/test_competition_full/test_name')
        assert response.status_code == 200
        assert b"No more places for sale!" in response.data
