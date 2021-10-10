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


class TestPointsDisplay:
    """ Test club points display no login required """
    def test_happy_points_display(self, fixture_loadClubs):
        response = server.app.test_client().get('/displayPoints')
        assert response.status_code == 200

    # Check that points are correctly displayed
        test_name_points = str(13)
        assert str(server.clubs[0]['points']) == test_name_points
