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


class TestShowSummary:
    """ Test login with email """

    def test_happy_show_summary(self, fixture_loadClubs):
        """ Test email registered """
        response = server.app.test_client().post('/showSummary', data=dict(email="test@email.com"))
        assert response.status_code == 200

    def test_sad_show_summary(self):
        """ Test email not registered """
        response = server.app.test_client().post('/showSummary', data=dict(email="wrong_email@email.com"))
        assert response.status_code == 302

    def test_sad2_show_summary(self):
        """ Test email blank email """
        response = server.app.test_client().post('/showSummary', data=dict(email=""))
        assert response.status_code == 302
